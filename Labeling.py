from __future__ import annotations

from PySide6 import (
    QtWidgets as qtw, 
    QtGui as qtg, 
    QtCore as qtc,
)
from PySide6.QtCore import Qt

import cv2
import numpy as np

from typing import List, Dict, Tuple
from itertools import count
from dataclasses import dataclass, astuple, field
from abc import abstractmethod

from AIWrapper import SAM_wrapper
from Utils import *

@dataclass(order=True, frozen=True)
class Class_Label:
    id:int = field(default_factory=count().__next__, init=False, hash=False)
    name:str
    color:np.ndarray = field(init=False, hash=False)

    def __post_init__(self):
        object.__setattr__(self, 'color', hash_to_hue(self.name))

@dataclass(order=True, frozen=True)
class Label:
    label_id: int = None
    x: float = None
    y: float = None
    w: float = None
    h: float = None

    @staticmethod
    def from_str(string:str) -> Label:
        inputs = string.split(" ")
        assert len(inputs) == 5
        return Label(int(inputs[0]), float(inputs[1]), float(inputs[2]), float(inputs[3]), float(inputs[4]))

    @staticmethod
    def from_bbox(rect: qtc.QRect, im_shape:Tuple[int], label_id:int) -> Label:
        iw, ih, _ =  im_shape
        cx, cy = rect.center().toTuple()
        w,h = rect.size().toTuple()
        return Label(label_id, cx/iw, cy/ih, w/iw, h/ih)
    
    def draw_rect(self, img: np.ndarray, color: Tuple[int,int,int], thickness = 2) -> np.ndarray:
        _,x,y,w,h = astuple(self)
        iw , ih, _ = img.shape
        return cv2.rectangle(
            img,
            pt1 = (int((x-w/2) * iw),int((y-h/2) * ih)),
            pt2 = (int((x+w/2) * iw),int((y+h/2) * ih)),
            color = color, 
            thickness = thickness
        )
    
    def to_coco_format(self) -> str:
        l,x,y,w,h = astuple(self)
        return f"{l} {x} {y} {w} {h}"

class LabelManager(qtc.QObject):
    temp_bbox_update = qtc.Signal(qtc.QRect)
    label_created = qtc.Signal(qtc.QRect)

    @abstractmethod
    def process_image(self, image: np.ndarray): pass

    @abstractmethod
    def clicked(self, x:int, y:int, mod: Qt.KeyboardModifier): pass
    
    @abstractmethod
    def released(self, x:int, y:int, mod: Qt.KeyboardModifier): pass
    
    @abstractmethod
    def moved(self, x:int, y:int, mod: Qt.KeyboardModifier): pass

    @abstractmethod
    def cancel(self): pass

    @abstractmethod
    def confirm(self): pass

    @abstractmethod
    def bbox(self) -> qtc.QRect: pass

class DefaultLabeling(LabelManager):
    
    def __init__(self):
        super().__init__()
        self.corner1 : Tuple[int,int] = None
        self.corner2 : Tuple[int,int] = None

    def process_image(self, image: np.ndarray) -> np.ndarray: 
        return image

    def clicked(self, x:int, y:int, mod: Qt.KeyboardModifier): 
        self.corner1 = (x,y)
    
    def released(self, x:int, y:int, mod: Qt.KeyboardModifier): 
        self.corner2 = (x,y)
        self.label_created.emit(self.bbox())
    
    def moved(self, x:int, y:int, mod: Qt.KeyboardModifier):
        self.corner2 = (x,y)
        self.temp_bbox_update.emit(self.bbox())

    def cancel(self):
        pass

    def confirm(self): 
        pass

    def bbox(self) -> qtc.QRect:
        x1, y1 = self.corner1
        x2, y2 = self.corner2
        
        return qtc.QRect(qtc.QPoint(x1,y1), qtc.QPoint(x2,y2))

class SAMLabeling(LabelManager):
    def __init__(self):
        super().__init__()
        self.sam = SAM_wrapper()
        self._default_xywh = (-10,-10,0,0)
        self.xywhs = []

    def process_image(self, image: np.ndarray): 
        return self.sam.segment(image, lambda : True)

    def clicked(self, x:int, y:int, mod: Qt.KeyboardModifier): 
        pass
    
    def released(self, x:int, y:int, mod: Qt.KeyboardModifier): 
        xywh = self.get_segmentation(x,y)
        
        match mod:
            case Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier: 
                if xywh in self.xywhs:
                    self.xywhs.remove(xywh)
                else:
                    self.xywhs.append(xywh)

            case Qt.KeyboardModifier.AltModifier: 
                if xywh in self.xywhs: self.xywhs.remove(xywh)

            case Qt.KeyboardModifier.NoModifier: 
                self.xywhs = [xywh]

        self.temp_bbox_update.emit(self.bbox())
    
    def moved(self, x:int, y:int, mod: Qt.KeyboardModifier):
        pass

    def cancel(self):
        self.xywhs.clear()
        self.temp_bbox_update.emit(self.bbox())

    def confirm(self): 
        if len(self.xywhs) == 0: return
        
        self.label_created.emit(self.bbox())
        self.xywhs.clear()

    def bbox(self) -> qtc.QRect:
        if len(self.xywhs) == 0:
            x,y,w,h = self._default_xywh
            return qtc.QRect(x,y,w,h)
        
        min_x = self.xywhs[0][0]
        min_y = self.xywhs[0][1]
        max_x = 0
        max_y = 0

        for x,y,w,h in self.xywhs:
            min_x = min(min_x , x)
            min_y = min(min_y , y)
            max_x = max(max_x , x+w)
            max_y = max(max_y , y+h)

        return qtc.QRect(qtc.QPoint(min_x, min_y), qtc.QPoint(max_x, max_y))
        
        
    def get_segmentation(self, x:int, y:int) -> Tuple:
        d = self.sam.detections
        masked_indices = np.where(d.mask[:,y,x])
        masks = np.take(d.mask, masked_indices, axis=0)[0] * 255.
        masks = [remove_stray_pixels(masks[i]) for i in range(len(masks))]
        xywhs = [cv2.boundingRect(cv2.findNonZero(mask)) for mask in masks]
        idx = np.argmin([w*h for x,y,w,h in xywhs])

        return xywhs[idx]
    
LABELING_CLASSES : Dict[str, type[LabelManager]]= {
    "Manual Labeling": DefaultLabeling,    
    "Segmentation (SAM)": SAMLabeling, 
}

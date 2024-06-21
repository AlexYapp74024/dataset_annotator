from __future__ import annotations

import os
from typing import List, Dict, Tuple
from pathlib import Path
import cv2
import numpy as np
import qimage2ndarray
import torch
import gc

from PySide6 import (
    QtWidgets as qtw, 
    QtGui as qtg, 
    QtCore as qtc,
)
from PySide6.QtCore import Qt

from ProjectManager import ProjectManager
from Labeling import *
from History_List import HistoryList

class ImageScene(qtw.QGraphicsScene):
    
    image_changed = qtc.Signal()
    labels_changed = qtc.Signal()
    
    clicked = qtc.Signal(int,int, Qt.KeyboardModifier)
    released = qtc.Signal(int,int, Qt.KeyboardModifier)
    moved = qtc.Signal(int,int, Qt.KeyboardModifier)
    confirm = qtc.Signal()
    cancel = qtc.Signal()

    def __init__(self, proj_manager: ProjectManager) -> None:
        super().__init__()
        
        self.proj_manager = proj_manager
        self._original_image : np.ndarray = None
        self._processed_image : np.ndarray = None
        self._label_path : Path = None
        self.show_processed : bool = False
        self.scale : float = 1.0

        self.labels : HistoryList[Label] = HistoryList(1,2,3)
        self.current_label : Class_Label = None

        self.label_manager : LabelManager = None
        self.set_up_label_manager(DefaultLabeling)

        self.labels_changed.connect(self.update_label_file)
        self.pixmap = self.addPixmap(qtg.QPixmap())

        line_pen = qtg.QPen(qtc.Qt.PenStyle.SolidLine)
        line_pen.setWidth(3)
        self.current_rect = self.addRect(-5,-5,-1,-1, line_pen)

    def set_up_label_manager(self, label_manager: type[LabelManager]):
        if self.label_manager is not None: 
            del self.label_manager
            gc.collect()
            torch.cuda.empty_cache()

        self.label_manager = label_manager()
        self.clicked.connect(self.label_manager.clicked)
        self.released.connect(self.label_manager.released)
        self.moved.connect(self.label_manager.moved)
        self.confirm.connect(self.label_manager.confirm)
        self.cancel.connect(self.label_manager.cancel)

        self.label_manager.temp_bbox_update.connect(self.temp_bbox_update)
        self.label_manager.label_created.connect(self.bbox_update)
        
        if self._original_image is not None:
            self._processed_image = self.label_manager.process_image(self._original_image)
            self.draw_bboxes()

    def open_image_file(self, image_path:Path, label_path:Path):
        image_path = cv2.imread(str(image_path))
        image = cv2.cvtColor(image_path, cv2.COLOR_BGR2RGB)
        self.image = image
        self._processed_image = self.label_manager.process_image(image)
        
        self._label_path = label_path
        if os.path.exists(self._label_path):
            with open(self._label_path, 'r') as file:
                self.labels = HistoryList(Label.from_str(line) for line in file.readlines())
        
        self.labels_changed.emit()
        self.current_label_index = None
        self.draw_bboxes()
        self.current_rect.hide()

    def update_label_file(self):
        with open(self._label_path, 'w') as file:
            for lb in self.labels:
                file.write(lb.to_coco_format() + "\n")

    def draw_bboxes(self):
        image = self.image.copy()
        for i, lb in enumerate(self.labels):
            thickness = 4 if i == self.current_label_index else 2
            lb.draw_rect(image, self.proj_manager.classes[lb.label_id].color, thickness)
        self.update_image(image)

    def update_image(self, image:np.ndarray = None):
        if image is None: image = self.image
        qimage : qtg.QImage = qimage2ndarray.array2qimage(image)
        self.pixmap.setPixmap(qtg.QPixmap(qimage.scaled(qimage.size() / self.scale, qtc.Qt.AspectRatioMode.KeepAspectRatio)))
        self.image_changed.emit()

    @property
    def image(self) -> np.ndarray:
        return self._processed_image if self.show_processed else self._original_image 
    
    @image.setter
    def image(self, image:np.ndarray):
        self._original_image = image
        self.update_image(image)

    def keyPress(self, event: qtg.QKeyEvent) -> None:
        key: int = event.key()
        modifier = event.modifiers()

        match key:
            case Qt.Key.Key_Escape | Qt.Key.Key_Delete:
                if self.current_label_index is not None:
                    if len(self.labels) == 0: return
                    del self.labels[self.current_label_index]
                    if self.current_label_index >= len(self.labels):
                        self.current_label_index = len(self.labels)
                    self.draw_bboxes()
                    self.labels_changed.emit()
                    self.confirm.emit()
                else:
                    self.cancel.emit()
            
            case Qt.Key.Key_Z:
                if modifier == Qt.KeyboardModifier.ControlModifier:
                    self.labels.undo()
                    self.draw_bboxes()
                    self.labels_changed.emit()

            case Qt.Key.Key_Return | Qt.Key.Key_Enter:
                self.confirm.emit()

    def wheelEvent(self, event: qtw.QGraphicsSceneWheelEvent) -> None:
        if event.modifiers() != qtc.Qt.KeyboardModifier.ControlModifier : return
        if self.image is None: return

        self.scale += event.delta() / 120 * -0.1
        self.update_image()

    def mousePressEvent(self, event: qtw.QGraphicsSceneMouseEvent) -> None:
        if event.button() == qtc.Qt.MouseButton.LeftButton and self.image is not None:
            x,y = (event.scenePos() * self.scale).toTuple()
            w,h,_ = self.image.shape

            if x >= 0 and x <= w and y >= 0 and y <= h:
                self.clicked.emit(int(x),int(y), event.modifiers())

    def mouseMoveEvent(self, event: qtw.QGraphicsSceneMouseEvent) -> None:
        if self.image is not None:
            x,y = (event.scenePos() * self.scale).toTuple()
            w,h,_ = self.image.shape

            if x >= 0 and x <= w and y >= 0 and y <= h:
                self.moved.emit(int(x),int(y), event.modifiers())

    def mouseReleaseEvent(self, event: qtw.QGraphicsSceneMouseEvent) -> None:
        if event.button() == qtc.Qt.MouseButton.LeftButton and self.image is not None:
            x,y = (event.scenePos() * self.scale).toTuple()
            w,h,_ = self.image.shape

            if x >= 0 and x <= w and y >= 0 and y <= h:
                self.released.emit(int(x),int(y), event.modifiers())


    def temp_bbox_update(self, rect:qtc.QRect):
        self.current_label_index = None
        self.current_rect.show()
        self.current_rect.setRect(rect)
        self.update()

    def bbox_update(self, rect:qtc.QRect):
        self.labels.append(Label.from_bbox(rect, self.image.shape, self.current_label.id))
        self.current_label_index = len(self.labels) - 1
        
        self.current_rect.hide()
        self.current_rect.setRect(rect)

        self.draw_bboxes()
        self.labels_changed.emit()
        self.update()

    def update_color(self, label:Class_Label):
        pen = self.current_rect.pen()
        pen.setColor(qtg.QColor(*label.color,255))
        self.current_label = label
        self.current_rect.setPen(pen)
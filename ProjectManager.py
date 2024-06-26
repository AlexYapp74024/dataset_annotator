from __future__ import annotations

import yaml
import os
from typing import List, Dict, Callable
from pathlib import Path
from itertools import zip_longest

from PySide6 import (
    QtWidgets as qtw, 
    QtGui as qtg, 
    QtCore as qtc,
)
from PySide6.QtCore import Qt

from Labeling import Class_Label, LabelManager
from Utils import *

def is_image_file(path:str) -> bool:
    IMAGE_EXTS = [".png",".jpg",".jpeg",".jpe",".jfif",".exif",".bmp",".dib",".rle",".tif",".tga",".dds",".webp"]
    return any(path.lower().endswith(ext) for ext in IMAGE_EXTS)

class Preprocess_Thread(qtc.QThread):
    image_processed = qtc.Signal(int)

    def __init__(self, project_manager: ProjectManager, *, cache_ahead:int = 5, cache_behind: int = 1) -> None:
        super().__init__()
        self.cashes : Dict[int, dict] = {}
        self._cache_indices = []
        self.proj_manager = project_manager
        self._to_cache = []
        self.process_img_callback: Callable[[np.ndarray], dict] = None
        
        self._reset_cache = False
        
        for i0, i1 in zip_longest(list(range(0, -cache_behind-1, -1)), list(range(1, cache_ahead+1))):
            if i0 is not None: self._cache_indices.append(i0)
            if i1 is not None: self._cache_indices.append(i1)

    def run(self): 
        while True:
            if self.process_img_callback is not None:
                to_cache = list(self._to_cache - self.cashes.keys())
                
                for idx in to_cache[:1]:
                    image = cv2.imread(str(self.proj_manager.image_paths[idx]))
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    self.cashes[idx] = self.process_img_callback(image)
                    self.image_processed.emit(idx)

                self._reset_cache = False
            self.msleep(200)

    def index_changed(self):
        pm = self.proj_manager
        index = pm.index
        self._to_cache = [i for i in [index + idx for idx in self._cache_indices] if i >= 0 and i < len(pm.image_paths)]
        self._reset_cache = True

    def clear_cache(self):
        self.cashes.clear()
        

class ProjectManager(qtc.QObject):
    image_updated = qtc.Signal(Path, Path, np.ndarray)

    def __init__(self, project_dir = "") -> None:
        super().__init__()
        self.yaml_file : str = ""
        self.yaml_data : dict = {}
        self._project_dir : str = project_dir
        self._classes : Dict[int, Class_Label] = {}
        self.image_paths : List[Path] = []

        self.find_data_yaml()
        self.cache = Preprocess_Thread(self)
        self.cache.image_processed.connect(self.cache_update)
        self.cache.start()

    @property
    def project_dir(self):
        return self._project_dir

    @project_dir.setter
    def project_dir(self, value:str):
        self._project_dir = value
        self.find_data_yaml()
        self.find_images()
    
    @property
    def classes(self) -> Dict[int, Class_Label]:
        if len(self._classes) == 0:
            with open(self.yaml_file, "r") as stream:
                self.yaml_data = yaml.safe_load(stream)
                for c in self.yaml_data["names"]:
                    cl = Class_Label(c)
                    self._classes[cl.id] = cl
        
        return self._classes

    @classes.setter
    def classes(self, class_list: Dict[int, Class_Label]) -> None:
        if not os.path.exists(self.project_dir): return
        if not os.path.exists(self.yaml_file): return
        self._classes = class_list

        self.yaml_data["names"] = class_list
        self.yaml_data["nc"] = len(class_list)
        
        with open(self.yaml_file, "w") as stream:
            yaml.dump(self.yaml_data, stream, default_flow_style=False)
    
    def find_images(self) -> None:
        if not os.path.exists(self.project_dir): return

        dirs_with_images = list(Path(root) for root, dirs, files in os.walk(self._project_dir) 
                                if any(is_image_file(file) for file in files))
        dirs_with_labels = list(dir.parent.joinpath("labels") for dir in dirs_with_images)
        list(dir.mkdir(exist_ok=True) for dir in dirs_with_labels)

        self.image_paths = list(dir.joinpath(file) for dir in dirs_with_images for file in os.listdir(dir) if is_image_file(file))

    @property
    def index(self) -> int:
        return self.yaml_data["current_index"]

    @index.setter
    def index(self, value:int):
        self.yaml_data["current_index"] = value
        self.cache.index_changed()
        
        if len(self.image_paths) > 0:
            self.image_updated.emit(self.image_path, self.label_path, self.saved_cache)
        
        with open(self.yaml_file, "w") as stream:
            yaml.dump(self.yaml_data, stream, default_flow_style=False)
    
    @property
    def image_path(self) -> Path:
        return self.image_paths[self.index]
    
    @property
    def label_path(self) -> Path:
        return Path("labels".join(str(self.image_path).rsplit("images", 1))).with_suffix(".txt")
    
    @property
    def saved_cache(self) -> np.ndarray|None:
        out = self.cache.cashes.get(self.index, None)
        return out

    def find_data_yaml(self) -> None:
        if not os.path.exists(self.project_dir): return
        self.yaml_file = f"{self._project_dir}/data.yaml"

        if not os.path.exists(self.yaml_file):
            self.classes = []
        else:
            self.classes
        
        self.index = self.yaml_data.get("current_index", 0)

    def has_yaml_file(self) -> bool: 
        return self.yaml_file != ""
    
    def has_image(self) -> bool: 
        return len(self.image_paths) != 0
    
    def label_manager_changed(self, label_manager:LabelManager) -> bool:
        self.cache.process_img_callback = label_manager.save_cache
        self.cache.clear_cache()

    def cache_update(self, index:int):
        if self.index == index:
            self.image_updated.emit(self.image_path, self.label_path, self.saved_cache)
    
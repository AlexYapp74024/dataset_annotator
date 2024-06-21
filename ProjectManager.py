import yaml
import os
from typing import List, Dict
from pathlib import Path

from Labeling import Class_Label
from Utils import *

def is_image_file(path:str) -> bool:
    IMAGE_EXTS = [".png",".jpg",".jpeg",".jpe",".jfif",".exif",".bmp",".dib",".rle",".tif",".tga",".dds",".webp"]
    return any(path.lower().endswith(ext) for ext in IMAGE_EXTS)

class ProjectManager(object):
    def __init__(self, project_dir = "") -> None:
        self.yaml_file : str = ""
        self.yaml_data : dict = {}
        self._project_dir : str = project_dir
        self._classes : Dict[int, Class_Label] = {}
        self.images_paths : List[Path] = []

        self.find_data_yaml()

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

        self.images_paths = list(dir.joinpath(file) for dir in dirs_with_images for file in os.listdir(dir) if is_image_file(file))

    @property
    def index(self):
        return self.yaml_data["current_index"]

    @index.setter
    def index(self, value:str):
        self.yaml_data["current_index"] = value
        
        with open(self.yaml_file, "w") as stream:
            yaml.dump(self.yaml_data, stream, default_flow_style=False)
    
    @property
    def image_path(self):
        return self.images_paths[self.index]
    
    @property
    def label_path(self):
        return Path("labels".join(str(self.image_path).rsplit("images", 1))).with_suffix(".txt")

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
        return len(self.images_paths) != 0
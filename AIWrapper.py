import os
import cv2
import numpy as np
import supervision as sv
# from inference.models import YOLOWorld
from PIL import Image
import requests
import torch
from segment_anything import sam_model_registry, SamPredictor, SamAutomaticMaskGenerator
from segment_anything.modeling import Sam
from typing import Callable

from PySide6 import (
    QtWidgets as qtw, 
    QtGui as qtg, 
    QtCore as qtc,
)
from PySide6.QtCore import Qt

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class SAM_wrapper():
    SAM_LINK = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth"
    SAM_FILE = "sam_vit_b.pth"

    def __init__(self, confirm_download_callback: Callable[[],bool] = lambda _ : True) -> None:
        self.sam : Sam = None
        
        if self.sam is None: 
            self.load_model(confirm_download_callback)

    def download_model(self):
        # Streaming, so we can iterate over the response.
        response = requests.get(SAM_wrapper.SAM_LINK, stream=True)

        # Sizes in bytes.
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024

        if not os.path.exists(SAM_wrapper.SAM_FILE):
            with open(SAM_wrapper.SAM_FILE, "wb") as file:
                for data in response.iter_content(block_size):
                    # progress_bar.update(len(data))
                    file.write(data)

            if total_size != 0:
                raise RuntimeError("Could not download file")
    
    def load_model(self, confirm_download_callback: Callable[[],bool]):
        if not os.path.exists(SAM_wrapper.SAM_FILE):
            if not confirm_download_callback():
                raise Exception("download rejected")
            self.download_model()

        SAM_ENCODER_VERSION = "vit_b"
        self.sam = sam_model_registry[SAM_ENCODER_VERSION](checkpoint=SAM_wrapper.SAM_FILE).to(device=DEVICE)
        self.mask_generator = SamAutomaticMaskGenerator(self.sam)
        # self.sam_predictor = SamPredictor(self.sam)

    def segment(self, image: np.ndarray) -> tuple[sv.Detections, np.ndarray]:
        sam_result = self.mask_generator.generate(image)
        mask_annotator = sv.MaskAnnotator(color_lookup=sv.ColorLookup.INDEX)
        detections = sv.Detections.from_sam(sam_result)
        annotated_images = mask_annotator.annotate(scene=image.copy(), detections=detections)
        return detections, annotated_images
    

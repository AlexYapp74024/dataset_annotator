from __future__ import annotations

import cv2
from hashlib import md5
from skimage.color import hsv2rgb
import numpy as np

def hash_to_hue(label:str) -> np.ndarray:
    hash = md5(label.encode()).hexdigest()
    hue = int(hash[:2],16)
    color = (hsv2rgb(np.array([[[hue/255.,1.,1.]]])) * 255)[0][0]
    return color

def remove_stray_pixels(image:np.ndarray) -> np.ndarray:
        input_image = cv2.threshold(image, 254, 255, cv2.THRESH_BINARY)[1]
        input_image_comp = cv2.bitwise_not(input_image)  # could just use 255-img

        kernel1 = np.array([[0, 0, 0],
                            [0, 1, 0],
                            [0, 0, 0]], np.uint8)
        kernel2 = np.array([[1, 1, 1],
                            [1, 0, 1],
                            [1, 1, 1]], np.uint8)

        hitormiss1 = cv2.morphologyEx(input_image, cv2.MORPH_ERODE, kernel1)
        hitormiss2 = cv2.morphologyEx(input_image_comp, cv2.MORPH_ERODE, kernel2)
        return cv2.bitwise_and(hitormiss1, cv2.bitwise_not(hitormiss2))
import cv2
import base64
import numpy as np

def image_to_base64(image: np.ndarray) -> str:
    image = cv2.imencode('.jpg', image)[1].tostring()
    image = base64.b64encode(image).decode("utf-8")
    return image

def base64_to_nparray(image: str) -> np.ndarray:
    image = base64.b64decode(image)
    image = np.asarray(bytearray(image), dtype=np.uint8)
    image = cv2.imdecode(image, -1)
    return image
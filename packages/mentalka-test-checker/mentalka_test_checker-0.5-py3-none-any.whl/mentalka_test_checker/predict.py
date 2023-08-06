from keras.models import load_model
import cv2
import numpy as np
from .setting import DONT_SHOW, logger, BASE_DIR
import time
import os

model_path = os.path.join(BASE_DIR, 'model/model_mnist.h5')
model = load_model(model_path)


def predict_img(img):
    try:
        width = int(28)
        height = int(28)
        dim = (width, height)
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        if not DONT_SHOW:
            time.sleep(0.001)
            cv2.imwrite(f'write/v_{str(int(time.time() * 1000))}.jpg', img)
        if np.sum(img) > 188000:
            return 10
        else:
            img = 255 - img
            img = img / 255
            if not DONT_SHOW:
                cv2.imshow(f'ff{4}', img)
            img = img.reshape(1, 28, 28, 1)
            return int(np.argmax( model.predict([img])))
    except Exception as ex:
        logger.warning(f'Ошибка при предсказании числа: {ex}')
import cv2
import numpy as np
from .setting import logger


def display(im, bbox):
    n = len(bbox)
    for j in range(n):
        cv2.line(im, tuple(bbox[j][0]), tuple(bbox[(j + 1) % n][0]), (255, 0, 0), 3)
    cv2.imshow("Results", im)


def read_qrcode(img):
    try:
        qrDecoder = cv2.QRCodeDetector()
        data, bbox, rectifiedImage = qrDecoder.detectAndDecode(img)
        if len(data) > 0:
            return data
        else:
            return 'cant find qrcode'
    except Exception as ex:
        logger.warning(f'Ошибка расопзновании QR кода: {ex}')

if __name__ == '__main__':
    inputImage = cv2.imread("data/v6.jpg")
    qrDecoder = cv2.QRCodeDetector()
    data, bbox, rectifiedImage = qrDecoder.detectAndDecode(inputImage)
    if len(data) > 0:
        print("Decoded Data : {}".format(data))
        display(inputImage, bbox)
        rectifiedImage = np.uint8(rectifiedImage);
        cv2.imshow("Rectified QRCode", rectifiedImage);
    else:
        print("QR Code not detected")
        cv2.imshow("Results", inputImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

import cv2
from .read_cell import make_it
from .qr_table1_table2 import  take_it
from .preprocessing import clever_resize
from .paint_orign import paint_marks
from .read_qrcode import read_qrcode
from .setting import logger
import numpy as np
from .utils import image_to_base64

def check(image, all_marks):
    try:
        if type(image) != type(np.array([])):
            image = np.array(image)
        qr_code = read_qrcode(image)
        # qr_code = 'v6x10_blankinfo_childinfo' #
        blank_type = qr_code.split('_')[0]
        image, scans, rects = take_it(image, blank_type)
        result = make_it(scans, blank_type)
        logger.info('Распознование проведено!')
    except Exception as ex:
        logger.warning(f'Ошибка при проверке бланка {ex}')
        return bytes([]), bytes([])

    if type(image) != type(np.array([])):
        image = np.array(image)
    try:
        for i, marks in enumerate(all_marks):
            painted_image = paint_marks(image, rects[i], marks, blank_type)
    except Exception as ex:
        logger.warning(f'Ошибка при исовании отметок {ex}')
        return bytes(result), bytes([])
    logger.info('Разметка проведена!')
    return bytes(result), bytes(painted_image)


def main():
    # параметр для сканируемого изображения
    args_image = '/home/yuna/Hobby/Test_checker_0.1/data/v6.jpg'
    # прочитать изображение
    image = cv2.imread(args_image)
    marks1 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    marks2 = [0, 1, 0, 1, 1, 0, 1, 0, 0, 1]
    all_marks = [marks1, marks2]
    #image = clever_resize(image)
    result, painted_iamge = check(image, all_marks)
    cv2.destroyAllWindows()
    return result

if __name__ == '__main__':
    main()

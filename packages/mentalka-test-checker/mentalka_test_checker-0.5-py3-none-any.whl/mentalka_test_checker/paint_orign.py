import cv2
from .setting import mark_size, correct_mark_color, wrong_mark_color, mark_thickness
from .setting import logger


def paint_marks(image, rect, marks, blank_type):
    try:
        (tl, tr, br, bl) = rect
        w = br[0] - bl[0]
        hl = bl[1] - tl[1]
        hr = br[1] - tr[1]
        for i in range(len(marks)):
            w_ = ((4 + 5 * i) * w / 52)
            xm = bl[0] + w_
            ymm = (((1 * hl / 16) * (w - w_) + (1 * hr / 16) * w_) / w)
            ym = ((bl[1] * (w - w_) + br[1] * w_) / w) - ymm
            x_new, y_new = int(xm), int(ym)
            if marks[i] == 0:
                image = cv2.line(image, (x_new - mark_size, y_new), (x_new + mark_size, y_new), wrong_mark_color, mark_thickness)
            else:
                image = cv2.line(image, (x_new - mark_size, y_new), (x_new + mark_size, y_new), correct_mark_color, mark_thickness)
                image = cv2.line(image, (x_new, y_new + mark_size), (x_new, y_new - mark_size), correct_mark_color, mark_thickness)
        return image
    except Exception as ex:
        logger.warning(f'Ошибка при наложении результатов проверки на изображение: {ex}')

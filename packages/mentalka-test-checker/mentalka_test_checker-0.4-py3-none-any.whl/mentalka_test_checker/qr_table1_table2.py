import numpy as np
import cv2
import imutils
from .setting import DONT_SHOW, logger
import time



def find_contours(grayImageBlur):
    v = np.median(grayImageBlur)
    sigma = 0.5
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    # теперь производим определение границы по методу Canny
    edgedImage = cv2.Canny(grayImageBlur, lower, upper, 3)
    # найти контуры на обрезанном изображении, рационально организовать область
    # оставить только большие варианты
    allContours = cv2.findContours(edgedImage.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    allContours = imutils.grab_contours(allContours)
    return allContours


def find_dimensions(allContours):
    # сортировка контуров области по уменьшению и сохранение топ-1
    allContours = sorted(allContours, key=cv2.contourArea, reverse=True)
    all_dimensions = []
    for contour in allContours:
        # aппроксимация контура
        perimeter = cv2.arcLength(contour, True)
        ROIdimensions = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        # изменение массива координат
        if ROIdimensions.shape == (4, 1, 2):
            ROIdimensions = ROIdimensions.reshape(4, 2)
            all_dimensions.append(ROIdimensions)
    return all_dimensions


def chose_contours(all_dimensions, img_high, img_weight, blank_type):
    try:
        table_1 = all_dimensions[0]
        table_2 = all_dimensions[1]
        if blank_type[0] == 'v':
            for i in range(len(all_dimensions)):
                contour_mid_h = (all_dimensions[i][2][1] + all_dimensions[i][3][1]) / 2
                if img_high * 0.2 < contour_mid_h and contour_mid_h < img_high * 0.6:
                    table_1 = all_dimensions[i]
                    break
        elif blank_type[0] == 'h':
            for i in range(len(all_dimensions)):
                contour_mid_w = (all_dimensions[i][2][0] + all_dimensions[i][3][0]) / 2
                if contour_mid_w > img_weight * 0.5:
                    table_1 = all_dimensions[i]
                    break
        elif blank_type[0] == 'q':
            for i in range(len(all_dimensions)):
                contour_mid_w = (all_dimensions[i][2][0] + all_dimensions[i][3][0]) / 2
                if contour_mid_w > img_weight * 0.5:
                    table_1 = all_dimensions[i]
                    break
        else:
            logger.warning('не удалось опознать тип бланка')
        table_1_right_side = sorted(table_1, key=lambda x: x[0])[2:]
        table_1_right_bottom = sorted(table_1_right_side, key=lambda x: x[1])[1][1]
        for i in range(len(all_dimensions)):
            right_side = sorted(all_dimensions[i], key=lambda x: x[0])[2:]
            right_top = sorted(right_side, key=lambda x: x[1])[0][1]
            if right_top > table_1_right_bottom:
                table_2 = all_dimensions[i]
                break
        return [table_1, table_2]
    except Exception as ex:
        logger.warning(f'Ошибка при выборе контуров таблиц: {ex}')



def find_coordinates(ROIdimensions):
    rect = np.zeros((4, 2), dtype="float32")

    s = np.sum(ROIdimensions, axis=1)

    rect[0] = ROIdimensions[np.argmin(s)]
    rect[2] = ROIdimensions[np.argmax(s)]

    diff = np.diff(ROIdimensions, axis=1)
    rect[1] = ROIdimensions[np.argmin(diff)]
    rect[3] = ROIdimensions[np.argmax(diff)]
    return rect


def find_dist(x1, x2, y1, y2):
    dist = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return dist


def find_max_width(rect):
    # верх-лево, верх-право, низ-право, низ-лево
    (tl, tr, br, bl) = rect

    # вычислить ширину ROI
    widthA = find_dist(tl[0], tr[0], tl[1], tr[1])
    widthB = find_dist(bl[0], br[0], bl[1], br[1])
    maxWidth = max(int(widthA), int(widthB))

    # вычислить высоту ROI
    heightA = find_dist(tl[0], bl[0], tl[1], bl[1])
    heightB = find_dist(tr[0], br[0], tr[1], br[1])
    maxHeight = max(int(heightA), int(heightB))

    return maxWidth, maxHeight


def transform_img(grayImage, rect, maxWidth, maxHeight):
    # набор итоговых точек для обзора всего документа
    # размер нового изображения
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # вычислить матрицу перспективного преобразования и применить её
    transformMatrix = cv2.getPerspectiveTransform(rect, dst)
    # преобразовать ROI
    scan = cv2.warpPerspective(grayImage, transformMatrix, (maxWidth, maxHeight))
    return scan, transformMatrix

def take_it(image, blank_type):
    try:
        start_time = time.time()
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # размытие картинки, чтобы убрать высокочастотный шум
        # это помогает определить контур в сером изображении
        grayImageBlur = cv2.blur(grayImage, (3, 3))
        allContours = find_contours(grayImageBlur)
        all_dimensions = find_dimensions(allContours)
        img_high = image.shape[0]
        img_weight = image.shape[1]
        all_rect = []
        for dim in all_dimensions:
            rect = find_coordinates(dim)
            all_rect.append(rect)
        all_dimensions = chose_contours(all_dimensions, img_high, img_weight, blank_type)
        rects = []
        scans = []
        for ROIdimensions in all_dimensions:
            rect = find_coordinates(ROIdimensions)

            maxWidth, maxHeight = find_max_width(rect)

            scan, t_matrix = transform_img(grayImage, rect, maxWidth, maxHeight)
            cv2.drawContours(image, [ROIdimensions], -1, (0, 255, 0), 2)
            rects.append(rect)
            scans.append(scan)
        if not DONT_SHOW:
            cv2.imshow('Contour Outline', image)
            print("--- %s seconds ---" % (time.time() - start_time))

        return image, scans, rects
    except Exception as ex:
        logger.warning(f'Ошибка при поиске таблиц задач: {ex}')
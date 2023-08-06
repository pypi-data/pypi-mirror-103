import numpy as np
import cv2
from .predict import predict_img
from .preprocessing import make_contrast
from .setting import DONT_SHOW, logger
import time


def crop_results_v(image, num, blank_type):
    try:
        w = image.shape[1]
        h = image.shape[0]
        y0 = 23 * h // 32
        y1 = 28 * h // 32
        if blank_type[1:] == '6x10':
            y0 = 24 * h // 32
            y1 = 29 * h // 32
        elif blank_type[1:] == '7x10':
            y0 = 49 * h // 64
            y1 = 59 * h // 64
        elif blank_type[1:] == '8x10':
            y0 = 51 * h // 64
            y1 = 59 * h // 64
        elif blank_type[1:] == '9x10':
            y0 = 52 * h // 64
            y1 = 60 * h // 64
        elif blank_type[1:] == '10x10':
            y0 = 53 * h // 64
            y1 = 60 * h // 64
        tetta = 0.1
        x0 = (31 + 80 * num) * w / 832
        x1 = (31 + 80 * (num + 1)) * w / 832
        zetta = (x1 - x0) * tetta
        x0, x1 = int(x0 - zetta), int(x1 + zetta)
        gretta = 1
        crop_img = image[y0 - gretta:y1 + gretta, x0:x1]
        if not DONT_SHOW:
            cv2.imwrite(f'write/v_0crop_{str(int(time.time() * 1000))}.jpg', crop_img)
            cv2.imshow('crop_mrop', image)
        return crop_img
    except Exception as ex:
        logger.warning(f'Ошибка при вырезании одного ответа: {ex}')

def crop_results_h(image, num, blank_type):
    try:
        w = image.shape[1]
        h = image.shape[0]
        y0 = 23 * h // 32
        y1 = 28 * h // 32
        if blank_type[1:] == '6x10':
            y0 = 24 * h // 32
            y1 = 29 * h // 32
        tetta = 0.05
        x0 = (31 + 80 * num) * w / 832
        x1 = (31 + 80 * (num + 1)) * w / 832
        zetta = (x1 - x0) * tetta
        x0, x1 = int(x0 - zetta), int(x1 + zetta)
        crop_img = image[y0:y1, x0:x1]
        if not DONT_SHOW:
            image = cv2.rectangle(image, (x0, y0), (x1, y1), (255, 255, 255), 1)
            cv2.imshow('crop_mrop', image)
        return crop_img
    except Exception as ex:
        logger.warning(f'Ошибка при вырезании одного ответа: {ex}')


def crop_three(contrast_scan, image):
    try:
        g = 0
        im2 = contrast_scan
        img_w = image.shape[1]
        img_h = image.shape[0]
        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        all_rects = []
        for i in range(len(contours)):
            cnt = contours[i]
            im = im2.copy()
            im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
            cv2.drawContours(im,[cnt],0,255,-1)
            cv2.imwrite(f'write/z_{time.time()}_' + str(i) + '.png', im)
            x,y,w,h = cv2.boundingRect(cnt)
            if w<h*1.4 and h<w*1.4 and w > 0.25 * img_w and h > 0.6 * img_h:
                all_rects.append([x,y,w,h])

        all_rects = sorted(all_rects, key=lambda x: x[-1] * x[-2])[-3:]
        all_rects = sorted(all_rects, key=lambda x: x[0])
        while len(all_rects) < 3:
            all_rects.append([0, 0, 0, 0])
        x,y,w,h = all_rects[0][:4]
        if not(0.05 * img_w < x and x < 0.15 * img_w):
            x = int(0.1 * img_w)
        if not (0.13 * img_h < y < 0.22 * img_h):
            y = int(0.19 * img_h)
        if not(0.2 * img_w < w < 0.3 * img_w):
            w = int(0.26 * img_w)
        if not (0.55 * img_h < h < 0.74 * img_h):
            h = int(0.64 * img_h)
        image1 = im2[y+ g:y + h -g,x+g:x+w-g]

        x,y,w,h = all_rects[1][:4]
        if not(0.32 * img_w < x < 0.42 * img_w):
            x = int(0.36 * img_w)
        if not (0.13 * img_h < y < 0.22 * img_h):
            y = int(0.19 * img_h)
        if not(0.2 * img_w < w < 0.3 * img_w):
            w = int(0.26 * img_w)
        if not (0.55 * img_h < h < 0.74 * img_h):
            h = int(0.64 * img_h)
        image2 = im2[y+ g:y + h -g,x+g:x+w-g]

        x,y,w,h = all_rects[2][:4]
        if not(0.6 * img_w < x < 0.72 * img_w):
            x = int(0.67 * img_w)
        if not (0.13 * img_h < y < 0.22 * img_h):
            y = int(0.19 * img_h)
        if not(0.22 * img_w < w < 0.32 * img_w):
            w = int(0.28 * img_w)
        if not (0.55 * img_h < h < 0.74 * img_h):
            h = int(0.64 * img_h)
        image3 = im2[y+ g:y + h -g,x+g:x+w-g]
        return image1, image2, image3
    except Exception as ex:
        logger.warning(f'Ошибка при вырезании одной цифры ответа: {ex}')



def make_it(scans, blank_type):
    try:
        table_1, table_2 = scans
        result = []
        for table in [table_1, table_2]:
            table_result = []
            for num in range(10):
                if not DONT_SHOW:
                    print(num)
                try:
                    if blank_type[0] == 'v':
                        scan = crop_results_v(table, num, blank_type)
                    else:
                        scan = crop_results_h(table, num, blank_type)
                    bg_img = cv2.medianBlur(scan, 25)
                    diff_img = 255 - cv2.absdiff(scan, bg_img)
                    norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX,
                                             dtype=cv2.CV_8UC1)
                    if not DONT_SHOW:
                        cv2.imshow('norm_img', cv2.resize(norm_img, (0, 0), fx=3.5, fy=3.5))
                        cv2.imwrite(f'write/aaaaaa{num}.png', norm_img)

                    contrast_scan = make_contrast(scan)
                    contrast_img = make_contrast(norm_img)
                    croped_one, croped_two, croped_three = crop_three(contrast_scan, contrast_img)
                    result_one = predict_img(croped_one)
                    result_two = predict_img(croped_two)
                    result_three = predict_img(croped_three)
                    result_list = [result_one, result_two, result_three]
                    table_result.extend(result_list)
                except:
                    table_result.append('error')
                    if not DONT_SHOW:
                        print('Не удалось распознать цифры в ячейке!')
            result.extend(table_result)
        return result
    except Exception as ex:
        logger.warning(f'Ошибка при работе распозновании одной таблицы: {ex}')



if __name__ == '__main__':
    pass

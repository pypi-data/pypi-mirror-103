import cv2
from skimage.filters import threshold_local


def img_resize(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return image


def clever_resize(image):
    if image.shape[1] >= image.shape[0] >= 1300:
        scale_percent = 100000 // image.shape[1]
        return img_resize(image, scale_percent)
    elif image.shape[0] > image.shape[1] > 1300:
        scale_percent = 100000 // image.shape[0]
        return img_resize(image, scale_percent)
    return image


def make_contrast(img):
    th = threshold_local(img, 9, offset=10, method="gaussian")
    contrast_img = (img > th).astype("uint8") * 255
    return contrast_img


if __name__ == '__main__':
    pass

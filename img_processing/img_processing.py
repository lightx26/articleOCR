import cv2
import numpy as np


def resize_image(image, scale_percent=None, new_width=1000):
    if scale_percent is None:
        scale_percent = new_width / image.shape[1] * 100

    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


def global_thresholding(image, ksize):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)

    return thresh_image


def adaptive_thresholding(image, blocksize=251):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray_image, (9, 9), 0)

    thresh_image = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize, 2)

    return thresh_image


def find_contours(thresh_image):
    contours, hierarchy = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def filter_contours(contours, filter_object):
    filtered_contours = []

    mean_height = np.mean([cv2.boundingRect(cnt)[3] for cnt in contours if 20 < cv2.boundingRect(cnt)[3] < 60])

    if filter_object == "lines":
        # mean_width = np.mean([cv2.boundingRect(cnt)[2] for cnt in contours])

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # print(h)

            # Filter based on aspect ratio, area, and other desired criteria
            # if (h > 30 and h < 150):
            if mean_height * 0.5 < h < mean_height * 1.5:
                filtered_contours.append(cnt)

    elif filter_object == "words":
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # if mean_height * 0.75 < h < mean_height * 1.5 and w < 100:
            if 10 < h < 60:
                filtered_contours.append(cnt)

    return filtered_contours


def sort_contours(cnts, method="left-to-right"):
    reverse = False
    i = 0
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    if method == "top-to-bottom":
        i = 1

    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    if len(boundingBoxes) > 0:
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                            key=lambda b: b[1][i], reverse=reverse))
    # return the list of sorted contours and bounding boxes
    return cnts, boundingBoxes

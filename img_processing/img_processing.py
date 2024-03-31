import os
import random
import string
import time

import cv2
import numpy as np
import pandas as pd


# import pytesseract


def resize_image(image, scale_percent=None, new_width=1000):
    if scale_percent is None:
        scale_percent = new_width / image.shape[1] * 100

    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


def preprocess_image_global(image, ksize):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)

    # random_string1 = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
    # cv2.imshow(random_string1, thresh_image)

    # Display the image
    # random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
    # cv2.imshow(random_string, dst)
    return thresh_image


def preprocess_image(image, ksize, blocksize=251):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)

    thresh_image = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize, 2)

    # thresh_image = cv2.threshold((gray_image + thresh_image)//2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # random_string1 = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
    # cv2.imshow(random_string1, 255 - thresh_image)

    return thresh_image


def preprocess_image2(image, ksize):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    image_final = cv2.bitwise_and(gray_image, gray_image, mask=mask)
    ret, thresh_image = cv2.threshold(image_final, 0, 255, cv2.THRESH_OTSU)

    random_string1 = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
    cv2.imshow(random_string1, 255 - thresh_image)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, ksize)
    # ero = cv2.erode(255 - thresh_image, (3,3), iterations=1)
    # random_string2 = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
    # cv2.imshow(random_string2, ero)
    dst = cv2.dilate(255 - thresh_image, kernel, iterations=1)

    # Display the image
    # random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
    # cv2.imshow(random_string, dst)
    return dst
    # return thresh_image


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


def detect_lines(image, ksize=(8, 2), show_result=False):
    preprocessed_image = preprocess_image(image, ksize, blocksize=251)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, ksize)
    dilated = cv2.dilate(255 - preprocessed_image, kernel, iterations=2)

    contours = find_contours(dilated)
    line_contours = filter_contours(contours, filter_object="lines")
    line_contours = sort_contours(line_contours, method="top-to-bottom")[0]

    regions = []
    regions_coor = []

    image2 = image.copy()

    for contour in line_contours:
        x, y, w, h = cv2.boundingRect(contour)
        regions_coor.append((x, y, w, h))
        cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 255, 0), 1)
        regions.append(image[y:y + h, x:x + w])

    if show_result:
        cv2.imshow("Lines detected", image2)

    return regions, regions_coor


def detect_words(image, ksize=(2, 2), show_result=False):
    preprocessed_image = preprocess_image(image, ksize, blocksize=101)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, ksize)
    dilated = cv2.dilate(255 - preprocessed_image, kernel, iterations=1)

    contours = find_contours(dilated)
    word_contours = filter_contours(contours, filter_object="words")
    word_contours = sort_contours(word_contours, method="left-to-right")[0]

    regions = []
    regions_coor = []

    image2 = image.copy()

    for contour in word_contours:
        x, y, w, h = cv2.boundingRect(contour)
        regions_coor.append((x, y, w, h))
        cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 255, 0), 1)
        regions.append(image[y:y + h, x:x + w])

    if show_result:
        random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
        cv2.imshow(random_string, image2)
        # cv2.imshow("Words detected", image2)

    return regions, regions_coor


def __extract_lines(image, ksize=(8, 2)):
    preprocessed_image = 255 - preprocess_image(image, ksize, blocksize=251)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, ksize)
    dilated = cv2.dilate(preprocessed_image, kernel, iterations=2)

    contours = find_contours(dilated)
    line_contours = filter_contours(contours, filter_object="lines")
    line_contours = sort_contours(line_contours, method="top-to-bottom")[0]

    lines = []

    for contour in line_contours:
        x, y, w, h = cv2.boundingRect(contour)

        mask = np.zeros_like(preprocessed_image)
        cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)
        out = np.zeros_like(preprocessed_image)  # Extract out the object and place into output image
        out[mask == 255] = preprocessed_image[mask == 255]

        lines.append(out[y:y + h, x:x + w])

    return lines


def extract_words(image, ksize=(2, 2), show_result=False):
    lines_orig = detect_lines(image)[0]
    lines = __extract_lines(image)

    words = []

    for i, line in enumerate(lines):

        dilated = cv2.dilate(line, cv2.getStructuringElement(cv2.MORPH_CROSS, ksize), iterations=1)

        contours = find_contours(dilated)
        word_contours = filter_contours(contours, filter_object="words")
        word_contours = sort_contours(word_contours, method="left-to-right")[0]

        linecpy = lines_orig[i].copy()
        for contour in word_contours:
            x, y, w, h = cv2.boundingRect(contour)

            cv2.rectangle(linecpy, (x, y), (x + w, y + h), (0, 255, 0), 1)

            words.append(lines_orig[i][y:y + h, x:x + w])

        if show_result:
            # for i, line in enumerate(lines):
            #     cv2.imshow("Line " + str(i), line)
            #     cv2.imshow("Line " + str(i) + " orig", lines_orig[i])
            random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
            cv2.imshow(random_string, linecpy)

    return words


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


def separate_pages(image, ksize):
    line_coor = pd.DataFrame(detect_lines(image, ksize=ksize, show_result=False)[1])

    threshold = line_coor.iloc[:, 0].mean()

    page_1 = line_coor[line_coor.iloc[:, 0] < threshold].iloc[:, [0, 2]].sum(axis=1).mean()
    page_2 = line_coor[line_coor.iloc[:, 0] > threshold].iloc[:, 0].mean()

    x_line = (page_1 + page_2) // 2
    #
    # Separate pages based on the x-coordinate of the center of the bounding box
    pages = []

    pages.append(image[:, :int(x_line)])
    pages.append(image[:, int(x_line):])

    return pages

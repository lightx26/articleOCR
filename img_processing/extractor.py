import random
import string
import numpy as np
import pandas as pd

from img_processing import img_processing as imgp

import cv2


def detect_lines(image, ksize=(8, 2), show_result=False):
    '''
    Detects lines in an image, work effectively with straight text lines
    :param image:
    :param ksize:
    :param show_result:
    :return: A list of images contains text line (cut from original image) and a list of coordinates of the rectangle bounding each line
    '''
    preprocessed_image = imgp.preprocess_image(image, ksize, blocksize=251)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, ksize)
    dilated = cv2.dilate(255 - preprocessed_image, kernel, iterations=2)

    contours = imgp.find_contours(dilated)
    line_contours = imgp.filter_contours(contours, filter_object="lines")
    line_contours = imgp.sort_contours(line_contours, method="top-to-bottom")[0]

    lines = []
    lines_coor = []

    image2 = image.copy()

    for contour in line_contours:
        x, y, w, h = cv2.boundingRect(contour)
        lines_coor.append((x, y, w, h))
        cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 255, 0), 1)
        lines.append(image[y:y + h, x:x + w])

    if show_result:
        cv2.imshow("Lines detected", image2)

    return lines, lines_coor


def extract_lines(image, ksize=(8, 2)):
    '''
    Extracts lines from an image, work effectively with curved text lines
    :param image: original image
    :param ksize: kernel size for dilation (x: horizontal, y: vertical)
    :return: A list of images (black background) containing the extracted lines (white text)
    '''
    preprocessed_image = 255 - imgp.preprocess_image(image, ksize, blocksize=251)

    dilated_image = cv2.dilate(preprocessed_image, cv2.getStructuringElement(cv2.MORPH_CROSS, ksize), iterations=2)

    line_contours = imgp.find_contours(dilated_image)
    line_contours = imgp.filter_contours(line_contours, filter_object="lines")
    line_contours = imgp.sort_contours(line_contours, method="top-to-bottom")[0]

    lines = []

    for contour in line_contours:
        x, y, w, h = cv2.boundingRect(contour)

        mask = np.zeros_like(preprocessed_image)
        cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)
        out = np.zeros_like(preprocessed_image)  # Extract out the object and place into output image
        out[mask == 255] = preprocessed_image[mask == 255]

        lines.append(out[y:y + h, x:x + w])

    return lines


def detect_words(image, ksize=(2, 2), show_result=False):
    '''
    Detects words in an image using the extracted lines
    :param image:
    :param ksize:
    :return: A list of images contains words (cut from original image)
    '''
    lines_orig = detect_lines(image)[0]
    lines = extract_lines(image)

    words = []
    words_coor = []

    for i, line in enumerate(lines):

        dilated = cv2.dilate(line, cv2.getStructuringElement(cv2.MORPH_CROSS, ksize), iterations=1)

        contours = imgp.find_contours(dilated)
        word_contours = imgp.filter_contours(contours, filter_object="words")
        word_contours = imgp.sort_contours(word_contours, method="left-to-right")[0]

        linecpy = lines_orig[i].copy()

        for contour in word_contours:
            x, y, w, h = cv2.boundingRect(contour)

            cv2.rectangle(linecpy, (x, y), (x + w, y + h), (0, 255, 0), 1)

            words.append(lines_orig[i][y:y + h, x:x + w])
            words_coor.append((x, y, w, h))

        if show_result:
            # for i, line in enumerate(lines):
            #     cv2.imshow("Line " + str(i), line)
            #     cv2.imshow("Line " + str(i) + " orig", lines_orig[i])
            random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
            cv2.imshow(random_string, linecpy)

    return words, words_coor


def separate_pages(image, ksize):
    line_coor = pd.DataFrame(detect_lines(image, ksize=ksize, show_result=False)[1])

    threshold = line_coor.iloc[:, 0].mean()

    page_1 = line_coor[line_coor.iloc[:, 0] < threshold].iloc[:, [0, 2]].sum(axis=1).mean()
    page_2 = line_coor[line_coor.iloc[:, 0] > threshold].iloc[:, 0].mean()

    x_line = (page_1 + page_2) // 2
    #
    # Separate pages based on the x-coordinate of the center of the bounding box
    return [image[:, :int(x_line)], image[:, int(x_line):]]

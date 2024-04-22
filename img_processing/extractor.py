import random
import string
import numpy as np
from img_processing import img_processing as imgp
import cv2


def detect_lines(image, ksize=(12, 4), show_result=False):
    """
    Detects lines in an image, work effectively with straight text lines
    :param image:
    :param ksize:
    :param show_result:
    :return: A list of images contains text line (cut from original image) and a list of coordinates of the rectangle bounding each line
    """
    preprocessed_image = imgp.adaptive_thresholding(image, blocksize=15, c=10)

    median_blur = cv2.medianBlur(preprocessed_image, 3)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, ksize)
    dilated = cv2.dilate(255 - median_blur, kernel, iterations=2)

    contours = imgp.find_contours(dilated)
    line_contours = imgp.filter_contours(contours, filter_object="lines")
    # line_contours = imgp.sort_contours(line_contours, method="top-to-bottom")[0]
    line_contours = imgp.cluster_by_line(imgp.sort_contours(line_contours, method="top-to-bottom")[0])

    lines = []
    lines_coor = []

    image2 = image.copy()

    for line in line_contours:
        sub_line = []
        sub_line_coor = []
        for contour in line:
            x, y, w, h = cv2.boundingRect(contour)
            sub_line_coor.append((x, y, w, h))
            cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 255, 0), 1)
            sub_line.append(image[y:y + h, x:x + w])
        lines.append(sub_line)
        lines_coor.append(sub_line_coor)
    if show_result:
        # random_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
        random_name = "detected_lines"
        cv2.imwrite(random_name + ".jpg", image2)
        # cv2.imshow("Lines detected", image2)

    return lines, lines_coor


def extract_lines_mask(image, ksize=(12, 4)):
    """
    Extracts lines from an image, work effectively with curved text lines
    :param image: original image
    :param ksize: kernel size for dilation (x: horizontal, y: vertical)
    :return: A list of images (black background) containing the extracted lines (white text)
    """

    hl_text_preprocessed = 255 - imgp.adaptive_thresholding(image, blur=False, blocksize=51, c=4)
    preprocessed_image = imgp.adaptive_thresholding(image, blocksize=15, c=10)

    median_blur = cv2.medianBlur(preprocessed_image, 3)

    dilated_image = cv2.dilate(255 - median_blur, cv2.getStructuringElement(cv2.MORPH_CROSS, ksize), iterations=2)

    line_contours = imgp.find_contours(dilated_image)
    line_contours = imgp.filter_contours(line_contours, filter_object="lines")
    # line_contours = imgp.sort_contours(line_contours, method="top-to-bottom")[0]
    line_contours = imgp.cluster_by_line(imgp.sort_contours(line_contours, method="top-to-bottom")[0])

    lines = []

    for line in line_contours:
        sub_line = []
        for contour in line:
            x, y, w, h = cv2.boundingRect(contour)

            mask = np.zeros_like(preprocessed_image)
            cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)
            out = np.zeros_like(preprocessed_image)  # Extract out the object and place into output image
            out[mask == 255] = hl_text_preprocessed[mask == 255]

            sub_line.append(out[y:y + h, x:x + w])
        lines.append(sub_line)
    return lines


def extract_lines_image(image, ksize=(12, 4)):
    '''
    Extracts lines from an image, work effectively with curved text lines
    :param image: original image
    :param ksize: kernel size for dilation (x: horizontal, y: vertical)
    :return: A list of images containing the convexhull around original text
    '''

    # hl_text_preprocessed = 255 - imgp.adaptive_thresholding(image, blur=False, blocksize=51, c=4)
    preprocessed_image = 255 - imgp.adaptive_thresholding(image, blocksize=15)

    dilated_image = cv2.dilate(preprocessed_image, cv2.getStructuringElement(cv2.MORPH_CROSS, ksize), iterations=2)

    line_contours = imgp.find_contours(dilated_image)
    line_contours = imgp.filter_contours(line_contours, filter_object="lines")
    # line_contours = imgp.sort_contours(line_contours, method="top-to-bottom")[0]
    line_contours = imgp.cluster_by_line(imgp.sort_contours(line_contours, method="top-to-bottom")[0])

    lines = []

    for line in line_contours:
        for contour in line:
            x, y, w, h = cv2.boundingRect(contour)

            hull = cv2.convexHull(contour)

            mask = np.full_like(image, 255)
            cv2.drawContours(mask, [hull], -1, (0, 0, 0), -1)
            out = np.full_like(image, 255)  # Extract out the object and place into output image
            out[mask == 0] = image[mask == 0]

            lines.append(out[y:y + h, x:x + w])

    return lines


# def detect_words(image, ksize=(8, 10), show_result=False):
#     '''
#     Detects words in an image using the extracted lines
#     :param image:
#     :param ksize:
#     :return: A list of images contains words (cut from original image)
#     '''
#     lines_orig = detect_lines(image, show_result=False)[0]
#     lines = extract_lines_mask(image)
#
#     words = []
#     words_coor = []
#
#     for i, line in enumerate(lines):
#         for j, sub_line in enumerate(line):
#
#             dilated = cv2.dilate(sub_line, cv2.getStructuringElement(cv2.MORPH_RECT, ksize), iterations=1)
#
#             # random_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
#             # cv2.imshow(random_name, dilated)
#
#             contours = imgp.find_contours(dilated)
#             word_contours = imgp.filter_contours(contours, filter_object="words")
#             word_contours = imgp.sort_contours(word_contours, method="left-to-right")[0]
#
#             linecpy = lines_orig[i][j].copy()
#
#             for contour in word_contours:
#                 x, y, w, h = cv2.boundingRect(contour)
#
#                 if imgp.is_none_text(lines_orig[i][j][y:y + h, x:x + w]):
#                     continue
#
#                 cv2.rectangle(linecpy, (x, y), (x + w, y + h), (0, 255, 0), 1)
#
#                 words.append(lines_orig[i][j][y:y + h, x:x + w])
#                 words_coor.append((x, y, w, h))
#
#             if show_result:
#                 # for i, line in enumerate(lines):
#                 #     cv2.imshow("Line " + str(i), line)
#                 #     cv2.imshow("Line " + str(i) + " orig", lines_orig[i])
#                 random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
#                 cv2.imshow(random_string, linecpy)
#
#     return words, words_coor


def detect_words_in_line(line, mask, ksize=(6, 6), show_result=False):
    '''
    Detects words in a line
    :param line: original line
    :param mask: mask of the line
    :param ksize: kernel size for dilation (x: horizontal, y: vertical)
    :param show_result:
    :return: A list of images contains words (cut from original line)
    '''
    dilated = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_RECT, ksize), iterations=2)

    contours = imgp.find_contours(dilated)
    word_contours = imgp.filter_contours(contours, filter_object="words")
    word_contours = imgp.sort_contours(word_contours, method="left-to-right")[0]

    words = []
    words_coor = []

    for contour in word_contours:
        x, y, w, h = cv2.boundingRect(contour)

        if imgp.is_none_text(line[y:y + h, x:x + w]):
            continue
        words.append(line[y:y + h, x:x + w])
        words_coor.append((x, y, w, h))

    if show_result:
        line_copy = line.copy()
        for contour in word_contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(line_copy, (x, y), (x + w, y + h), (0, 255, 0), 1)

        random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
        cv2.imshow(random_string, line_copy)

    return words, words_coor


def separate_pages(image):
    """
    Separates double pages into two single pages
    :param image: original image
    :return: A list of two images, each contains one page
    """
    height, width = image.shape[:2]

    return [image[:, :width // 2], image[:, width // 2:]]

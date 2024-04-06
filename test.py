import os
import random
import string

import numpy as np
from jdeskew.estimator import get_angle
from jdeskew.utility import rotate
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image
from img_processing import img_processing as imgp, extractor
import cv2

image_path = 'data/test/test2_1.jpg'
output_folder = 'data/output'
image = cv2.imread(image_path)

image = imgp.resize_image(image, new_width=1000)
# preprocessed1 = imgp.global_thresholding(image, True)
preprocessed = imgp.adaptive_thresholding(image,  blocksize=15)
# cv2.imwrite(os.path.join(output_folder, 'oriprp.jpg'), 255 - imgp.adaptive_thresholding(image, blur=False, blocksize=51, c=4))
# height, width = preprocessed.shape
# cv2.imshow("Preprocessed image 1", preprocessed[:height//2, :])
# cv2.imshow("Preprocessed image 2", preprocessed[height//2:, :])
# cv2.imshow("Preprocessed image", preprocessed)
# cv2.imwrite(os.path.join(output_folder, 'test2_1_prp.jpg'),255- preprocessed)


# kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (12, 3))
# dilated = cv2.dilate(255 - preprocessed, kernel, iterations=2)
# cv2.imwrite(os.path.join(output_folder, 'test2_1_dilated.jpg'), dilated)
# cv2.imshow("Dilated image 1", dilated[:height//2, :])
# cv2.imshow("Dilated image 2", dilated[height//2:, :])
# cv2.imshow("Dilated image", dilated)

line_rec = extractor.detect_lines(image, (12, 3), show_result=False)[0]
line_prp = extractor.extract_lines_mask(image, (12, 3))
# #
# cv2.imwrite(os.path.join(output_folder, 'mline6.jpg'), line_rec[6][0])

# for i, line in enumerate(line_prp):
#     for j, sub_line in enumerate(line):
#         random_name1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
#         random_name2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
#         cv2.imshow(random_name1, sub_line)
#         cv2.imshow(random_name2, line_rec[i][j])

words = extractor.detect_words_in_line(line_rec[6][0], line_prp[6][0], ksize=(6,6), show_result=True)[0]
# for i, word in enumerate(words):
#     random_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
#     cv2.imwrite(random_name + ".jpg", word)
# cv2.imwrite(os.path.join(output_folder, 'word.jpg'), words[0])



# words = extractor.detect_words(image, (10, 6), show_result=False)[0]

# for line in line_rec[1]:
#     print(line)

# words = extractor.detect_words(image, (4, 2), show_result=True)[0]



# kernel = cv2.getStructuringElement(cv2.MORPH_DILATE, (5, 15))



# contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# hull = cv2.convexHull(contours[15:20])
#
# image2 = image.copy()
# cv2.drawContours(image2, contours[15:20], -1, (0, 0, 255), 1)
# cv2.drawContours(image2, [hull], -1, (0, 255, 0), 1)
# for contour in hull:
    # x, y, w, h = cv2.boundingRect(contour)
    # cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 255, 0), 1)


# for contour in contours:
#     print(cv2.contourArea(contour))
#     x, y, w, h = cv2.boundingRect(contour)
#     cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 0, 255), 1)

# full_line = [contour for contour in contours if 15000 < cv2.contourArea(contour) < 30000 and cv2.boundingRect(contour)[2] > 600]
#
# full_line_area = [cv2.contourArea(contour) for contour in full_line]
#
# for contour in full_line:
#     print(cv2.contourArea(contour))
#     x, y, w, h = cv2.boundingRect(contour)
#     cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 255, 0), 1)
#
# print("Mean height: ", np.mean([cv2.boundingRect(contour)[3] for contour in full_line]))
# print("Median height: ", np.median([cv2.boundingRect(contour)[3] for contour in full_line]))
# print("Min height: ", np.min([cv2.boundingRect(contour)[3] for contour in full_line]))
# print("Max height: ", np.max([cv2.boundingRect(contour)[3] for contour in full_line]))
# print("Mean: ", np.mean(full_line_area))
# print("Median", np.median(full_line_area))
#
# print("Max: ", np.max([cv2.contourArea(contour) for contour in contours]))
#
#
# cv2.imshow("Lines detected 1", image2[:height//2, :])
# cv2.imshow("Lines detected 2", image2[height//2:, :])


# lines_rec = extractor.detect_lines(image, ksize=(10, 2), show_result=True)[0]
# lines_cur = extractor.extract_lines(image, ksize=(10, 2))
# for i, line in enumerate(lines_rec):
#     random_name1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
#     cv2.imshow(random_name1, line)
#     random_name2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
#     cv2.imshow(random_name2, lines_cur[i])

# ksize = (8, 2)
#
# # Resize image for better results
# image = imgp.resize_image(image, new_width=1200)
# # regions = imgp.detect_lines(image, ksize=ksize, show_result=True)
# image0 = imgp.adaptive_thresholding(image, ksize)
# # cv2.imshow("Preprocessed image", image0)
#
# pages = imgp.separate_pages(image, ksize=ksize)
#
# cv2.imshow("First page", pages[0])
# cv2.imshow("Second page", pages[1])
#
# # ----------------- Detecting lines -----------------
# # Configure scale_percent, ksize and blocksize for different results
# # regions = imgp.detect_lines(pages[0], ksize=ksize, show_result=True)
#
# config = Cfg.load_config_from_name('vgg_seq2seq')
# config['device'] = 'cpu'
# detector = Predictor(config)
#
# # for page in pages:
# # lines = imgp.extract_lines(pages[0], ksize=ksize, save_result=(True, 'data/output'))
# lines = imgp.detect_lines(pages[0], ksize=ksize, show_result=True)[0]
#
# # for line in lines:
# #     line_img = Image.fromarray(line)
# #     s = detector.predict(line_img)
# #     with open('output2.txt', 'a', encoding='utf-8') as file:
# #             # Write some text to the file
# #         file.write(s + "\n\n")
#
# # for line in lines:
# #     angle = get_angle(line)
# #     line = rotate(line, angle)
# #     words = imgp.detect_words(lines[0], ksize=(2, 3), show_result=True)[0]
#
# angle = get_angle(lines[0])
# line = rotate(lines[0], angle)
# words = imgp.detect_words(lines[0], ksize=(2, 3), show_result=True)[0]
# for word in words:
#     word_img = Image.fromarray(word)
#     s = detector.predict(word_img)
#     with open('output3.txt', 'a', encoding='utf-8') as file:
#         # Write some text to the file
#         file.write(s + " ")
#
#

# Press enter to destroy all windows
cv2.waitKey(0)
cv2.destroyAllWindows()

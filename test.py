import os
import random
import string
from pathlib import Path

import numpy as np
from img_processing import img_processing as imgp, extractor
import cv2
from jdeskew.estimator import get_angle
from jdeskew.utility import rotate

image_path = "data/input/test.jpeg"
output_folder = "data/output"

image = cv2.imread(image_path)

image = imgp.resize_image(image, new_width=2000)
image = extractor.separate_pages(image)[0]

line_ksize = (12, 4)
word_ksize = (4, 6)

preprocessed_image = imgp.adaptive_thresholding(image, c=10)
cv2.imshow("preprocessed: ", preprocessed_image)

median_blur = cv2.medianBlur(preprocessed_image, 3)
cv2.imshow('median_blur', median_blur)

kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, line_ksize)
dilated = cv2.dilate(255 - median_blur, kernel, iterations=2)

cv2.imshow("dilated: ", dilated[dilated.shape[0] // 2 - 100:, :])

# lines_bound = extractor.detect_lines(image, ksize=line_ksize, show_result=True)
# line_prp = extractor.extract_lines_mask(image, ksize=line_ksize)
#
# left_offset = np.median([line[0][0] for line in lines_bound[1] if line[0][2] > 500])
# right_offset = np.median([line[-1][0] + line[-1][2] for line in lines_bound[1] if line[-1][2] > 500])
#
# num = 0
# for i, line in enumerate(lines_bound[0]):
#     for j, subline in enumerate(line):
#         if (lines_bound[1][i][j][0] < left_offset - 100) or (
#                 lines_bound[1][i][j][0] + lines_bound[1][i][j][2] > right_offset + 100):
#             continue
#         words = extractor.detect_words_in_line(subline, line_prp[i][j], ksize=word_ksize, show_result=False)
#         for k in range(0, len(words[0]) - 1, 2):
#             x, y, w, h = words[1][k]
#             x2, y2, w2, h2 = words[1][k + 1]
#             cv2.imwrite(os.path.join(output_folder, Path(image_path).stem + f"wp_{num}.jpg"), subline[min(y, y2): max(y+h, y2+h2), x: x2+w2])
#             num += 1
# for k, word in enumerate(words):
# random_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
# cv2.imwrite(os.path.join(output_folder, Path(image_path).stem + f"_{num}.jpg"), word)
# num += 1

# print(num)

# Press enter to destroy all windows
cv2.waitKey(0)
cv2.destroyAllWindows()

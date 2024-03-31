import os

from jdeskew.estimator import get_angle
from jdeskew.utility import rotate
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image

from img_processing import img_processing as imgp
import cv2

image_path = 'data/test/test1.jpg'
output_folder = 'data/output'
image = cv2.imread(image_path)

ksize = (8, 2)

# Resize image for better results
image = imgp.resize_image(image, new_width=1200)
# regions = imgp.detect_lines(image, ksize=ksize, show_result=True)
image0 = imgp.adaptive_thresholding(image, ksize)
# cv2.imshow("Preprocessed image", image0)

pages = imgp.separate_pages(image, ksize=ksize)

cv2.imshow("First page", pages[0])
cv2.imshow("Second page", pages[1])

# ----------------- Detecting lines -----------------
# Configure scale_percent, ksize and blocksize for different results
# regions = imgp.detect_lines(pages[0], ksize=ksize, show_result=True)

config = Cfg.load_config_from_name('vgg_seq2seq')
config['device'] = 'cpu'
detector = Predictor(config)

# for page in pages:
# lines = imgp.extract_lines(pages[0], ksize=ksize, save_result=(True, 'data/output'))
lines = imgp.detect_lines(pages[0], ksize=ksize, show_result=True)[0]

# for line in lines:
#     line_img = Image.fromarray(line)
#     s = detector.predict(line_img)
#     with open('output2.txt', 'a', encoding='utf-8') as file:
#             # Write some text to the file
#         file.write(s + "\n\n")

# for line in lines:
#     angle = get_angle(line)
#     line = rotate(line, angle)
#     words = imgp.detect_words(lines[0], ksize=(2, 3), show_result=True)[0]

angle = get_angle(lines[0])
line = rotate(lines[0], angle)
words = imgp.detect_words(lines[0], ksize=(2, 3), show_result=True)[0]
for word in words:
    word_img = Image.fromarray(word)
    s = detector.predict(word_img)
    with open('output3.txt', 'a', encoding='utf-8') as file:
        # Write some text to the file
        file.write(s + " ")


# Press enter to destroy all windows
cv2.waitKey(0)
cv2.destroyAllWindows()

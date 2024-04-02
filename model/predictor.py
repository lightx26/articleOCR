import cv2
from jdeskew.estimator import get_angle
from jdeskew.utility import rotate
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image

from img_processing import img_processing as imgp, extractor


def predict(image, line_ksize=(16, 2), word_ksize=(4, 2), mode='word', page='double', save_result=(False, None)):
    # Resize image for better detection
    resized_image = imgp.resize_image(image, new_width=2000)

    global pages
    if page == 'double':
        # pages = extractor.separate_pages(resized_image, ksize=line_ksize)
        pages = extractor.separate_pages(resized_image)
        # cv2.imshow("Double pages: first page", pages[0])
        # cv2.imshow("Double pages: second page", pages[1])
    elif page == 'single':
        resized_image = imgp.resize_image(resized_image, new_width=1000)
        pages = [resized_image]
        # cv2.imshow("Single page", pages[0])

    else:
        raise ValueError("This page mode isn't supported. Choose 'single' or 'double'.")

    config = Cfg.load_config_from_name('vgg_seq2seq')
    config['device'] = 'cpu'
    detector = Predictor(config)

    result = ""

    for page in pages:

        if mode == 'line':
            lines = extractor.detect_lines(page, ksize=line_ksize, show_result=False)[0]
            for line in lines:
                angle = get_angle(line)
                line = rotate(line, angle)
                line_img = Image.fromarray(line)
                s = detector.predict(line_img)
                result += s + "\n"

        # elif mode == 'line-word':
        #     lines = extractor.detect_lines(page, ksize=line_ksize, show_result=False)[0]
        #     for line in lines:
        #         words = extractor.detect_words(line, ksize=word_ksize, show_result=False)[0]
        #         for word in words:
        #             word_img = Image.fromarray(word)
        #             s = detector.predict(word_img)
        #             result += s + " "
        #         result += "\n"

        elif mode == 'word':
            # lines = imgp.detect_lines(page, ksize=line_ksize, show_result=False)[0]
            words = extractor.detect_words(page, ksize=word_ksize, show_result=False)[0]
            for word in words:
                word_img = Image.fromarray(word)
                s = detector.predict(word_img)
                result += s + " "
        else:
            raise ValueError("This mode isn't supported. Choose 'line', 'word' or 'line-word'.")

    if save_result[0] and save_result[1] is not None:
        with open(save_result[1], 'a', encoding='utf-8') as file:
            file.write(result)

    return result
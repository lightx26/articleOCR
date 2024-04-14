import numpy as np
from PIL import Image
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor
import cv2

from img_processing import img_processing as imgp, extractor
from model.utils import get_config


class BookReader:
    def __init__(self, config=None):
        if config is None:
            config = {
                'mode': 'double-page',
                # 'page': 'double',
                'line_ksize': (12, 3),
                'word_ksize': (8, 10)
            }

        self.config = config

        # model_config = get_config.load_config_from_file("model\\config\\base.yml", "model\\config\\vgg-seq2seq.yml")
        model_config = Cfg.load_config_from_file("model/config/myconfig.yml")
        model_config['device'] = 'cpu'
        model_config['weights'] = 'model/config/myseq2seq.pth'
        self.detector = Predictor(model_config)

    def set_config(self, config):
        self.config = config

    def read(self, image):
        if self.config is None:
            raise ValueError("Config is not set.")

        if self.config['mode'] == 'double-page':
            resized_image = imgp.resize_image(image, new_width=2000)
            pages = extractor.separate_pages(resized_image)

            return self.__read_page(pages[0]) + self.__read_page(pages[1])

        elif self.config['mode'] == 'single-page':
            resized_image = imgp.resize_image(image, new_width=1000)
            return self.__read_page(resized_image)

        else:
            raise ValueError("This page mode isn't supported. Choose 'single-page' or 'double-page'.")

    def __read_page(self, page):
        """
        Read text from a page
        :param page: image of a page
        :return: text from the page
        """
        lines_bound = extractor.detect_lines(page, ksize=self.config['line_ksize'], show_result=False)
        lines_mask = extractor.extract_lines_mask(page, ksize=self.config['line_ksize'])

        left_offset = np.median([line[0][0] for line in lines_bound[1] if line[0][2] > 500])
        right_offset = np.median([line[-1][0] + line[-1][2] for line in lines_bound[1] if line[-1][2] > 500])

        result = ""

        for i, line in enumerate(lines_bound[0]):
            for j, subline in enumerate(line):
                if (lines_bound[1][i][j][0] < left_offset - 100) or (
                        lines_bound[1][i][j][0] + lines_bound[1][i][j][2] > right_offset + 100):
                    continue

                result += self.__read_line(subline, lines_mask[i][j]) + " "
            result += "\n"

        return result

    def __read_line(self, line, line_mask):
        """
        Read text from a line
        :param line: image of a line
        :return: text from the line
        """
        # if self.config['mode'] == 'line':
        #     return self.detector.predict(Image.fromarray(line))

        # elif self.config['mode'] == 'word':
        result = ""
        words = extractor.detect_words_in_line(line, line_mask, ksize=self.config['word_ksize'], show_result=False)[0]
        for word in words:
            word_img = Image.fromarray(word)
            s = self.detector.predict(word_img)
            # if len(s) == 1:
            #     if not imgp.is_char_ratio(char_shape=word.shape, line_shape=line.shape):
            #         s = '-'
            result += s + " "

        return result

        # else:
        #     raise ValueError("This mode isn't supported. Choose 'line', 'line-word' or 'word'.")
import time

import numpy as np
from PIL import Image
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor
from img_processing import img_processing as imgp, extractor


class BookReader:
    def __init__(self, config=None):
        if config is None:
            config = {
                'mode': 'double-page',
                # 'page': 'double',
                'line_ksize': (12, 4),
                'word_ksize': (4, 6),
                'device': 'cpu',
            }

        self.config = config

        model_config = Cfg.load_config_from_file(config['model']['config'])
        model_config['device'] = config['model']['device']
        model_config['weights'] = config['model']['weights']
        self.detector = Predictor(model_config)

    def set_config(self, config):
        self.config = config

    def make_pages(self, image):
        if self.config is None:
            raise ValueError("Config is not set.")

        if self.config['mode'] == 'double-page':
            resized_image = imgp.resize_image(image, new_width=2000)
            return extractor.separate_pages(resized_image)

        elif self.config['mode'] == 'single-page':
            return [imgp.resize_image(image, new_width=1000)]

        else:
            raise ValueError("This page mode isn't supported. Choose 'single-page' or 'double-page'.")

    def read_line(self, line, line_mask):
        """
        Read text from a line
        :param line_mask:
        :param line: image of a line
        :return: text from the line
        """
        words = extractor.detect_words_in_line(line, line_mask, ksize=self.config['word_ksize'], show_result=False)[0]
        words_img = [Image.fromarray(word) for word in words]
        return " ".join(self.detector.predict_batch(words_img))

    def get_words_in_line(self, line, line_mask):
        words = extractor.detect_words_in_line(line, line_mask, ksize=self.config['word_ksize'], show_result=False)[0]
        return [Image.fromarray(word) for word in words]

    def read_word(self, word):
        return self.detector.predict(word)

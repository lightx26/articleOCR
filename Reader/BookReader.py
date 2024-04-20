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

        self.total_predict_time = 0

    def set_config(self, config):
        self.config = config

    def read(self, image):
        if self.config is None:
            raise ValueError("Config is not set.")

        if self.config['mode'] == 'double-page':
            resized_image = imgp.resize_image(image, new_width=2000)
            pages = extractor.separate_pages(resized_image)
            page_number_1, content_1 = self.__read_page(pages[0])
            page_number_2, content_2 = self.__read_page(pages[1])
            return [page_number_1, page_number_2], content_1 + content_2

        elif self.config['mode'] == 'single-page':
            resized_image = imgp.resize_image(image, new_width=1000)
            page_number, content = self.__read_page(resized_image)
            return [page_number], content

        else:
            raise ValueError("This page mode isn't supported. Choose 'single-page' or 'double-page'.")

    def __read_page(self, page):
        """
        Read text from a page
        :param page: image of a page
        :return: text from the page
        """
        page_number = 0
        lines_bound = extractor.detect_lines(page, ksize=self.config['line_ksize'], show_result=False)
        lines_mask = extractor.extract_lines_mask(page, ksize=self.config['line_ksize'])

        try:
            top_offset = np.min([line[0][1] for line in lines_bound[1] if line[0][2] > 500])
            bottom_offset = np.max([line[-1][1] + line[-1][3] for line in lines_bound[1] if line[-1][2] > 500])
        except:
            top_offset = 0
            bottom_offset = page.shape[0]

        left_offset = np.median([line[0][0] for line in lines_bound[1]])
        right_offset = np.median([line[-1][0] + line[-1][2] for line in lines_bound[1]])

        words_img = []

        for i, line in enumerate(lines_bound[0]):
            try:
                l = i - 5
                r = i + 5
                if i - 5 < 0:
                    l = 0
                    r = 9
                if i + 5 > len(lines_bound[1]) - 1:
                    l = len(lines_bound[1]) - 10
                    r = len(lines_bound[1]) - 1
                ad_left_offset = np.min(
                    [line[0][0] for line in lines_bound[1][l:r] if line[0][2] > 500])
                ad_right_offset = np.max(
                    [line[-1][0] + line[-1][2] for line in lines_bound[1][l:r] if line[-1][2] > 500])

            except:
                ad_left_offset = left_offset
                ad_right_offset = right_offset

            # print("ad_left_offset: ", ad_left_offset)
            # print("ad_right_offset: ", ad_right_offset)

            for j, subline in enumerate(line):
                x, y, w, h = lines_bound[1][i][j]

                if (x < ad_left_offset - 20 or x + w > ad_right_offset + 20) and (w < 100 or h > 200 or w / h < 2):
                    continue

                if w < 100 and (y < top_offset or y > bottom_offset):
                    s = self.detector.predict(Image.fromarray(subline))
                    if s.isdigit():
                        page_number = int(s)
                        continue

                words_img.extend(self.__batch_line(subline, lines_mask[i][j]))

        words_img = [Image.fromarray(word) for word in words_img]
        begin_predict = time.time()
        result = " ".join(self.detector.predict_batch(words_img))
        print("Predict time: %s seconds" % (time.time() - begin_predict))

        if page_number == 0:
            return None, result

        return page_number, result

    # def __read_page1(self, page):
    #     """
    #     Read text from a page
    #     :param page: image of a page
    #     :return: text from the page
    #     """
    #     page_number = 0
    #     lines_bound = extractor.detect_lines(page, ksize=self.config['line_ksize'], show_result=False)
    #     lines_mask = extractor.extract_lines_mask(page, ksize=self.config['line_ksize'])
    #
    #     top_offset = np.min([line[0][1] for line in lines_bound[1] if line[0][2] > 500])
    #     bottom_offset = np.max([line[-1][1] + line[-1][3] for line in lines_bound[1] if line[-1][2] > 500])
    #
    #     left_offset = np.median([line[0][0] for line in lines_bound[1]])
    #     right_offset = np.median([line[-1][0] + line[-1][2] for line in lines_bound[1]])
    #
    #     result = ""
    #
    #     for i, line in enumerate(lines_bound[0]):
    #         try:
    #             l = i - 5
    #             r = i + 5
    #             if i - 5 < 0:
    #                 l = 0
    #                 r = 9
    #             if i + 5 > len(lines_bound[1]) - 1:
    #                 l = len(lines_bound[1]) - 10
    #                 r = len(lines_bound[1]) - 1
    #             ad_left_offset = np.min(
    #                 [line[0][0] for line in lines_bound[1][l:r] if line[0][2] > 500])
    #             ad_right_offset = np.max(
    #                 [line[-1][0] + line[-1][2] for line in lines_bound[1][l:r] if line[-1][2] > 500])
    #
    #         except:
    #             ad_left_offset = left_offset
    #             ad_right_offset = right_offset
    #
    #         # print("ad_left_offset: ", ad_left_offset)
    #         # print("ad_right_offset: ", ad_right_offset)
    #
    #         for j, subline in enumerate(line):
    #             x, y, w, h = lines_bound[1][i][j]
    #
    #             if (x < ad_left_offset - 20 or x + w > ad_right_offset + 20) and (w < 100 or h > 200 or w / h < 2):
    #                 continue
    #
    #             if w < 100 and (y < top_offset or y > bottom_offset):
    #                 s = self.detector.predict(Image.fromarray(subline))
    #                 if s.isdigit():
    #                     page_number = int(s)
    #                     continue
    #
    #             result += self.__read_line(subline, lines_mask[i][j]) + " "
    #
    #         result += "\n"
    #
    #     if page_number == 0:
    #         return None, result
    #
    #     return page_number, result

    def __read_line(self, line, line_mask):
        """
        Read text from a line
        :param line: image of a line
        :return: text from the line
        """
        words = extractor.detect_words_in_line(line, line_mask, ksize=self.config['word_ksize'], show_result=False)[0]
        words_img = [Image.fromarray(word) for word in words]
        return " ".join(self.detector.predict_batch(words_img))

    def __batch_line(self, line, line_mask):
        return extractor.detect_words_in_line(line, line_mask, ksize=self.config['word_ksize'], show_result=False)[0]

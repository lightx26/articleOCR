import time

import numpy as np
import threading
from Reader.BookReader import BookReader
from img_processing import extractor


class ReadThread(threading.Thread):
    def __init__(self, image, config, text_queue, start_time=0):
        super().__init__()
        self.image = image
        self.reader = BookReader(config)
        self.buffer_text = text_queue
        self.read_finished_event = threading.Event()
        self.start_time = start_time

    def run(self):
        pages = self.reader.make_pages(self.image)

        for page in pages:
            self.read_page(page)

        self.read_finished_event.set()

    def read_page(self, page):
        """
        Read text from a page
        :param page: image of a page
        :return: text from the page
        """
        page_number = 0
        lines_bound = extractor.detect_lines(page, ksize=self.reader.config['line_ksize'], show_result=False)
        lines_mask = extractor.extract_lines_mask(page, ksize=self.reader.config['line_ksize'])

        try:
            top_offset = np.min([line[0][1] for line in lines_bound[1] if line[0][2] > 500])
            bottom_offset = np.max([line[-1][1] + line[-1][3] for line in lines_bound[1] if line[-1][2] > 500])
        except:
            top_offset = 0
            bottom_offset = page.shape[0]

        left_offset = np.median([line[0][0] for line in lines_bound[1]])
        right_offset = np.median([line[-1][0] + line[-1][2] for line in lines_bound[1]])

        s = ""
        for i, line in enumerate(lines_bound[0]):
            try:
                left = i - 5
                right = i + 5
                if i - 5 < 0:
                    left = 0
                    right = 9
                if i + 5 > len(lines_bound[1]) - 1:
                    left = len(lines_bound[1]) - 10
                    right = len(lines_bound[1]) - 1
                ad_left_offset = np.min(
                    [line[0][0] for line in lines_bound[1][left:right] if line[0][2] > 500])
                ad_right_offset = np.max(
                    [line[-1][0] + line[-1][2] for line in lines_bound[1][left:right] if line[-1][2] > 500])

            except:
                ad_left_offset = left_offset
                ad_right_offset = right_offset

            for j, subline in enumerate(line):
                x, y, w, h = lines_bound[1][i][j]

                if (x < ad_left_offset - 20 or x + w > ad_right_offset + 20) and (w < 100 or h > 200 or w / h < 2):
                    continue

                if w < 100 and (y < top_offset or y > bottom_offset):
                    continue

                words = self.reader.get_words_in_line(subline, lines_mask[i][j])

                for word in words:
                    mini_seq = self.reader.detector.predict(word)
                    s = s + mini_seq + " "
                    if mini_seq[-1] in [".", "?", "!", ":", ";"]:
                        print("Line after: ", time.time() - self.start_time, "s", sep="")
                        self.buffer_text.put_nowait(s)
                        s = ""

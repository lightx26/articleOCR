import time
import argparse

import os
import cv2
import yaml
from AppThread.ReadThread import ReadThread
from AppThread.ExportThread import ExportThread
from queue import Queue


if __name__ == "__main__":
    # Read config file and set input/output paths
    with open("config/config.yml", "r") as f:
        config = yaml.safe_load(f)

    input_path = config['input_path']
    image_file = 'test.jpeg'
    image_path = os.path.join(input_path, image_file)

    # Create an argument parser
    parser = argparse.ArgumentParser(description='Read text from an image and save it to a file')

    # Add arguments
    parser.add_argument('--image', '-i', required=False, default=image_path,type=str, help='Path to the input image file')
    parser.add_argument('--destination', '-d', required=False, default=config['output_path'], type=str, help='Path to the output text file')
    parser.add_argument('--mode', '-m', required=False, default=config['reader']['mode'], type=str, help='Mode of reading (single-page or double-page)')

    # Parse parameters from command line
    args = parser.parse_args()

    # Read image
    print("Reading image from " + args.image)

    image = cv2.imread(args.image)

    if image is None:
        print("Failed to load image.")
    else:
        # Set config for reader:
        # mode: 'single-page' or 'double-page'
        reader_config = config['reader']
        reader_config['mode'] = args.mode

        start_time = time.time()

        text_output_path = os.path.join(args.destination, os.path.basename(args.image))
        q = Queue()

        read_thread = ReadThread(image, reader_config, q)
        export_thread = ExportThread(text_output_path, q, read_thread.read_finished_event, start_time)

        read_thread.start()
        export_thread.start()

        read_thread.join()
        export_thread.join()

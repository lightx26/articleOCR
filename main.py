import time
import argparse
from Reader.BookReader import BookReader
import os
import cv2
import yaml


def save_to_file(output_path, file_name, text):
    with open(os.path.join(output_path, file_name), 'w', encoding='utf-8') as f:
        f.write(text)


if __name__ == "__main__":
    # Read config file and set input/output paths
    with open("config/config.yml", "r") as f:
        config = yaml.safe_load(f)

    input_path = config['input_path']
    output_path = config['output_path']

    # Read the image, convert it to Matrix
    image_file = '3.jpg'
    image_path = os.path.join(input_path, image_file)

    # Create an argument parser
    parser = argparse.ArgumentParser(description='Read text from an image and save it to a file')

    # Add arguments
    parser.add_argument('--image', '-i', required=False, default=image_path,type=str, help='Path to the input image file')
    parser.add_argument('--destination', '-d', required=False, default=output_path, type=str, help='Path to the output text file')
    parser.add_argument('--mode', '-m', required=False, default='double-page', type=str, help='Mode of reading (single-page or double-page)')

    # Parse các tham số từ dòng lệnh
    args = parser.parse_args()

    print("Reading image from " + args.image)

    image = cv2.imread(args.image)

    if image is None:
        print("Failed to load image.")
    else:
        # Set config for reader:
        # mode: 'single-page' or 'double-page'
        reader_config = config['reader']
        reader_config['mode'] = args.mode

        reader = BookReader(reader_config)

        start_time = time.time()

        # Read the text from the image
        page_numbers, content = reader.read(image)

        result = content
        if page_numbers[0] is None and page_numbers[-1] is None:
            pass
        elif page_numbers[0] is None:
            page_numbers[0] = page_numbers[-1] - 1
            result = "Trang " + ",".join(map(str, page_numbers)) + ".\n" + content
        elif page_numbers[1] is None:
            page_numbers[1] = page_numbers[0] + 1
            result = "Trang " + ",".join(map(str, page_numbers)) + ".\n" + content


        # Save the result to a file
        save_to_file(args.destination, os.path.basename(args.image) + ".txt", result)
        print("Time: ", time.time() - start_time)
        print("The result is saved to " + os.path.join(args.destination, os.path.basename(args.image) + ".txt"))
        # print(s)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

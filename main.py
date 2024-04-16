import time

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

    print("Reading image from " + image_path)

    image = cv2.imread(image_path)

    if image is None:
        print("Failed to load image.")
    else:
        # Set config for reader:
        # mode: 'single-page' or 'double-page'
        reader_config = config['reader']
        reader = BookReader(reader_config)

        start_time = time.time()

        # Read the text from the image
        s = reader.read(image)

        print("Time: ", time.time() - start_time)

        # Save the result to a file
        save_to_file(output_path, os.path.basename(image_path) + ".txt", s)
        print("The result is saved to " + os.path.join(output_path, os.path.basename(image_path) + ".txt"))

    cv2.waitKey(0)
    cv2.destroyAllWindows()

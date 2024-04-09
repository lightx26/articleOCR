from Reader.BookReader import BookReader
import os
import cv2
import yaml

if __name__ == "__main__":

    with open("config/config.yml", "r") as f:
        config = yaml.safe_load(f)

    input_path = config['input_path']
    output_path = config['output_path']

    image_path = os.path.join(input_path, 'test.jpeg')
    image = cv2.imread(image_path)

    if image is None:
        print("Failed to load image.")
    else:
        reader_config = config['reader']
        reader = BookReader(reader_config)
        print(reader.read(image))

    cv2.waitKey(0)
    cv2.destroyAllWindows()
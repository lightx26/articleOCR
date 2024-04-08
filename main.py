from model import predictor
import os
import cv2
import yaml

if __name__ == "__main__":

    with open("file.yaml", "r") as f:
        config = yaml.load(f)

    input_path = config['input_path']
    output_path = config['output_path']

    image_path = os.path.join(input_path, 'image.jpg')
    image = cv2.imread(image_path)

    if image is None:
        print("Failed to load image.")
    else:
        # mode: line, line-word or word
        # page: single or double
        predictor.predict(image, mode='word', page='double', save_result=(True, output_path))

    cv2.waitKey(0)
    cv2.destroyAllWindows()
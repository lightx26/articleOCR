from model import predictor
import os
import cv2

if __name__ == "__main__":
    image_path = os.path.join("data", "test", "2.jpg")
    output_path = os.path.join("data", "output", "output_" + os.path.basename(image_path) + ".txt")

    image = cv2.imread(image_path)

    if image is None:
        print("Failed to load image.")
    else:
        # mode: line or word
        # page: single or double
        predictor.predict(image, mode='line', page='single', save_result=(True, output_path))

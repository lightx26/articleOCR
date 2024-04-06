from model import predictor
import os
import cv2

if __name__ == "__main__":
    # image_path = os.path.join("data", "test", "test6.jpg")
    image_path = os.path.join("D:\\QUANG\\Hoctap\\Python\\projects\\audio2", "Image", "test7.jpg")
    # output_path = os.path.join("data", "output", "output_" + os.path.basename(image_path) + ".txt")
    output_path = os.path.join("D:\\QUANG\\Hoctap\\Python\\projects\\audio2\\Text", os.path.basename(image_path) + ".txt")

    image = cv2.imread(image_path)

    if image is None:
        print("Failed to load image.")
    else:
        # mode: line, line-word or word
        # page: single or double
        predictor.predict(image, mode='word', page='double', save_result=(True, output_path))

    cv2.waitKey(0)
    cv2.destroyAllWindows()
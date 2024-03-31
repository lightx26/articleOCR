from model import predictor
import cv2

if __name__ == "__main__":
    image_path = "data/test/test1.jpg"
    output_path = "data/output/output_" + image_path.split("/")[-1] + ".txt"

    image = cv2.imread(image_path)
    predictor.predict(image, mode='word', page='double', save_result=(True, output_path))

    cv2.waitKey(0)
    cv2.destroyAllWindows()
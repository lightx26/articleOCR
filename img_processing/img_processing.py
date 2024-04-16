import random
import string
import cv2


def resize_image(image, scale_percent=None, new_width=1000):
    if scale_percent is None:
        scale_percent = new_width / image.shape[1] * 100

    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


def global_thresholding(image, OTSU=False):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if OTSU:
        return cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    return cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)[1]


def is_none_text(image):
    preprocessed = global_thresholding(image)

    if image.shape[0] * image.shape[1] < 200 or cv2.countNonZero(preprocessed) / preprocessed.size > 0.96:
        # random_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        # cv2.imshow(random_name, preprocessed)
        return True

    return False


def is_char_ratio(char_shape, line_shape):
    if char_shape[0] / line_shape[0] > 0.4 or char_shape[1] > 25:
        return True

    return False


def adaptive_thresholding(image, blur=True, blocksize=15, c=8):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if blur:
        gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    thresh_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize,
                                         c)

    return thresh_image


def find_contours(thresh_image):
    contours, hierarchy = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def filter_contours(contours, filter_object):
    filtered_contours = []

    # full_line = [cnt for cnt in contours if 20000 < cv2.contourArea(cnt) < 30000 and cv2.boundingRect(cnt)[2] > 600]

    if filter_object == "lines":
        # mean_width = np.mean([cv2.boundingRect(cnt)[2] for cnt in contours])
        # print(cv2.contourArea(contours[0]))

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # print(h)

            # Filter based on aspect ratio, area, and other desired criteria
            # if (h > 30 and h < 150):
            # if mean_height * 0.5 < h < mean_height * 1.5:
            if 20 < h < 80 or (80 <= h <= 400 and 0.6 < w / h < 15):
                # if True:
                filtered_contours.append(cnt)

    elif filter_object == "full-line":

        # mean_height = np.mean([cv2.boundingRect(cnt)[3] for cnt in contours if 20 < cv2.boundingRect(cnt)[3] < 100])

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # if mean_height * 0.75 < h < mean_height * 1.5 and w < 100:
            if 20 < h < 80 and w > 600:
                filtered_contours.append(cnt)

    elif filter_object == "words":
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            # if mean_height * 0.75 < h < mean_height * 1.5 and w < 100:
            if (10 < h < 60 and area > 100) or (60 <= h <= 400 and 0.1 < w / h < 5):
                filtered_contours.append(cnt)

    return filtered_contours


def sort_contours(cnts, method="left-to-right"):
    if len(cnts) == 0:
        return cnts, None

    if len(cnts) == 1:
        return cnts, cv2.boundingRect(cnts[0])

    reverse = False
    i = 0
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    if method == "top-to-bottom":
        i = 1

    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    if len(boundingBoxes) > 0:
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                            key=lambda b: b[1][i], reverse=reverse))
    # return the list of sorted contours and bounding boxes
    return cnts, boundingBoxes


def cluster_by_line(contours, threshold=20):
    clusters = []
    cluster = []
    for i, cnt in enumerate(contours):
        # Append the first subline to the cluster
        if i == 0:
            cluster.append(cnt)
            continue

        x1, y1, w1, h1 = cv2.boundingRect(cnt)
        x2, y2, w2, h2 = cv2.boundingRect(contours[i - 1])
        if y1 - y2 < threshold or abs(y1 + h1 - y2 - h2) < threshold:
            # Overlap check
            is_overlap = False
            for other_subline in cluster:
                x3, y3, w3, h3 = cv2.boundingRect(other_subline)
                if (min(x1 + w1, x3 + w3) - max(x1, x3)) / min(w1, w3) > 0.25:
                    is_overlap = True
                    break

            if not is_overlap:
                cluster.append(cnt)
                continue

        cluster = sort_contours(cluster, method="left-to-right")[0]
        clusters.append(cluster)
        cluster = [cnt]

    cluster = sort_contours(cluster, method="left-to-right")[0]
    clusters.append(cluster)

    return clusters

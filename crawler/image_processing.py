import cv2
import numpy as np


def process_img(imgpath):
    img = cv2.imread(imgpath, cv2.IMREAD_COLOR)
    mask = cv2.inRange(img, np.array([0, 0, 126]), np.array([250, 250, 255]))

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img[mask != 0] = 255

    img = cv2.inpaint(img, mask, 1, cv2.INPAINT_TELEA)

    # cv2.imshow("img", img)
    # cv2.waitKey(0)

    img = cv2.GaussianBlur(img, (3, 1), 0)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)


    img = cv2.dilate(img, np.ones((3, 2), np.uint8), iterations=1)
    img = cv2.GaussianBlur(img, (3, 3), 0)

    xmin = next((i for i, x in enumerate(
        cv2.bitwise_not(img).sum(axis=0)) if x), None)

    img = img[:, xmin:]
    img = cv2.copyMakeBorder(img, 0, 0, 10, 10, cv2.BORDER_CONSTANT, value=255)
    cv2.imwrite("crawler/.tmp/captcha_processed.jpg", img)


if __name__ == "__main__":
    process_img("crawler/.tmp/captcha.png")

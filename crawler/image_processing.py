import cv2
import numpy as np
import pytesseract
from PIL import Image

def process_img(img: Image):
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)

    mask = cv2.inRange(img, np.array([0, 0, 126]), np.array([250, 250, 255]))

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img[mask != 0] = 255

    img = cv2.inpaint(img, mask, 1, cv2.INPAINT_TELEA)

    img = cv2.GaussianBlur(img, (3, 1), 0)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)


    img = cv2.dilate(img, np.ones((3, 2), np.uint8), iterations=1)
    img = cv2.GaussianBlur(img, (3, 3), 0)

    xmin = next((i for i, x in enumerate(
        cv2.bitwise_not(img).sum(axis=0)) if x), None)

    img = img[:, xmin:]
    img = cv2.copyMakeBorder(img, 0, 0, 10, 10, cv2.BORDER_CONSTANT, value=255)

    return img


if __name__ == "__main__":
    img = Image.open("crawler/.tmp/captcha.png")   
    process_img(img)

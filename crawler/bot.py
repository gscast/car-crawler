import time
from io import BytesIO

import cv2
import numpy as np
import pytesseract
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# def process_img(img):
#     img = np.array(img) 
#     # Convert RGB to BGR 
#     img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)

#     mask = cv2.inRange(img, np.array([0, 0, 200]), np.array([250, 250, 255]))

#     img[mask != 0] = [255, 255, 255]
#     _, img = cv2.threshold(img, 0, 255, fcv2.THRESH_BINARY+cv2.THRESH_OTSU)

#     img = cv2.erode(img, np.ones((5,2),np.uint8), iterations=1)
#     img = cv2.dilate(img, np.ones((5,5),np.uint8), iterations=1)

#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     img = Image.fromarray(img)
# f
#     return img

def get_captcha(driver, element, path):
    # now that we have the preliminary stuff out of the way time to get that image :D
    location = element.location
    size = element.size
    # saves screenshot of entire page
    im = driver.get_screenshot_as_png()

    driver.quit()

    # uses PIL library to open image in memory
    im = Image.open(BytesIO(im)) 

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    
    im = im.crop((left, top, right, bottom)) # defines crop points

    # im = process_img(im)
    im.save(path) # saves new cropped image

    

load_time = 5
url = "https://www.car.gov.br/publico/imoveis/index"

browser = webdriver.Firefox()
browser.get(url)

time.sleep(load_time)

downloads_xpath = "/html/body/div[2]/div/div[2]/div[2]/div/div/div[3]/a/div[2]"
downloads_bttn = browser.find_element_by_xpath(downloads_xpath)
downloads_bttn.click()

time.sleep(load_time)

shp_xpath = ("/html/body/div[1]/div/div[2]/div[1]/div[2]"
             + "/div/div[2]/div/div/button[1]/h4/i")

shp_bttn = browser.find_element_by_xpath(shp_xpath)
shp_bttn.click()

time.sleep(load_time)

captcha_xpath = '//*[@id="img-captcha-base-downloads"]'
captcha = browser.find_element_by_xpath(captcha_xpath)

get_captcha(browser, captcha, "crawler/.tmp/captcha.png")

import time
from io import BytesIO

import pytesseract
import string
import requests
import os

import random
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from image_processing import process_img


class ScrapingBotCAR:
    """Scraping Bot for the SIICAR download page."""

    def __init__(self, cod_estado="AP",
                 download_dir="/media/gabriel/Gabriel/Datasets/CAR/2020",
                 email_addr="gabriel.sc@hotmail.com"):

        self.url = "https://www.car.gov.br/publico/imoveis/index"

        self.email = "gabriel.sc@hotmail.com"
        self.download_dir = os.path.join(download_dir, cod_estado)

        if not os.path.isdir(self.download_dir):
            os.makedirs(self.download_dir, exist_ok=True)

        # define download location and suprees download pop up
        profile = webdriver.FirefoxProfile()
        profile.set_preference(
            'browser.download.folderList', 2)  # custom location
        profile.set_preference(
            'browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', self.download_dir)
        profile.set_preference(
            'browser.helperApps.neverAsk.saveToDisk', 'application/zip')
        self.driver = webdriver.Firefox(profile)

        # configure tesseract OCR to read numbers, letters and define
        # --psm 6 for one line reading.
        valid_chars = string.ascii_letters + string.digits
        self.tess_config = f"--psm 7 -c tessedit_char_whitelist={valid_chars}"

        # define jascrip elements paths
        self.xpath = {
            "download_bttn": "/html/body/div[2]/div/div[2]/div[2]/div/div/div[3]/a/div[2]",
            "captcha_img": '//*[@id="img-captcha-base-downloads"]',
            "refresh_bttn": '//*[@id="btn-atualizar-captcha"]',
            "answer_txtbox": '//*[@id="form-captcha-download-base"]',
            "email_txtbox": '//*[@id="form-email-download-base"]',
            "alert_message": '//*[@id="alert-download-error"]',
            "close_bttn": "/html/body/div[1]/div/div[2]/div[3]/div/div/div[1]/button/span",
            "download_shp": ("/html/body/div[1]/div/div[2]/div[3]/div/div/div[2]"
                             + "/div[3]/div[3]/button/span[1]"),
            "shp_parent": ("/html/body/div[1]/div/div[2]/div[1]/div[2]"
                           + "/div/div[{idx}]/div/div/button[1]")
        }

    def __call__(self):
        """Call bot."""
        self.driver.get(self.url)

        # open downloads page
        download_bttn = self.driver.find_element_by_xpath(
            self.xpath["download_bttn"])
        download_bttn.click()

        # iterate the cites shp buttons fpor download
        idx = 1
        while True:
            time.sleep(0.5)
            idx += 1

            shp_parent = self.driver.find_element_by_xpath(
                self.xpath["shp_parent"].format(idx=idx))

            # no buttons left, end scapping
            if shp_parent is None:
                break

            filename = f"SHAPE_{shp_parent.get_attribute('data-municipio')}.zip"
            downloaded_fp = os.path.join(self.download_dir, filename)

            shp_bttn = self.driver.find_element_by_xpath(
                self.xpath["shp_parent"].format(idx=idx) + "/h4/i")

            shp_bttn.click()

            time.sleep(0.5)
            refresh_bttn = self.driver.find_element_by_xpath(
                self.xpath["refresh_bttn"])

            close_bttn = self.driver.find_element_by_xpath(
                self.xpath["close_bttn"]
            )
            if not os.path.exists(downloaded_fp):
                self.__perform_download_actions()

                while not(os.path.exists(downloaded_fp)):
                    refresh_bttn.click()
                    self.__perform_download_actions()

            close_bttn.click()

        self.driver.quit()

    def __solve_captcha(self):
        # now that we have the preliminary stuff out of the way time to get that image :D
        captcha_img = self.driver.find_element_by_xpath(
            self.xpath["captcha_img"])

        location = captcha_img.location
        size = captcha_img.size
        # saves screenshot of entire page
        img = self.driver.get_screenshot_as_png()

        # uses PIL library to open image in memory
        img = Image.open(BytesIO(img))

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        img = img.crop((left, top, right, bottom))  # defines crop points
        # img.save("crawler/.tmp/captcha.png")
        img = process_img(img)

        answer = pytesseract.image_to_string(img, config=self.tess_config)
        time.sleep(random.random())
        return answer.split('\n')[0]

    def __perform_download_actions(self):
        time.sleep(0.5)

        answer_txtbox = self.driver.find_element_by_xpath(
            self.xpath["answer_txtbox"])
        alert_message = self.driver.find_element_by_xpath(
            self.xpath["alert_message"])
        email_txtbox = self.driver.find_element_by_xpath(
            self.xpath["email_txtbox"])
        download_shp = self.driver.find_element_by_xpath(
            self.xpath["download_shp"])

        answer_txtbox.clear()
        answer_txtbox.send_keys(self.__solve_captcha())

        email_txtbox.clear()
        email_txtbox.send_keys(self.email)

        download_shp.click()
        return bool(alert_message is None)


if __name__ == "__main__":
    bot = ScrapingBotCAR()

    try:
        bot()
    finally:
        bot.driver.quit()

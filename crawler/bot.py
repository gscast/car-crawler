import time
from io import BytesIO

import pytesseract
import string
import requests
import os
from glob import glob
import random
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

from image_processing import process_img


class ScrapingBotCAR:
    """Scraping Bot for the SIICAR download page."""

    def __init__(self, cod_estado="MS",
                 download_dir="/media/gabriel/Gabriel/Datasets/CAR/2020",
                 email_addr="gabriel.sc@hotmail.com"):

        self.url = "https://www.car.gov.br/publico/imoveis/index"
        self.email = "gabriel.sc@hotmail.com"
        self.download_dir = os.path.join(download_dir, cod_estado)

        if not os.path.isdir(self.download_dir):
            os.makedirs(self.download_dir, exist_ok=True)
        
        # define headless browser
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # define download location and suprees download pop up
        profile = webdriver.FirefoxProfile()
        profile.set_preference(
            'browser.download.folderList', 2)  # custom location
        profile.set_preference(
            'browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', self.download_dir)
        profile.set_preference(
            'browser.helperApps.neverAsk.saveToDisk', 'application/zip')
        self.driver = webdriver.Firefox(firefox_profile=profile, options=options)

        # configure tesseract OCR to read numbers, letters and define
        # --psm 6 for one line reading.
        valid_chars = string.ascii_letters + string.digits
        self.tess_config = f"--psm 6 -c tessedit_char_whitelist={valid_chars}"

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
                           + "/div/div[{idx}]/div/div/button[1]"),
            "change_uf_bttn": ("/html/body/div[1]/div/div[2]/div[1]/"
                                 "div[1]/div/div/div[3]/button"),
            "uf_bttn": "/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div[{idx}]/a"
        }

        # UF ids for acessing download page.
        uf_id = {
            "AC": 1, "AL": 2, "AP": 3, "AM": 4, "CE": 5, "DF": 6,
            "ES": 7, "GO": 8, "MA": 9, "MS": 10, "MG": 11, "PA": 12,
            "PB": 13, "PR": 14, "PE": 15, "PI": 16, "RJ": 17, "RN": 18,
            "RS":19, "RR": 20, "SC":21, "SP": 22, "SE": 23, "TO": 24,
            "RO": 25, "MT": 26, "BA": 27
        }

        self.uf_id = uf_id[cod_estado]

    def __call__(self):
        """Call bot."""
        self.driver.get(self.url)

        # open downloads page
        download_bttn = self.driver.find_element_by_xpath(
            self.xpath["download_bttn"])
        download_bttn.click()

        # go to change UF menu
        change_uf_bttn = self.driver.find_element_by_xpath(
            self.xpath["change_uf_bttn"]
        )
        change_uf_bttn.click()

        #change to uf download page
        uf_bttn = self.driver.find_element_by_xpath(
            self.xpath["uf_bttn"].format(idx = self.uf_id)
        )
        uf_bttn.click()

        # iterate the cites shp buttons download
        idx = 1
        while True:
            time.sleep(0.5)
            idx += 1 # city idx starts at two
            
            try:
                shp_parent = self.driver.find_element_by_xpath(
                    self.xpath["shp_parent"].format(idx=idx))

            except NoSuchElementException:
                # No more shp download butons
                break
            
            # destination path
            filename = f"SHAPE_{shp_parent.get_attribute('data-municipio')}.zip"
            downloaded_fp = os.path.join(self.download_dir, filename)

            #skip downloaded files
            if os.path.exists(downloaded_fp):
                print(f"Skipped: {downloaded_fp}\n")
                continue
            
            # click button to open captcha page
            shp_bttn = self.driver.find_element_by_xpath(
                self.xpath["shp_parent"].format(idx=idx) + "/h4/i")
            shp_bttn.click()
            time.sleep(1)

            self.__perform_download_actions()

            # first attempt to donwload fail
            # refresh captch and try until success
            while not(os.path.exists(downloaded_fp)):
                self.driver.find_element_by_xpath(
                self.xpath["refresh_bttn"]).click()
                self.__perform_download_actions()

            # close download pop-up
            close_bttn = self.driver.find_element_by_xpath(
                self.xpath["close_bttn"])
            close_bttn.click()
            print(f"Downloading: {downloaded_fp}\n")

    def __solve_captcha(self):
        captcha_img = self.driver.find_element_by_xpath(
            self.xpath["captcha_img"])

        location = captcha_img.location
        size = captcha_img.size
        # saves screenshot of entire page
        img = self.driver.get_screenshot_as_png()
        img = Image.open(BytesIO(img))
        rect = captcha_img.rect
        img = img.crop((rect["x"], rect["y"],
                        rect["x"] + rect["width"],
                        rect["y"] + rect["height"]))

        img.save("crawler/.tmp/captcha.png")
        img = process_img(img)

        answer = pytesseract.image_to_string(img, config=self.tess_config)
        return answer.split('\n')[0]

    def __perform_download_actions(self):
        time.sleep(random.random())

        answer_txtbox = self.driver.find_element_by_xpath(
            self.xpath["answer_txtbox"])
        alert_message = self.driver.find_element_by_xpath(
            self.xpath["alert_message"])
        email_txtbox = self.driver.find_element_by_xpath(
            self.xpath["email_txtbox"])
        download_shp = self.driver.find_element_by_xpath(
            self.xpath["download_shp"])

        js_script = '''\
            element1 = document.getElementById('alert-download-base');
            element1.style.display = 'none';
            element2 = document.getElementById('alert-download-error');
            element2.style.display = 'none';
        '''
        self.driver.execute_script(js_script)

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
        while bool(glob(os.path.join(bot.download_dir, "*.part"))):
            pass

        bot.driver.quit()

import argparse
import os
import random
import string
import sys
import time
from glob import glob
from io import BytesIO

import pytesseract
import requests
import tqdm
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from image_processing import process_img
import logging


class MaxTriesExceeded(Exception):
    """Cannot solve captcha"""


class ScrapingBotCAR:
    """Scraping Bot for the SIICAR download page."""

    def __init__(self, uf, email, download_dir, debug=False):

        self.url = "https://www.car.gov.br/publico/imoveis/index"
        self.email = email
        self.debug = debug
        self.uf = uf.upper()

        logfile = os.path.join("crawler", ".log", f'downloaded_files.log')
        logging.basicConfig(filename=logfile)

        self.n_tries = 0
        self.MAX_TRIES = 80

        self.download_dir = os.path.join(download_dir, uf.upper())
        if not os.path.isdir(self.download_dir):
            os.makedirs(self.download_dir, exist_ok=True)

        # define headless browser
        options = Options()
        if not self.debug:
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

        # define download location and suprees download pop up
        profile = webdriver.FirefoxProfile()
        profile.set_preference(
            'browser.download.folderList', 2)
        profile.set_preference(
            'browser.download.manager.showWhenStarting', False)
        profile.set_preference(
            'browser.download.dir', self.download_dir)
        profile.set_preference(
            'browser.helperApps.neverAsk.saveToDisk', 'application/zip')

        self.driver = webdriver.Firefox(
            firefox_profile=profile, options=options)

        # configure tesseract OCR to read numbers, letters and define
        # --psm 6 for one line reading.
        valid_chars = string.ascii_letters + string.digits
        self.tess_config = f"--psm 6 -c tessedit_char_whitelist={valid_chars}"

    def __call__(self):
        """Call bot."""
        self.driver.get(self.url)

        # open downloads page
        download_bttn_xpath = '//div[@class="quadro-dados botao-download"]'
        download_bttn = self.driver.find_element_by_xpath(download_bttn_xpath)
        download_bttn.click()

        # go to change UF menu
        change_uf_xpath = ('//div[@class="pull-right btn-alterar"]' +
                           '//button[@class="btn btn-alterar"]')
        change_uf_bttn = self.driver.find_element_by_xpath(change_uf_xpath)
        change_uf_bttn.click()

        # change to uf download page
        uf_xpath = f'//a[@class="selecione-uf" and contains(@href, "{self.uf}")]'
        uf_bttn = self.driver.find_element_by_xpath(uf_xpath)
        uf_bttn.click()

        logging.info(f"{self.uf} selected. Saving to {self.download_dir}")

        # iterate the cites shp buttons download
        cities_xpath = '//div[@class="item-municipio"]'
        cities = self.driver.find_elements_by_xpath(cities_xpath)

        for city in tqdm.tqdm(cities):
            city_text = city.text
            shp_parent_xpath = './/button[@title="Baixar Shapefile"]'
            shp_parent = city.find_element_by_xpath(shp_parent_xpath)

            # destination path
            filename = f"SHAPE_{shp_parent.get_attribute('data-municipio')}.zip"
            downloaded_fp = os.path.join(self.download_dir, filename)

            # skip downloaded files
            if os.path.exists(downloaded_fp):
                logging.info(
                    f"Skipped {city_text}/{self.uf}: shapefile already downloaded.\n")
                continue
            
            csv_filename = f"{shp_parent.get_attribute('data-municipio')}.csv"
            csv_downloaded_fp = os.path.join(self.download_dir, csv_filename)
            if os.path.exists(csv_downloaded_fp):
                logging.warning(
                    f"Skipped {city_text}/{self.uf}: csv already downloaded.\n")
                continue

            # click button to open captcha page
            shp_bttn = shp_parent.find_element_by_xpath('.//h4')
            shp_bttn.click()
            time.sleep(1)

            try:
                # first attempt to donwload fail
                # refresh captch and try until success
                self.n_tries = 0
                self.__perform_download_actions()

                while not(os.path.exists(downloaded_fp)):

                    refresh_xpath = '//*[@id="btn-atualizar-captcha"]'
                    self.driver.find_element_by_xpath(refresh_xpath).click()
                    self.__perform_download_actions()

                    if self.n_tries >= self.MAX_TRIES:
                        raise MaxTriesExceeded

            except MaxTriesExceeded:
                error = f"Skipped {city_text}/{self.uf}: max tries exceeded."
                print(error+"\n")
                logging.error(error)
                continue

            finally:
                # close download pop-up
                close_xpath = ("/html/body/div[1]/div/div[2]/div[3]"
                               "/div/div/div[1]/button/span")
                close_bttn = self.driver.find_element_by_xpath(close_xpath)
                close_bttn.click()
                time.sleep(0.1 + random.random())

            logging.info(f"Downloading shapefile for {city_text}:\n" +
                         f"\t {downloaded_fp}")

    def __solve_captcha(self):
        captcha_xpath = '//*[@id="img-captcha-base-downloads"]'
        captcha_img = self.driver.find_element_by_xpath(captcha_xpath)

        location = captcha_img.location
        size = captcha_img.size
        # saves screenshot of entire page
        img = self.driver.get_screenshot_as_png()
        img = Image.open(BytesIO(img))
        rect = captcha_img.rect
        img = img.crop((rect["x"], rect["y"],
                        rect["x"] + rect["width"],
                        rect["y"] + rect["height"]))

        if self.debug:
            img.save("crawler/.tmp/captcha.png")

        img = process_img(img)

        answer = pytesseract.image_to_string(img, config=self.tess_config)
        return answer.split('\n')[0]

    def __perform_download_actions(self):
        self.n_tries += 1

        time.sleep(random.random())

        answer_txtbox = self.driver.find_element_by_xpath(
            '//*[@id="form-captcha-download-base"]')
        alert_message = self.driver.find_element_by_xpath(
            '//*[@id="alert-download-error"]')
        email_txtbox = self.driver.find_element_by_xpath(
            '//*[@id="form-email-download-base"]')
        download_shp = self.driver.find_element_by_xpath(
            '//*[@id="btn-baixar-dados"]')

        # hide warning banners and scroll up to prevent
        # captcha crop misalignment.
        js_script = '''\
            element1 = document.getElementById('alert-download-base');
            element1.style.display = 'none';
            element2 = document.getElementById('alert-download-error');
            element2.style.display = 'none';
            window.scrollTo(0, 0)
        '''
        self.driver.execute_script(js_script)

        answer_txtbox.clear()
        answer_txtbox.send_keys(self.__solve_captcha())

        email_txtbox.clear()
        email_txtbox.send_keys(self.email)

        download_shp.click()
        return bool(alert_message is None)


def get_args(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument("dst")
    parser.add_argument("--uf", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--debug", action='store_true')

    return parser.parse_args(argv)


if __name__ == "__main__":
    args = get_args(sys.argv[1:])

    bot = ScrapingBotCAR(args.uf, args.email, args.dst, args.debug)

    try:
        bot()
    finally:
        while bool(glob(os.path.join(bot.download_dir, "*.part"))):
            pass
        bot.driver.quit()

        for f in glob(os.path.join(bot.download_dir, "*(1).zip")):
            os.remove(f)

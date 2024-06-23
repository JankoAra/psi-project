# Autor: Srdjan Lucic 260/2021
import time
import os

from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from .utilities import login, initialize_content_ls210260, delete_content_ls210260d
from django.urls import reverse
from selenium.webdriver.support import expected_conditions as EC

class TestAddImageToGallery(StaticLiveServerTestCase):

    def setUp(self):
        service = webdriver.ChromeService(executable_path='./chromedriver.exe')
        self.browser = webdriver.Chrome(service=service)
        self.appUrl = self.live_server_url
        initialize_content_ls210260(self)

    def tearDown(self):
        self.browser.close()
        delete_content_ls210260d(self)

    def test_success(self):
        self.browser.get(self.appUrl + reverse('user_login'))
        wait = WebDriverWait(self.browser, 20)

        login(self.browser, self.appUrl, 'srdjanR', 'srkiLozinka3')

        detaljnije_xpath = '//a[text()="Detaljnije"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, detaljnije_xpath)))
        article_link = self.browser.find_element(By.XPATH, detaljnije_xpath)
        article_link.click()

        galerija_xpath = '//a[text()="Galerija"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, galerija_xpath)))
        self.browser.find_element(By.XPATH, galerija_xpath).click()

        add_photo_button = wait.until(EC.element_to_be_clickable((By.ID, 'add-to-gallery-button')))
        add_photo_button.click()

        photo_path = os.path.abspath('./test_data/patka.jpg')
        photo_input = self.browser.find_element(By.ID, "id_image")
        wait.until(EC.visibility_of(photo_input))
        photo_input.send_keys(photo_path)
        time.sleep(2)

        confirm_button = self.browser.find_element(By.ID, 'postaviButton')
        wait.until(EC.element_to_be_clickable(confirm_button))
        confirm_button.click()

        galerija_xpath = '//a[text()="Galerija"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, galerija_xpath)))
        self.browser.find_element(By.XPATH, galerija_xpath).click()

        time.sleep(3)

        new_image_div_xpath = '(//div[@class="image-item col"])[3]'
        try:
            self.browser.find_element(By.XPATH, new_image_div_xpath)
            message = 'success'
        except Exception:
            message = 'failure'

        self.assertEqual(message,'success')


    def test_wrong_format(self):
        self.browser.get(self.appUrl + reverse('user_login'))
        wait = WebDriverWait(self.browser, 20)

        login(self.browser, self.appUrl, 'srdjanR', 'srkiLozinka3')

        detaljnije_xpath = '//a[text()="Detaljnije"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, detaljnije_xpath)))
        article_link = self.browser.find_element(By.XPATH, detaljnije_xpath)
        article_link.click()

        galerija_xpath = '//a[text()="Galerija"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, galerija_xpath)))
        self.browser.find_element(By.XPATH, galerija_xpath).click()

        add_photo_button = wait.until(EC.element_to_be_clickable((By.ID, 'add-to-gallery-button')))
        add_photo_button.click()

        photo_path = os.path.abspath('./test_data/patka.avif')
        photo_input = self.browser.find_element(By.ID, "id_image")
        wait.until(EC.visibility_of(photo_input))
        photo_input.send_keys(photo_path)
        time.sleep(2)

        confirm_button = self.browser.find_element(By.ID, 'postaviButton')
        wait.until(EC.element_to_be_clickable(confirm_button))
        confirm_button.click()

        time.sleep(2)

        try:
            self.browser.find_element(By.XPATH, '//p[text()="Tip fajla mora biti .jpeg, .jpg ili .png"]')
            message = 'success'
        except Exception:
            message = 'failure'

        self.assertEqual(message, 'success')

    def test_give_up(self):
        self.browser.get(self.appUrl + reverse('user_login'))
        wait = WebDriverWait(self.browser, 20)

        login(self.browser, self.appUrl, 'srdjanR', 'srkiLozinka3')

        detaljnije_xpath = '//a[text()="Detaljnije"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, detaljnije_xpath)))
        article_link = self.browser.find_element(By.XPATH, detaljnije_xpath)
        article_link.click()

        galerija_xpath = '//a[text()="Galerija"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, galerija_xpath)))
        self.browser.find_element(By.XPATH, galerija_xpath).click()

        add_photo_button = wait.until(EC.element_to_be_clickable((By.ID, 'add-to-gallery-button')))
        add_photo_button.click()

        photo_path = os.path.abspath('./test_data/patka.jpg')
        photo_input = self.browser.find_element(By.ID, "id_image")
        wait.until(EC.visibility_of(photo_input))
        photo_input.send_keys(photo_path)
        time.sleep(2)

        confirm_button = self.browser.find_element(By.ID, 'ponistiButton')
        wait.until(EC.element_to_be_clickable(confirm_button))
        confirm_button.click()

        galerija_xpath = '//a[text()="Galerija"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, galerija_xpath)))
        self.browser.find_element(By.XPATH, galerija_xpath).click()

        time.sleep(3)

        new_image_div_xpath = '(//div[@class="image-item col"])[3]'
        try:
            self.browser.find_element(By.XPATH, new_image_div_xpath)
            message = 'success'
        except Exception:
            message = 'failure'

        self.assertEqual(message,'failure')


# Autor: Srdjan Lucic 260/2021

import selenium.webdriver
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from .utilities import login, initialize_content_ls210260, delete_content_ls210260d
from django.urls import reverse
from selenium.webdriver.support import expected_conditions as EC

class TestDeleteGalleryImageSelenium(StaticLiveServerTestCase):
    # Testiranje brisanje fotografije iz galerije: 1 od 3 scenarija, ostala 2 su testirana pomocu Selenium ID ekstenzije
    def setUp(self):
        service = webdriver.ChromeService(executable_path='./chromedriver.exe')
        self.browser = webdriver.Chrome(service=service)
        self.appUrl = self.live_server_url
        initialize_content_ls210260(self)

    def tearDown(self):
        self.browser.close()
        delete_content_ls210260d(self)

    def test_not_owner(self):
        # Pokusaj brisanja fotografije kada korisnik nije vlasnik
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

        photo_button_dropdown_xpath = '//div[@class="image-item col"]/div[@class="dropdown position-absolute"]/button'
        wait.until(EC.element_to_be_clickable((By.XPATH, photo_button_dropdown_xpath)))
        self.browser.find_element(By.XPATH, photo_button_dropdown_xpath).click()

        photo_button_delete_xpath = \
            '//div[@class="image-item col"]/div[@class="dropdown position-absolute"]/div/button[text()="Obriši sliku"]'
        try:
            self.browser.find_element(By.XPATH, photo_button_delete_xpath).click()
            message = "Photo can be deleted"
        except Exception as e:
            message = "User is not the owner"

        self.assertEqual(message, "User is not the owner")
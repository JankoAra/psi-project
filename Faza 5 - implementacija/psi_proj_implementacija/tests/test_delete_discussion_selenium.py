# Autor: Srdjan Lucic 260/2021
import time

from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from .utilities import login, initialize_content_ls210260, delete_content_ls210260d
from django.urls import reverse
from selenium.webdriver.support import expected_conditions as EC


class TestDeleteDiscussionSelenium(StaticLiveServerTestCase):
    # Klasa za testiranje brisanja diskusije
    def setUp(self):
        service = webdriver.ChromeService(executable_path='./chromedriver.exe')
        self.browser = webdriver.Chrome(service=service)
        self.appUrl = self.live_server_url
        initialize_content_ls210260(self)

    def tearDown(self):
        self.browser.close()
        delete_content_ls210260d(self)

    def test_success(self):
        # Test: urednik brise diskusiju
        self.browser.get(self.appUrl + reverse('user_login'))
        wait = WebDriverWait(self.browser, 20)

        login(self.browser, self.appUrl, 'srdjanU', 'srkiLozinka1')

        detaljnije_xpath = '//a[text()="Detaljnije"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, detaljnije_xpath)))
        article_link = self.browser.find_element(By.XPATH, detaljnije_xpath)
        article_link.click()

        diskusije_xpath = '//a[text()="Diskusije"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, diskusije_xpath)))
        self.browser.find_element(By.XPATH, diskusije_xpath).click()

        time.sleep(3)

        dosadna_diskusija_button_xpath = '/html/body/div/div/div[3]/div[2]/div/div[2]/div/button'
        wait.until(EC.element_to_be_clickable((By.XPATH, dosadna_diskusija_button_xpath)))
        self.browser.find_element(By.XPATH,dosadna_diskusija_button_xpath).click()

        dosadna_diskusija_clear_xpath = '/html/body/div/div/div[3]/div[2]/div/div[2]/div/ul/a[@class="dropdown-item delete-discussion-link"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, dosadna_diskusija_clear_xpath)))
        self.browser.find_element(By.XPATH, dosadna_diskusija_clear_xpath).click()

        wait.until(EC.element_to_be_clickable((By.ID, 'confirmDeleteButton')))
        self.browser.find_element(By.ID, "confirmDeleteButton").click()

        dosadna_diskusija_xpath = '//h3[text() = "Neka Dosadna Disusija"]'
        wait.until(EC.invisibility_of_element_located((By.XPATH, dosadna_diskusija_xpath)))

        preostala_diskusija = self.browser.find_element(By.CLASS_NAME, 'discussion-title')
        self.assertNotEqual("Neka dosadna diskusija", preostala_diskusija.text)

    def test_give_up1(self):
        # Test: admin odustaje od brisanja diskusije
        self.browser.get(self.appUrl + reverse('user_login'))
        wait = WebDriverWait(self.browser, 20)

        login(self.browser, self.appUrl, 'srdjanA', 'srkiLozinka2')

        detaljnije_xpath = '//a[text()="Detaljnije"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, detaljnije_xpath)))
        article_link = self.browser.find_element(By.XPATH, detaljnije_xpath)
        article_link.click()

        diskusije_xpath = '//a[text()="Diskusije"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, diskusije_xpath)))
        self.browser.find_element(By.XPATH, diskusije_xpath).click()

        dosadna_diskusija_button_xpath = '/html/body/div/div/div[3]/div[2]/div/div[2]/div/button'
        wait.until(EC.element_to_be_clickable((By.XPATH, dosadna_diskusija_button_xpath)))
        self.browser.find_element(By.XPATH, dosadna_diskusija_button_xpath).click()

        dosadna_diskusija_clear_xpath = '/html/body/div/div/div[3]/div[2]/div/div[2]/div/ul/a[@class="dropdown-item delete-discussion-link"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, dosadna_diskusija_clear_xpath)))
        self.browser.find_element(By.XPATH, dosadna_diskusija_clear_xpath).click()

        wait.until(EC.element_to_be_clickable((By.ID, 'dontDeletePicture')))
        self.browser.find_element(By.ID, "dontDeletePicture").click()

        dosadna_diskusija_xpath = '//h3[text() = "Neka Dosadna Diskusija"]'
        wait.until(EC.visibility_of_element_located((By.XPATH, dosadna_diskusija_xpath)))
        preostala_diskusija = self.browser.find_element(By.CLASS_NAME, 'discussion-title')
        #print(preostala_diskusija.text)
        self.assertEqual("Neka Dosadna Diskusija", preostala_diskusija.text)

    def test_give_up2(self):
        # Test: admin odustaje od brisanja diskusije
        self.browser.get(self.appUrl + reverse('user_login'))
        wait = WebDriverWait(self.browser, 20)

        login(self.browser, self.appUrl, 'srdjanA', 'srkiLozinka2')

        detaljnije_xpath = '//a[text()="Detaljnije"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, detaljnije_xpath)))
        article_link = self.browser.find_element(By.XPATH, detaljnije_xpath)
        article_link.click()

        diskusije_xpath = '//a[text()="Diskusije"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, diskusije_xpath)))
        self.browser.find_element(By.XPATH, diskusije_xpath).click()

        dosadna_diskusija_button_xpath = '/html/body/div/div/div[3]/div[2]/div/div[2]/div/button'
        wait.until(EC.element_to_be_clickable((By.XPATH, dosadna_diskusija_button_xpath)))
        self.browser.find_element(By.XPATH, dosadna_diskusija_button_xpath).click()

        dosadna_diskusija_clear_xpath = '/html/body/div/div/div[3]/div[2]/div/div[2]/div/ul/a[@class="dropdown-item delete-discussion-link"]'
        wait.until(EC.element_to_be_clickable((By.XPATH, dosadna_diskusija_clear_xpath)))
        self.browser.find_element(By.XPATH, dosadna_diskusija_clear_xpath).click()

        X_button_xpath = '//div[@class="modal-header"]/button'
        wait.until(EC.element_to_be_clickable((By.XPATH, X_button_xpath)))
        self.browser.find_element(By.XPATH, X_button_xpath).click()

        dosadna_diskusija_xpath = '//h3[text() = "Neka Dosadna Diskusija"]'
        wait.until(EC.visibility_of_element_located((By.XPATH, dosadna_diskusija_xpath)))
        preostala_diskusija = self.browser.find_element(By.CLASS_NAME, 'discussion-title')
        #print(preostala_diskusija.text)
        self.assertEqual("Neka Dosadna Diskusija", preostala_diskusija.text)
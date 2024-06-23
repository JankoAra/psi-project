# Autor: Srdjan Lucic 260/2021
import time

from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from .utilities import login, initialize_content_ls210260, delete_content_ls210260d
from django.urls import reverse
from selenium.webdriver.support import expected_conditions as EC


class TestDeleteCommentSelenium(StaticLiveServerTestCase):
    # Klasa za testiranje brisanja komentara
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

        dosadna_diskusija_komentar_div_xpath = '/html/body/div/div/div[3]/div[2]/div/div[3]/div[2]/div/button'
        dosadna_diskusija_dropdown_button = wait.until(EC.element_to_be_clickable((By.XPATH, dosadna_diskusija_komentar_div_xpath)))
        dosadna_diskusija_dropdown_button.click()

        dosadna_diskusija_komentar_clear_xpath = \
            '/html/body/div/div/div[3]/div[2]/div/div[3]/div[2]/div/ul/a[@class="dropdown-item delete-comment-link"]'
        dosadna_diskusija_komentar_clear_button = wait.until(EC.element_to_be_clickable((By.XPATH, dosadna_diskusija_komentar_clear_xpath)))
        dosadna_diskusija_komentar_clear_button.click()

        wait.until(EC.element_to_be_clickable((By.ID, 'confirmDeleteButton')))
        self.browser.find_element(By.ID, "confirmDeleteButton").click()

        dosadna_diskusija_komentar_xpath = '//p[text() = "Brate je li moglo sta dosadnije"]'
        wait.until(EC.invisibility_of_element_located((By.XPATH, dosadna_diskusija_komentar_xpath)))
        time.sleep(3)

        preostali_komentar = self.browser.find_element(By.XPATH, '//div[@class="comment position-relative"]/p')
        self.assertNotEqual("Brate je li moglo sta dosadnije", preostali_komentar.text)

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

        dosadna_diskusija_komentar_div_xpath = '/html/body/div/div/div[3]/div[2]/div/div[3]/div[2]/div/button'
        dosadna_diskusija_dropdown_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, dosadna_diskusija_komentar_div_xpath)))
        dosadna_diskusija_dropdown_button.click()

        dosadna_diskusija_komentar_clear_xpath = \
            '/html/body/div/div/div[3]/div[2]/div/div[3]/div[2]/div/ul/a[@class="dropdown-item delete-comment-link"]'
        dosadna_diskusija_komentar_clear_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, dosadna_diskusija_komentar_clear_xpath)))
        dosadna_diskusija_komentar_clear_button.click()

        wait.until(EC.element_to_be_clickable((By.ID, 'dontDeletePicture')))
        self.browser.find_element(By.ID, "dontDeletePicture").click()

        dosadna_diskusija_komentar_xpath = '//p[text() = "Brate je li moglo sta dosadnije"]'
        wait.until(EC.visibility_of_element_located((By.XPATH, dosadna_diskusija_komentar_xpath)))

        preostali_komentar = self.browser.find_element(By.XPATH, '//div[@class="comment position-relative"]/p[@class="keep-whitespace"]')
        self.assertEqual("Brate je li moglo sta dosadnije", preostali_komentar.text)

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

        dosadna_diskusija_komentar_div_xpath = '/html/body/div/div/div[3]/div[2]/div/div[3]/div[2]/div/button'
        dosadna_diskusija_dropdown_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, dosadna_diskusija_komentar_div_xpath)))
        dosadna_diskusija_dropdown_button.click()

        dosadna_diskusija_komentar_clear_xpath = \
            '/html/body/div/div/div[3]/div[2]/div/div[3]/div[2]/div/ul/a[@class="dropdown-item delete-comment-link"]'
        dosadna_diskusija_komentar_clear_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, dosadna_diskusija_komentar_clear_xpath)))
        dosadna_diskusija_komentar_clear_button.click()

        wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="modal-header"]/button')))
        self.browser.find_element(By.XPATH, '//div[@class="modal-header"]/button').click()

        dosadna_diskusija_komentar_xpath = '//p[text() = "Brate je li moglo sta dosadnije"]'
        wait.until(EC.visibility_of_element_located((By.XPATH, dosadna_diskusija_komentar_xpath)))

        preostali_komentar = self.browser.find_element(By.XPATH, '//div[@class="comment position-relative"]/p[@class="keep-whitespace"]')
        self.assertEqual("Brate je li moglo sta dosadnije", preostali_komentar.text)
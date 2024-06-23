# Autor: Anđela Ćirić 2021/0066
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException

from slobodna_enciklopedija_ptica_srbije.models import *

import os

class TestDeletePictureArticleSelenium(StaticLiveServerTestCase):


    def setUp(self):
        service = webdriver.ChromeService(executable_path='./chromedriver.exe')
        self.browser = webdriver.Chrome(service=service)
        self.app_url = self.live_server_url
        self.editor = Korisnik.objects.create_user(username='uredniktest', password='odiseja123', tip="U")
        self.admin = Korisnik.objects.create_user(username='admintest', password='odiseja123', tip="A")
        self.registered = Korisnik.objects.create_user(username='regtest', password='odiseja123', tip="R")

        article1 = Clanak()
        article1.id_autora = self.editor
        article1.sadrzaj = "Test sadrzaj 1 jesam autor"
        article1.save()
        article2 = Clanak()
        article2.id_autora = self.admin
        article2.sadrzaj = "Test sadrzaj 2 nisam autor"
        article2.save()

        image_data = open(os.path.abspath("./test_data/owl.jpg"), "rb").read()
        table1 = PticaTabela()
        table1.id_clanka = article1
        table1.vrsta = "V1 test"
        table1.carstvo = "C1 test"
        table1.klasa = "K1 test"
        table1.porodica = "P1 test"
        table1.red = "R1 test"
        table1.rod = "R11 test"
        table1.slika_vrste = image_data
        table1.status_ugrozenosti="N1 test"
        table1.tezina = 10
        table1.velicina = 10
        table1.tip = "T1 test"
        table2 = PticaTabela()
        table2.id_clanka = article2
        table2.vrsta = "V2 test"
        table2.carstvo = "C2 test"
        table2.klasa = "K2 test"
        table2.porodica = "P2 test"
        table2.red = "R2 test"
        table2.rod = "R21 test"
        table2.slika_vrste = image_data
        table2.status_ugrozenosti="N2 test"
        table2.tezina = 20
        table2.velicina = 20

        table1.save()
        table2.save()


        self.table1 = table1
        self.table2 = table2
        self.article1 = article1
        self.article2 = article2

    def tearDown(self):
        self.browser.close()
        self.table1.delete()
        self.table2.delete()
        self.article1.delete()
        self.article2.delete()
        self.editor.delete()
        self.admin.delete()
        self.registered.delete()


    def login(self, browser, app_url, username, password):

        browser.get(app_url + reverse('user_login'))

        user_input = browser.find_element(By.ID, "korisnickoImePrijava")
        user_input.send_keys(username)

        pass_input = browser.find_element(By.ID, "lozinkaPrijava")
        browser.execute_script("arguments[0].value = arguments[1]", pass_input, password)

        submit_btn = browser.find_element(By.XPATH, "/html/body/section/div/div/form/table/tbody/tr[3]/td/input")
        submit_btn.click()


    def test_editor_delete_successful(self):
        self.login(self.browser, self.app_url, self.editor.username, "odiseja123")
        self.browser.get(self.app_url + reverse('show_article', args=[self.article1.id_clanka]))
        self.browser.implicitly_wait(10)
        delete_img_btn = self.browser.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/button[3]")
        delete_img_btn.click()

        confirm_delete_btn = WebDriverWait(self.browser, 100).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]"))
        )

        confirm_delete_btn.click()

        WebDriverWait(self.browser, 100).until(
            EC.invisibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]"))
        )


        bird_image = self.browser.find_element(By.XPATH,"//div[@id='content1']/div/div/div[2]/table/tbody/tr[2]/td/img")
        self.assertEqual(bird_image.get_attribute("src"), self.app_url + "/static/images/logo.png")

    def test_editor_dont_want_to_delete(self):
        self.login(self.browser, self.app_url, self.editor.username, "odiseja123")
        self.browser.get(self.app_url + reverse('show_article', args=[self.article1.id_clanka]))
        self.browser.implicitly_wait(10)
        bird_image_prev = self.browser.find_element(By.XPATH,
                                                    "//div[@id='content1']/div/div/div[2]/table/tbody/tr[2]/td/img")
        bird_image_prev_src = bird_image_prev.get_attribute("src")
        delete_img_btn = self.browser.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/button[3]")

        delete_img_btn.click()

        WebDriverWait(self.browser, 50).until(
            EC.visibility_of_element_located((By.ID, "confirmDeleteModal"))
        )

        dont_delete_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "dontDeletePicture"))
        )
        self.browser.execute_script("arguments[0].click();", dont_delete_btn)

        WebDriverWait(self.browser, 50).until(
            EC.invisibility_of_element_located((By.ID, "confirmDeleteModal"))
        )

        bird_image = self.browser.find_element(By.XPATH,
                                               "//div[@id='content1']/div/div/div[2]/table/tbody/tr[2]/td/img")
        self.assertEqual(bird_image.get_attribute("src"), bird_image_prev_src)


    def test_admin_successful_delete(self):
        self.login(self.browser, self.app_url, self.admin.username, "odiseja123")
        self.browser.get(self.app_url + reverse('show_article', args=[self.article1.id_clanka]))
        self.browser.implicitly_wait(10)
        delete_img_btn = self.browser.find_element(By.XPATH,
                                                   "/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/button[3]")
        delete_img_btn.click()

        confirm_delete_btn = WebDriverWait(self.browser, 100).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]"))
        )

        confirm_delete_btn.click()

        WebDriverWait(self.browser, 100).until(
            EC.invisibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]"))
        )

        bird_image = self.browser.find_element(By.XPATH,
                                               "//div[@id='content1']/div/div/div[2]/table/tbody/tr[2]/td/img")
        self.assertEqual(bird_image.get_attribute("src"), self.app_url + "/static/images/logo.png")


    def test_editor_but_not_for_current_article(self):
        self.login(self.browser, self.app_url, self.editor.username, "odiseja123")
        self.browser.get(self.app_url + reverse('show_article', args=[self.article2.id_clanka]))
        self.browser.implicitly_wait(10)
        bird_image_prev = self.browser.find_element(By.XPATH,
                                                    "//div[@id='content1']/div/div/div[2]/table/tbody/tr[2]/td/img")
        bird_image_prev_src = bird_image_prev.get_attribute("src")
        error = 0
        try:
            delete_img_button = WebDriverWait(self.browser, 5).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/button[3]"))
            )
            error = 0
        except TimeoutException:
            error = 1

        bird_image = self.browser.find_element(By.XPATH,
                                               "//div[@id='content1']/div/div/div[2]/table/tbody/tr[2]/td/img")
        self.assertEqual(bird_image.get_attribute("src"), bird_image_prev_src)
        self.assertEqual(error, 1)


    def test_regular_user_try_to_delete(self):
        self.login(self.browser, self.app_url, self.registered.username, "odiseja123")
        self.browser.get(self.app_url + reverse('show_article', args=[self.article2.id_clanka]))
        self.browser.implicitly_wait(10)
        bird_image_prev = self.browser.find_element(By.XPATH,
                                                    "//div[@id='content1']/div/div/div[2]/table/tbody/tr[2]/td/img")
        bird_image_prev_src = bird_image_prev.get_attribute("src")
        error = 0
        try:
            delete_img_button = WebDriverWait(self.browser, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/button[3]"))
            )
            error = 0
        except TimeoutException:
            error = 1

        bird_image = self.browser.find_element(By.XPATH,
                                               "//div[@id='content1']/div/div/div[2]/table/tbody/tr[2]/td/img")
        self.assertEqual(bird_image.get_attribute("src"), bird_image_prev_src)
        self.assertEqual(error, 1)



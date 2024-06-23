# Autor: Anđela Ćirić 2021/0066

import threading
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from slobodna_enciklopedija_ptica_srbije.models import *

import os


class CreateArticleSelenium(StaticLiveServerTestCase):
    def login(self, browser, app_url, username, password):
        browser.get(app_url + reverse('user_login'))

        user_input = browser.find_element(By.ID, "korisnickoImePrijava")
        user_input.send_keys(username)

        pass_input = browser.find_element(By.ID, "lozinkaPrijava")
        browser.execute_script("arguments[0].value = arguments[1]", pass_input, password)

        submit_btn = browser.find_element(By.XPATH, "/html/body/section/div/div/form/table/tbody/tr[3]/td/input")
        submit_btn.click()

    def setUp(self):
        service = webdriver.ChromeService(executable_path='./chromedriver.exe')
        self.browser = webdriver.Chrome(service=service)
        self.app_url = self.live_server_url
        self.admin = Korisnik.objects.create_user(username='testadmin', password='odiseja123', tip="A")
        self.editor = Korisnik.objects.create_user(username="testurednik", password="odiseja123", tip="U")

        article2 = Clanak()
        article2.id_autora = self.admin
        article2.sadrzaj ="Neki sadržaj"
        article2.save()
        self.articleAlreadyExist = article2

        image_data = open(os.path.abspath("./test_data/owl.jpg"), "rb").read()
        table1 = PticaTabela()
        table1.id_clanka = article2
        table1.vrsta = "Sova"
        table1.carstvo = "C1 test"
        table1.klasa = "K1 test"
        table1.porodica = "P1 test"
        table1.red = "R1 test"
        table1.rod = "R1 test"
        table1.slika_vrste = image_data
        table1.status_ugrozenosti = "N1 test"
        table1.tezina = 10
        table1.velicina = 10
        table1.tip = "T1 test"
        table1.save()
        self.tableAlreadyExist = table1

        self.article_created = None
        #self.article2 = Clanak()
        self.table_created = None
        #self.table2 = PticaTabela()


    def tearDown(self):
        self.browser.close()
        if (self.table_created != None):
            self.table_created.delete()
        if(self.article_created != None):
            self.article_created.delete()
        self.tableAlreadyExist.delete()
        self.articleAlreadyExist.delete()
        self.admin.delete()
        self.editor.delete()


    def test_admin_creates_article(self):
        self.login(self.browser, self.app_url, self.admin.username, "odiseja123")
        self.browser.implicitly_wait(10)
        self.browser.get(self.app_url + reverse('create_article'))
        self.browser.implicitly_wait(10)

        vrsta_input = self.browser.find_element(By.ID, "vrsta")
        self.browser.execute_script("arguments[0].scrollIntoView();", vrsta_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "vrsta")))
        vrsta_input.send_keys("Vrsta test")

        rod_input = self.browser.find_element(By.ID, "rod")
        self.browser.execute_script("arguments[0].scrollIntoView();", rod_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "rod")))
        rod_input.send_keys("Rod test")

        porodica_input = self.browser.find_element(By.ID, "porodica")
        self.browser.execute_script("arguments[0].scrollIntoView();", porodica_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "porodica")))
        porodica_input.send_keys("Porodica test")

        red_input = self.browser.find_element(By.ID, "red")
        self.browser.execute_script("arguments[0].scrollIntoView();", red_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "red")))
        red_input.send_keys("Red test")

        klasa_input = self.browser.find_element(By.ID, "klasa")
        self.browser.execute_script("arguments[0].scrollIntoView();", klasa_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "klasa")))
        klasa_input.send_keys("Klasa test")


        tip_input = self.browser.find_element(By.ID, "tip")
        self.browser.execute_script("arguments[0].scrollIntoView();", tip_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "tip")))
        tip_input.send_keys("Tip test")

        carstvo_input = self.browser.find_element(By.ID, "carstvo")
        self.browser.execute_script("arguments[0].scrollIntoView();", carstvo_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "carstvo")))
        carstvo_input.send_keys("Carstvo test")

        tezina_input = self.browser.find_element(By.ID, "tezina")
        self.browser.execute_script("arguments[0].scrollIntoView();", tezina_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "tezina")))
        tezina_input.send_keys(str(int(100)))

        velicina_input = self.browser.find_element(By.ID, "velicina")
        self.browser.execute_script("arguments[0].scrollIntoView();", velicina_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "velicina")))
        velicina_input.send_keys(str(int(50)))

        status_ugrozenosti_input = self.browser.find_element(By.ID, "status-ugrozenosti")
        self.browser.execute_script("arguments[0].scrollIntoView();", status_ugrozenosti_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "status-ugrozenosti")))
        status_ugrozenosti_input.send_keys("nije ugrožena")

        slika_input = self.browser.find_element(By.ID, "slika")
        self.browser.execute_script("arguments[0].scrollIntoView();", slika_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "slika")))
        slika_input.send_keys(os.path.abspath("./test_data/owl.jpg"))

        sadrzaj_input =  self.browser.find_element(By.ID, "glavniTekst")
        self.browser.execute_script("arguments[0].scrollIntoView();", sadrzaj_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "glavniTekst")))
        sadrzaj_input.send_keys("Sadrzaj novi clanak")

        create_article_btn = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Kreiraj nov članak')]")
        self.browser.execute_script("arguments[0].scrollIntoView();", create_article_btn)
        time.sleep(2)
        WebDriverWait(self.browser, 30).until(
            EC.visibility_of(create_article_btn)
        )

        self.browser.execute_script("arguments[0].click();", create_article_btn)
        alert = WebDriverWait(self.browser, 30).until(EC.alert_is_present())
        time.sleep(3)
        alert.accept()
        time.sleep(3)
        article = Clanak.objects.order_by('-id_clanka').first()
        table = PticaTabela.objects.get(id_clanka=article)
        self.article_created = article
        self.table_created = table

        self.assertEqual(self.browser.current_url, self.app_url + f"/pregled_clanka/{self.article_created.id_clanka}")


    def test_editor_creates_article(self):
        self.login(self.browser, self.app_url, self.editor.username, "odiseja123")
        self.browser.implicitly_wait(10)
        self.browser.get(self.app_url + reverse('create_article'))
        self.browser.implicitly_wait(10)

        vrsta_input = self.browser.find_element(By.ID, "vrsta")
        self.browser.execute_script("arguments[0].scrollIntoView();", vrsta_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "vrsta")))
        vrsta_input.send_keys("Vrsta test")

        rod_input = self.browser.find_element(By.ID, "rod")
        self.browser.execute_script("arguments[0].scrollIntoView();", rod_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "rod")))
        rod_input.send_keys("Rod test")

        porodica_input = self.browser.find_element(By.ID, "porodica")
        self.browser.execute_script("arguments[0].scrollIntoView();", porodica_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "porodica")))
        porodica_input.send_keys("Porodica test")

        red_input = self.browser.find_element(By.ID, "red")
        self.browser.execute_script("arguments[0].scrollIntoView();", red_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "red")))
        red_input.send_keys("Red test")

        klasa_input = self.browser.find_element(By.ID, "klasa")
        self.browser.execute_script("arguments[0].scrollIntoView();", klasa_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "klasa")))
        klasa_input.send_keys("Klasa test")


        tip_input = self.browser.find_element(By.ID, "tip")
        self.browser.execute_script("arguments[0].scrollIntoView();", tip_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "tip")))
        tip_input.send_keys("Tip test")

        carstvo_input = self.browser.find_element(By.ID, "carstvo")
        self.browser.execute_script("arguments[0].scrollIntoView();", carstvo_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "carstvo")))
        carstvo_input.send_keys("Carstvo test")

        tezina_input = self.browser.find_element(By.ID, "tezina")
        self.browser.execute_script("arguments[0].scrollIntoView();", tezina_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "tezina")))
        tezina_input.send_keys(str(int(100)))

        velicina_input = self.browser.find_element(By.ID, "velicina")
        self.browser.execute_script("arguments[0].scrollIntoView();", velicina_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "velicina")))
        velicina_input.send_keys(str(int(50)))

        status_ugrozenosti_input = self.browser.find_element(By.ID, "status-ugrozenosti")
        self.browser.execute_script("arguments[0].scrollIntoView();", status_ugrozenosti_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "status-ugrozenosti")))
        status_ugrozenosti_input.send_keys("nije ugrožena")

        slika_input = self.browser.find_element(By.ID, "slika")
        self.browser.execute_script("arguments[0].scrollIntoView();", slika_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "slika")))
        slika_input.send_keys(os.path.abspath("./test_data/owl.jpg"))

        sadrzaj_input =  self.browser.find_element(By.ID, "glavniTekst")
        self.browser.execute_script("arguments[0].scrollIntoView();", sadrzaj_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "glavniTekst")))
        sadrzaj_input.send_keys("Sadrzaj novi clanak")

        create_article_btn = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Kreiraj nov članak')]")
        self.browser.execute_script("arguments[0].scrollIntoView();", create_article_btn)
        time.sleep(2)
        WebDriverWait(self.browser, 30).until(
            EC.visibility_of(create_article_btn)
        )

        self.browser.execute_script("arguments[0].click();", create_article_btn)
        alert = WebDriverWait(self.browser, 30).until(EC.alert_is_present())
        time.sleep(3)
        alert.accept()
        time.sleep(3)
        article = Clanak.objects.order_by('-id_clanka').first()
        table = PticaTabela.objects.get(id_clanka=article)
        self.article_created = article
        self.table_created = table

        self.assertEqual(self.browser.current_url, self.app_url + f"/pregled_clanka/{self.article_created.id_clanka}")



    def test_admin_dismiss_creating_article(self):
        self.login(self.browser, self.app_url, self.admin.username, "odiseja123")
        self.browser.implicitly_wait(10)
        self.browser.get(self.app_url + reverse('create_article'))
        self.browser.implicitly_wait(10)

        vrsta_input = self.browser.find_element(By.ID, "vrsta")
        self.browser.execute_script("arguments[0].scrollIntoView();", vrsta_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "vrsta")))
        vrsta_input.send_keys("Vrsta test")

        prev_vrsta = vrsta_input.get_attribute("value")

        rod_input = self.browser.find_element(By.ID, "rod")
        self.browser.execute_script("arguments[0].scrollIntoView();", rod_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "rod")))
        rod_input.send_keys("Rod test")

        prev_rod = rod_input.get_attribute("value")

        porodica_input = self.browser.find_element(By.ID, "porodica")
        self.browser.execute_script("arguments[0].scrollIntoView();", porodica_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "porodica")))
        porodica_input.send_keys("Porodica test")

        prev_porodica = porodica_input.get_attribute("value")

        red_input = self.browser.find_element(By.ID, "red")
        self.browser.execute_script("arguments[0].scrollIntoView();", red_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "red")))
        red_input.send_keys("Red test")

        prev_red = red_input.get_attribute("value")

        klasa_input = self.browser.find_element(By.ID, "klasa")
        self.browser.execute_script("arguments[0].scrollIntoView();", klasa_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "klasa")))
        klasa_input.send_keys("Klasa test")

        prev_klasa = klasa_input.get_attribute("value")


        tip_input = self.browser.find_element(By.ID, "tip")
        self.browser.execute_script("arguments[0].scrollIntoView();", tip_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "tip")))
        tip_input.send_keys("Tip test")

        prev_tip = tip_input.get_attribute("value")

        carstvo_input = self.browser.find_element(By.ID, "carstvo")
        self.browser.execute_script("arguments[0].scrollIntoView();", carstvo_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "carstvo")))
        carstvo_input.send_keys("Carstvo test")

        prev_carstvo = carstvo_input.get_attribute("value")

        tezina_input = self.browser.find_element(By.ID, "tezina")
        self.browser.execute_script("arguments[0].scrollIntoView();", tezina_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "tezina")))
        tezina_input.send_keys(str(int(100)))

        prev_tezina = tezina_input.get_attribute("value")

        velicina_input = self.browser.find_element(By.ID, "velicina")
        self.browser.execute_script("arguments[0].scrollIntoView();", velicina_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "velicina")))
        velicina_input.send_keys(str(int(50)))

        prev_velicina = velicina_input.get_attribute("value")

        status_ugrozenosti_input = self.browser.find_element(By.ID, "status-ugrozenosti")
        self.browser.execute_script("arguments[0].scrollIntoView();", status_ugrozenosti_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "status-ugrozenosti")))
        status_ugrozenosti_input.send_keys("nije ugrožena")

        prev_status = status_ugrozenosti_input.get_attribute("value")

        slika_input = self.browser.find_element(By.ID, "slika")
        self.browser.execute_script("arguments[0].scrollIntoView();", slika_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "slika")))
        slika_input.send_keys(os.path.abspath("./test_data/owl.jpg"))

        prev_slika = slika_input.get_attribute("value")

        sadrzaj_input =  self.browser.find_element(By.ID, "glavniTekst")
        self.browser.execute_script("arguments[0].scrollIntoView();", sadrzaj_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "glavniTekst")))
        sadrzaj_input.send_keys("Sadrzaj novi clanak")

        prev_sadrzaj = sadrzaj_input.get_attribute("value")
        prev_url = self.browser.current_url
        create_article_btn = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Kreiraj nov članak')]")
        self.browser.execute_script("arguments[0].scrollIntoView();", create_article_btn)
        time.sleep(2)
        WebDriverWait(self.browser, 30).until(
            EC.visibility_of(create_article_btn)
        )

        self.browser.execute_script("arguments[0].click();", create_article_btn)
        alert = WebDriverWait(self.browser, 30).until(EC.alert_is_present())
        time.sleep(3)
        alert.dismiss()
        time.sleep(7)

        self.assertEqual(self.browser.current_url, prev_url)
        self.assertEqual(prev_slika, slika_input.get_attribute("value"))
        self.assertEqual(prev_red, red_input.get_attribute("value"))
        self.assertEqual(prev_rod, rod_input.get_attribute("value"))
        self.assertEqual(prev_tip, tip_input.get_attribute("value"))
        self.assertEqual(prev_klasa, klasa_input.get_attribute("value"))
        self.assertEqual(prev_vrsta, vrsta_input.get_attribute("value"))
        self.assertEqual(prev_status, status_ugrozenosti_input.get_attribute("value"))
        self.assertEqual(prev_sadrzaj, sadrzaj_input.get_attribute("value"))
        self.assertEqual(prev_tezina, tezina_input.get_attribute("value"))
        self.assertEqual(prev_carstvo, carstvo_input.get_attribute("value"))
        self.assertEqual(prev_porodica, porodica_input.get_attribute("value"))
        self.assertEqual(prev_velicina, velicina_input.get_attribute("value"))


    def test_create_article_without_name(self):
        self.login(self.browser, self.app_url, self.admin.username, "odiseja123")
        self.browser.implicitly_wait(10)
        self.browser.get(self.app_url + reverse('create_article'))
        self.browser.implicitly_wait(10)

        porodica_input = self.browser.find_element(By.ID, "porodica")
        self.browser.execute_script("arguments[0].scrollIntoView();", porodica_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "porodica")))
        porodica_input.send_keys("Porodica test")

        prev_porodica = porodica_input.get_attribute("value")

        sadrzaj_input = self.browser.find_element(By.ID, "glavniTekst")
        self.browser.execute_script("arguments[0].scrollIntoView();", sadrzaj_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "glavniTekst")))
        sadrzaj_input.send_keys("Sadrzaj novi clanak")
        prev_url = self.browser.current_url

        prev_sadrzaj = sadrzaj_input.get_attribute("value")

        create_article_btn = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Kreiraj nov članak')]")
        self.browser.execute_script("arguments[0].scrollIntoView();", create_article_btn)
        time.sleep(2)
        WebDriverWait(self.browser, 30).until(
            EC.visibility_of(create_article_btn)
        )

        self.browser.execute_script("arguments[0].click();", create_article_btn)
        alert = WebDriverWait(self.browser, 30).until(EC.alert_is_present())
        time.sleep(3)
        alert.accept()
        time.sleep(7)

        error_msg = self.browser.find_element(By.ID, "error_msg")
        self.browser.execute_script("arguments[0].scrollIntoView();", error_msg)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "error_msg")))
        error_msg_val = error_msg.text

        sadrzaj_input = self.browser.find_element(By.ID, "glavniTekst")
        self.browser.execute_script("arguments[0].scrollIntoView();", sadrzaj_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "glavniTekst")))

        porodica_input = self.browser.find_element(By.ID, "porodica")
        self.browser.execute_script("arguments[0].scrollIntoView();", porodica_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "porodica")))

        self.assertEqual(self.browser.current_url, prev_url)
        self.assertEqual(prev_sadrzaj, sadrzaj_input.get_attribute("value"))
        self.assertEqual(prev_porodica, porodica_input.get_attribute("value"))
        #print(error_msg_val)
        self.assertEqual(error_msg_val, "Niste uneli polje za koju vrstu ptice želite da napravite članak.")

    def test_create_article_with_name_which_already_exist(self):
        self.login(self.browser, self.app_url, self.admin.username, "odiseja123")
        self.browser.implicitly_wait(10)
        self.browser.get(self.app_url + reverse('create_article'))
        self.browser.implicitly_wait(10)

        vrsta_input = self.browser.find_element(By.ID, "vrsta")
        self.browser.execute_script("arguments[0].scrollIntoView();", vrsta_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "vrsta")))
        vrsta_input.send_keys("Sova")

        prev_vrsta = vrsta_input.get_attribute("value")

        porodica_input = self.browser.find_element(By.ID, "porodica")
        self.browser.execute_script("arguments[0].scrollIntoView();", porodica_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "porodica")))
        porodica_input.send_keys("Porodica test")

        prev_porodica = porodica_input.get_attribute("value")

        sadrzaj_input = self.browser.find_element(By.ID, "glavniTekst")
        self.browser.execute_script("arguments[0].scrollIntoView();", sadrzaj_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "glavniTekst")))
        sadrzaj_input.send_keys("Sadrzaj novi clanak")
        prev_url = self.browser.current_url

        prev_sadrzaj = sadrzaj_input.get_attribute("value")

        create_article_btn = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Kreiraj nov članak')]")
        self.browser.execute_script("arguments[0].scrollIntoView();", create_article_btn)
        time.sleep(2)
        WebDriverWait(self.browser, 30).until(
            EC.visibility_of(create_article_btn)
        )

        self.browser.execute_script("arguments[0].click();", create_article_btn)
        alert = WebDriverWait(self.browser, 30).until(EC.alert_is_present())
        time.sleep(3)
        alert.accept()
        time.sleep(7)

        error_msg = self.browser.find_element(By.ID, "error_msg")
        self.browser.execute_script("arguments[0].scrollIntoView();", error_msg)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "error_msg")))
        error_msg_val = error_msg.text

        vrsta_input = self.browser.find_element(By.ID, "vrsta")
        self.browser.execute_script("arguments[0].scrollIntoView();", vrsta_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "vrsta")))

        sadrzaj_input = self.browser.find_element(By.ID, "glavniTekst")
        self.browser.execute_script("arguments[0].scrollIntoView();", sadrzaj_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "glavniTekst")))

        porodica_input = self.browser.find_element(By.ID, "porodica")
        self.browser.execute_script("arguments[0].scrollIntoView();", porodica_input)
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, "porodica")))

        self.assertEqual(self.browser.current_url, prev_url)
        self.assertEqual(prev_sadrzaj, sadrzaj_input.get_attribute("value"))
        self.assertEqual(prev_porodica, porodica_input.get_attribute("value"))
        self.assertEqual(prev_vrsta, vrsta_input.get_attribute("value"))
        #print(error_msg_val)
        self.assertEqual(error_msg_val, "Pokušali ste da napravite članak za vrstu ptice koja već postoji.")














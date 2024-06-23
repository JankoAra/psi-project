# Autor testa: Jaroslav Veseli 2021/0480

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import os

from slobodna_enciklopedija_ptica_srbije.models import *
from .utilities import initialize_data_vj210480, delete_data_vj210480, login


class TestChangeBirdImage(StaticLiveServerTestCase):
    def setUp(self):
        # Napravi objekat koji predstavlja selenium chrome driver. Dohvati URL live servera. Inicijalizuj podatke.
        service = webdriver.ChromeService(executable_path='./chromedriver.exe')
        self.browser = webdriver.Chrome(service=service)
        self.app_url = self.live_server_url
        initialize_data_vj210480(self)
        
    def tearDown(self):
        # Ugasi chrome driver.
        self.browser.close()
        delete_data_vj210480(self)

    def test_success(self):
        login(self.browser, self.app_url, "jaroslav_1", "WhoKnows455@")
        self.browser.get(self.app_url + reverse('show_article', args=[self.article_1.id_clanka]))

        # Promena slike vrste dugme.
        change_img_btn = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/button[2]")
        change_img_btn.click()
        
        # Unesi putanju slike.
        img_input = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/form/input[2]")
        img_input.send_keys(os.path.abspath("./test_data/owl.jpg"))
        
        # Uzmi element slike pre potvrde. 
        bird_image = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/img")

        # Potvrdi izmenu.
        img_confirm_change = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/form/button")
        img_confirm_change.click()
        
        # Sacekaj da se refreshuje stranica. To se desava se stari element slike skloni sa stranice.
        WebDriverWait(self.browser, 20).until(EC.staleness_of(bird_image))
        
        # Assertuj da je slika promenjena.
        bird_image = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/img")
        self.assertNotEqual(bird_image.get_attribute("src"), self.app_url + "/static/images/logo.png")
        
    def test_give_up(self):
        login(self.browser, self.app_url, "jaroslav_1", "WhoKnows455@")
        self.browser.get(self.app_url + reverse('show_article', args=[self.article_1.id_clanka]))

        # Promena slike vrste.
        change_img_btn = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/button[2]")
        change_img_btn.click()
        
        # Odustani od promene.
        give_up_btn = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/button[1]")
        give_up_btn.click()

        # Assertuj da je slika ostala ista.
        bird_image = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/img")
        self.assertEqual(bird_image.get_attribute("src"), self.app_url + "/static/images/logo.png")
    
    def test_bad_file(self):
        login(self.browser, self.app_url, "jaroslav_1", "WhoKnows455@")
        self.browser.get(self.app_url + reverse('show_article', args=[self.article_1.id_clanka]))

        # Pokusaj promene slike vrste u random binarni fajl.
        change_img_btn = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/button[2]")
        change_img_btn.click()
        
        # Unesi putanju nekog random fajla.
        img_input = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/form/input[2]")
        img_input.send_keys(os.path.abspath("./test_data/binary_file.bin"))

        # Uzmi element slike pre potvrde. 
        bird_image = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/img")
        
        # Potvrdi izmenu.
        img_confirm_change = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/form/button")
        img_confirm_change.click()

        # Sacekaj da se refreshuje stranica. To se desava se stari element slike skloni sa stranice.
        WebDriverWait(self.browser, 20).until(EC.staleness_of(bird_image))
        
        # Assertuj da slika nije promenjena.
        bird_image = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/img")
        self.assertEqual(bird_image.get_attribute("src"), self.app_url + "/static/images/logo.png")
    
    def test_not_author(self):
        login(self.browser, self.app_url, "jaroslav_1", "WhoKnows455@")
        self.browser.get(self.app_url + reverse('show_article', args=[self.article_2.id_clanka]))

        # Pokusaj da pronadjes dugme za izmenu slike, assertuj da nije pronadjeno.
        find_elem = lambda: self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/table/tbody/tr[2]/td/button[2]")
        self.assertRaises(NoSuchElementException, find_elem)

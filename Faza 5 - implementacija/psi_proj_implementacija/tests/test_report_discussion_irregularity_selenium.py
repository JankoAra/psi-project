# Autor testa: Jaroslav Veseli 2021/0480

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from slobodna_enciklopedija_ptica_srbije.models import *
from .utilities import initialize_data_vj210480, delete_data_vj210480, login


class TestReportDiscussionIrregularity(StaticLiveServerTestCase):
    def setUp(self):
        # Napravi objekat koji predstavlja selenium chrome driver. Dohvati URL live servera.
        service = webdriver.ChromeService(executable_path='./chromedriver.exe')
        self.browser = webdriver.Chrome(service=service)
        self.app_url = self.live_server_url
        initialize_data_vj210480(self)
        
    def tearDown(self):
        # Ugasi chrome driver.
        self.browser.close()
        delete_data_vj210480(self)
    
    def test_success(self):
        login(self.browser, self.app_url, "jaroslav_4", "WhoKnows455@")
        self.browser.get(self.app_url + reverse('show_article', args=[self.article_1.id_clanka]))
        
        # Idi u diskusije.
        discussion_tab = self.browser.find_element(By.XPATH, "/html/body/div[1]/ul/li[3]/a")
        discussion_tab.click()
        
        # Idi na stranicu za prijavljivanje diskusije.
        drop_down_btn = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[3]/div[2]/div/div[2]/div/button")))
        drop_down_btn.click()

        report_btn = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div[2]/div/div[2]/div/ul/a")
        report_btn.click()

        # Sacekaj da predjes na stranicu za prijavu nepravilnosti.
        WebDriverWait(self.browser, 20).until(EC.url_matches(self.app_url + f"/prijavi_nepravilnost_diskusije/{self.discussion.id_diskusije}"))
        
        # Prijavi nepravilnost.
        confirm_btn = self.browser.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/div/div[2]/button[1]")
        confirm_btn.click()

        # Ako je prijava uspesna, ocekujem da ce mi se prikazati tekst o uspehu.
        success_text = self.browser.find_element(By.XPATH, "/html/body/div/div[2]/div/div[1]")
        WebDriverWait(self.browser, 20).until(EC.visibility_of(success_text))
        self.assertEqual(success_text.text, "Uspešno ste prijavili nepravilnost.")
        
        back_button = self.browser.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/button")
        back_button.click()
        
        # Nakon pritiskanja dugmeta za give up, ocekujem da cu se vratiti na clanak. Ako se to nece desiti za 20 sekundi, baca se exception.
        WebDriverWait(self.browser, 20).until(EC.url_matches(self.app_url + f"/pregled_clanka/{self.article_1.id_clanka}"))
    
    def test_give_up(self):
        login(self.browser, self.app_url, "jaroslav_4", "WhoKnows455@")
        self.browser.get(self.app_url + reverse('show_article', args=[self.article_1.id_clanka]))
        
        # Idi u diskusije.
        discussion_tab = self.browser.find_element(By.XPATH, "/html/body/div[1]/ul/li[3]/a")
        discussion_tab.click()
        
        # Prijavi diskusiju.
        drop_down_btn = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[3]/div[2]/div/div[2]/div/button")))
        drop_down_btn.click()

        report_btn = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div[2]/div/div[2]/div/ul/a")
        report_btn.click()

        # Sacekaj da predjes na stranicu za prijavu nepravilnosti.
        WebDriverWait(self.browser, 20).until(EC.url_matches(self.app_url + f"/prijavi_nepravilnost_diskusije/{self.discussion.id_diskusije}"))

        # Odustani od prijave nepravilnosti.
        give_up_btn = self.browser.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/div/div[2]/button[2]")
        give_up_btn.click()

        # Nakon pritiskanja dugmeta za give up, ocekujem da cu se vratiti na clanak. Ako se to nece desiti za 20 sekundi, baca se exception.
        WebDriverWait(self.browser, 20).until(EC.url_matches(self.app_url + f"/pregled_clanka/{self.article_1.id_clanka}"))
        
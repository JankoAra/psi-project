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


class TestReportArticleIrregularity(StaticLiveServerTestCase):
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

        # Idi na prijavu nepravilnosti.
        report_button = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/div/button[3]")
        report_button.click()

        # Sacekaj da predjes na stranicu za prijavu nepravilnosti
        WebDriverWait(self.browser, 20).until(EC.url_matches(self.app_url + f"/prijavi_nepravilnost_clanka/{self.article_1.id_clanka}"))
        
        # Prijavi nepravilnost.
        report_input = self.browser.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/div/div[1]/textarea")
        report_input.send_keys("Imate gramatičke greške u vašem članku.")
        
        confirm_btn = self.browser.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/div/div[3]/button[1]")
        confirm_btn.click()
        
        # Ako je prijava uspesna, ocekujem da ce mi se prikazati tekst o uspehu.
        success_text = self.browser.find_element(By.XPATH, "/html/body/div/div[2]/div/div[1]")
        WebDriverWait(self.browser, 20).until(EC.visibility_of(success_text))
        self.assertEqual(success_text.text, "Uspešno ste prijavili nepravilnost.")
        
        # Klikni na dugme povratka.
        back_button = self.browser.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/button")
        back_button.click()

        # Nakon pritiskanja dugmeta za povratak, ocekujem da cu se vratiti na clanak. Ako se to nece desiti za 20 sekundi, baca se exception.
        WebDriverWait(self.browser, 20).until(EC.url_matches(self.app_url + f"/pregled_clanka/{self.article_1.id_clanka}"))

    def test_give_up(self):
        login(self.browser, self.app_url, "jaroslav_4", "WhoKnows455@")
        self.browser.get(self.app_url + reverse('show_article', args=[self.article_1.id_clanka]))

        # Idi na stranicu prijave nepravilnosti.
        report_button = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/div/button[3]")
        report_button.click()

        # Sacekaj da predjes na stranicu za prijavu nepravilnosti
        WebDriverWait(self.browser, 20).until(EC.url_matches(self.app_url + f"/prijavi_nepravilnost_clanka/{self.article_1.id_clanka}"))
        
        # Odustani od prijave nepravilnosti.
        give_up_btn = self.browser.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/div/div[3]/button[2]")
        give_up_btn.click()

        # Nakon pritiskanja dugmeta za give up, ocekujem da cu se vratiti na clanak. Ako se to nece desiti za 20 sekundi, baca se exception.
        WebDriverWait(self.browser, 20).until(EC.url_matches(self.app_url + f"/pregled_clanka/{self.article_1.id_clanka}"))
    
    def test_empty_text(self):
        login(self.browser, self.app_url, "jaroslav_4", "WhoKnows455@")
        self.browser.get(self.app_url + reverse('show_article', args=[self.article_1.id_clanka]))

        # Prijavi nepravilnost bez teksta.
        report_button = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/div/button[3]")
        report_button.click()

        # Sacekaj da predjes na stranicu za prijavu nepravilnosti
        WebDriverWait(self.browser, 20).until(EC.url_matches(self.app_url + f"/prijavi_nepravilnost_clanka/{self.article_1.id_clanka}"))
        
        # Probaj da prijavis nepravilnost bez teksta.
        confirm_btn = self.browser.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/div/div[3]/button[1]")
        confirm_btn.click()
        
        report_input = self.browser.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/div/div[1]/textarea")
        self.assertEqual(report_input.get_attribute("placeholder"), "Morate uneti nešto kao razlog prijave")
    
    def test_long_text(self):
        login(self.browser, self.app_url, "jaroslav_4", "WhoKnows455@")
        self.browser.get(self.app_url + reverse('show_article', args=[self.article_1.id_clanka]))

        # Prijavi nepravilnost.
        report_button = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/div/button[3]")
        report_button.click()

        # Sacekaj da predjes na stranicu za prijavu nepravilnosti
        WebDriverWait(self.browser, 20).until(EC.url_matches(self.app_url + f"/prijavi_nepravilnost_clanka/{self.article_1.id_clanka}"))
        
        # Unesi predugacak tekst od 800+ karaktera.
        report_input = self.browser.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/div/div[1]/textarea")
        report_input.send_keys("Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.Imate gramatičke greške u vašem članku.")
        
        # Ocekujem da ce duzina teksta biti limitirana na 300 karaktera.
        self.assertEquals(len(report_input.get_attribute("value")), 300)
        
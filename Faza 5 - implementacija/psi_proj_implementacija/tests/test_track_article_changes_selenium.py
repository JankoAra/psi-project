# Autor: Janko Arandjelovic 2021/0328

import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from slobodna_enciklopedija_ptica_srbije.models import Clanak, Korisnik, PrijavljenNaObavestenja, PticaTabela


class TestTrackArticleChangesSelenium(StaticLiveServerTestCase):
    
    def login(self, redirect_url, username, password):
        self.client.login(username=username, password=password)
        
        cookies = self.client.cookies
        
        self.browser.get(redirect_url)
        for key, value in cookies.items():
            self.browser.add_cookie({
                'name': key,
                'value': value.value,
                'path': '/',
            })
        
        self.browser.refresh()
    def setUp(self):
        service = webdriver.ChromeService(executable_path='./chromedriver.exe')
        self.browser = webdriver.Chrome(service = service)
        self.app_url = self.live_server_url
        self.user = Korisnik.objects.create_user(username='testuser', password='testpassword', tip="R")
        self.article = Clanak.objects.create(sadrzaj='Test Content', id_autora=self.user)
        self.bird_table = PticaTabela.objects.create(id_clanka=self.article, vrsta='test ptica')
        
    def tearDown(self):
        self.browser.close()
        self.bird_table.delete()
        self.article.delete()
        self.user.delete()
        
    def test_track_article_changes_not_tracking(self):
        redirect_url = self.live_server_url + reverse('show_article', args=[self.article.id_clanka])
        self.login(redirect_url=redirect_url, username='testuser', password='testpassword')
        track_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'track_changes_button'))
        )
        track_btn.click()
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(self.app_url + reverse('track_changes_on_article', args=[self.article.id_clanka]))
        )
        page_title_text = self.browser.find_elements(By.ID, 'title_text_start_tracking')
        self.assertTrue(page_title_text[0].is_displayed())
        track_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'prijavi_button_ID'))
        )
        track_btn.click()
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.ID, 'uspesna_prijava'))
        )
        return_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'povratak_button_ID'))
        )
        return_btn.click()
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(redirect_url)
        )
        dont_track_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'dont_track_changes_button'))
        )
        track_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'track_changes_button'))
        )
        self.assertFalse(track_btn.is_displayed())
        self.assertTrue(dont_track_btn.is_displayed())
        dbSub = PrijavljenNaObavestenja.objects.filter(id_clanka=self.article, id_korisnika=self.user)
        self.assertTrue(dbSub.count() == 1)
        
    def test_untrack_article_changes(self):
        subscription = PrijavljenNaObavestenja.objects.create(id_clanka=self.article, id_korisnika=self.user, primaj_na_mail=False)
        redirect_url = self.live_server_url + reverse('show_article', args=[self.article.id_clanka])
        self.login(redirect_url=redirect_url, username='testuser', password='testpassword')
        dont_track_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'dont_track_changes_button'))
        )
        track_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'track_changes_button'))
        )
        self.assertFalse(track_btn.is_displayed())
        self.assertTrue(dont_track_btn.is_displayed())
        dont_track_btn.click()
        dont_track_btn = WebDriverWait(self.browser, 10).until(
            EC.invisibility_of_element_located((By.ID, 'dont_track_changes_button'))
        )
        track_btn = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.ID, 'track_changes_button'))
        )
        self.assertFalse(dont_track_btn.is_displayed())
        self.assertTrue(track_btn.is_displayed())
        dbSub = PrijavljenNaObavestenja.objects.filter(id_clanka=self.article, id_korisnika=self.user)
        self.assertTrue(dbSub.count() == 0)
        
    def test_track_article_changes_cancel(self):
        redirect_url = self.live_server_url + reverse('show_article', args=[self.article.id_clanka])
        self.login(redirect_url=redirect_url, username='testuser', password='testpassword')
        cancel_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'track_changes_button'))
        )
        cancel_btn.click()
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(self.app_url + reverse('track_changes_on_article', args=[self.article.id_clanka]))
        )
        page_title_text = self.browser.find_elements(By.ID, 'title_text_start_tracking')
        self.assertTrue(page_title_text[0].is_displayed())
        cancel_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'odustani_button_ID'))
        )
        cancel_btn.click()
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(redirect_url)
        )
        dont_track_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'dont_track_changes_button'))
        )
        track_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'track_changes_button'))
        )
        self.assertFalse(dont_track_btn.is_displayed())
        self.assertTrue(track_btn.is_displayed())
        dbSub = PrijavljenNaObavestenja.objects.filter(id_clanka=self.article, id_korisnika=self.user)
        self.assertTrue(dbSub.count() == 0)
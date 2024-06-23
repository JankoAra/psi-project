# Autor: Janko Arandjelovic 2021/0328

import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from slobodna_enciklopedija_ptica_srbije.models import Clanak, Korisnik, PticaTabela


class TestLogoutSelenium(StaticLiveServerTestCase):
    
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
        self.user = Korisnik.objects.create_user(username='testuser', password='testpassword')
        
    def tearDown(self):
        self.browser.close()
        self.user.delete()
        
    def test_logout_success(self):
        self.login(self.app_url, 'testuser', 'testpassword')
        
        expected_url = self.live_server_url + reverse('index')  
        WebDriverWait(self.browser, 10).until(EC.url_to_be(expected_url))
        self.assertEqual(self.browser.current_url, expected_url)
        
        dropdown = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.ID, 'navbarDropdown'))
        )
        
        dropdown.click()
        
        odjava_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.ID, 'odjava_button_navbar'))
        )
        
        odjava_button.click()
        
        prijava_button_navbar = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'prijava_button_navbar'))
        )
        
        self.assertEqual(len(self.browser.find_elements(By.ID, 'prijava_button_navbar')), 1)
        
        self.assertFalse('_auth_user_id' in self.client.session)
        
    def test_logout_unauthenticated(self):
        self.browser.get(self.app_url)
        self.assertFalse('_auth_user_id' in self.client.session)
        
        prijava_button_navbar = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'prijava_button_navbar'))
        )
        
        self.assertEqual(len(self.browser.find_elements(By.ID, 'prijava_button_navbar')), 1)
        
        dropdown = self.browser.find_elements(By.ID, 'navbarDropdown')
        self.assertEqual(len(dropdown), 0)
        
    def test_logout_redirect_to_next(self):
        article = Clanak.objects.create(id_autora=self.user)
        bird_table = PticaTabela.objects.create(id_clanka=article, vrsta='test_ptica')
        
        redirect_to = self.live_server_url + reverse('show_article', args=[article.id_clanka])
        # print(redirect_to)
        self.login(redirect_to, 'testuser', 'testpassword')
        
        WebDriverWait(self.browser, 10).until(EC.url_to_be(redirect_to))
        
        dropdown = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.ID, 'navbarDropdown'))
        )
        
        dropdown.click()
        
        odjava_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.ID, 'odjava_button_navbar'))
        )
        
        odjava_button.click()
        
        WebDriverWait(self.browser, 10).until(EC.url_to_be(redirect_to))
        self.assertEqual(self.browser.current_url, redirect_to)
        prijava_button_navbar = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'prijava_button_navbar'))
        )
        
        self.assertEqual(len(self.browser.find_elements(By.ID, 'prijava_button_navbar')), 1)
        
        self.assertFalse('_auth_user_id' in self.client.session)
        bird_table.delete()
        article.delete()
        
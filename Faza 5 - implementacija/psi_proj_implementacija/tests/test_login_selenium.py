# Autor: Janko Arandjelovic 2021/0328

import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from slobodna_enciklopedija_ptica_srbije.models import Korisnik


class TestLoginSelenium(StaticLiveServerTestCase):
    
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
        self.app_url = self.live_server_url + reverse('user_login')
        self.user = Korisnik.objects.create_user(username='testuser', password='testpassword')
        
    def tearDown(self):
        self.browser.close()
        self.user.delete()
        
    def test_login_success(self):
        self.browser.get(self.app_url)
        username_input = self.browser.find_element(By.ID, "korisnickoImePrijava")
        username_input.send_keys("testuser")
        password_input = self.browser.find_element(By.ID, "lozinkaPrijava")
        password_input.send_keys("testpassword")
        submit_btn = self.browser.find_element(By.ID, 'prijava_button_ID')
        submit_btn.click()
        WebDriverWait(self.browser, 10).until(EC.url_changes(self.app_url))
        expected_url = self.live_server_url + reverse('index')  
        self.assertEqual(self.browser.current_url, expected_url)
        
    def test_login_wrong_username(self):
        self.browser.get(self.app_url)
        username_input = self.browser.find_element(By.ID, "korisnickoImePrijava")
        username_input.send_keys("greska")
        password_input = self.browser.find_element(By.ID, "lozinkaPrijava")
        password_input.send_keys("testpassword")
        submit_btn = self.browser.find_element(By.ID, 'prijava_button_ID')
        submit_btn.click()
        error_msg = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'greskaPrijava'))
        )
        self.assertTrue(error_msg.is_displayed())
        expected_url = self.app_url
        self.assertEqual(self.browser.current_url, expected_url)
        
    def test_login_wrong_password(self):
        self.browser.get(self.app_url)
        username_input = self.browser.find_element(By.ID, "korisnickoImePrijava")
        username_input.send_keys("testuser")
        password_input = self.browser.find_element(By.ID, "lozinkaPrijava")
        password_input.send_keys("greska")
        submit_btn = self.browser.find_element(By.ID, 'prijava_button_ID')
        submit_btn.click()
        error_msg = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'greskaPrijava'))
        )
        self.assertTrue(error_msg.is_displayed())
        expected_url = self.app_url
        self.assertEqual(self.browser.current_url, expected_url)
        
    def test_login_no_username(self):
        self.browser.get(self.app_url)
        password_input = self.browser.find_element(By.ID, "lozinkaPrijava")
        password_input.send_keys("testpassword")
        submit_btn = self.browser.find_element(By.ID, 'prijava_button_ID')
        submit_btn.click()
        error_msg = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'greskaPrijava'))
        )
        self.assertTrue(error_msg.is_displayed())
        expected_url = self.app_url
        self.assertEqual(self.browser.current_url, expected_url)
        
    def test_login_no_password(self):
        self.browser.get(self.app_url)
        username_input = self.browser.find_element(By.ID, "korisnickoImePrijava")
        username_input.send_keys("testuser")
        submit_btn = self.browser.find_element(By.ID, 'prijava_button_ID')
        submit_btn.click()
        error_msg = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'greskaPrijava'))
        )
        self.assertTrue(error_msg.is_displayed())
        expected_url = self.app_url
        self.assertEqual(self.browser.current_url, expected_url)
        
    def test_show_user_in_navbar(self):
        self.browser.get(self.app_url)
        navbarName = self.browser.find_elements(By.ID, 'navbarDropdown')
        self.assertEqual(len(navbarName), 0)
        username_input = self.browser.find_element(By.ID, "korisnickoImePrijava")
        username_input.send_keys("testuser")
        password_input = self.browser.find_element(By.ID, "lozinkaPrijava")
        password_input.send_keys("testpassword")
        submit_btn = self.browser.find_element(By.ID, 'prijava_button_ID')
        submit_btn.click()
        WebDriverWait(self.browser, 10).until(EC.url_changes(self.app_url))
        expected_url = self.live_server_url + reverse('index')  
        self.assertEqual(self.browser.current_url, expected_url)
        navbarName = self.browser.find_elements(By.ID, 'navbarDropdown')
        self.assertEqual(len(navbarName), 1)
        self.assertEqual(navbarName[0].text, 'testuser')
        
    def test_already_logged_in(self):
        self.login(self.live_server_url, 'testuser', 'testpassword')
        WebDriverWait(self.browser, 10).until(EC.url_changes(self.app_url))
        prijava_button_navbar = self.browser.find_elements(By.ID, 'prijava_button_navbar') 
        self.assertEqual(len(prijava_button_navbar), 0)
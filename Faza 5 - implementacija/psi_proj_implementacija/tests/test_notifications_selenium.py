# Autor: Janko Arandjelovic 2021/0328

import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from slobodna_enciklopedija_ptica_srbije.models import Clanak, Korisnik, Poruka, PrijavljenNaObavestenja, PrimljenePoruke, PticaTabela


class TestNotifications(StaticLiveServerTestCase):
    
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
        PrimljenePoruke.objects.filter(id_korisnika=self.user).delete()
        self.bird_table.delete()
        self.article.delete()
        self.user.delete()
        
    def test_notifications_show_no_content(self):
        redirect_url = self.live_server_url + reverse('index')
        self.login(redirect_url=redirect_url, username='testuser', password='testpassword')
        inbox_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'inbox_link'))
        )
        inbox_btn.click()
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(self.app_url + reverse('notifications'))
        )
        title_text = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'title_text'))
        )
        self.assertTrue(title_text.is_displayed())
        
    def test_notifications_show_with_content(self):
        msg = Poruka.objects.create(tekst='test poruke')
        received_msg = PrimljenePoruke.objects.create(id_poruke=msg, id_korisnika=self.user, procitana=0, tip_prijave='C', id_prijavljene_stvari=self.article.id_clanka)
        redirect_url = self.live_server_url + reverse('index')
        self.login(redirect_url=redirect_url, username='testuser', password='testpassword')
        inbox_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'inbox_link'))
        )
        inbox_btn.click()
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(self.app_url + reverse('notifications'))
        )
        title_text = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'title_text'))
        )
        self.assertTrue(title_text.is_displayed())
        msg_row = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'row_' + str(msg.id_poruke)))
        )
        self.assertTrue(msg_row.is_displayed())
        
        first_child = msg_row.find_element(By.CSS_SELECTOR, ':first-child')
        
        style_value = self.browser.execute_script(
            "return window.getComputedStyle(arguments[0]).getPropertyValue(arguments[1]);",
            first_child,
            'background-color'
        )
        self.assertNotEqual(style_value, 'rgb(221, 221, 221)')
        
    def test_notifications_show_with_content_read(self):
        msg = Poruka.objects.create(tekst='test poruke')
        received_msg = PrimljenePoruke.objects.create(id_poruke=msg, id_korisnika=self.user, procitana=1, tip_prijave='C', id_prijavljene_stvari=self.article.id_clanka)
        redirect_url = self.live_server_url + reverse('index')
        self.login(redirect_url=redirect_url, username='testuser', password='testpassword')
        inbox_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'inbox_link'))
        )
        inbox_btn.click()
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(self.app_url + reverse('notifications'))
        )
        title_text = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'title_text'))
        )
        self.assertTrue(title_text.is_displayed())
        msg_row = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'row_' + str(msg.id_poruke)))
        )
        self.assertTrue(msg_row.is_displayed())
        
        first_child = msg_row.find_element(By.CSS_SELECTOR, ':first-child')
        
        style_value = self.browser.execute_script(
            "return window.getComputedStyle(arguments[0]).getPropertyValue(arguments[1]);",
            first_child,
            'background-color'
        )
        self.assertEqual(style_value, 'rgb(221, 221, 221)')
        
    def test_open_notification(self):
        msg = Poruka.objects.create(tekst='test poruke')
        received_msg = PrimljenePoruke.objects.create(id_poruke=msg, id_korisnika=self.user, procitana=0, tip_prijave='C', id_prijavljene_stvari=self.article.id_clanka)
        redirect_url = self.live_server_url + reverse('index')
        self.login(redirect_url=redirect_url, username='testuser', password='testpassword')
        inbox_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'inbox_link'))
        )
        inbox_btn.click()
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(self.app_url + reverse('notifications'))
        )
        title_text = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'title_text'))
        )
        self.assertTrue(title_text.is_displayed())
        msg_row = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'row_' + str(msg.id_poruke)))
        )
        self.assertTrue(msg_row.is_displayed())
        
        first_child = msg_row.find_element(By.CSS_SELECTOR, ':first-child')
        
        style_value = self.browser.execute_script(
            "return window.getComputedStyle(arguments[0]).getPropertyValue(arguments[1]);",
            first_child,
            'background-color'
        )
        self.assertNotEqual(style_value, 'rgb(221, 221, 221)')
        
        open_link =msg_row.find_element(By.CSS_SELECTOR, ':nth-child(4) a')
        open_link.click()
        
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(self.live_server_url + reverse('one_message_view', args=[msg.id_poruke]))
        )
        title_text = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'title_text'))
        )
        self.assertTrue(title_text.is_displayed())
        is_read = PrimljenePoruke.objects.get(id_primljena_poruka=received_msg.id_primljena_poruka).procitana
        self.assertEqual(is_read, 1)
        
        return_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'return_button'))
        )
        return_btn.click()
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(self.live_server_url + reverse('notifications'))
        )
        
        title_text = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'title_text'))
        )
        self.assertTrue(title_text.is_displayed())
        msg_row = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'row_' + str(msg.id_poruke)))
        )
        self.assertTrue(msg_row.is_displayed())
        
        first_child = msg_row.find_element(By.CSS_SELECTOR, ':first-child')
        
        style_value = self.browser.execute_script(
            "return window.getComputedStyle(arguments[0]).getPropertyValue(arguments[1]);",
            first_child,
            'background-color'
        )
        self.assertEqual(style_value, 'rgb(221, 221, 221)')
        
    def test_delete_notification(self):
        msg = Poruka.objects.create(tekst='test poruke')
        received_msg = PrimljenePoruke.objects.create(id_poruke=msg, id_korisnika=self.user, procitana=0, tip_prijave='C', id_prijavljene_stvari=self.article.id_clanka)
        redirect_url = self.live_server_url + reverse('index')
        self.login(redirect_url=redirect_url, username='testuser', password='testpassword')
        inbox_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'inbox_link'))
        )
        inbox_btn.click()
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(self.app_url + reverse('notifications'))
        )
        title_text = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'title_text'))
        )
        self.assertTrue(title_text.is_displayed())
        msg_row = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'row_' + str(msg.id_poruke)))
        )
        self.assertTrue(msg_row.is_displayed())
        
        first_child = msg_row.find_element(By.CSS_SELECTOR, ':first-child')
        
        style_value = self.browser.execute_script(
            "return window.getComputedStyle(arguments[0]).getPropertyValue(arguments[1]);",
            first_child,
            'background-color'
        )
        self.assertNotEqual(style_value, 'rgb(221, 221, 221)')
        
        delete_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'delete_btn_' + str(msg.id_poruke)))
        )
        delete_btn.click()
        
        WebDriverWait(self.browser, 10).until(EC.alert_is_present())

        alert = self.browser.switch_to.alert
        alert.accept()
        
        msg_row = WebDriverWait(self.browser, 10).until(
            EC.invisibility_of_element_located((By.ID, 'row_' + str(msg.id_poruke)))
        )
        
        inDB = PrimljenePoruke.objects.filter(id_primljena_poruka=received_msg.id_primljena_poruka).exists()
        self.assertFalse(inDB)
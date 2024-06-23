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


class TestIndexView(StaticLiveServerTestCase):
    
    def login(self, redirect_url, username, password):
        self.client.login(username=username, password=password)
        
        # Kopiramo django kolacice u selenium browser
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
        self.app_url = self.live_server_url + reverse('index')
        self.user = Korisnik.objects.create_user(username='testuser', password='testpassword', tip="R")
        self.num_of_articles = 10
        
        for i in range(self.num_of_articles):
            article = Clanak.objects.create(
                id_autora=self.user,
                broj_ocena=5,
                zbir_ocena=5*(i+1), 
                sadrzaj=f'Test Article {i} Content',
            )
            PticaTabela.objects.create(
                id_clanka=article,
                vrsta=f'Test Article {i}',
            )
        
    def tearDown(self):
        self.browser.close()
        PticaTabela.objects.all().delete()
        Clanak.objects.all().delete()
        self.user.delete()
        
    def test_index_initial(self):
        self.browser.get(self.app_url)
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(self.app_url)
        )
        index_container = self.browser.find_element(By.ID, 'container-article-brief')
        child_count = self.browser.execute_script("return arguments[0].children.length;", index_container)
        self.assertEqual(child_count, 4)
        

    def test_load_more_once(self):
        self.browser.get(self.app_url)
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(self.app_url)
        )
        index_container = self.browser.find_element(By.ID, 'container-article-brief')
        child_count = self.browser.execute_script("return arguments[0].children.length;", index_container)
        self.assertEqual(child_count, 4)

        load_more_button = self.browser.find_element(By.ID, 'load_more_button')
        self.browser.execute_script("arguments[0].scrollIntoView();", load_more_button)
        load_more_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.ID, 'load_more_button'))
        )
        
        self.browser.execute_script("arguments[0].click();", load_more_button)
        
        def child_count_updated(driver):
            return driver.execute_script("return arguments[0].children.length;", index_container) == 8

        WebDriverWait(self.browser, 10).until(child_count_updated)
        
        index_container = self.browser.find_element(By.ID, 'container-article-brief')
        child_count = self.browser.execute_script("return arguments[0].children.length;", index_container)
        self.assertEqual(child_count, 8)
        
    def test_load_more_max(self):
        self.browser.get(self.app_url)
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(self.app_url)
        )
        index_container = self.browser.find_element(By.ID, 'container-article-brief')
        child_count = self.browser.execute_script("return arguments[0].children.length;", index_container)
        self.assertEqual(child_count, 4)

        load_more_button = self.browser.find_element(By.ID, 'load_more_button')
        self.browser.execute_script("arguments[0].scrollIntoView();", load_more_button)
        load_more_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.ID, 'load_more_button'))
        )
        
        self.browser.execute_script("arguments[0].click();", load_more_button)
        
        def child_count_8(driver):
            return driver.execute_script("return arguments[0].children.length;", index_container) == 8

        WebDriverWait(self.browser, 10).until(child_count_8)
        
        index_container = self.browser.find_element(By.ID, 'container-article-brief')
        child_count = self.browser.execute_script("return arguments[0].children.length;", index_container)
        self.assertEqual(child_count, 8)
        
        load_more_button = self.browser.find_element(By.ID, 'load_more_button')
        self.browser.execute_script("arguments[0].scrollIntoView();", load_more_button)
        load_more_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.ID, 'load_more_button'))
        )
        
        self.browser.execute_script("arguments[0].click();", load_more_button)
        
        def child_count_10(driver):
            return driver.execute_script("return arguments[0].children.length;", index_container) == 10

        WebDriverWait(self.browser, 10).until(child_count_10)
        
        index_container = self.browser.find_element(By.ID, 'container-article-brief')
        child_count = self.browser.execute_script("return arguments[0].children.length;", index_container)
        self.assertEqual(child_count, 10)
        
        load_more_button = WebDriverWait(self.browser, 10).until(
            EC.invisibility_of_element_located((By.ID, 'load_more_button'))
        )
        
    def test_index_open_article(self):
        self.browser.get(self.app_url)
        article_id = Clanak.objects.order_by('-id_clanka').first().id_clanka
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(self.app_url)
        )
        index_container = self.browser.find_element(By.ID, 'container-article-brief')
        link_to_article = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Detaljnije"))
        )
        link_to_article.click()
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be(self.live_server_url + reverse('show_article', args=[article_id]))
        )
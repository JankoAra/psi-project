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

from slobodna_enciklopedija_ptica_srbije.models import Korisnik


class TestDeleteProfileSelenium(StaticLiveServerTestCase):

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
        self.user_to_delete1 = Korisnik.objects.create_user(username='testuser1', password='odiseja123', tip="R")
        self.user_to_delete2 = Korisnik.objects.create_user(username='testuser2', password='odiseja123', tip="R")
        self.user_to_delete3 = Korisnik.objects.create_user(username='testuser3', password='odiseja123', tip="R")
        self.user_to_delete4 = Korisnik.objects.create_user(username='testuser4', password='odiseja123', tip="R")
        self.user_to_delete5 = Korisnik.objects.create_user(username='testuser5', password='odiseja123', tip="R")
        self.user_to_delete6 = Korisnik.objects.create_user(username='testuser6', password='odiseja123', tip="R")
        self.user_to_delete7 = Korisnik.objects.create_user(username='testuser7', password='odiseja123', tip="R")
        self.user_to_delete8 = Korisnik.objects.create_user(username='testuser8', password='odiseja123', tip="R")
        self.user_to_delete9 = Korisnik.objects.create_user(username='testuser9', password='odiseja123', tip="R")
        self.user_to_delete10 = Korisnik.objects.create_user(username='testuser10', password='odiseja123', tip="R")
        self.user_to_delete11 = Korisnik.objects.create_user(username='testuser11', password='odiseja123', tip="R")
        self.user_to_delete12 = Korisnik.objects.create_user(username='testuser12', password='odiseja123', tip="R")
        self.user_to_delete13 = Korisnik.objects.create_user(username='testuser13', password='odiseja123', tip="R")
        self.user_to_delete14 = Korisnik.objects.create_user(username='testuser14', password='odiseja123', tip="R")
        self.user_to_delete15 = Korisnik.objects.create_user(username='testuser15', password='odiseja123', tip="R")



    def tearDown(self):
        self.browser.close()
        self.admin.delete()
        self.user_to_delete1.delete()
        self.user_to_delete2.delete()
        self.user_to_delete3.delete()
        self.user_to_delete4.delete()
        self.user_to_delete5.delete()
        self.user_to_delete6.delete()
        self.user_to_delete7.delete()
        self.user_to_delete8.delete()
        self.user_to_delete9.delete()
        self.user_to_delete10.delete()
        self.user_to_delete11.delete()
        self.user_to_delete12.delete()
        self.user_to_delete13.delete()
        self.user_to_delete14.delete()
        self.user_to_delete15.delete()


    def test_admin_deletes_user_accept(self):
        self.login(self.browser, self.app_url, self.admin.username, "odiseja123")
        self.browser.get(self.app_url + reverse('user_deletion'))
        self.browser.implicitly_wait(10)
        username_to_search = "testuser7"
        search_input = self.browser.find_element(By.ID, "searchInput")
        search_input.send_keys("testuser7")
        search_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Pretraga')]")
        search_button.click()
        time.sleep(3)

        last_user_row = self.browser.find_element(By.XPATH, f"//tr[./td[contains(text(), '{username_to_search}')]]")

        WebDriverWait(self.browser, 30).until(
            EC.visibility_of(last_user_row)
        )

        delete_user_btn = WebDriverWait(last_user_row, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".dugme-brisanja"))
        )
        delete_user_btn.click()
        alert = WebDriverWait(self.browser, 30).until(EC.alert_is_present())
        time.sleep(3)
        alert.accept()
        time.sleep(3)
        #WebDriverWait(self.browser, 30).until_not(
        #    EC.staleness_of(last_user_row)
        #)

        self.user_to_delete7 = Korisnik.objects.get(id=self.user_to_delete7.id)
        self.assertFalse(self.user_to_delete7.is_active)

    def test_admin_deletes_user_accept_byID(self):
        self.login(self.browser, self.app_url, self.admin.username, "odiseja123")
        self.browser.get(self.app_url + reverse('user_deletion'))
        self.browser.implicitly_wait(10)
        id_to_search = self.user_to_delete12.id
        search_input = self.browser.find_element(By.ID, "searchInput")
        search_input.send_keys(str(id_to_search))
        search_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Pretraga')]")
        search_button.click()
        time.sleep(3)

        last_user_row = self.browser.find_element(By.XPATH, f"//tr[./td[contains(text(), '{id_to_search}')]]")

        WebDriverWait(self.browser, 30).until(
            EC.visibility_of(last_user_row)
        )

        delete_user_btn = WebDriverWait(last_user_row, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".dugme-brisanja"))
        )
        delete_user_btn.click()
        alert = WebDriverWait(self.browser, 30).until(EC.alert_is_present())
        time.sleep(3)
        alert.accept()
        #WebDriverWait(self.browser, 30).until_not(
        #    EC.staleness_of(last_user_row)
        #)
        time.sleep(3)
        self.user_to_delete12 = Korisnik.objects.get(id=self.user_to_delete12.id)
        self.assertFalse(self.user_to_delete12.is_active)


    def test_admin_deletes_user_dismiss(self):
        self.login(self.browser, self.app_url, self.admin.username, "odiseja123")
        self.browser.get(self.app_url + reverse('user_deletion'))
        self.browser.implicitly_wait(10)
        time.sleep(3)

        last_user = self.browser.find_elements(By.CSS_SELECTOR, "#tabela-korisnika tr")[-1]

        actions = ActionChains(self.browser)
        actions.scroll_to_element(last_user).perform()
        WebDriverWait(self.browser, 30).until(
            EC.visibility_of(last_user)
        )

        delete_user_btn = WebDriverWait(self.browser, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#tabela-korisnika tr:last-child .dugme-brisanja"))
        )
        delete_user_btn.click()
        alert = WebDriverWait(self.browser, 30).until(EC.alert_is_present())
        time.sleep(3)
        alert.dismiss()
        WebDriverWait(self.browser, 30).until_not(
            EC.staleness_of(last_user)
        )
        time.sleep(3)
        self.user_to_delete15 = Korisnik.objects.get(id=self.user_to_delete15.id)
        self.assertTrue(self.user_to_delete15.is_active)




# Autor: Anđela Ćirić 2021/0066

import json
from django.test import TestCase, Client
from django.urls import reverse
from django.test.client import RequestFactory

from django.utils import timezone

from slobodna_enciklopedija_ptica_srbije.models import *
import os


class TestChangeArticleContentTestCase(TestCase):



    def setUp(self):
        self.client = Client()
        self.editor = Korisnik.objects.create_user(username='uredniktest', password='odiseja123', tip="U")
        self.editor2 = Korisnik.objects.create_user(username='uredniktest2', password='odiseja123', tip="U")
        self.admin = Korisnik.objects.create_user(username='admintest', password='odiseja123', tip="A")
        self.registered = Korisnik.objects.create_user(username='regtest', password='odiseja123', tip="R")
        article1 = Clanak()
        article1.id_autora = self.editor
        article1.sadrzaj = "Test sadrzaj 1 jesam autor"
        article1.save()
        image_data = open(os.path.abspath("./test_data/owl.jpg"), "rb").read()
        table1 = PticaTabela()
        table1.id_clanka = article1
        table1.vrsta = "V1 test"
        table1.carstvo = "C1 test"
        table1.klasa = "K1 test"
        table1.porodica = "P1 test"
        table1.red = "R1 test"
        table1.rod = "R11 test"
        table1.slika_vrste = image_data
        table1.status_ugrozenosti = "N1 test"
        table1.tezina = 10
        table1.velicina = 10
        table1.tip = "T1 test"
        table1.save()
        self.table1 = table1
        self.article1 = article1


    def tearDown(self):
        self.registered.delete()
        self.table1.delete()
        self.article1.delete()
        self.editor.delete()
        self.editor2.delete()
        self.admin.delete()



    def test_modify_content_by_editor(self):
        response = self.client.post(reverse("user_login"),data={"username": self.editor.username, "password": "odiseja123"})
        response = self.client.post(reverse("change_article_text"),
                                    data=json.dumps({'article_id': self.article1.id_clanka, 'new_text':"Novi sadržaj"}),
                                    content_type='application/json', follow=True)
        json_response = response.json()
        self.assertTrue(json_response['success'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Clanak.objects.get(id_clanka=self.article1.id_clanka).sadrzaj, "Novi sadržaj")

    def test_modify_content_by_admin(self):
        response = self.client.post(reverse("user_login"),data={"username": self.admin.username, "password": "odiseja123"})
        response = self.client.post(reverse("change_article_text"),
                                    data=json.dumps({'article_id': self.article1.id_clanka, 'new_text':"Novi sadržaj 2"}),
                                    content_type='application/json', follow=True)
        json_response = response.json()
        self.assertTrue(json_response['success'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Clanak.objects.get(id_clanka=self.article1.id_clanka).sadrzaj, "Novi sadržaj 2")


    def test_modify_content_by_noneditor_registered_user(self):
        response = self.client.post(reverse("user_login"),data={"username": self.registered.username, "password": "odiseja123"})
        response = self.client.post(reverse("change_article_text"),
                                    data=json.dumps({'article_id': self.article1.id_clanka, 'new_text':"Novi sadržaj 3"}),
                                    content_type='application/json')
        self.assertEqual(response.url, "/")
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(Clanak.objects.get(id_clanka=self.article1.id_clanka).sadrzaj, "Novi sadržaj 3")


    def test_modify_content_by_noneditor_another_editor(self):
        response = self.client.post(reverse("user_login"),
                                    data={"username": self.editor2.username, "password": "odiseja123"})
        response = self.client.post(reverse("change_article_text"),
                                    data=json.dumps({'article_id': self.article1.id_clanka, 'new_text': "Novi sadržaj 3"}),
                                    content_type='application/json', follow=True)
        json_response = response.json()
        self.assertFalse(json_response['success'])
        self.assertEqual(json_response['error'], "Niste autor clanka")
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(Clanak.objects.get(id_clanka=self.article1.id_clanka).sadrzaj, "Novi sadržaj 3")

    def test_modify_content_on_nonexisting_article(self):
        response = self.client.post(reverse("user_login"),data={"username": self.editor.username, "password": "odiseja123"})
        response = self.client.post(reverse("change_article_text"),
                                    data=json.dumps({'article_id': None, 'new_text':"Novi sadržaj 3"}),
                                    content_type='application/json', follow=True)
        json_response = response.json()
        self.assertFalse(json_response['success'])
        self.assertEqual(json_response['error'], 'Clanak ne postoji')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(Clanak.objects.get(id_clanka=self.article1.id_clanka).sadrzaj, "Novi sadržaj 3")


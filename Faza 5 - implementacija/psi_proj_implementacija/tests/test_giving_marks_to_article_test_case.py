# Autor: Anđela Ćirić 2021/0066

import json
from django.test import TestCase, Client
from django.urls import reverse

from django.utils import timezone

from slobodna_enciklopedija_ptica_srbije.models import *
import os


class TestMarksTestCase(TestCase):


    def setUp(self):
        self.client = Client()
        self.editor = Korisnik.objects.create_user(username='uredniktest', password='odiseja123', tip="U")
        self.admin = Korisnik.objects.create_user(username='admintest', password='odiseja123', tip="A")
        self.registered = Korisnik.objects.create_user(username='regtest', password='odiseja123', tip="R")
        article1 = Clanak()
        article1.id_autora = self.editor
        article1.sadrzaj = "Test sadrzaj 1"
        article1.save()
        article2 = Clanak()
        article2.id_autora = self.admin
        article2.sadrzaj = "Test sadrzaj 2"
        article2.save()

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
        table2 = PticaTabela()
        table2.id_clanka = article2
        table2.vrsta = "V2 test"
        table2.carstvo = "C2 test"
        table2.klasa = "K2 test"
        table2.porodica = "P2 test"
        table2.red = "R2 test"
        table2.rod = "R21 test"
        table2.slika_vrste = image_data
        table2.status_ugrozenosti = "N2 test"
        table2.tezina = 20
        table2.velicina = 20

        table1.save()
        table2.save()

        self.table1 = table1
        self.table2 = table2
        self.article1 = article1
        self.article2 = article2

        self.ocena = None

    def tearDown(self):
        if(self.ocena != None):
            self.ocena.delete()
        self.table1.delete()
        self.table2.delete()
        self.article1.delete()
        self.article2.delete()
        self.editor.delete()
        self.admin.delete()
        self.registered.delete()

    def test_admin_alters_rating(self):
        response = self.client.post(reverse("user_login"),data={"username": self.admin.username, "password": "odiseja123"})

        response = self.client.post(reverse("alter_rating"),  data=json.dumps({'article_id': self.article1.id_clanka, 'grade':10}), content_type='application/json')
        json_response = response.json()
        self.assertTrue(json_response['success'])
        self.assertEqual(response.status_code, 200)
        article = Clanak.objects.get(id_clanka=self.article1.id_clanka)
        self.ocena = Ocena.objects.latest("id_ocene")
        self.assertEqual(json_response["avg_rating"]*article.broj_ocena, article.zbir_ocena)

    def test_non_loged_user(self):
        response = self.client.post(reverse("alter_rating"),  data=json.dumps({'article_id': self.article1.id_clanka, 'grade':10}), content_type='application/json')

        self.assertTrue(response.url.startswith('/prijava/'))
        self.assertEqual(response.status_code, 302)

    def test_logged_user_alter_ratings_nonexisting_article(self):
        response = self.client.post(reverse("user_login"),data={"username": self.registered.username, "password": "odiseja123"})

        response = self.client.post(reverse("alter_rating"),data=json.dumps({ 'grade': 10}),content_type='application/json')
        #print(response)
        json_response = response.json()
        self.assertFalse(json_response['success'])
        self.assertEqual(json_response['error'], "Clanak ne postoji")

    def test_logged_user_alter_ratings_small_mark(self):
        response = self.client.post(reverse("user_login"),data={"username": self.registered.username, "password": "odiseja123"})
        response = self.client.post(reverse("alter_rating"),data=json.dumps({'article_id': self.article1.id_clanka, 'grade':-1}),content_type='application/json')
        json_response = response.json()
        self.assertFalse(json_response['success'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['error'], 'Ocena mora biti izmedju 1 i 10')

    def test_logged_user_alter_ratings_big_mark(self):
        response = self.client.post(reverse("user_login"),data={"username": self.registered.username, "password": "odiseja123"})
        response = self.client.post(reverse("alter_rating"),data=json.dumps({'article_id': self.article1.id_clanka, 'grade':13}),content_type='application/json')
        json_response = response.json()
        self.assertFalse(json_response['success'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['error'], 'Ocena mora biti izmedju 1 i 10')



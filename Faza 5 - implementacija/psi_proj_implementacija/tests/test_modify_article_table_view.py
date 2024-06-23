#Autor: Srdjan Lucic 260/2021
import os

from django.test import TestCase, Client
from django.urls import reverse
from slobodna_enciklopedija_ptica_srbije.models import *

from .utilities import initialize_content_ls210260, delete_content_ls210260d

class TestModifyArticleTableView(TestCase):
    def setUp(self):
        initialize_content_ls210260(self)
        self.client = Client()

    def tearDown(self):
        delete_content_ls210260d(self)

    def test_get(self):
        response = self.client.get(reverse('change_article_table'))
        self.assertEqual(response.status_code, 302)

    def test_admin_vrsta_change(self):
        self.client.login(username = 'srdjanA', password='srkiLozinka2')
        article_id = self.article_2.id_clanka
        response = self.client.post(
            reverse('change_article_table'),
            data={ 'article_id': article_id, 'vrsta': 'vrsta', 'rod': '', 'porodica': '', 'red': '', 'klasa': '', 'tip': '',
                   'carstvo': '', 'tezina': '', 'velicina': '', 'status': ''
            },
            content_type = 'application/json'
        )
        self.assertEqual(response.content.decode(),'{"success": true}')
        self.assertEqual(PticaTabela.objects.get(id_clanka=self.article_2).vrsta, 'vrsta')

    def test_admin_rod_change(self):
        self.client.login(username = 'srdjanA', password='srkiLozinka2')
        article_id = self.article_2.id_clanka
        response = self.client.post(
            reverse('change_article_table'),
            data={ 'article_id': article_id, 'vrsta': '', 'rod': 'vrsta', 'porodica': '', 'red': '', 'klasa': '', 'tip': '',
                   'carstvo': '', 'tezina': '', 'velicina': '', 'status': ''
            },
            content_type = 'application/json'
        )
        self.assertEqual(response.content.decode(),'{"success": true}')
        self.assertEqual(PticaTabela.objects.get(id_clanka=self.article_2).rod, 'vrsta')

    def test_admin_porodica_change(self):
        self.client.login(username = 'srdjanA', password='srkiLozinka2')
        article_id = self.article_2.id_clanka
        response = self.client.post(
            reverse('change_article_table'),
            data={ 'article_id': article_id, 'vrsta': '', 'rod': '', 'porodica': 'vrsta', 'red': '', 'klasa': '', 'tip': '',
                   'carstvo': '', 'tezina': '', 'velicina': '', 'status': ''
            },
            content_type = 'application/json'
        )
        self.assertEqual(response.content.decode(),'{"success": true}')
        self.assertEqual(PticaTabela.objects.get(id_clanka=self.article_2).porodica, 'vrsta')

    def test_admin_red_change(self):
        self.client.login(username = 'srdjanA', password='srkiLozinka2')
        article_id = self.article_2.id_clanka
        response = self.client.post(
            reverse('change_article_table'),
            data={ 'article_id': article_id, 'vrsta': '', 'rod': '', 'porodica': '', 'red': 'vrsta', 'klasa': '', 'tip': '',
                   'carstvo': '', 'tezina': '', 'velicina': '', 'status': ''
            },
            content_type = 'application/json'
        )
        self.assertEqual(response.content.decode(),'{"success": true}')
        self.assertEqual(PticaTabela.objects.get(id_clanka=self.article_2).red, 'vrsta')

    def test_admin_klasa_change(self):
        self.client.login(username = 'srdjanA', password='srkiLozinka2')
        article_id = self.article_2.id_clanka
        response = self.client.post(
            reverse('change_article_table'),
            data={ 'article_id': article_id, 'vrsta': '', 'rod': '', 'porodica': '', 'red': '', 'klasa': 'vrsta', 'tip': '',
                   'carstvo': '', 'tezina': '', 'velicina': '', 'status': ''
            },
            content_type = 'application/json'
        )
        self.assertEqual(response.content.decode(),'{"success": true}')
        self.assertEqual(PticaTabela.objects.get(id_clanka=self.article_2).klasa, 'vrsta')

    def test_admin_tip_change(self):
        self.client.login(username = 'srdjanA', password='srkiLozinka2')
        article_id = self.article_2.id_clanka
        response = self.client.post(
            reverse('change_article_table'),
            data={ 'article_id': article_id, 'vrsta': '', 'rod': '', 'porodica': '', 'red': '', 'klasa': '', 'tip': 'vrsta',
                   'carstvo': '', 'tezina': '', 'velicina': '', 'status': ''
            },
            content_type = 'application/json'
        )
        self.assertEqual(response.content.decode(),'{"success": true}')
        self.assertEqual(PticaTabela.objects.get(id_clanka=self.article_2).tip, 'vrsta')

    def test_admin_carstvo_change(self):
        self.client.login(username = 'srdjanA', password='srkiLozinka2')
        article_id = self.article_2.id_clanka
        response = self.client.post(
            reverse('change_article_table'),
            data={ 'article_id': article_id, 'vrsta': '', 'rod': '', 'porodica': '', 'red': '', 'klasa': '', 'tip': '',
                   'carstvo': 'vrsta', 'tezina': '', 'velicina': '', 'status': ''
            },
            content_type = 'application/json'
        )
        self.assertEqual(response.content.decode(),'{"success": true}')
        self.assertEqual(PticaTabela.objects.get(id_clanka=self.article_2).carstvo, 'vrsta')

    def test_admin_tezina_change(self):
        self.client.login(username = 'srdjanA', password='srkiLozinka2')
        article_id = self.article_2.id_clanka
        response = self.client.post(
            reverse('change_article_table'),
            data={ 'article_id': article_id, 'vrsta': '', 'rod': '', 'porodica': '', 'red': '', 'klasa': '', 'tip': '',
                   'carstvo': '', 'tezina': 0, 'velicina': '', 'status': ''
            },
            content_type = 'application/json'
        )
        self.assertEqual(response.content.decode(),'{"success": true}')
        self.assertEqual(PticaTabela.objects.get(id_clanka=self.article_2).tezina, 0)

    def test_admin_velicina_change(self):
        self.client.login(username = 'srdjanA', password='srkiLozinka2')
        article_id = self.article_2.id_clanka
        response = self.client.post(
            reverse('change_article_table'),
            data={ 'article_id': article_id, 'vrsta': '', 'rod': '', 'porodica': '', 'red': '', 'klasa': '', 'tip': '',
                   'carstvo': '', 'tezina': '', 'velicina': 0, 'status': ''
            },
            content_type = 'application/json'
        )
        self.assertEqual(response.content.decode(),'{"success": true}')
        self.assertEqual(PticaTabela.objects.get(id_clanka=self.article_2).velicina, 0)

    def test_admin_status_change(self):
        self.client.login(username = 'srdjanA', password='srkiLozinka2')
        article_id = self.article_2.id_clanka
        response = self.client.post(
            reverse('change_article_table'),
            data={ 'article_id': article_id, 'vrsta': '', 'rod': '', 'porodica': '', 'red': '', 'klasa': '', 'tip': '',
                   'carstvo': '', 'tezina': '', 'velicina': '', 'status': 'vrsta'
            },
            content_type = 'application/json'
        )
        self.assertEqual(response.content.decode(),'{"success": true}')
        self.assertEqual(PticaTabela.objects.get(id_clanka=self.article_2).status_ugrozenosti, 'vrsta')

    def test_urednik_status_change(self):
        self.client.login(username='srdjanU', password='srkiLozinka1')
        article_id = self.article_1.id_clanka
        response = self.client.post(
            reverse('change_article_table'),
            data={'article_id': article_id, 'vrsta': '', 'rod': '', 'porodica': '', 'red': '', 'klasa': '', 'tip': '',
                  'carstvo': '', 'tezina': '', 'velicina': '', 'status': 'vrsta'
                  },
            content_type='application/json'
        )
        self.assertEqual(response.content.decode(), '{"success": true}')
        self.assertEqual(PticaTabela.objects.get(id_clanka=self.article_1).status_ugrozenosti, 'vrsta')


    def test_urednik_not_author_status_change(self):
        self.client.login(username='srdjanU', password='srkiLozinka1')
        article_id = self.article_2.id_clanka
        old_status = PticaTabela.objects.get(id_clanka=self.article_2).status_ugrozenosti
        response = self.client.post(
            reverse('change_article_table'),
            data={'article_id': article_id, 'vrsta': '', 'rod': '', 'porodica': '', 'red': '', 'klasa': '', 'tip': '',
                  'carstvo': '', 'tezina': '', 'velicina': '', 'status': 'vrsta'
                  },
            content_type='application/json'
        )
        self.assertEqual(response.content.decode(), '{"success": false, "error": "Niste autor clanka"}')
        self.assertEqual(PticaTabela.objects.get(id_clanka=self.article_2).status_ugrozenosti, old_status)

    def test_admin_no_id(self):
        self.client.login(username='srdjanA', password='srkiLozinka2')
        article_id = None
        response = self.client.post(
            reverse('change_article_table'),
            data={'article_id': article_id, 'vrsta': '', 'rod': '', 'porodica': '', 'red': '', 'klasa': '', 'tip': '',
                  'carstvo': '', 'tezina': '', 'velicina': '', 'status': 'vrsta'
                  },
            content_type='application/json'
        )
        self.assertEqual(response.content.decode(), '{"success": false, "error": "Clanak ne postoji"}')

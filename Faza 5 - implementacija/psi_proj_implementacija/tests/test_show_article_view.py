# Autor testa: Jaroslav Veseli 2021/0480

from django.test import TestCase, Client
from django.urls import reverse

from .utilities import initialize_data_vj210480, delete_data_vj210480


class TestShowArticleView(TestCase):
    def setUp(self):
        self.client = Client()
        initialize_data_vj210480(self)
    
    def tearDown(self):
        delete_data_vj210480(self)

    def test_show_article_success(self):
        # Obzirom da clanak postoji, ocekujem da mi vrati status kod 200.
        response = self.client.get(reverse("show_article", args=[self.article_1.id_clanka]))
        self.assertEquals(response.status_code, 200)

    def test_show_article_fail(self):
        # Ako prosledim ID clanka koji ne postoji, zelim da me redirektuje backend na indeks.
        response = self.client.get(reverse("show_article", args=[1293784]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, "/")

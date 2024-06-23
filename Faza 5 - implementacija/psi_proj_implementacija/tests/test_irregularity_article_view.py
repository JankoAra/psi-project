# Autor testa: Jaroslav Veseli 2021/0480.

from django.test import TestCase, Client
from django.urls import reverse

from .utilities import initialize_data_vj210480, delete_data_vj210480


class TestIrregularityArticleView(TestCase):
    def setUp(self):
        self.client = Client()
        initialize_data_vj210480(self)
        
    def tearDown(self):
        delete_data_vj210480(self)

    def test_get(self):
        # Prelaizmo na get stranicu. Ocekujemo kod 200.
        response = self.client.post(reverse("user_login"), data = { "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.get(reverse("report_irregularity_article_get", args=[self.article_1.id_clanka]))
        self.assertEqual(response.status_code, 200)
        
    def test_page_success(self):
        # Obzirom da clanak postoji, ocekujemo success true poruku.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_article_page"), data={ "article": self.article_1.id_clanka }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": true}')
        
    def test_page_fail(self):
        # Obzirom da clanak ne postoji, ocekujemo success fail poruku.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_article_page"), data={ "article": None }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": false, "error": "Artikal ne postoji"}')
    
    def test_confirm_success(self): 
        # Obzirom da smo naveli i clanak koji postoji i razlog za prijavu ocekujemo success true.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_article_confirm"), data={ "id_article": self.article_1.id_clanka, "reason": "Nekakav razlog prijave." }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": true}')

    def test_confirm_unknown_article(self): 
        # Obzirom da smo naveli ID clanka koji ne postoji, ocekujemo success false.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_article_confirm"), data={ "id_article": 123412, "reason": "Nekakav razlog prijave." }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": false}')

    def test_confirm_without_article(self): 
        # Obzirom da nismo naveli id clanka, ocekujemo success false.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_article_confirm"), data={ "reason": "Nekakav razlog prijave." }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": false, "error": "Clanak ili razlog prijave nije naveden"}')
        
    def test_confirm_without_reason(self): 
        # Obzirom da nismo naveli razlog, ocekujemo false.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_article_confirm"), data={ "id_article": self.article_1.id_clanka }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": false, "error": "Clanak ili razlog prijave nije naveden"}')

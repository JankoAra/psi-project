# Autor testa: Jaroslav Veseli 2021/0480.
from django.test import TestCase, Client
from django.urls import reverse

from .utilities import initialize_data_vj210480, delete_data_vj210480


class TestIrregularityCommentView(TestCase):
    def setUp(self):
        self.client = Client()
        initialize_data_vj210480(self)
        
    def tearDown(self):
        delete_data_vj210480(self)
        
    def test_get(self):
        # Prelaizmo na get stranicu. Ocekujemo kod 200.
        response = self.client.post(reverse("user_login"), data = { "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.get(reverse("report_irregularity_comment_get", args=[self.comment.id_komentara]))
        self.assertEqual(response.status_code, 200)
    
    def test_page_success(self):
        # Obzirom da komentar postoji, ocekujemo success true poruku.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_comment_page"), data={ "idComm": self.comment.id_komentara }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": true}')

    def test_page_fail(self):
        # Obzirom da diskusija ne postoji, ocekujemo success false poruku.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_comment_page"), data={ "idComm": None }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": false, "error": "Komentar ne postoji"}')
    
    def test_confirm_success(self):
        # Obzirom da radimo prijavu za postojecu diskusiju, sa postojecim razlogom, od postojeceg korisnika, ocekujemo success poruku.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_comment_confirm"), data={ "idComm": self.comment.id_komentara, "reason": self.reason_comment_1.id_razlog_komentar, "username": "jaroslav_4" }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": true}')

    def test_confirm_fail_unknown_discussion(self):
        # Obzirom da pokusavamo da prijavimo diskusiju koja ne postoji, ocekujemo success fail.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_comment_confirm"), data={ "idComm": 12341234, "reason": self.reason_comment_1.id_razlog_komentar, "username": "jaroslav_4" }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": false, "error": "Niste dostavili sve podatke!"}')

    def test_confirm_fail_unknown_reason(self):
        # Obzirom da pokusavamo da prijavimo postojecu diskusiju sa ne postojecim razlogom, ocekujemo success fail.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_comment_confirm"), data={ "idComm": self.comment.id_komentara, "reason": 1234, "username": "jaroslav_4" }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": false, "error": "Niste dostavili sve podatke!"}')

    def test_confirm_fail_unknown_user(self):
        # Obzirom da pokusavamo da prijavimo postojecu diskusiju sa ne postojecim korisnikom, ocekujemo success fail.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_comment_confirm"), data={ "idComm": self.comment.id_komentara, "reason": self.reason_comment_1.id_razlog_komentar, "username": "neko_nasumicno_ime" }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": false, "error": "Niste dostavili sve podatke!"}')

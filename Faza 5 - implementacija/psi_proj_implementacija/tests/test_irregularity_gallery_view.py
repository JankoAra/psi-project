# Autor testa: Jaroslav Veseli 2021/0480.
from django.test import TestCase, Client
from django.urls import reverse

from .utilities import initialize_data_vj210480, delete_data_vj210480


class TestIrregularityGalleryView(TestCase):
    def setUp(self):
        self.client = Client()
        initialize_data_vj210480(self)

    def tearDown(self):
        delete_data_vj210480(self)
    
    def test_get(self):
        # Prelazimo na get stranicu. Ocekujemo kod 200.
        response = self.client.post(reverse("user_login"), data = { "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.get(reverse("report_irregularity_photograph_get", args=[self.gallery_image.id_fotografije]))
        self.assertEqual(response.status_code, 200)
    
    def test_page_success(self):
        # Obzirom da slika postoji, ocekujemo success true poruku.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_photogrpah_page"), data={ "imageId": self.gallery_image.id_fotografije }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": true}')

    def test_page_fail(self):
        # Obzirom da slika ne postoji, ocekujemo success false poruku.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_photogrpah_page"), data={ "imageId": None }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": false, "error": "Fotografija ne postoji"}')
        
    def test_confirm_success(self):
        # Obzirom da slika postoji, ocekujemo success poruku.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_photograph_confirm"), data={ "imageId": self.gallery_image.id_fotografije, "reason": self.reason_image_1.id_razlog_fotografija, "username": "jaroslav_4" }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": true}')

    def test_confirm_fail_unknown_image(self):
        # Obzirom da slika ne postoji, ocekujemo success fail poruku.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_photograph_confirm"), data={ "imageId": 12341234, "reason": self.reason_image_1.id_razlog_fotografija, "username": "jaroslav_4" }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": false, "error": "Fotografija ili razlog ili korisnicko ime ne postoji"}')

    def test_confirm_fail_unknown_reason(self):
        # Obzirom da slika postoji, ali razlog ne, ocekujemo success fail poruku.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_photograph_confirm"), data={ "imageId": self.gallery_image.id_fotografije, "reason": 12341324, "username": "jaroslav_4" }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": false, "error": "Fotografija ili razlog ili korisnicko ime ne postoji"}')

    def test_confirm_fail_unknown_user(self):
        # Obzirom da slika postoji, ali korisnik ne, ocekujemo success fail poruku.
        response = self.client.post(reverse("user_login"), data={ "username": "jaroslav_4", "password": "WhoKnows455@" })
        response = self.client.post(reverse("report_irregularity_photograph_confirm"), data={ "imageId": self.gallery_image.id_fotografije, "reason": self.reason_image_1.id_razlog_fotografija, "username": "someone_unknown" }, content_type="application/json")
        self.assertEquals(response.content.decode(), '{"success": false, "error": "Fotografija ili razlog ili korisnicko ime ne postoji"}')

# Autor testa: Jaroslav Veseli 2021/0480

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

import os

from .utilities import initialize_data_vj210480, delete_data_vj210480

class TestChangeTableImageView(TestCase):
    def setUp(self):
        self.client = Client()
        initialize_data_vj210480(self)
    
    def tearDown(self):
        delete_data_vj210480(self)
        
    def test_success(self):
        # Login pre bilo kakve izmene.
        response = self.client.post(reverse("user_login"), data = { "username": "jaroslav_1", "password": "WhoKnows455@" })
        
        # Pokusaj pozivanja endpoint-a.
        response = self.client.post(reverse("change_table_image"), data = {
            "article_id": self.article_1.id_clanka,
            "image": SimpleUploadedFile("owl.jpg", open(os.path.abspath("./test_data/owl.jpg"), "rb").read())
        })
        
        # Ako je uspesno, ocekujem da ce se desiti redirect.
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f"/pregled_clanka/{self.article_1.id_clanka}")
    
    def test_image_article_not_found(self):
        # Login pre bilo kakve izmene.
        response = self.client.post(reverse("user_login"), data = { "username": "jaroslav_1", "password": "WhoKnows455@" })
        
        # Pokusaj pozivanja endpoint-a za clanak koji ne postoji.
        response = self.client.post(reverse("change_table_image"), data = {
            "article_id": 1927384,
            "image": SimpleUploadedFile("owl.jpg", open(os.path.abspath("./test_data/owl.jpg"), "rb").read())
        })

        # Obzirom da clanak za taj ID ne postoji, ocekujem da cu dobiti success false poruku.
        self.assertEquals(response.content.decode(), '{"success": false, "error": "Clanak ne postoji"}')
    
    def test_not_author(self):
        # Login pre bilo kakve izmene.
        response = self.client.post(reverse("user_login"), data = { "username": "jaroslav_1", "password": "WhoKnows455@" })
        
        # Pokusaj pozivanja endpoint-a.
        response = self.client.post(reverse("change_table_image"), data = {
            "article_id": self.article_2.id_clanka,
            "image": SimpleUploadedFile("owl.jpg", open(os.path.abspath("./test_data/owl.jpg"), "rb").read())
        })

        # Posto sam probao da radim izmenu sa naloga koji nije autor, ocekujem da failuje.
        self.assertEquals(response.content.decode(), '{"success": false, "error": "Niste autor clanka"}')

    def test_bad_file(self):
        # Login pre bilo kakve izmene.
        response = self.client.post(reverse("user_login"), data = { "username": "jaroslav_1", "password": "WhoKnows455@" })
        
        # Pokusaj pozivanja endpoint-a.
        response = self.client.post(reverse("change_table_image"), data = {
            "article_id": self.article_1.id_clanka,
            "image": SimpleUploadedFile("owl.jpg", open(os.path.abspath("./test_data/binary_file.bin"), "rb").read())
        })

        # Obzirom da sam pokusao da podmetnem binarni fajl. Ocekujem da budem redirektovan na stranicu clanka.
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f"/pregled_clanka/{self.article_1.id_clanka}") 

    def test_regular_user(self):
        response = self.client.post(reverse("user_login"), data = { "username": "jaroslav_4", "password": "WhoKnows455@" })
        
        # Pokusaj pozivanja endpoint-a.
        response = self.client.post(reverse("change_table_image"), data = {
            "article_id": self.article_1.id_clanka,
            "image": SimpleUploadedFile("owl.jpg", open(os.path.abspath("./test_data/owl.jpg"), "rb").read())
        })
        
        # Obzirom da pokusava ovoj funkcionalnosti da pristupi obican korisnik ocekujemo redirekciju na index.
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, "/")
        
    def test_admin_user(self):
        response = self.client.post(reverse("user_login"), data = { "username": "jaroslav_2", "password": "WhoKnows455@" })
        
        # Pokusaj pozivanja endpoint-a.
        response = self.client.post(reverse("change_table_image"), data = {
            "article_id": self.article_2.id_clanka,
            "image": SimpleUploadedFile("owl.jpg", open(os.path.abspath("./test_data/owl.jpg"), "rb").read())
        })
        
        # Ako je uspesno, ocekujem da ce se desiti redirect.
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, f"/pregled_clanka/{self.article_2.id_clanka}")

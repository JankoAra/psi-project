#Autor: Srdjan Lucic 260/2021

from django.test import TestCase, Client
from django.urls import reverse
from slobodna_enciklopedija_ptica_srbije.models import *


from .utilities import initialize_content_ls210260, delete_content_ls210260d

class TestDeleteCommentView(TestCase):
    def setUp(self):
        initialize_content_ls210260(self)
        self.client = Client()

    def tearDown(self):
        delete_content_ls210260d(self)

    def test_admin(self):
        comment_id = self.comment2.id_komentara
        self.client.login(username='srdjanA', password='srkiLozinka2')
        response = self.client.post(
            reverse('delete_comment'),
            data={'comment_id': comment_id},
            content_type="application/json"
        )
        self.assertEqual(response.content.decode(), '{"success": true}')
        try:
            Komentar.objects.get(id_komentara=comment_id)
            message = 'found'
        except Exception:
            message = 'deleted'
        self.assertEqual(message, 'deleted')


    def test_urednik(self):
        comment_id = self.comment2.id_komentara
        self.client.login(username='srdjanU', password='srkiLozinka1')
        response = self.client.post(
            reverse('delete_comment'),
            data={'comment_id': comment_id},
            content_type="application/json"
        )
        self.assertEqual(response.content.decode(), '{"success": true}')
        try:
            Komentar.objects.get(id_komentara=comment_id)
            message = 'found'
        except Exception:
            message = 'deleted'
        self.assertEqual(message, 'deleted')


    def test_urednik_no_id(self):
        comment_id = self.comment2.id_komentara
        self.client.login(username='srdjanU', password='srkiLozinka1')
        response = self.client.post(
            reverse('delete_comment'),
            data={'comment_id': None},
            content_type="application/json"
        )
        self.assertEqual(response.content.decode(), '{"success": false, "error": "Invalid data"}')


    def test_registrovani(self):
        comment_id = self.comment2.id_komentara
        self.client.login(username='srdjanR', password='srkiLozinka3')
        response = self.client.post(
            reverse('delete_comment'),
            data={'comment_id': comment_id},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 302)
        try:
            Komentar.objects.get(id_komentara=comment_id)
            message = 'found'
        except Exception:
            message = 'deleted'
        self.assertEqual(message, 'found')


    def test_neregistrovani(self):
        comment_id = self.comment2.id_komentara
        response = self.client.post(
            reverse('delete_comment'),
            data={'comment_id': comment_id},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 302)
        try:
            Komentar.objects.get(id_komentara=comment_id)
            message = 'found'
        except Exception as e:
            message = 'deleted'
            print(e)
        self.assertEqual(message, 'found')


    def test_get(self):
        response = self.client.get(reverse('delete_comment'))
        self.assertEqual(response.status_code, 302)
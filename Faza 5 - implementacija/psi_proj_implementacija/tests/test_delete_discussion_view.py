# Autor: Srdjan Lucic 260/2021

from django.test import TestCase, Client
from django.urls import reverse
from slobodna_enciklopedija_ptica_srbije.models import *


from .utilities import initialize_content_ls210260, delete_content_ls210260d

class TestDeleteDiscussionView(TestCase):
    def setUp(self):
        initialize_content_ls210260(self)
        self.client = Client()

    def tearDown(self):
        delete_content_ls210260d(self)

    def test_admin(self):
        discussion_id = self.discussion1.id_diskusije
        self.client.login(username='srdjanA', password='srkiLozinka2')
        response = self.client.post(
            reverse('delete_discussion'),
            data={'discussion_id': discussion_id},
            content_type="application/json"
        )
        self.assertEqual(response.content.decode(), '{"success": true}')
        try:
            Diskusija.objects.get(id_diskusije=discussion_id)
            message = 'found'
        except Exception:
            message = 'deleted'
        self.assertEqual(message, 'deleted')

    def test_admin_no_id(self):
        discussion_id = self.discussion1.id_diskusije
        self.client.login(username='srdjanA', password='srkiLozinka2')
        response = self.client.post(
            reverse('delete_discussion'),
            data={'discussion_id': None},
            content_type="application/json"
        )
        self.assertEqual(response.content.decode(), '{"success": false, "error": "Invalid data"}')


    def test_urednik(self):
        discussion_id = self.discussion2.id_diskusije
        self.client.login(username='srdjanU', password='srkiLozinka1')
        response = self.client.post(
            reverse('delete_discussion'),
            data={'discussion_id': discussion_id},
            content_type="application/json"
        )
        self.assertEqual(response.content.decode(), '{"success": true}')
        try:
            Diskusija.objects.get(id_diskusije=discussion_id)
            message = 'found'
        except Exception:
            message = 'deleted'
        self.assertEqual(message, 'deleted')


    def test_reg(self):
        discussion_id = self.discussion1.id_diskusije
        self.client.login(username='srdjanR', password='srkiLozinka3')
        response = self.client.post(
            reverse('delete_discussion'),
            data={'discussion_id': discussion_id},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 302)
        try:
            Diskusija.objects.get(id_diskusije=discussion_id)
            message = 'found'
        except Exception:
            message = 'deleted'
        self.assertEqual(message, 'found')


    def test_guest(self):
        discussion_id = self.discussion1.id_diskusije
        response = self.client.post(
            reverse('delete_discussion'),
            data={'discussion_id': discussion_id},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 302)
        try:
            Diskusija.objects.get(id_diskusije=discussion_id)
            message = 'found'
        except Exception:
            message = 'deleted'
        self.assertEqual(message, 'found')

    def test_get(self):
        discussion_id = self.discussion1.id_diskusije
        response = self.client.get(reverse('delete_discussion'))
        self.assertEqual(response.status_code, 302)
        try:
            Diskusija.objects.get(id_diskusije=discussion_id)
            message = 'found'
        except Exception:
            message = 'deleted'
        self.assertEqual(message, 'found')
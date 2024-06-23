#Autor: Srdjan Lucic 260/2021

from django.test import TestCase, Client
from django.urls import reverse
from slobodna_enciklopedija_ptica_srbije.models import *


from .utilities import initialize_content_ls210260, delete_content_ls210260d

class TestDeleteGalleryImageView(TestCase):
    def setUp(self):
        initialize_content_ls210260(self)
        self.client = Client()


    def tearDown(self):
        delete_content_ls210260d(self)


    def test_admin(self):
        image_id = self.gallery_image1.id_fotografije
        self.client.login(username='srdjanA', password='srkiLozinka2')
        response = self.client.post(
            reverse('delete_image_from_gallery', args=[image_id]),
            data={'username': '', 'userType': '', 'image_id':image_id},
            content_type="application/json"
        )
        self.assertEqual(response.content.decode(), '{"success": true}')
        try:
            FotografijaGalerija.objects.get(id_fotografije=image_id)
            message = 'found'
        except Exception:
            message = 'deleted'
        self.assertEqual(message, 'deleted')


    def test_urednik(self):
        image_id = self.gallery_image1.id_fotografije
        self.client.login(username='srdjanU', password='srkiLozinka1')
        response = self.client.post(
            reverse('delete_image_from_gallery', args=[image_id]),
            data={'username': '', 'userType': '', 'image_id':image_id},
            content_type="application/json"
        )
        self.assertEqual(response.content.decode(), '{"success": true}')
        try:
            FotografijaGalerija.objects.get(id_fotografije=image_id)
            message = 'found'
        except Exception:
            message = 'deleted'
        self.assertEqual(message, 'deleted')


    def test_registrovani_owner(self):
        image_id = self.gallery_image.id_fotografije
        self.client.login(username='srdjanR', password='srkiLozinka3')
        response = self.client.post(
            reverse('delete_image_from_gallery', args=[image_id]),
            data={'username': '', 'userType': '', 'image_id': image_id},
            content_type="application/json"
        )
        self.assertEqual(response.content.decode(), '{"success": true}')
        try:
            FotografijaGalerija.objects.get(id_fotografije=image_id)
            message = 'found'
        except Exception:
            message = 'deleted'
        self.assertEqual(message, 'deleted')

    def test_registrovani_not_the_owner(self):
        image_id = self.gallery_image1.id_fotografije
        self.client.login(username='srdjanR', password='srkiLozinka3')
        response = self.client.post(
            reverse('delete_image_from_gallery', args=[image_id]),
            data={'username': '', 'userType': '', 'image_id': image_id},
            content_type="application/json"
        )
        self.assertEqual(response.content.decode(), '{"success": false, "msg": "Niste autor slike"}')
        try:
            FotografijaGalerija.objects.get(id_fotografije=image_id)
            message = 'found'
        except Exception:
            message = 'deleted'
        self.assertEqual(message, 'found')

    def test_neregistrovani(self):
        image_id = self.gallery_image1.id_fotografije
        response = self.client.post(
            reverse('delete_image_from_gallery', args=[image_id]),
            data={'username': '', 'userType': '', 'image_id': image_id},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 302)
        try:
            FotografijaGalerija.objects.get(id_fotografije=image_id)
            message = 'found'
        except Exception:
            message = 'deleted'
        self.assertEqual(message, 'found')

    def test_get(self):
        image_id = self.gallery_image1.id_fotografije
        response = self.client.get(reverse('delete_image_from_gallery', args=[image_id]))
        self.assertEqual(response.status_code, 302)

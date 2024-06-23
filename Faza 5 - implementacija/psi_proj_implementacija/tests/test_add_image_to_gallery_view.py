#Autor: Srdjan Lucic 260/2021
import os

from django.test import TestCase, Client
from django.urls import reverse
from slobodna_enciklopedija_ptica_srbije.models import *

from .utilities import initialize_content_ls210260, delete_content_ls210260d


class TestAddImageToGalleryView(TestCase):

    def setUp(self):
        initialize_content_ls210260(self)
        self.client = Client()

    def tearDown(self):
        delete_content_ls210260d(self)


    def test_neregistrovani_get(self):
        article_id = self.article_2.id_clanka
        response = self.client.get(
            reverse('add_image_to_gallery'),
            data = {'article_id':article_id},
            content_type='text/plain'
        )
        self.assertEqual(response.status_code, 302)


    def test_registrovani_get(self):
        self.client.login(username='srdjanR', password='srkiLozinka3')
        article_id = self.article_2.id_clanka
        response = self.client.get(
            reverse('add_image_to_gallery'),
            data = {'article_id':article_id},
            content_type='text/plain'
        )
        self.assertTemplateUsed(
            response,
            'slobodna_enciklopedija_ptica_srbije/dodavanje_slike_u_galeriju.html'
        )


    def test_admin_get_no_data(self):
        self.client.login(username='srdjanA', password='srkiLozinka2')
        response = self.client.get(
            reverse('add_image_to_gallery'),
            content_type='text/plain'
        )
        self.assertEqual(response.status_code, 400)


    def test_put_success(self):
        self.client.login(username = 'srdjanR', password='srkiLozinka3')
        image_file = open(os.path.abspath('./test_data/patka.jpg'), "rb")
        article_id = self.article_1.id_clanka
        author_id = Korisnik.objects.get(username='srdjanR').id

        gallery_size = FotografijaGalerija.objects.filter(id_clanka=article_id).count()
        photos_of_this_author = FotografijaGalerija.objects.filter(id_autora=author_id).count()

        response = self.client.post(
            reverse('add_image_to_gallery'),
            data = {'image':image_file, 'article_id': article_id}
        )
        self.assertEqual(FotografijaGalerija.objects.filter(id_clanka=article_id).count(), gallery_size+1)
        self.assertEqual(FotografijaGalerija.objects.filter(id_autora=author_id).count(), photos_of_this_author+1)


    def test_put_no_image(self):
        self.client.login(username = 'srdjanR', password='srkiLozinka3')
        article_id = self.article_1.id_clanka
        author_id = Korisnik.objects.get(username='srdjanR').id

        gallery_size = FotografijaGalerija.objects.filter(id_clanka=article_id).count()
        photos_of_this_author = FotografijaGalerija.objects.filter(id_autora=author_id).count()

        response = self.client.post(
            reverse('add_image_to_gallery'),
            data = {'article_id': article_id}
        )
        self.assertEqual(FotografijaGalerija.objects.filter(id_clanka=article_id).count(), gallery_size)
        self.assertEqual(FotografijaGalerija.objects.filter(id_autora=author_id).count(), photos_of_this_author)
        self.assertEqual(response.status_code, 302)


    def test_put_wrong_format(self):
        self.client.login(username='srdjanR', password='srkiLozinka3')
        image_file = open(os.path.abspath('./test_data/patka.avif'), "rb")
        article_id = self.article_1.id_clanka
        author_id = Korisnik.objects.get(username='srdjanR').id

        gallery_size = FotografijaGalerija.objects.filter(id_clanka=article_id).count()
        photos_of_this_author = FotografijaGalerija.objects.filter(id_autora=author_id).count()

        response = self.client.post(
            reverse('add_image_to_gallery'),
            data={'image': image_file, 'article_id': article_id}
        )
        self.assertEqual(FotografijaGalerija.objects.filter(id_clanka=article_id).count(), gallery_size)
        self.assertEqual(FotografijaGalerija.objects.filter(id_autora=author_id).count(), photos_of_this_author)
        self.assertContains(response, 'Tip fajla mora biti .jpeg, .jpg ili .png', html=True)


    def test_put_give_up(self):
        self.client.login(username='srdjanR', password='srkiLozinka3')
        image_file = open(os.path.abspath('./test_data/patka.jpg'), "rb")
        article_id = self.article_1.id_clanka
        author_id = Korisnik.objects.get(username='srdjanR').id

        gallery_size = FotografijaGalerija.objects.filter(id_clanka=article_id).count()
        photos_of_this_author = FotografijaGalerija.objects.filter(id_autora=author_id).count()

        response = self.client.post(
            reverse('add_image_to_gallery'),
            data={'image': image_file, 'article_id': article_id, 'submit_type':"Poništi"}
        )
        self.assertEqual(FotografijaGalerija.objects.filter(id_clanka=article_id).count(), gallery_size)
        self.assertEqual(FotografijaGalerija.objects.filter(id_autora=author_id).count(), photos_of_this_author)
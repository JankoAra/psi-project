# Janko Arandjelovic 2021/0328

import json
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from django.utils import timezone

from slobodna_enciklopedija_ptica_srbije.models import Clanak, Korisnik, PticaTabela

class TestCreateArticleView(TestCase):
    def setUp(self):
        self.userA = Korisnik.objects.create_user(username='admin', password='admin', tip="A")
        self.userU = Korisnik.objects.create_user(username='urednik', password='urednik', tip="U")
        self.userR = Korisnik.objects.create_user(username='korisnik', password='korisnik', tip="R")
        
    def tearDown(self):
        PticaTabela.objects.all().delete()
        Clanak.objects.all().delete()
        Korisnik.objects.all().delete()
        
    def test_admin_access(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('create_article'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/kreiranje_clanka.html')

    def test_editor_access(self):
        self.client.login(username='urednik', password='urednik')
        response = self.client.get(reverse('create_article'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/kreiranje_clanka.html')

    def test_regular_user_access(self):
        self.client.login(username='korisnik', password='korisnik')
        response = self.client.get(reverse('create_article'))
        self.assertEqual(response.status_code, 302)
        
    def test_not_logged_in(self):
        response = self.client.get(reverse('create_article'))
        self.assertEqual(response.status_code, 302)
        
    def test_create_article_success(self):
        self.client.login(username='urednik', password='urednik')
        with open('slobodna_enciklopedija_ptica_srbije/static/images/logo.png', 'rb') as file:
            image_data = file.read()

        image = SimpleUploadedFile('logo.png', image_data)
        data = {
            'vrsta': 'vrsta test',
            'rod': 'rod test',
            'porodica': 'porodica test',
            'red': 'red test',
            'klasa': 'klasa test',
            'tip':'tip test',
            'carstvo': 'carstvo test',
            'tezina': 10,
            'velicina': 10,
            'status_ugrozenosti': 'status ugrozenosti test',
            'sadrzaj': 'sadrzaj test',
            'slika_vrste':image
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertEqual(response.status_code, 302)
        
        self.assertRedirects(response, reverse('show_article', args=[Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).first().id_clanka]))

        self.assertTrue(Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).exists())
        self.assertTrue(PticaTabela.objects.filter(vrsta='vrsta test').exists())
    
    def test_no_vrsta(self):
        self.client.login(username='urednik', password='urednik')
        with open('slobodna_enciklopedija_ptica_srbije/static/images/logo.png', 'rb') as file:
            image_data = file.read()

        image = SimpleUploadedFile('logo.png', image_data)
        data = {
            'vrsta': '',
            'rod': 'rod test',
            'porodica': 'porodica test',
            'red': 'red test',
            'klasa': 'klasa test',
            'tip':'tip test',
            'carstvo': 'carstvo test',
            'tezina': 10,
            'velicina': 10,
            'status_ugrozenosti': 'status ugrozenosti test',
            'sadrzaj': 'sadrzaj test',
            'slika_vrste':image
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/kreiranje_clanka.html')
        self.assertTrue('error_msg' in response.context)
        self.assertTrue(response.context['error_msg']=='Niste uneli polje za koju vrstu ptice želite da napravite članak.')
        self.assertFalse(Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).exists())
        
    def test_no_rod(self):
        self.client.login(username='urednik', password='urednik')
        with open('slobodna_enciklopedija_ptica_srbije/static/images/logo.png', 'rb') as file:
            image_data = file.read()

        image = SimpleUploadedFile('logo.png', image_data)
        data = {
            'vrsta': 'vrsta test',
            'rod': '',
            'porodica': 'porodica test',
            'red': 'red test',
            'klasa': 'klasa test',
            'tip':'tip test',
            'carstvo': 'carstvo test',
            'tezina': 10,
            'velicina': 10,
            'status_ugrozenosti': 'status ugrozenosti test',
            'sadrzaj': 'sadrzaj test',
            'slika_vrste':image
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_article', args=[Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).first().id_clanka]))

        self.assertTrue(Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).exists())
        self.assertTrue(PticaTabela.objects.filter(vrsta='vrsta test').exists())
        
    def test_no_porodica(self):
        self.client.login(username='urednik', password='urednik')
        with open('slobodna_enciklopedija_ptica_srbije/static/images/logo.png', 'rb') as file:
            image_data = file.read()

        image = SimpleUploadedFile('logo.png', image_data)
        data = {
            'vrsta': 'vrsta test',
            'rod': 'rod test',
            'porodica': '',
            'red': 'red test',
            'klasa': 'klasa test',
            'tip':'tip test',
            'carstvo': 'carstvo test',
            'tezina': 10,
            'velicina': 10,
            'status_ugrozenosti': 'status ugrozenosti test',
            'sadrzaj': 'sadrzaj test',
            'slika_vrste':image
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_article', args=[Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).first().id_clanka]))

        self.assertTrue(Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).exists())
        self.assertTrue(PticaTabela.objects.filter(vrsta='vrsta test').exists())
        
    def test_no_red(self):
        self.client.login(username='urednik', password='urednik')
        with open('slobodna_enciklopedija_ptica_srbije/static/images/logo.png', 'rb') as file:
            image_data = file.read()

        image = SimpleUploadedFile('logo.png', image_data)
        data = {
            'vrsta': 'vrsta test',
            'rod': 'rod test',
            'porodica': 'porodica test',
            'red': '',
            'klasa': 'klasa test',
            'tip':'tip test',
            'carstvo': 'carstvo test',
            'tezina': 10,
            'velicina': 10,
            'status_ugrozenosti': 'status ugrozenosti test',
            'sadrzaj': 'sadrzaj test',
            'slika_vrste':image
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_article', args=[Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).first().id_clanka]))

        self.assertTrue(Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).exists())
        self.assertTrue(PticaTabela.objects.filter(vrsta='vrsta test').exists())
        
    def test_no_klasa(self):
        self.client.login(username='urednik', password='urednik')
        with open('slobodna_enciklopedija_ptica_srbije/static/images/logo.png', 'rb') as file:
            image_data = file.read()

        image = SimpleUploadedFile('logo.png', image_data)
        data = {
            'vrsta': 'vrsta test',
            'rod': 'rod test',
            'porodica': 'porodica test',
            'red': 'red test',
            'klasa': '',
            'tip':'tip test',
            'carstvo': 'carstvo test',
            'tezina': 10,
            'velicina': 10,
            'status_ugrozenosti': 'status ugrozenosti test',
            'sadrzaj': 'sadrzaj test',
            'slika_vrste':image
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_article', args=[Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).first().id_clanka]))

        self.assertTrue(Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).exists())
        self.assertTrue(PticaTabela.objects.filter(vrsta='vrsta test').exists())
        
    def test_no_tip(self):
        self.client.login(username='urednik', password='urednik')
        with open('slobodna_enciklopedija_ptica_srbije/static/images/logo.png', 'rb') as file:
            image_data = file.read()

        image = SimpleUploadedFile('logo.png', image_data)
        data = {
            'vrsta': 'vrsta test',
            'rod': 'rod test',
            'porodica': 'porodica test',
            'red': 'red test',
            'klasa': 'klasa test',
            'tip':'',
            'carstvo': 'carstvo test',
            'tezina': 10,
            'velicina': 10,
            'status_ugrozenosti': 'status ugrozenosti test',
            'sadrzaj': 'sadrzaj test',
            'slika_vrste':image
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_article', args=[Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).first().id_clanka]))

        self.assertTrue(Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).exists())
        self.assertTrue(PticaTabela.objects.filter(vrsta='vrsta test').exists())
        
    def test_no_carstvo(self):
        self.client.login(username='urednik', password='urednik')
        with open('slobodna_enciklopedija_ptica_srbije/static/images/logo.png', 'rb') as file:
            image_data = file.read()

        image = SimpleUploadedFile('logo.png', image_data)
        data = {
            'vrsta': 'vrsta test',
            'rod': 'rod test',
            'porodica': 'porodica test',
            'red': 'red test',
            'klasa': 'klasa test',
            'tip':'tip test',
            'carstvo': '',
            'tezina': 10,
            'velicina': 10,
            'status_ugrozenosti': 'status ugrozenosti test',
            'sadrzaj': 'sadrzaj test',
            'slika_vrste':image
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_article', args=[Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).first().id_clanka]))

        self.assertTrue(Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).exists())
        self.assertTrue(PticaTabela.objects.filter(vrsta='vrsta test').exists())
        
    def test_no_tezina(self):
        self.client.login(username='urednik', password='urednik')
        with open('slobodna_enciklopedija_ptica_srbije/static/images/logo.png', 'rb') as file:
            image_data = file.read()

        image = SimpleUploadedFile('logo.png', image_data)
        data = {
            'vrsta': 'vrsta test',
            'rod': 'rod test',
            'porodica': 'porodica test',
            'red': 'red test',
            'klasa': 'klasa test',
            'tip':'tip test',
            'carstvo': 'carstvo test',
            'tezina': '',
            'velicina': 10,
            'status_ugrozenosti': 'status ugrozenosti test',
            'sadrzaj': 'sadrzaj test',
            'slika_vrste':image
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_article', args=[Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).first().id_clanka]))

        self.assertTrue(Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).exists())
        self.assertTrue(PticaTabela.objects.filter(vrsta='vrsta test').exists())
        
    def test_no_velicina(self):
        self.client.login(username='urednik', password='urednik')
        with open('slobodna_enciklopedija_ptica_srbije/static/images/logo.png', 'rb') as file:
            image_data = file.read()

        image = SimpleUploadedFile('logo.png', image_data)
        data = {
            'vrsta': 'vrsta test',
            'rod': 'rod test',
            'porodica': 'porodica test',
            'red': 'red test',
            'klasa': 'klasa test',
            'tip':'tip test',
            'carstvo': 'carstvo test',
            'tezina': 10,
            'velicina': '',
            'status_ugrozenosti': 'status ugrozenosti test',
            'sadrzaj': 'sadrzaj test',
            'slika_vrste':image
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_article', args=[Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).first().id_clanka]))

        self.assertTrue(Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).exists())
        self.assertTrue(PticaTabela.objects.filter(vrsta='vrsta test').exists())
        
    def test_no_status_ugrozenosti(self):
        self.client.login(username='urednik', password='urednik')
        with open('slobodna_enciklopedija_ptica_srbije/static/images/logo.png', 'rb') as file:
            image_data = file.read()

        image = SimpleUploadedFile('logo.png', image_data)
        data = {
            'vrsta': 'vrsta test',
            'rod': 'rod test',
            'porodica': 'porodica test',
            'red': 'red test',
            'klasa': 'klasa test',
            'tip':'tip test',
            'carstvo': 'carstvo test',
            'tezina': 10,
            'velicina': 10,
            'status_ugrozenosti': '',
            'sadrzaj': 'sadrzaj test',
            'slika_vrste':image
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_article', args=[Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).first().id_clanka]))

        self.assertTrue(Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).exists())
        self.assertTrue(PticaTabela.objects.filter(vrsta='vrsta test').exists())
        
    def test_no_sadrzaj(self):
        self.client.login(username='urednik', password='urednik')
        with open('slobodna_enciklopedija_ptica_srbije/static/images/logo.png', 'rb') as file:
            image_data = file.read()

        image = SimpleUploadedFile('logo.png', image_data)
        data = {
            'vrsta': 'vrsta test',
            'rod': 'rod test',
            'porodica': 'porodica test',
            'red': 'red test',
            'klasa': 'klasa test',
            'tip':'tip test',
            'carstvo': 'carstvo test',
            'tezina': 10,
            'velicina': 10,
            'status_ugrozenosti': 'status ugrozenosti test',
            'sadrzaj': '',
            'slika_vrste':image
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_article', args=[Clanak.objects.filter(sadrzaj='', id_autora=self.userU).first().id_clanka]))

        self.assertTrue(Clanak.objects.filter(sadrzaj='', id_autora=self.userU).exists())
        self.assertTrue(PticaTabela.objects.filter(vrsta='vrsta test').exists())
        
    def test_no_slika(self):
        self.client.login(username='urednik', password='urednik')
        
        data = {
            'vrsta': 'vrsta test',
            'rod': 'rod test',
            'porodica': 'porodica test',
            'red': 'red test',
            'klasa': 'klasa test',
            'tip':'tip test',
            'carstvo': 'carstvo test',
            'tezina': 10,
            'velicina': 10,
            'status_ugrozenosti': 'status ugrozenosti test',
            'sadrzaj': 'sadrzaj test',
            'slika_vrste':''
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_article', args=[Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).first().id_clanka]))

        self.assertTrue(Clanak.objects.filter(sadrzaj='sadrzaj test', id_autora=self.userU).exists())
        self.assertTrue(PticaTabela.objects.filter(vrsta='vrsta test').exists())
        
    def test_vrsta_already_exists(self):
        self.client.login(username='urednik', password='urednik')
        article = Clanak.objects.create(sadrzaj='posotojeci', id_autora=self.userA)
        bird_table = PticaTabela.objects.create(vrsta='vrsta test', id_clanka=article)
        with open('slobodna_enciklopedija_ptica_srbije/static/images/logo.png', 'rb') as file:
            image_data = file.read()

        image = SimpleUploadedFile('logo.png', image_data)
        data = {
            'vrsta': 'vrsta test',
            'rod': 'rod test',
            'porodica': 'porodica test',
            'red': 'red test',
            'klasa': 'klasa test',
            'tip':'tip test',
            'carstvo': 'carstvo test',
            'tezina': 10,
            'velicina': 10,
            'status_ugrozenosti': 'status ugrozenosti test',
            'sadrzaj': 'sadrzaj test',
            'slika_vrste':image
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/kreiranje_clanka.html')
        self.assertTrue('error_msg' in response.context)
        self.assertTrue(response.context['error_msg']=='Pokušali ste da napravite članak za vrstu ptice koja već postoji.')
        self.assertEqual(PticaTabela.objects.filter(vrsta='vrsta test').count(), 1)
        self.assertFalse(Clanak.objects.filter(id_autora=self.userU).exists())
        
    def test_tezina_not_number(self):
        self.client.login(username='urednik', password='urednik')
        with open('slobodna_enciklopedija_ptica_srbije/static/images/logo.png', 'rb') as file:
            image_data = file.read()

        image = SimpleUploadedFile('logo.png', image_data)
        data = {
            'vrsta': 'vrsta test',
            'rod': 'rod test',
            'porodica': 'porodica test',
            'red': 'red test',
            'klasa': 'klasa test',
            'tip':'tip test',
            'carstvo': 'carstvo test',
            'tezina': 'blabla',
            'velicina': 10,
            'status_ugrozenosti': 'status ugrozenosti test',
            'sadrzaj': 'sadrzaj test',
            'slika_vrste':image
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/kreiranje_clanka.html')
        self.assertTrue('error_msg' in response.context)
        self.assertTrue(response.context['error_msg']=='Težina i veličina mora da bude pozitivan broj!')
        self.assertEqual(PticaTabela.objects.filter(vrsta='vrsta test').count(), 0)
        self.assertFalse(Clanak.objects.filter(id_autora=self.userU).exists())
        
    def test_velicina_not_number(self):
        self.client.login(username='urednik', password='urednik')
        with open('slobodna_enciklopedija_ptica_srbije/static/images/logo.png', 'rb') as file:
            image_data = file.read()

        image = SimpleUploadedFile('logo.png', image_data)
        data = {
            'vrsta': 'vrsta test',
            'rod': 'rod test',
            'porodica': 'porodica test',
            'red': 'red test',
            'klasa': 'klasa test',
            'tip':'tip test',
            'carstvo': 'carstvo test',
            'tezina': 10,
            'velicina': 'blabla',
            'status_ugrozenosti': 'status ugrozenosti test',
            'sadrzaj': 'sadrzaj test',
            'slika_vrste':image
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/kreiranje_clanka.html')
        self.assertTrue('error_msg' in response.context)
        self.assertTrue(response.context['error_msg']=='Težina i veličina mora da bude pozitivan broj!')
        self.assertEqual(PticaTabela.objects.filter(vrsta='vrsta test').count(), 0)
        self.assertFalse(Clanak.objects.filter(id_autora=self.userU).exists())
        
    def test_velicina_not_positive(self):
        self.client.login(username='urednik', password='urednik')
        with open('slobodna_enciklopedija_ptica_srbije/static/images/logo.png', 'rb') as file:
            image_data = file.read()

        image = SimpleUploadedFile('logo.png', image_data)
        data = {
            'vrsta': 'vrsta test',
            'rod': 'rod test',
            'porodica': 'porodica test',
            'red': 'red test',
            'klasa': 'klasa test',
            'tip':'tip test',
            'carstvo': 'carstvo test',
            'tezina': 10,
            'velicina': -10,
            'status_ugrozenosti': 'status ugrozenosti test',
            'sadrzaj': 'sadrzaj test',
            'slika_vrste':image
        }
        response = self.client.post(reverse('create_article'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/kreiranje_clanka.html')
        self.assertTrue('error_msg' in response.context)
        self.assertTrue(response.context['error_msg']=='Težina i veličina mora da bude pozitivan broj!')
        self.assertEqual(PticaTabela.objects.filter(vrsta='vrsta test').count(), 0)
        self.assertFalse(Clanak.objects.filter(id_autora=self.userU).exists())
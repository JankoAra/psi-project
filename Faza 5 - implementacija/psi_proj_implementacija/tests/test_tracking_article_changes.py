# Autor: Janko Arandjelovic 2021/0328

import json
from django.test import TestCase
from django.urls import reverse

from slobodna_enciklopedija_ptica_srbije.models import Clanak, Korisnik, PrijavljenNaObavestenja, PticaTabela

class TestArticleTracking(TestCase):
    
    def setUp(self):
        self.user = Korisnik.objects.create_user(username='testuser', email='test@gmail.com', password='testpassword')
        
        self.article = Clanak.objects.create(sadrzaj='Test Content', id_autora=self.user)
        PticaTabela.objects.create(id_clanka=self.article, vrsta='Test Article')
        
    def test_track_changes_on_article_check_if_exists_true(self):
        self.client.login(username='testuser', password='testpassword')

        data = {'article': self.article.id_clanka}
        
        response = self.client.post(reverse('track_changes_on_article_page'), data=data, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
    
    def test_track_changes_on_article_check_if_exists_false(self):
        self.client.login(username='testuser', password='testpassword')

        data = {'article': 666}
        
        response = self.client.post(reverse('track_changes_on_article_page'), data=data, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        
    def test_track_changes_on_article_check_if_exists_no_article_id(self):
        self.client.login(username='testuser', password='testpassword')

        data = {}
        
        response = self.client.post(reverse('track_changes_on_article_page'), data=data, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        
    def test_track_changes_page_with_email(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('track_changes_on_article', args=[self.article.id_clanka]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "slobodna_enciklopedija_ptica_srbije/prijava_na_obavestenja.html")
        self.assertEqual(response.context["id_article"], self.article.id_clanka)
        self.assertEqual(response.context["show_question"], 1)
        
    def test_track_changes_page_with_no_email(self):
        new_user = Korisnik.objects.create_user(username='testuser2', password='testpassword2')
        self.client.login(username='testuser2', password='testpassword2')

        response = self.client.get(reverse('track_changes_on_article', args=[self.article.id_clanka]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "slobodna_enciklopedija_ptica_srbije/prijava_na_obavestenja.html")
        self.assertEqual(response.context["id_article"], self.article.id_clanka)
        self.assertEqual(response.context["show_question"], 0)
        
    def test_track_changes_page_not_logged_in(self):
        response = self.client.get(reverse('track_changes_on_article', args=[self.article.id_clanka]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/prijava/?next=/prijavi_se_na_pracenje_obavestenja/" + str(self.article.id_clanka))
        
    def test_track_changes_confirm_with_email(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('track_changes_on_article_confirm'),
            data=json.dumps({'id_article': self.article.id_clanka, 'get_on_email': True}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['success'], True)

        self.assertTrue(PrijavljenNaObavestenja.objects.filter(id_clanka=self.article, id_korisnika=self.user, primaj_na_mail=True).exists())

    def test_track_changes_confirm_without_email(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('track_changes_on_article_confirm'),
            data=json.dumps({'id_article': self.article.id_clanka, 'get_on_email': False}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['success'], True)

        self.assertTrue(PrijavljenNaObavestenja.objects.filter(id_clanka=self.article, id_korisnika=self.user, primaj_na_mail=False).exists())

    def test_track_changes_confirm_no_email_param(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('track_changes_on_article_confirm'),
            data=json.dumps({'id_article': self.article.id_clanka}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['success'], False)
        self.assertTrue(PrijavljenNaObavestenja.objects.filter(id_clanka=self.article, id_korisnika=self.user).exists()==False)


    def test_track_changes_confirm_no_article_id_param(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('track_changes_on_article_confirm'),
            data=json.dumps({'get_on_email': True}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['success'], False)

        self.assertTrue(PrijavljenNaObavestenja.objects.filter(id_clanka=self.article, id_korisnika=self.user).exists()==False)
        
    def test_track_changes_confirm_no_params(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('track_changes_on_article_confirm'),
            data=json.dumps({}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['success'], False)

        self.assertTrue(PrijavljenNaObavestenja.objects.filter(id_clanka=self.article, id_korisnika=self.user).exists()==False)
        
    def test_track_changes_confirm_non_existing_article(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('track_changes_on_article_confirm'),
            data=json.dumps({"id_article": 666, "get_on_email": True}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['success'], False)

        self.assertTrue(PrijavljenNaObavestenja.objects.filter(id_clanka=self.article, id_korisnika=self.user).exists()==False)

    def test_check_if_already_track_tracking(self):
        self.client.login(username='testuser', password='testpassword')
        prijava = PrijavljenNaObavestenja.objects.create(id_clanka=self.article, id_korisnika=self.user, primaj_na_mail=True)
        response = self.client.post(
            reverse('check_if_already_track'),
            data=json.dumps({"article": self.article.id_clanka}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['success'], False)

        self.assertTrue(PrijavljenNaObavestenja.objects.filter(id_clanka=self.article, id_korisnika=self.user).exists())
        
    def test_check_if_already_track_not_tracking(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('check_if_already_track'),
            data=json.dumps({"article": self.article.id_clanka}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['success'], True)

        self.assertTrue(PrijavljenNaObavestenja.objects.filter(id_clanka=self.article, id_korisnika=self.user).exists()==False)

    def test_check_if_already_track_wrong_article_id(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('check_if_already_track'),
            data=json.dumps({"article": 666}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['success'], False)
        
    def test_check_if_already_track_not_logged_in(self):
        response = self.client.post(
            reverse('check_if_already_track'),
            data=json.dumps({"article": self.article.id_clanka}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['success'], False)
        

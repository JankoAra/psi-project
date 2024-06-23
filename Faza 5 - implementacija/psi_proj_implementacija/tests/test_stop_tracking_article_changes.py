# Autor: Janko Arandjelovic 2021/0328

import json
from django.test import TestCase
from django.urls import reverse

from slobodna_enciklopedija_ptica_srbije.models import Clanak, Korisnik, PrijavljenNaObavestenja, PticaTabela


class TestStopTrackingArticleChanges(TestCase):
    
    def setUp(self):
        self.user = Korisnik.objects.create_user(username='testuser', password='testpassword')

        self.article = Clanak.objects.create(
            id_autora=self.user,
            sadrzaj='testiranje',
            broj_ocena=1,
            zbir_ocena=5
        )
        
        PticaTabela.objects.create(id_clanka=self.article, vrsta='test ptica')

        self.subscription = PrijavljenNaObavestenja.objects.create(
            id_clanka=self.article,
            id_korisnika=self.user,
            primaj_na_mail=False
        )
        
    def test_stop_tracking_article_changes_success(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(
            reverse('stop_tracking_article_changes'),
            data=json.dumps({'article': self.article.id_clanka}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['success'], True)

        self.assertFalse(PrijavljenNaObavestenja.objects.filter(id_clanka=self.article, id_korisnika=self.user).exists())
        
    def test_stop_tracking_article_changes_not_logged_in(self):
        response = self.client.post(
            reverse('stop_tracking_article_changes'),
            data=json.dumps({'article': self.article.id_clanka}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 302)

        login_url = reverse('user_login')
        expected_url = f"{login_url}?next={reverse('stop_tracking_article_changes')}"

        self.assertRedirects(response, expected_url)
        
    def test_stop_tracking_article_changes_missing_data(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(
            reverse('stop_tracking_article_changes'),
            data=json.dumps({}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['success'], False)
        self.assertIn('error', response.json())
        
    def test_stop_tracking_article_changes_invalid_article(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(
            reverse('stop_tracking_article_changes'),
            data=json.dumps({'article': 666}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['success'], False)
        self.assertIn('error', response.json())
        
    def test_stop_tracking_article_changes_not_tracking(self):
        self.client.login(username='testuser', password='testpassword')

        new_article = Clanak.objects.create(
            id_autora=self.user,
            sadrzaj='Some new text'
        )

        response = self.client.post(
            reverse('stop_tracking_article_changes'),
            data=json.dumps({'article': new_article.id_clanka}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['success'], False)
        self.assertIn('error', response.json())




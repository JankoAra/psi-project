# Autor: Janko Arandjelovic 2021/0328

import json
from django.test import TestCase
from django.urls import reverse

from django.utils import timezone

from slobodna_enciklopedija_ptica_srbije.models import Clanak, Diskusija, Korisnik, PticaTabela


class TestCreateDiscussion(TestCase):
   
    def setUp(self):
        self.user = Korisnik.objects.create_user(username='testuser', password='testpassword')
        self.article = Clanak.objects.create(
            id_autora=self.user,
            broj_ocena=5,
            zbir_ocena=5,
            sadrzaj='Test Article Content',
        )
        bird_table = PticaTabela.objects.create(id_clanka=self.article, vrsta='test ptica')

    def test_create_discussion_not_logged_in(self):
        response = self.client.post(reverse('create_discussion'))
        self.assertEqual(response.status_code, 302)
        
    def test_create_discussion_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('create_discussion'))
        self.assertEqual(response.status_code, 405) # 405 - method not supported
        
    def test_success(self):
        self.client.login(username='testuser', password='testpassword')
        self.assertTrue(Diskusija.objects.filter(id_clanka=self.article).count()==0)
        data = {
            'discussion_title':'test title',
            'discussion_content':'test content',
            'article_id':self.article.id_clanka
        }
        data = json.dumps(data)
        response = self.client.post(reverse('create_discussion'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['success'], True)
        self.assertTrue(Diskusija.objects.filter(id_clanka=self.article).exists())
        self.assertTrue(Diskusija.objects.filter(id_clanka=self.article).count()==1)
        
    def test_empty_title(self):
        self.client.login(username='testuser', password='testpassword')
        self.assertTrue(Diskusija.objects.filter(id_clanka=self.article).count()==0)
        data = {
            'discussion_title':'',
            'discussion_content':'test content',
            'article_id':self.article.id_clanka
        }
        data = json.dumps(data)
        response = self.client.post(reverse('create_discussion'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['success'], True)
        self.assertTrue(Diskusija.objects.filter(id_clanka=self.article).exists())
        self.assertTrue(Diskusija.objects.filter(id_clanka=self.article).count()==1)
        self.assertTrue(Diskusija.objects.filter(id_clanka=self.article, naslov_diskusije='Nema naslova').count()==1)
        
    def test_empty_content(self):
        self.client.login(username='testuser', password='testpassword')
        self.assertTrue(Diskusija.objects.filter(id_clanka=self.article).count()==0)
        data = {
            'discussion_title':'test title',
            'discussion_content':'',
            'article_id':self.article.id_clanka
        }
        data = json.dumps(data)
        response = self.client.post(reverse('create_discussion'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['success'], True)
        self.assertTrue(Diskusija.objects.filter(id_clanka=self.article).exists())
        self.assertTrue(Diskusija.objects.filter(id_clanka=self.article).count()==1)
        self.assertTrue(Diskusija.objects.filter(id_clanka=self.article, sadrzaj='Nema sadrzaja').count()==1)
        
    def test_article_not_exist(self):
        self.client.login(username='testuser', password='testpassword')
        self.assertTrue(Diskusija.objects.filter(id_clanka=self.article).count()==0)
        data = {
            'discussion_title':'test title',
            'discussion_content':'test content',
            'article_id':6666
        }
        data = json.dumps(data)
        response = self.client.post(reverse('create_discussion'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['success'], False)
        self.assertFalse(Diskusija.objects.filter(id_clanka=self.article).exists())
        self.assertTrue(Diskusija.objects.count()==0)
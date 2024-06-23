# Autor: Janko Arandjelovic 2021/0328

import json
from django.test import TestCase
from django.urls import reverse

from django.utils import timezone

from slobodna_enciklopedija_ptica_srbije.models import Clanak, Diskusija, Komentar, Korisnik, PticaTabela


class TestCreateComment(TestCase):
   
    def setUp(self):
        self.user = Korisnik.objects.create_user(username='testuser', password='testpassword')
        self.article = Clanak.objects.create(
            id_autora=self.user,
            broj_ocena=5,
            zbir_ocena=5,
            sadrzaj='Test Article Content',
        )
        bird_table = PticaTabela.objects.create(id_clanka=self.article, vrsta='test ptica')
        self.discussion = Diskusija.objects.create(sadrzaj='test discussion', id_pokretaca=self.user, id_clanka=self.article)

    def test_create_comment_not_logged_in(self):
        response = self.client.post(reverse('create_comment'))
        self.assertEqual(response.status_code, 302)
        
    def test_create_discussion_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('create_comment'))
        self.assertEqual(response.status_code, 405) # 405 - method not supported
        
    def test_success(self):
        self.client.login(username='testuser', password='testpassword')
        self.assertTrue(Komentar.objects.filter(id_diskusije=self.discussion).count()==0)
        data = {
            'discussion_id':self.discussion.id_diskusije,
            'comment_content':'test content',
        }
        data = json.dumps(data)
        response = self.client.post(reverse('create_comment'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['success'], True)
        self.assertTrue(Komentar.objects.filter(id_diskusije=self.discussion).exists())
        self.assertTrue(Komentar.objects.filter(id_diskusije=self.discussion).count()==1)
        
    
        
    def test_empty_content(self):
        self.client.login(username='testuser', password='testpassword')
        self.assertTrue(Komentar.objects.filter(id_diskusije=self.discussion).count()==0)
        data = {
            'discussion_id':self.discussion.id_diskusije,
            'comment_content':'',
        }
        data = json.dumps(data)
        response = self.client.post(reverse('create_comment'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['success'], True)
        self.assertTrue(Komentar.objects.filter(id_diskusije=self.discussion).exists())
        self.assertTrue(Komentar.objects.filter(id_diskusije=self.discussion).count()==1)
        self.assertTrue(Komentar.objects.filter(id_diskusije=self.discussion, sadrzaj='Nema sadrzaja').count()==1)
        
    def test_discussion_not_exist(self):
        self.client.login(username='testuser', password='testpassword')
        self.assertTrue(Komentar.objects.filter(id_diskusije=self.discussion).count()==0)
        data = {
            'discussion_id':6666,
            'comment_content':'test content',
        }
        data = json.dumps(data)
        response = self.client.post(reverse('create_comment'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['success'], False)
        self.assertFalse(Komentar.objects.filter(id_diskusije=self.discussion).exists())
        
    def test_discussion_no_id(self):
        self.client.login(username='testuser', password='testpassword')
        self.assertTrue(Komentar.objects.filter(id_diskusije=self.discussion).count()==0)
        data = {
            'comment_content':'test content',
        }
        data = json.dumps(data)
        response = self.client.post(reverse('create_comment'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['success'], False)
        self.assertFalse(Komentar.objects.filter(id_diskusije=self.discussion).exists())
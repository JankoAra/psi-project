# Autor: Janko Arandjelovic 2021/0328

import json
from django.test import TestCase
from django.urls import reverse

from django.utils import timezone

from slobodna_enciklopedija_ptica_srbije.models import Clanak, Korisnik, PticaTabela


class TestIndexView(TestCase):
   
    def setUp(self):
        self.user = Korisnik.objects.create_user(username='testuser', password='testpassword')
        self.num_of_articles = 10
        
        for i in range(self.num_of_articles):
            article = Clanak.objects.create(
                id_autora=self.user,
                datum_vreme_kreiranja=timezone.now(),
                broj_ocena=5,
                zbir_ocena=5*(i+1),
                sadrzaj=f'Test Article {i} Content',
            )
            PticaTabela.objects.create(
                id_clanka=article,
                vrsta=f'Test Article {i}',
            )

    def test_index_view_initial_load(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/index.html')
        self.assertIn('articles', response.context)
        self.assertEqual(len(response.context['articles']), 4)
        self.assertEqual(response.context["total_articles"]==self.num_of_articles, True)
        self.assertContains(response, f'Test Article {self.num_of_articles - 1}')
        
    def test_index_load_more_first_time(self):
        initial_load_count = 4
        additional_load_count = 4
        response = self.client.post(reverse('index_load_more'), 
                                    json.dumps({'number_of_articles': initial_load_count}), 
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertTrue(response_json['success'])
        self.assertEqual(response_json['number_of_loaded_articles'], initial_load_count + additional_load_count)
        self.assertEqual(len(response_json['articles']), additional_load_count)
        self.assertEqual(response_json['articles'][0]["species"], f'Test Article {self.num_of_articles - 5}')

    def test_index_load_more_second_time(self):
        initial_load_count = 8
        additional_load_count = 4
        able_to_load = self.num_of_articles-initial_load_count
        response = self.client.post(reverse('index_load_more'), 
                                    json.dumps({'number_of_articles': initial_load_count}), 
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertTrue(response_json['success'])
        self.assertEqual(response_json['number_of_loaded_articles'], 
                         min(initial_load_count + additional_load_count,self.num_of_articles))
        self.assertEqual(len(response_json['articles']), min(additional_load_count,able_to_load))
        self.assertEqual(response_json['articles'][0]["species"], f'Test Article {self.num_of_articles-9}')
    
    def test_index_load_more_no_more(self):
        initial_load_count = self.num_of_articles
        response = self.client.post(reverse('index_load_more'), 
                                    json.dumps({'number_of_articles': initial_load_count}), 
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertTrue(response_json['success'])
        self.assertEqual(response_json['number_of_loaded_articles'], self.num_of_articles)
        self.assertEqual(len(response_json['articles']), 0)
        
    def test_article_search_find_multiple(self):
        
        query = 'Test'
        response = self.client.post(reverse('index'), {'search_input': query})

        
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/index.html')
        self.assertIn('articles', response.context)
        self.assertEqual(len(response.context['articles']), self.num_of_articles)
        self.assertIn('view', response.context)
        self.assertEqual(response.context["view"], 'specific')
        self.assertContains(response, f'Test Article {self.num_of_articles - 1}')
        
    def test_article_search_find_one(self):
        
        query = '3'
        response = self.client.post(reverse('index'), {'search_input': query})

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/index.html')
        self.assertIn('articles', response.context)
        self.assertEqual(len(response.context['articles']), 1)
        self.assertIn('view', response.context)
        self.assertEqual(response.context["view"], 'specific')
        self.assertContains(response, f'Test Article 3')
        
    def test_article_search_find_none(self):
        
        query = 'nema nista'
        response = self.client.post(reverse('index'), {'search_input': query})

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/index.html')
        self.assertIn('articles', response.context)
        self.assertEqual(len(response.context['articles']), 0)
        self.assertIn('view', response.context)
        self.assertEqual(response.context["view"], 'specific')
        
# Autor: Janko Arandjelovic 2021/0328

from django.test import TestCase
from django.urls import reverse

from django.utils import timezone

from slobodna_enciklopedija_ptica_srbije.models import Clanak, Korisnik, PticaTabela

class TestLogout(TestCase):
    
    def setUp(self):
        self.user = Korisnik.objects.create_user(username='testuser', password='testpassword')
    
    def test_logout_when_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(reverse('user_logout'))
        
        self.assertRedirects(response, reverse('index'))
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_logout_when_not_logged_in(self):
        response = self.client.get(reverse('user_logout'))
        
        self.assertRedirects(response, f"{reverse('user_login')}?next={reverse('user_logout')}")
    
    def test_logout_redirect_to_next_url(self):
        self.client.login(username='testuser', password='testpassword')
        
        article = Clanak.objects.create(id_autora=self.user, datum_vreme_kreiranja=timezone.now(), broj_ocena=0, zbir_ocena=0)
        article.save()
        bird_table = PticaTabela.objects.create(id_clanka=article, vrsta='test_ptica')
        bird_table.save()
        
        article_id = article.id_clanka
        redirection_page = reverse('show_article', args=[article_id])
        response = self.client.get(reverse('user_logout') + f'?next={redirection_page}')
        
        self.assertRedirects(response, redirection_page)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_logout_redirect_to_index_no_next_url(self):
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(reverse('user_logout'))
        
        self.assertRedirects(response, reverse('index'))
        self.assertFalse('_auth_user_id' in self.client.session)
        
        

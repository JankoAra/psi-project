# Autor: Janko Arandjelovic 2021/0328

from django.test import TestCase
from django.urls import reverse

from django.utils import timezone

from slobodna_enciklopedija_ptica_srbije.models import Korisnik

class TestLogin(TestCase):
    
    def setUp(self):
        self.user = Korisnik.objects.create_user(username='testuser', password='testpassword')

    def test_get_request_user_already_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(reverse('user_login'))
        
        self.assertRedirects(response, reverse('index'))

    def test_get_request_user_not_logged_in(self):
        response = self.client.get(reverse('user_login'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/login.html')

    def test_post_request_valid_credentials(self):
        response = self.client.post(reverse('user_login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        
        self.assertRedirects(response, reverse('index'))
        
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_post_request_invalid_username(self):
        response = self.client.post(reverse('user_login'), {
            'username': 'test',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/login.html')
        self.assertContains(response, 'Niste uneli ispravne kredencijale ili korisnik ne postoji!')
        
        self.assertFalse('_auth_user_id' in self.client.session)
        
    def test_post_request_invalid_password(self):
        response = self.client.post(reverse('user_login'), {
            'username': 'testuser',
            'password': 'wrongpassword123'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/login.html')
        self.assertContains(response, 'Niste uneli ispravne kredencijale ili korisnik ne postoji!')
        
        self.assertFalse('_auth_user_id' in self.client.session)

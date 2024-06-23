# Autor: Anđela Ćirić 2021/0066

import json
from django.test import TestCase, Client
from django.urls import reverse
from django.test.client import RequestFactory

from django.utils import timezone

from slobodna_enciklopedija_ptica_srbije.models import *
import os


class TestRegisterUserTestCase(TestCase):



    def setUp(self):
        self.client = Client()
        self.editor = Korisnik.objects.create_user(username='uredniktest', password='odiseja123', tip="U")
        self.admin = Korisnik.objects.create_user(username='admintest', password='odiseja123', tip="A")
        self.registered = Korisnik.objects.create_user(username='regtest', password='odiseja123', tip="R")
        self.newUser = None


    def tearDown(self):
        if self.newUser != None:
            self.newUser.delete()
        self.editor.delete()
        self.admin.delete()
        self.registered.delete()

    def test_registeruser_post(self):
        response = self.client.post(reverse('user_register'), {
            'username': 'registrovani123',
            'email': 'registrovani@gmail.com',
            'password1': 'enciklopedija1',
            'password2': 'enciklopedija1'
        }, follow=True)

        self.newUser = Korisnik.objects.latest("id")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Korisnik.objects.filter(username='registrovani123').exists())
        self.assertEqual(response.redirect_chain[-1][0], reverse('user_login'))

    def test_register_invalid_user_already_exist(self):
        response = self.client.post(reverse('user_register'), {
            'username': 'regtest',
            'email': 'regtest@gmail.com',
            'password1': 'enciklopedija1',
            'password2': 'enciklopedija1'
        }, follow=True)

        self.assertTrue(Korisnik.objects.filter(username='regtest').exists())
        self.assertIn('errors', response.context)

        errorFinal = ""
        if 'errors' in response.context:
            error_dict = response.context['errors']
            for field, errors in error_dict.items():
                for error in errors:
                    errorFinal+=error

        self.assertEqual(errorFinal,"Korisnik sa tim korisničkim imenom već postoji.")

    def test_register_invalid_user_passwordsdifferent(self):
        response = self.client.post(reverse('user_register'), {
            'username': 'regtest3',
            'email': 'regtest1@gmail.com',
            'password1': 'enciklopedija1',
            'password2': 'enciklopedija2'
        }, follow=True)


        self.assertFalse(Korisnik.objects.filter(username='regtest3').exists())
        self.assertIn('errors', response.context)

        errorFinal = ""
        if 'errors' in response.context:
            error_dict = response.context['errors']
            for field, errors in error_dict.items():
                for error in errors:
                    errorFinal+=error

        self.assertEqual(errorFinal,"Dva polja za lozinke se ne poklapaju.")

    def test_register_already_loggedin(self):
        response = self.client.post(reverse("user_login"), data={"username": self.registered.username, "password": "odiseja123"})
        response = self.client.get(reverse('user_register'), folow=True)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Korisnik.objects.filter(username='reggg123').exists())
        self.assertEqual(response.url, reverse('index'))

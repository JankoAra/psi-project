# Autor: Anđela Ćirić 2021/0066

import json
from django.test import TestCase, Client
from django.urls import reverse
from django.test.client import RequestFactory

from django.utils import timezone

from slobodna_enciklopedija_ptica_srbije.models import *
import os


class TestMakingEditorTestCase(TestCase):



    def setUp(self):
        self.client = Client()
        self.editor = Korisnik.objects.create_user(username='uredniktest', password='odiseja123', tip="U")
        self.admin = Korisnik.objects.create_user(username='admintest', password='odiseja123', tip="A")
        self.registered = Korisnik.objects.create_user(username='regtest', password='odiseja123', tip="R")


    def tearDown(self):
        self.editor.delete()
        self.admin.delete()
        self.registered.delete()

    def test_editor_register_get(self):
        response = self.client.post(reverse("user_login"),data={"username": self.admin.username, "password": "odiseja123"})
        response = self.client.get(reverse('editor_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/registracija.html')

    def test_editor_register_post(self):
        response = self.client.post(reverse("user_login"),data={"username": self.admin.username, "password": "odiseja123"})
        response = self.client.get(reverse('editor_register'))
        response = self.client.post(reverse('editor_register'), {
            'username': 'urednik123',
            'email': 'urednik1@gmail.com',
            'password1': 'enciklopedija1',
            'password2': 'enciklopedija1'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Korisnik.objects.filter(username='urednik123').exists())
        self.assertEqual(response.redirect_chain[-1][0], reverse('index'))

    def test_editor_invalid_user_already_exist_register_post(self):
        response = self.client.post(reverse("user_login"),data={"username": self.admin.username, "password": "odiseja123"})
        response = self.client.get(reverse('editor_register'))
        response = self.client.post(reverse('editor_register'), {
            'username': 'uredniktest',
            'email': 'urednik1@gmail.com',
            'password1': 'enciklopedija1',
            'password2': 'enciklopedija1'
        }, follow=True)


        self.assertTrue(Korisnik.objects.filter(username='uredniktest').exists())
        self.assertIn('errors', response.context)

        errorFinal = ""
        if 'errors' in response.context:
            error_dict = response.context['errors']
            for field, errors in error_dict.items():
                for error in errors:
                    errorFinal+=error

        self.assertEqual(errorFinal,"Korisnik sa tim korisničkim imenom već postoji.")

    def test_editor_invalid_user_passwordsdifferent_register_post(self):
        response = self.client.post(reverse("user_login"),data={"username": self.admin.username, "password": "odiseja123"})
        response = self.client.get(reverse('editor_register'))
        response = self.client.post(reverse('editor_register'), {
            'username': 'uredniktest3',
            'email': 'urednik1@gmail.com',
            'password1': 'enciklopedija1',
            'password2': 'enciklopedija2'
        }, follow=True)


        self.assertFalse(Korisnik.objects.filter(username='uredniktest3').exists())
        self.assertIn('errors', response.context)

        errorFinal = ""
        if 'errors' in response.context:
            error_dict = response.context['errors']
            for field, errors in error_dict.items():
                for error in errors:
                    errorFinal+=error

        self.assertEqual(errorFinal,"Dva polja za lozinke se ne poklapaju.")

    def test_editor_register_post_nonadmin(self):
        response = self.client.post(reverse("user_login"),
                                    data={"username": self.registered.username, "password": "odiseja123"})
        response = self.client.get(reverse('editor_register'))
        response = self.client.post(reverse('editor_register'), {
            'username': 'urednik123',
            'email': 'urednik1@gmail.com',
            'password1': 'enciklopedija1',
            'password2': 'enciklopedija1'
        })

        self.assertEqual(response.url, "/")
        self.assertEqual(response.status_code, 302)
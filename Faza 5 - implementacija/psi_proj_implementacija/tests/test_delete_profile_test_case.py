# Autor: Anđela Ćirić 2021/0066

import json
from django.test import TestCase, Client
from django.urls import reverse

from django.utils import timezone

from slobodna_enciklopedija_ptica_srbije.models import *
import os



class TestDeleteProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Korisnik.objects.create_user(username='testadmin', password='odiseja123', tip="A")
        self.user_to_delete1 = Korisnik.objects.create_user(username='testuser1', password='odiseja123', tip="R")
        self.user_to_delete2 = Korisnik.objects.create_user(username='testuser2', password='odiseja123', tip="R")
        self.user_to_delete3 = Korisnik.objects.create_user(username='testuser3', password='odiseja123', tip="R")
        self.user_to_delete4 = Korisnik.objects.create_user(username='testuser4', password='odiseja123', tip="R")
        self.user_to_delete5 = Korisnik.objects.create_user(username='testuser5', password='odiseja123', tip="R")
        self.user_to_delete6 = Korisnik.objects.create_user(username='testuser6', password='odiseja123', tip="R")
        self.user_to_delete7 = Korisnik.objects.create_user(username='testuser7', password='odiseja123', tip="R")
        self.user_to_delete8 = Korisnik.objects.create_user(username='testuser8', password='odiseja123', tip="R")
        self.user_to_delete9 = Korisnik.objects.create_user(username='testuser9', password='odiseja123', tip="R")
        self.user_to_delete10 = Korisnik.objects.create_user(username='testuser10', password='odiseja123', tip="R")
        self.user_to_delete11 = Korisnik.objects.create_user(username='testuser11', password='odiseja123', tip="R")
        self.user_to_delete12 = Korisnik.objects.create_user(username='testuser12', password='odiseja123', tip="R")
        self.user_to_delete13 = Korisnik.objects.create_user(username='testuser13', password='odiseja123', tip="R")
        self.user_to_delete14 = Korisnik.objects.create_user(username='testuser14', password='odiseja123', tip="R")
        self.user_to_delete15 = Korisnik.objects.create_user(username='testuser15', password='odiseja123', tip="R")



    def tearDown(self):
        self.admin.delete()
        self.user_to_delete1.delete()
        self.user_to_delete2.delete()
        self.user_to_delete3.delete()
        self.user_to_delete4.delete()
        self.user_to_delete5.delete()
        self.user_to_delete6.delete()
        self.user_to_delete7.delete()
        self.user_to_delete8.delete()
        self.user_to_delete9.delete()
        self.user_to_delete10.delete()
        self.user_to_delete11.delete()
        self.user_to_delete12.delete()
        self.user_to_delete13.delete()
        self.user_to_delete14.delete()
        self.user_to_delete15.delete()

    def test_admin_deletes_active_user(self):
        response = self.client.post(reverse("user_login"),data={"username": self.admin.username, "password": "odiseja123"})
        user_to_delete = self.user_to_delete15
        response = self.client.delete(reverse("delete_user", args=[user_to_delete.id]))
        json_response = response.json()
        self.assertEqual(json_response['message'], 'Uspešno ste obrisali korisnika!')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Korisnik.objects.get(id=user_to_delete.id).is_active)

    def test_admin_try_deleting_inactive_user(self):
        response = self.client.post(reverse("user_login"),data={"username": self.admin.username, "password": "odiseja123"})
        user_to_delete = self.user_to_delete15
        self.user_to_delete15.is_active = 0
        self.user_to_delete15.save()
        response = self.client.delete(reverse("delete_user", args=[self.user_to_delete15.id]))
        json_response = response.json()
        #print(response)
        self.assertEqual(json_response['message'], 'Uspešno ste obrisali korisnika!')
        self.assertEqual(response.status_code, 200)

    def test_admin_deletes_nonexisting_user(self):
        response = self.client.post(reverse("user_login"),data={"username": self.admin.username, "password": "odiseja123"})
        response = self.client.delete(reverse("delete_user", args=[123456789]))
        json_response = response.json()
        print(response)
        self.assertEqual(json_response['message'], 'Korisnik sa datim identifikatorom ne postoji!')
        self.assertEqual(response.status_code, 404)

    def test_nonadmin_user_try_to_delete(self):
        response = self.client.post(reverse("user_login"),data={"username": self.user_to_delete15.username, "password": "odiseja123"})
        response = self.client.delete(reverse("delete_user", args=[self.user_to_delete3.id]))
        self.assertEqual(response.url, "/")
        self.assertEqual(response.status_code, 302)

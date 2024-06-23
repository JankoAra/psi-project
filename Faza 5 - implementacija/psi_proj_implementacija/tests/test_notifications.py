# Autor: Janko Arandjelovic 2021/0328


import json
from django.test import RequestFactory, TestCase
from django.urls import reverse

from slobodna_enciklopedija_ptica_srbije.models import Clanak, Diskusija, FotografijaGalerija, Komentar, Korisnik, Poruka, PrimljenePoruke, PticaTabela
from slobodna_enciklopedija_ptica_srbije.views import delete_message


class TestNotificationsView(TestCase):
    def setUp(self):
        self.user = Korisnik.objects.create_user(username='testuser', password='testpassword')
        
    def test_notifications_no_notifications(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/prikaz_obavestenja.html')
        self.assertEqual(len(response.context['messages']),0)
        
    def test_notifications_not_logged_in(self):
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_login') + '?next=' + reverse('notifications'))
        
    def test_notifications_with_notifications(self):
        self.client.login(username='testuser', password='testpassword')
        for i in range(5):
            message = Poruka.objects.create(tekst=f'test{i}')
            PrimljenePoruke.objects.create(id_poruke=message, id_korisnika=self.user, procitana=0)
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/prikaz_obavestenja.html')
        self.assertEqual(len(response.context['messages']),5)
        self.assertContains(response, "test1")
        
class TestOneMessageView(TestCase):
    def setUp(self):
        self.user = Korisnik.objects.create_user(username='testuser', password='testpassword')
        
        self.message = Poruka.objects.create(tekst='test message')
        
        
    def test_one_message_view_success_C(self):
        self.client.login(username='testuser', password='testpassword')
        article = Clanak.objects.create(sadrzaj='Test Content', id_autora=self.user)
        bird_table = PticaTabela.objects.create(id_clanka=article, vrsta='test ptica')
        received_msg = PrimljenePoruke.objects.create(id_poruke=self.message, id_korisnika=self.user, procitana=0,
                                                      tip_prijave='C', id_prijavljene_stvari=article.id_clanka)
        response = self.client.get(reverse('one_message_view', args=[self.message.id_poruke]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/prikaz_jedne_poruke.html')
        received_msg = PrimljenePoruke.objects.get(id_poruke=self.message, id_korisnika=self.user)
        self.assertEqual(received_msg.procitana, 1)
        
    def test_one_message_view_success_D(self):
        self.client.login(username='testuser', password='testpassword')
        article = Clanak.objects.create(sadrzaj='Test Content', id_autora=self.user)
        bird_table = PticaTabela.objects.create(id_clanka=article, vrsta='test ptica')
        discussion = Diskusija.objects.create(sadrzaj='test discussion', id_pokretaca=self.user, id_clanka=article)
        received_msg = PrimljenePoruke.objects.create(id_poruke=self.message, id_korisnika=self.user, procitana=0,
                                                      tip_prijave='D', id_prijavljene_stvari=discussion.id_diskusije)
        response = self.client.get(reverse('one_message_view', args=[self.message.id_poruke]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/prikaz_jedne_poruke.html')
        received_msg = PrimljenePoruke.objects.get(id_poruke=self.message, id_korisnika=self.user)
        self.assertEqual(received_msg.procitana, 1)
        
    def test_one_message_view_success_K(self):
        self.client.login(username='testuser', password='testpassword')
        article = Clanak.objects.create(sadrzaj='Test Content', id_autora=self.user)
        bird_table = PticaTabela.objects.create(id_clanka=article, vrsta='test ptica')
        discussion = Diskusija.objects.create(sadrzaj='test discussion', id_pokretaca=self.user, id_clanka=article)
        comment = Komentar.objects.create(sadrzaj='test comment', id_korisnika=self.user, id_diskusije=discussion)
        received_msg = PrimljenePoruke.objects.create(id_poruke=self.message, id_korisnika=self.user, procitana=0,
                                                      tip_prijave='K', id_prijavljene_stvari=comment.id_komentara)
        response = self.client.get(reverse('one_message_view', args=[self.message.id_poruke]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/prikaz_jedne_poruke.html')
        received_msg = PrimljenePoruke.objects.get(id_poruke=self.message, id_korisnika=self.user)
        self.assertEqual(received_msg.procitana, 1)
        
    def test_one_message_view_success_F(self):
        self.client.login(username='testuser', password='testpassword')
        article = Clanak.objects.create(sadrzaj='Test Content', id_autora=self.user)
        bird_table = PticaTabela.objects.create(id_clanka=article, vrsta='test ptica')
        image_data = open('./test_data/owl.jpg', 'rb').read()
        gallery_image = FotografijaGalerija.objects.create(sadrzaj_slike=image_data, id_autora=self.user, id_clanka=article)
        received_msg = PrimljenePoruke.objects.create(id_poruke=self.message, id_korisnika=self.user, procitana=0,
                                                      tip_prijave='F', id_prijavljene_stvari=gallery_image.id_fotografije)
        response = self.client.get(reverse('one_message_view', args=[self.message.id_poruke]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'slobodna_enciklopedija_ptica_srbije/prikaz_jedne_poruke.html')
        received_msg = PrimljenePoruke.objects.get(id_poruke=self.message, id_korisnika=self.user)
        self.assertEqual(received_msg.procitana, 1)
        
    def test_one_message_view_not_logged_in(self):
        article = Clanak.objects.create(sadrzaj='Test Content', id_autora=self.user)
        bird_table = PticaTabela.objects.create(id_clanka=article, vrsta='test ptica')
        received_msg = PrimljenePoruke.objects.create(id_poruke=self.message, id_korisnika=self.user, procitana=0,
                                                      tip_prijave='C', id_prijavljene_stvari=article.id_clanka)
        response = self.client.get(reverse('one_message_view', args=[self.message.id_poruke]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_login') + '?next=' + reverse('one_message_view', args=[self.message.id_poruke]))
        received_msg = PrimljenePoruke.objects.get(id_poruke=self.message, id_korisnika=self.user)
        self.assertEqual(received_msg.procitana, 0)
        
class TestDeleteNotification(TestCase):
    def setUp(self):
        self.user = Korisnik.objects.create_user(username='testuser', password='testpassword')
        self.message = Poruka.objects.create(tekst='test')
        self.received_msg = PrimljenePoruke.objects.create(id_poruke=self.message, id_korisnika=self.user, procitana=0)
        
    def test_delete_notification_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete_message', args=[self.message.id_poruke]))
        json_response = json.loads(response.content)
        self.assertEqual(PrimljenePoruke.objects.count(), 0)
        self.assertEqual(Poruka.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['success'], True)
        
    def test_delete_notification_not_logged_in(self):
        response = self.client.post(reverse('delete_message', args=[self.message.id_poruke]))
        self.assertEqual(PrimljenePoruke.objects.count(), 1)
        self.assertEqual(Poruka.objects.count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_login') + '?next=' + reverse('delete_message', args=[self.message.id_poruke]))
        
    def test_delete_notification_wrong_message_id(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete_message', args=[666]))
        json_response = json.loads(response.content)
        self.assertEqual(PrimljenePoruke.objects.count(), 1)
        self.assertEqual(Poruka.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['success'], False)
        
    def test_delete_notification_wrong_user(self):
        self.client.login(username='testuser', password='testpassword')
        user2 = Korisnik.objects.create_user(username='testuser2', password='testpassword2')
        self.received_msg.id_korisnika = user2
        self.received_msg.save()
        response = self.client.post(reverse('delete_message', args=[self.message.id_poruke]))
        json_response = json.loads(response.content)
        self.assertEqual(PrimljenePoruke.objects.count(), 1)
        self.assertEqual(Poruka.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['success'], False)
        
    def test_delete_notification_no_msg_id(self):
        self.client.login(username='testuser', password='testpassword')
        
        factory = RequestFactory()
        request = factory.post(reverse('delete_message', args=[self.message.id_poruke]))
        request.user = self.user

        response = delete_message(request, msg_id=None)
        json_response = json.loads(response.content)
        self.assertEqual(PrimljenePoruke.objects.count(), 1)
        self.assertEqual(Poruka.objects.count(), 1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response['success'], False)
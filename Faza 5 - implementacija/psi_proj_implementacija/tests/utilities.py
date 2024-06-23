from django.urls import reverse

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from slobodna_enciklopedija_ptica_srbije.models import *

import os


def login(browser, app_url, username, password):
    # Ovo je pomocna login funkcija koja moze da se koristi u testovima koji zahtevaju da korisnik bude ulogovan.
    # Izdvojena je tu jer mnogi testovi zahtevaju korisnik da bude ulogovan. Pa da se ne bi duplirao kod.
    # Autor: Jaroslav veseli 2021/0480.

    # Idi na stranicu prijave.
    browser.get(app_url + reverse('user_login'))

    # Unesi korisnicko ime.
    user_input = browser.find_element(By.ID, "korisnickoImePrijava")
    user_input.send_keys(username)

    # Unesi lozinku.
    pass_input = browser.find_element(By.ID, "lozinkaPrijava")
    pass_input.send_keys(password)
    
    # Pritisni dugme prijave.
    submit_btn = browser.find_element(By.XPATH, "/html/body/section/div/div/form/table/tbody/tr[3]/td/input")
    submit_btn.click()

    # Sacekaj da predjes na index.
    WebDriverWait(browser, 20).until(EC.url_matches(app_url))


def initialize_data_vj210480(obj):
    # Ovo je izdvojeno tu da se ne bi duplirao kod u nekim testovima.
    obj.user_1 = Korisnik.objects.create(username='jaroslav_1', email='test@etf.bg.ac.rs', tip='U')
    obj.user_1.set_password('WhoKnows455@')
    obj.user_1.save()

    obj.user_2 = Korisnik.objects.create(username='jaroslav_2', email='test@etf.bg.ac.rs', tip='A')
    obj.user_2.set_password('WhoKnows455@')
    obj.user_2.save()

    obj.user_3 = Korisnik.objects.create(username='jaroslav_3', email='randomEmail1@unknown.com', tip='R')
    obj.user_3.set_password('WhoKnows455@')
    obj.user_3.save()

    obj.user_4 = Korisnik.objects.create(username='jaroslav_4', email='randomEmail2@unknown.com', tip='R')
    obj.user_4.set_password('WhoKnows455@')
    obj.user_4.save()

        
    obj.article_1 = Clanak.objects.create(id_autora=obj.user_1, sadrzaj='Neki tekst')
    obj.table_1 = PticaTabela.objects.create(id_clanka=obj.article_1, vrsta='Neka vrsta')

    obj.article_2 = Clanak.objects.create(id_autora=obj.user_2, sadrzaj='Neki tekst')
    obj.table_2 = PticaTabela.objects.create(id_clanka=obj.article_2, vrsta='Neka vrsta')


    obj.discussion = Diskusija.objects.create(id_pokretaca=obj.user_3, sadrzaj="Ovo je neka jako zanimljiva diskusija", naslov_diskusije="Neka Diskusija", id_clanka=obj.article_1)
    obj.comment = Komentar.objects.create(id_diskusije=obj.discussion, id_korisnika=obj.user_3, sadrzaj="Neki nasumicni komentar")

    image_data = open(os.path.abspath("./test_data/owl.jpg"), "rb").read()
    obj.gallery_image = FotografijaGalerija.objects.create(id_clanka=obj.article_1, id_autora=obj.user_3, sadrzaj_slike=image_data)

    
    obj.reason_discussion_1 = RazlogPrijaveDiskusija.objects.create(id_razlog_diskusija=1, opis="Uznemirujući/uvredljiv sadržaj")
    obj.reason_discussion_2 = RazlogPrijaveDiskusija.objects.create(id_razlog_diskusija=2, opis="Netačne informacije")

    obj.reason_comment_1 = RazlogPrijaveKomentar.objects.create(id_razlog_komentar=1, opis="Uznemirujući/uvredljiv sadržaj")
    obj.reason_comment_2 = RazlogPrijaveKomentar.objects.create(id_razlog_komentar=2, opis="Netačne informacije")

    obj.reason_image_1 = RazlogPrijaveFotografije.objects.create(id_razlog_fotografija=1, opis="Fotografija ne prikazuje pticu")
    obj.reason_image_2 = RazlogPrijaveFotografije.objects.create(id_razlog_fotografija=2, opis="Fotografija prikazuje pogrešnu pticu")
    obj.reason_image_3 = RazlogPrijaveFotografije.objects.create(id_razlog_fotografija=3, opis="Fotografija ima uznemirujući sadržaj")


def delete_data_vj210480(obj):
    # Ovde se brisu svi podaci iz baze podataka, onim redosledom tako da se ispostuju referencijalni integriteti.
    PticaTabela.objects.all().delete()
    Ocena.objects.all().delete()

    PrijavljenNaObavestenja.objects.all().delete()
    PrimljenePoruke.objects.all().delete()
    Poruka.objects.all().delete()

    NepravilnostFotografija.objects.all().delete()
    NepravilnostClanak.objects.all().delete()
    NepravilnostDiskusija.objects.all().delete()
    NepravilnostKomentar.objects.all().delete()
    PrijavaNepravilnosti.objects.all().delete()

    RazlogPrijaveDiskusija.objects.all().delete()
    RazlogPrijaveFotografije.objects.all().delete()
    RazlogPrijaveKomentar.objects.all().delete()

    Komentar.objects.all().delete()
    Diskusija.objects.all().delete()

    FotografijaGalerija.objects.all().delete()
    Clanak.objects.all().delete()

    Korisnik.objects.all().delete()
    


def initialize_content_ls210260(obj):

    # Ovo je izdvojeno tu da se ne bi duplirao kod u nekim testovima.
    obj.user_1 = Korisnik.objects.create(username='srdjanU', email='test@etf.bg.ac.rs', tip='U')
    obj.user_1.set_password('srkiLozinka1')
    obj.user_1.save()

    obj.user_2 = Korisnik.objects.create(username='srdjanA', email='test@etf.bg.ac.rs', tip='A')
    obj.user_2.set_password('srkiLozinka2')
    obj.user_2.save()

    obj.user_3 = Korisnik.objects.create(username='srdjanR', email='randomEmail1@unknown.com', tip='R')
    obj.user_3.set_password('srkiLozinka3')
    obj.user_3.save()

    obj.article_1 = Clanak.objects.create(id_autora=obj.user_1, sadrzaj='Neki tekst')
    obj.table_1 = PticaTabela.objects.create(id_clanka=obj.article_1, vrsta='Neka vrsta')

    obj.article_1.save(); obj.table_1.save()

    obj.article_2 = Clanak.objects.create(id_autora=obj.user_2, sadrzaj='Neki tekst')
    obj.table_2 = PticaTabela.objects.create(id_clanka=obj.article_2, vrsta='Neka vrsta 2')

    obj.article_2.save(); obj.table_2.save()

    obj.discussion1 = Diskusija.objects.create(id_pokretaca=obj.user_3, sadrzaj="Ovo je neka jako zanimljiva diskusija",
                                              naslov_diskusije="Neka Diskusija", id_clanka=obj.article_1)
    obj.comment1 = Komentar.objects.create(id_diskusije=obj.discussion1, id_korisnika=obj.user_3,
                                          sadrzaj="Neki nasumicni komentar")

    obj.discussion1.save(); obj.comment1.save()

    obj.discussion2 = Diskusija.objects.create(id_pokretaca=obj.user_1, sadrzaj="Ovo je neka veoma dosadna diskusija",
                                              naslov_diskusije="Neka Dosadna Diskusija", id_clanka=obj.article_1)
    obj.comment2 = Komentar.objects.create(id_diskusije=obj.discussion2, id_korisnika=obj.user_3,
                                          sadrzaj="Brate je li moglo sta dosadnije")
    obj.comment3 = Komentar.objects.create(id_diskusije=obj.discussion2, id_korisnika=obj.user_2,
                                           sadrzaj = "Nije uopste dosadna, ne znam o cemu pricas (please don't ban me)")

    obj.discussion2.save(); obj.comment2.save(); obj.comment3.save()

    image_data = open(os.path.abspath("./test_data/owl.jpg"), "rb").read()
    obj.gallery_image = FotografijaGalerija.objects.create(id_clanka=obj.article_1, id_autora=obj.user_3,
                                                           sadrzaj_slike=image_data)

    image_data2 = open(os.path.abspath('./test_data/patka.jpg'), "rb").read()
    obj.gallery_image1 = FotografijaGalerija.objects.create(id_clanka=obj.article_1, id_autora=obj.user_1,
                                                           sadrzaj_slike=image_data2)

    obj.gallery_image.save(); obj.gallery_image1.save()

def delete_content_ls210260d(obj):
    FotografijaGalerija.objects.all().delete()
    Komentar.objects.all().delete()
    Diskusija.objects.all().delete()
    PticaTabela.objects.all().delete()
    Clanak.objects.all().delete()
    Korisnik.objects.all().delete()

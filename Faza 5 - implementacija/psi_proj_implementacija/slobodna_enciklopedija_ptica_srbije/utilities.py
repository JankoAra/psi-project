# Andjela Ciric 2021/0066
# Srdjan Lucic 2021/0260
# Janko Arandjelovic 2021/0328
# Jaroslav Veseli 2021/0480


import base64
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.forms.utils import ErrorList
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import HttpResponseNotAllowed


from PIL import Image
from io import BytesIO

from functools import wraps
from .forms import KorisnikCreationForm


def cyrlic_to_latin(cyrilic_text):
    """
    Ova funkcija služi da prevede ćirilični tekst na latinični. Ono što nije ćirilično ostaje takvo kakvo je i bilo.
    Iako je u settings.py podešen LANGUAGE_CODE na sr-Latn, što znači da treba da se koristi latinično pismo.    
    Po neke stvari su ipak ćirilične u djangu (validacione greške i tako dalje).
    """
    

    # Dictionary koji mapira ćirilična slova na latinična (i velika i mala).
    letters = {
        'А': 'A',  'а': 'a',
        'Б': 'B',  'б': 'b',
        'В': 'V',  'в': 'v',
        'Г': 'G',  'г': 'g',
        'Д': 'D',  'д': 'd',
        'Ђ': 'Đ',  'ђ': 'đ',
        'Е': 'E',  'е': 'e',
        'Ж': 'Ž',  'ж': 'ž',
        'З': 'Z',  'з': 'z',
        'И': 'I',  'и': 'i',
        'Ј': 'J',  'ј': 'j',
        'К': 'K',  'к': 'k',
        'Л': 'L',  'л': 'l',
        'Љ': 'Lj', 'љ': 'lj',
        'М': 'M',  'м': 'm',
        'Н': 'N',  'н': 'n',
        'Њ': 'Nj', 'њ': 'nj',
        'О': 'O',  'о': 'o',
        'П': 'P',  'п': 'p',
        'Р': 'R',  'р': 'r',
        'С': 'S',  'с': 's',
        'Т': 'T',  'т': 't',
        'Ћ': 'Ć',  'ћ': 'ć',
        'У': 'U',  'у': 'u',
        'Ф': 'F',  'ф': 'f',
        'Х': 'H',  'х': 'h',
        'Ц': 'C',  'ц': 'c',
        'Ч': 'Č',  'ч': 'č',
        'Џ': 'Dž', 'џ': 'dž',
        'Ш': 'Š',  'ш': 'š'
    }

    # Rezultujući string.
    translated_string = ""

    # Prođi kroz svako slovo teksta, ako se nalazi u mapi kao ključ, znači da je ćirilično, uzmi vrednost za dat ključ (slovo), ako nije u mapi nije ćirilično i samo ga takvog dodaj u string.
    for character in cyrilic_text:
        if character in letters:
            translated_string += letters[character]
        else:
            translated_string += character

    return translated_string


def registration_form_save(request, user_type):
    """
    Ova funkcija sluzi da uzme podatke iz POST HTTP request-a za registraciju, validira ih, i ako su ispravni registruje korisnika odredjenog tipa na osnovu njih.
    Dodata je zbog toga sto je registracija za urednika / obicnog korisnika vrlo slicna, pa da se ne duplira kod.
    """
    
    form = KorisnikCreationForm(request.POST)

    if form.is_valid():
        # Napravi korisnika bez zavrsavanja transakcije, pa mu postavi tip, pa tek onda zavrsi transakciju.
        new_user = form.save(commit=False)
        new_user.tip = user_type
        new_user.save()
        return redirect("user_login")
    else:
        # Ako registracija nije uspešna, onda renderuj korisniku formu za registraciju sa greškama.
        # Pre toga, uzmi svaku grešku i prevedi je na latinično pismo, to radimo jer neke greške su u ćiriličnom pismu.
        for field in form.errors:
            form.errors[field] = ErrorList([cyrlic_to_latin(error) for error in form.errors[field]])
        
        # Uzmi i prevedi engleske ključeve grešaka na srpski (jer se i oni prikazuju korisniku).
        field_translations = { "username": "Korisničko ime:", "email": "E-mail Adresa:", "password1": "Lozinka:", "password2": "Potvrda Lozinke:" }
        for field in field_translations:
            if field in form.errors:
                form.errors[field_translations[field]] = form.errors[field]
                del form.errors[field]

        return render(request, 'slobodna_enciklopedija_ptica_srbije/registracija.html', { 'errors': form.errors, 'submit_btn_text': 'Kreiraj Profil', 'old_form': request.POST })


def specific_users_only(user_types):
    def decorator(function):
        """
        Ova funkcija sluzi da dekorise bilo koji view, za koji se zahteva da samo odredjena vrsta korisnika sme da pristupi istom.
        Ova funkcija zamenjuje prosledjenu funkciju koja predstavlja view, sa funkcijom koja se vraca, koja prvenstveno proverava da li je nego ulogovan.
        Ako jeste, nakon toga se proverava da li taj neko ko je ulogovan je odredjene vrste, ako jeste, pusta se funkcija, inace korisnik se rutira na indeks.
        """
        @wraps(function)
        @login_required(login_url='user_login')
        def wrapper(request, *args, **kwargs):
            if request.user.tip in user_types:
                return function(request, *args, **kwargs)
            else:
                return redirect("index")
        return wrapper
    return decorator


def is_valid_image(binary_data):
    """
    Ova funkcija prima binarne podatke, preko biblioteke Pillow pokušavamo da protumačimo te binarne podatke kao sliku i da ih verifikujemo.
    Funkcija verify() u slučaju da ti binarni podaci ne predstavljaju sliku će da baci grešku, i tada smo sigurni da ti podaci ne predstavljaju sliku.
    """
    try:
        with Image.open(BytesIO(binary_data)) as image:
            image.verify()
        return True
    except:
        return False

import os
from django.conf import settings


import threading
mutex_email = threading.Semaphore(1)
def send_email(subject, body, html_message, users: list[str]):
    """
    Ova funkcija kreira e-mail poruku i salje je sa naloga koji je definisan u settings.py (pri kraju fajla).
    Salje je na sve email adrese koje se nalaze u listi users koja se prosledjuje kao parametar ovoj funkciji.
    """
    try:
        image_path = os.path.join(settings.STATIC_ROOT, 'images', 'logo.png')
        print(users)
        email = EmailMultiAlternatives(from_email="",subject=subject, body=body, to=users)
        email.attach_alternative(html_message, "text/html")
        with open(image_path, 'rb') as f:
            email.attach('logo.png', f.read(), 'image/png')
        with mutex_email:
            email.send()
    except Exception as e:
        print(e)
        print("Nismo uspeli da pošaljemo mail!")


def require_GET(view_func):
    """
    Ovaj dekorater ogranicava funkciju view_func da mora biti pozvana kroz GET zahtev.
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.method != 'GET':
            return HttpResponseNotAllowed(['GET'])  # Return 405 Method Not Allowed if request method is not GET
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def articleSortKey(article):
    return article[1]

def articleSortKey2(article):
    return article.avg_pts

class ArticleIndexView:
    """
    Sadrzi informacije o clanku koje sluze za prikazivanje na pocetnoj stranici.
    """
    def __init__(self, species, genus, family, order, phylum, bioclass, kingdom,
                 conservation, creationDate, image, text, routeToArticle, weight, size, avg_pts):
        self.species = species
        self.genus = genus
        self.family = family
        self.order = order
        self.phylum = phylum
        self.bioclass = bioclass
        self.kingdom = kingdom
        self.conservation = conservation
        self.creationDate = creationDate
        self.image = image
        self.text = text
        self.routeToArticle = routeToArticle
        self.avg_pts = avg_pts
        self.weight = weight
        self.size = size

    def to_json(self):
        return {
            'species': self.species,
            'genus': self.genus,
            'family': self.family,
            'order': self.order,
            'phylum': self.phylum,
            'bioclass': self.bioclass,
            'kingdom': self.kingdom,
            'conservation': self.conservation,
            'creationDate': str(self.creationDate),
            'image': self.image,
            'text': self.text,
            'routeToArticle': self.routeToArticle,
            'avg_pts': str(self.avg_pts),
            'weight': str(self.weight),
            'size': str(self.size)
        }
        

from .models import Clanak, PticaTabela
def fetch_and_sort_articles():
    """
    Dohvata clanke iz baze podataka i sortira ih po prosecnoj oceni.
    """
    all_articles_from_db = Clanak.objects.defer('sadrzaj')
    all_articles_with_avg_grades = []
    for article in all_articles_from_db:
        all_articles_with_avg_grades.append((article, article.zbir_ocena / (max(article.broj_ocena, 1))))

    # Sortiranje prema najvisoj prosjecnoj ocjeni
    all_articles_with_avg_grades.sort(key=articleSortKey, reverse=True)
    return all_articles_with_avg_grades


def create_all_articles_view_for_index(all_articles_with_avg_grades, number_of_loaded_articles):
    """
    Vraca listu clanaka za prikaz na pocetnoj stranici. Ucitavaju se po 4 clanka.
    """
    articles_final = []

    for article in all_articles_with_avg_grades[number_of_loaded_articles:number_of_loaded_articles+4]:
        bird = PticaTabela.objects.defer('slika_vrste').get(id_clanka=article[0].id_clanka)
        bird_image = None
        if bird.slika_vrste is not None:
            bird_image = base64.b64encode(bird.slika_vrste).decode('utf-8')
            bird_image_display = f'data:image/png;base64,{bird_image}'
        else:
            # U slucaju da nema slike, ucitava se logo
            bird_image_display="../../../static/images/logo.png"

        avg_grade = article[1]
        if bird.velicina is not None:
            bird.velicina = round(bird.velicina, 2)
        if bird.tezina is not None:
            bird.tezina = round(bird.tezina, 2)
        if avg_grade is not None:
            avg_grade = round(article[1], 2)

        article_info = ArticleIndexView(bird.vrsta, bird.rod, bird.porodica, bird.red, bird.klasa,
                                        bird.tip, bird.carstvo, bird.status_ugrozenosti, article[0].datum_vreme_kreiranja,
                                        bird_image_display, article[0].sadrzaj[0:100]+"...",
                                        f"pregled_clanka/{article[0].id_clanka}",
                                        bird.velicina, bird.tezina, avg_grade)
        articles_final.append(article_info)

    return articles_final


class MessageView:
    def __init__(self, msg_id, path, date_time, type, content, read=None, id_of_reported_thing=None, image = None):
        self.path = path
        self.date_time = date_time
        self.type = type
        self.content = content
        self.image = image
        self.id_of_reported_thing = id_of_reported_thing
        self.read = read
        self.id = msg_id


def message_type(type, msg_text):
    if type == 'D': return 'Nepravilnost - diskusija'
    if type == 'F': return 'Nepravilnost - fotografija'
    if type == 'K': return 'Nepravilnost - komentar'
    if type == 'C' and msg_text.startswith('Izmenjen'): return 'Izmena - clanak'
    if type == 'C' and msg_text.startswith('Prijavljen'): return 'Nepravilnost - clanak'
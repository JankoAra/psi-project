# Andjela Ciric 2021/0066
# Srdjan Lucic 2021/0260
# Janko Arandjelovic 2021/0328
# Jaroslav Veseli 2021/0480


import json
import threading
from time import localtime

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods

from slobodna_enciklopedija_ptica_srbije.forms import UploadImageToGalleryForm

from .utilities import registration_form_save, require_GET, specific_users_only, is_valid_image, articleSortKey, articleSortKey2, ArticleIndexView, \
    fetch_and_sort_articles, create_all_articles_view_for_index, MessageView, message_type
from .models import *
import base64
from .utilities import send_email

from django.db import connection

def index(request):
    """
    Funkcija koja prikazuje pocetnu stranicu sajta, sa pregledom svih clanaka
    
    **Template:**
    
        - slobodna_enciklopedija_ptica_srbije/index.html
    
    **Rezultat:**
    
        - Prikazuje pocetnu stranicu sajta, sa pregledom svih clanaka. Clanci su sortirani po prosecnoj oceni.
    """

    if request.method=="POST":
        context = article_search(request)
        return render(request, 'slobodna_enciklopedija_ptica_srbije/index.html', context)

    # Ucitavanje clanaka i racunanje prosjecne ocjene za svaki
    all_articles_with_avg_grades = fetch_and_sort_articles()

    # Formiranje liste objekata koji ce biti proslijedjeni kroz kontekst i prikazani na stranici
    articles_final = create_all_articles_view_for_index(all_articles_with_avg_grades, 0)

    context = {
        "articles": articles_final,
        'view': 'all',
        "number_of_loaded_articles": 4,
        "total_articles": len(all_articles_with_avg_grades)
    }
    return render(request, 'slobodna_enciklopedija_ptica_srbije/index.html', context)


def index_load_more(request):
    """
    Funckija za ucitavanje novih clanaka na pocetnoj stranici. Predstavlja API poziv.
    
    **Argumenti:**
    
        - Argument zahteva je broj clanaka koji je vec ucitan. Dostavlja se kroz JSON objekat.
    
    **Rezultat:**
    
        - Rezultat je JSON objekat sa statusom uspeha, brojem ucitanih clanaka i objektom koji predstavlja ucitane clanke i informacije o njima
    """
    number_of_loaded_articles = int(json.loads(request.body)['number_of_articles'])
    all_articles_with_avg_grades = fetch_and_sort_articles()

    articles_final = create_all_articles_view_for_index(all_articles_with_avg_grades, number_of_loaded_articles)
    number_of_loaded_articles +=len (articles_final)

    for i in range(len(articles_final)):
        articles_final[i] = articles_final[i].to_json()

    return JsonResponse({
        'success': True,
        'number_of_loaded_articles': number_of_loaded_articles,
        'articles': articles_final,
    })

def article_search(request):
    """
    Funckija za pretragu clanaka. Predstavlja API poziv.
    
    **Argumenti:**
    
        - Argument zahteva je string po kome se vrsi pretraga. Dostavlja se kroz telo zahteva.
    
    **Rezultat:**
    
        - Rezultat je JSON objekat sa clancima koji odgovaraju pretrazi po imenu.
    """
    article_name = request.POST.get('search_input')
    query = '''
    SELECT *
        FROM Clanak, PticaTabela
        WHERE Clanak.IDClanka = PticaTabela.IDClanka AND PticaTabela.Vrsta LIKE %s
        '''
    name_param = f'%{article_name}%'
    with connection.cursor() as cursor:
        cursor.execute(query, [name_param])
        matching_articles = cursor.fetchall()

    articles_final=[]

    for art in matching_articles:
        if art[17] is None:
            bird_image_display = "../../../static/images/logo.png"
        else:
            bird_image = base64.b64encode(art[17]).decode('utf-8')
            bird_image_display = f'data:image/png;base64,{bird_image}'

        article_info = ArticleIndexView(art[7], art[8], art[9], art[10], art[11],
                                        art[12], art[13], art[16],
                                        art[2], bird_image_display, art[1][0:100]+'...',
                                        f"pregled_clanka/{art[0]}",
                                        art[15], art[14], art[4]/(max(art[3],1)))

        articles_final.append(article_info)

    articles_final.sort(reverse=True, key=articleSortKey2)

    context = {'articles': articles_final, 'view':'specific'}
    return context


@login_required(login_url='user_login')
def user_logout(request):
    """
    Funkcija za odjavu korisnika.
    
    **Rezultat:**
    
        - Ukoliko je korisnik bio prijavljen, odjavljuje se.
        - Ako korisnik nije bio prijavljen, redirektuje se na stranicu za prijavu.
        - Pri prijavi vrsi se redirekcija na stranicu zadatu kao parametar u query string-u, ukoliko postoji, u suprotnom na pocetnu stranicu.
    """
    # Odjavi korisnika ako je prijavljen, ako nije, pa ne mozes da se odjavis ako nisi prijavljen, tada se korisnik redirektuje na login.
    # Takodje, korisnika vrati na prethodnu stranicu na kojoj se nalazio, ako se to kojim slučajem nije prosledilo kroz query string, onda ga pošalji na index.
    logout(request)
    return redirect(request.GET.get('next', 'index'))


def user_login(request):
    """
    Funckija za prijavu korisnika i prikaz stranice za prijavu
    
    Ukoliko je GET zahtev, prikazuje se stranica za prijavljivanje.
    Ukoliko je POST zahtev, proveravaju se podaci iz prosledjene forme za prijavu.
    
    **Argumenti:**
    
        - Za POST zahtev, argument je popunjena forma za prijavljivanje.
        
    **Templates:**
    
        - slobodna_enciklopedija_ptica_srbije/login.html
    
    **Rezultat:**

        - Za GET zahtev, prikaz stranice za prijavljivanje ukoliko korisnik nije vec ulogovan, inace prikaz pocetne stranice preko redirekcije.
        - Za POST zahtev, provera parametara forme i prijava korisnika ako je sve uspesno, redirekcija na pocetnu stranicu.
        - Za POST zahtev, u slucaju neuspeha se prikazuje stranica za prijavljivanje sa porukom greske.
    """
    if request.method == 'GET':
        # Ukoliko je korisnik vec prijavljen, redirektuje se na index, inace mu se prikazuje forma za login.
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'slobodna_enciklopedija_ptica_srbije/login.html')
    else:
        # Ako se poslao HTTP POST, to znaci da se neko zeli ulogovati. Tada validiramo formu za logovanje, i logujemo korisnika ako je uneo ispravne kredencijale.
        # Ako korisnik nije uneo ispravne kredencijale, prikazuje mu se forma za login sa porukom greske.
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("index")
        else:
            return render(request, 'slobodna_enciklopedija_ptica_srbije/login.html', { 'show_error': True, 'old_form': request.POST })


def user_register(request):
    """
    Funkcija za registraciju korisnika i prikaz stranice za registraciju.
    
    **Templates:**
    
        - slobodna_enciklopedija_ptica_srbije/registracija.html
    
    **Rezultat:**
    
        - Za GET zahtev, prikaz stranice za registraciju ukoliko korisnik nije vec ulogovan, inace prikaz pocetne stranice preko redirekcije.
        - Za POST zahtev, provera parametara forme i registracija korisnika ako je sve uspesno, redirekcija na pocetnu stranicu.
        - Za POST zahtev, u slucaju neuspeha se prikazuje stranica za registraciju sa porukom greske.
    """
    # Registraciji može da pristupi bilo ko, ali ako je korisnik već prijavljen, rutira se na indeks, inače mu se prikazuje forma za registraciju.
    # Ako se prima HTTP POST zahtev, to znači da neko pokušava da se registruje kao običan korisnik.
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'slobodna_enciklopedija_ptica_srbije/registracija.html', { 'register_title': 'Otvaranje novog korisničkog profila', 'submit_btn_text': 'Kreiraj Profil' })
    else:
        return registration_form_save(request, 'R')


@specific_users_only(['A'])
def editor_register(request):
    """
    Funckija za registraciju urednika i prikaz stranice za registraciju urednika. Ovoj funkciji pristupa samo admin.
    
    **Templates:**
    
        - slobodna_enciklopedija_ptica_srbije/registracija.html
    
    **Rezultat:**
    
        - Za GET zahtev, prikaz stranice za registraciju urednika, ako onaj sto pristupa ovom delu aplikacije nije administrator, vraca se na pocetnu stranicu preko redirekcije.
        - Za POST zahtev, provera parametara forme i registracija urednika ako je sve uspesno, redirekcija na pocetnu stranicu.
        - Za POST zahtev, u slucaju neuspeha se prikazuje stranica za registraciju urednika sa porukom greske.
    """
    # Za registraciju urednika može da pristupi samo administrator, i slobodno mu se renderuje forma.
    # Ako se prima HTTP POST, to znači da administrator želi da napravi nalog za urednika.
    if request.method == "GET":
        return render(request, 'slobodna_enciklopedija_ptica_srbije/registracija.html', { 'register_title': 'Kreiraj korisnički profil uredniku', 'submit_btn_text': 'Registruj Urednika' })
    else:
        return registration_form_save(request, 'U')


@specific_users_only(['A'])
def user_deletion(request):
    """
    Funkcija za prikaz spiska prijavljenih korisnika. Ovoj funkciji pristupa samo administrator.
    
    **Templates:**
    
        - slobodna_enciklopedija_ptica_srbije/brisanje_korisnika.html
    
    **Rezultat:**
    
        - Prikaz stranice sa listom korisnika, sa mogucnoscu deaktiviranja naloga.
        - Ukoliko proba neko da pristupi njoj ko nije administrator, vraca se na pocetnu stranicu.
    """
    # Brisanju korisnika može da pristupi samo administrator, njemu se prikazuju svi korisnici koji su aktivivni.
    all_users = Korisnik.objects.filter(is_active=1).all()
    context = { 'all_users': all_users }
    return render(request, 'slobodna_enciklopedija_ptica_srbije/brisanje_korisnika.html', context)


@specific_users_only(['A'])
@require_http_methods(["DELETE"])
def delete_user_endpoint(request, user_id):
    """
    Funkcija za deaktiviranje naloga korisnika. Predstavlja API poziv. Ovoj funkciji pristupa samo admin.
    
    **Argumenti:**
    
        - username korisnika koji se brise, dostavlja se kroz url
        
    **Rezultat:**
    
        - JSON objekat sa statusom uspeha i porukom
        - Ukoliko je poziv uspesan, korisnikov nalog se oznacava deaktiviranim, ali se ne brise iz baze
    """
    # HTTP Request na ovu putanju može da uradi samo administrator. Pri brisanju se samo pronađe određen korisnik, i postavi se flag da je neaktivan.
    if Korisnik.objects.filter(id=user_id).update(is_active=0):
        return JsonResponse({ 'message': 'Uspešno ste obrisali korisnika!' }, status=200)
    else:
        return JsonResponse({ 'message': 'Korisnik sa datim identifikatorom ne postoji!' }, status=404)


@specific_users_only(['A', 'U'])
def create_article(request):
    """
    Funkcija za prikaz forme za kreiranje novog clanka i za kreiranje novog clanka. Ovoj funkciji pristupaju samo administrator i urednik.
    
    **Templates:**
    
        - slobodna_enciklopedija_ptica_srbije/kreiranje_clanka.html
        
    **Argumenti:**
    
        - Za POST zahtev, parametri forme za kreiranje
    
    **Rezultat:**
    
        - Za GET zahtev, prikaz stranice za kreiranje clanka.
        - Za POST zahtev, kreiranje novog clanka sa parametrima iz POST zahteva.
        - Ukoliko clanak za datu pticu vec postoji, zahtev se odbija.
        
    """
    if request.method == 'POST':
        # print(type(request.POST['tezina']))
        # Ukoliko nije prosleđena informacija za koju pticu se pravi članak, ili ako za tu pticu članak već postoji, odbij zahtev.
        if request.POST.get('vrsta', '').strip() == '':
            return render(request, 'slobodna_enciklopedija_ptica_srbije/kreiranje_clanka.html', { 'error_msg': 'Niste uneli polje za koju vrstu ptice želite da napravite članak.', 'old_form': request.POST })
        elif len(PticaTabela.objects.filter(vrsta=request.POST['vrsta'])) > 0:
            return render(request, 'slobodna_enciklopedija_ptica_srbije/kreiranje_clanka.html', { 'error_msg': 'Pokušali ste da napravite članak za vrstu ptice koja već postoji.', 'old_form': request.POST })

        # Kreiraj instance članka i tabele za članak, i popuni ih podacima, ako nešto fali u formi postavi defaultnu vrednost na prazan string (jedino se polje 'vrsta' zahteva).
        new_article = Clanak(id_autora=request.user, sadrzaj=request.POST.get('sadrzaj', ''))
        new_bird_table = PticaTabela(id_clanka          = new_article,
                                     vrsta              = request.POST.get('vrsta', ''),
                                     rod                = request.POST.get('rod', ''),
                                     porodica           = request.POST.get('porodica', ''),
                                     red                = request.POST.get('red', ''),
                                     klasa              = request.POST.get('klasa', ''),
                                     tip                = request.POST.get('tip', ''),
                                     carstvo            = request.POST.get('carstvo', ''),
                                     tezina             = request.POST.get('tezina', '0'),
                                     velicina           = request.POST.get('velicina', '0'),
                                     status_ugrozenosti = request.POST.get('status_ugrozenosti', ''))

        # Ukoliko je slika prosleđena, pročitaj je kao binarni sadržaj, validiraj sliku, i ako je ispravna dodaj je u tabelu.
        if 'slika_vrste' in request.FILES:
            image_data = request.FILES['slika_vrste'].read()
            if is_valid_image(image_data):
                new_bird_table.slika_vrste = image_data
        
        # U slučaju da je neko prosledio prazan string, postavljamo defaultnu vrednost na string 0. Django ORM ga posle pretvara u Decimal.
        if new_bird_table.tezina.strip() == '':
            new_bird_table.tezina = '0'
        if new_bird_table.velicina.strip() == '':
            new_bird_table.velicina = '0'

        try:
            # Pre nego što sačuvaš bilo šta, proveri da li je sve validno, tek ako to sve prođe, onda sačuvaj objekte modela.
            # Ako kojim slučajem nešto nije u redu, to jedino može biti zbog polja "veličina" i "težina" kod modela "PticaTabela", jer je sve ostalo CharField.
            # Tako da ako je neko uneo tekst ili negativan broj to se smatra greškom i tada metode za validaciju če da bace grešku, tada se korisnik ponovo prebacuje na formuprebacuje na formu.
            new_article.full_clean()
            new_bird_table.clean_fields(exclude=['id_clanka'])
            new_article.save()
            new_bird_table.save()
        except Exception as e:
            return render(request, 'slobodna_enciklopedija_ptica_srbije/kreiranje_clanka.html', { 'error_msg': 'Težina i veličina mora da bude pozitivan broj!', 'old_form': request.POST })

        # Ako je administrator/urednik uspešno napravio članak, redirektuj ga na stranicu članka.
        return redirect("show_article", article_id = new_article.id_clanka)
    else:
        # U slučaju da neko pokušava da uđe na stranicu (a to jedino može biti ili administrator ili urednik), onda renderuj mu formu za kreiranje članka.
        return render(request, 'slobodna_enciklopedija_ptica_srbije/kreiranje_clanka.html')


def show_article(request, article_id):
    """
    Funkcija za prikaz stranice za pregled jednog clanka. Dovlace se sve informacije o clanku iz baze.
    
    **Argumenti:**
    
        - ID clanka, dostavlja se kroz url.
        
    **Template:**
    
        - slobodna_enciklopedija_ptica_srbije/pregled_clanka.html
    
    **Rezultat:**
    
        - Prikaz stranice za pregled jednog clanka.
    """
    try:
        if request.method == 'GET':
            article = Clanak.objects.get(id_clanka=article_id)
            bird_table = PticaTabela.objects.get(id_clanka=article_id)

            if bird_table.slika_vrste is not None:
                bird_table.slika_vrste = base64.b64encode(bird_table.slika_vrste).decode('utf-8')
            else:
                bird_table.slika_vrste = None

            images_from_gallery = FotografijaGalerija.objects.filter(id_clanka=article)
            for image in images_from_gallery:
                image.sadrzaj_slike = base64.b64encode(image.sadrzaj_slike).decode('utf-8')

            discussions_with_comments = []
            discussions = Diskusija.objects.filter(id_clanka=article_id)
            for discussion in discussions:
                discussion_data = {
                    'diskusija': discussion,
                    'komentari': [],
                    'autorDiskusije': discussion.id_pokretaca.username
                }
                comments = Komentar.objects.filter(id_diskusije=discussion.id_diskusije)
                for comment in comments:
                    comment_data = {
                        'komentar': comment,
                        'autorKomentara': comment.id_korisnika.username
                    }
                    discussion_data['komentari'].append(comment_data)
                discussions_with_comments.append(discussion_data)

            avg_grade = article.zbir_ocena * 1.0 / article.broj_ocena if article.broj_ocena != 0 else 0
            if request.user.is_authenticated:
                user_grade = Ocena.objects.filter(id_korisnika=request.user, id_clanka=article)
                if user_grade.exists():
                    user_grade = user_grade[0].ocena
                else:
                    user_grade = 0
            else:
                user_grade = 0  # Da se omogući pristup članku i neautentifikovanim korisnicima

            if request.user.is_authenticated:
                was_registered = PrijavljenNaObavestenja.objects.filter(id_korisnika=request.user, id_clanka=article)
                if was_registered.exists():
                    show_want_to_register = 2
                else:
                    show_want_to_register = 1
            else:
                show_want_to_register = 0

            context = {
                'clanak': article,
                'pticaTabela': bird_table,
                'slikeGalerija': images_from_gallery,
                'diskusijeKomentari': discussions_with_comments,
                'avg_grade': avg_grade,
                'user_grade': user_grade,
                'show_want_to_register': show_want_to_register
            }
        return render(request, 'slobodna_enciklopedija_ptica_srbije/pregled_clanka.html', context)
    except: 
        return redirect("index")


@login_required(login_url='user_login')
def add_image_to_gallery(request):
    """
    Funkcija za dodavanje fotografije u galeriju
    
    Ako je GET zahtev vraca :template:`slobodna_enciklopedija_ptica_srbije/add_image_to_gallery.html`
    
    Ako je POST zahtev dodaje fotografiju u bazu i vraca :template:`slobodna_enciklopedija_ptica_srbije/show_article.html`
    
    **Argumenti:**
    
        - Argument POST zahteva je popunjena forma `slobodna_enciklopedija_ptica_srbije.forms.UploadImageToGalleryForm`
        - Argument GET zahteva je ID clanka
            
    """
    if request.method == 'POST':
        form = UploadImageToGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            article_id = form.cleaned_data['article_id']
            if request.POST.get('submit_type') == "Poništi":
                return redirect('show_article', article_id=article_id)
            image = form.cleaned_data['image']
            if image == None:
                return redirect('show_article', article_id=article_id)
            image_file = form.cleaned_data['image'].read()


            new_image_in_gallery = FotografijaGalerija()
            if is_valid_image(image_file):
                new_image_in_gallery.sadrzaj_slike = image_file
                new_image_in_gallery.id_clanka = Clanak.objects.get(
                    id_clanka=article_id)
                new_image_in_gallery.id_autora = request.user
                new_image_in_gallery.save()

            return redirect('show_article', article_id=article_id)
        else:
            context = {
                'article_id': form.cleaned_data['article_id'],
                'form': form,
                'error_msg': 'Tip fajla mora biti .jpeg, .jpg ili .png',
            }
            return render(request, 'slobodna_enciklopedija_ptica_srbije/dodavanje_slike_u_galeriju.html', context)
    else:
        article_id = request.GET.get('article_id')
        if article_id is None:
            return HttpResponseBadRequest("Missing 'article_id' parameter in the query string.")
        form = UploadImageToGalleryForm(initial={'article_id': article_id})
        context = {
            'article_id': article_id,
            'form': form,
            'error_msg': '',
        }
        return render(request, 'slobodna_enciklopedija_ptica_srbije/dodavanje_slike_u_galeriju.html', context)


@login_required(login_url='user_login')
@require_POST
def delete_image_from_gallery(request, image_id):
    """
    Funckija za brisanje fotografije iz galerije, predstavlja API poziv.
    
    **Argumenti:**
    
        - Argument zahteva je ID fotografije
        
    **Preduslov:**
    
        - Korisnik je autor slike ili urednik ili admin
        
    **Rezultat:**
    
        - Rezultat je JSON objekat sa statusom uspeha i porukom greske ako postoji
    """
    if image_id is not None:
        image = FotografijaGalerija.objects.get(id_fotografije=image_id)
        if request.user.tip == "A" or request.user.tip == 'U' or \
            request.user.tip =='R' and image.id_autora == request.user:
            messages = PrimljenePoruke.objects.filter(id_prijavljene_stvari=image_id, tip_prijave='F')
            message_id = -1
            for message in messages:
                message_id = message.id_poruke.id_poruke
                message.delete()

            #print(message_id)
            primary_message = Poruka.objects.filter(id_poruke=message_id)
            if primary_message:
                primary_message.delete()
            image.delete()
            return JsonResponse({'success': True})
        else:
            print("Niste autor slike")
            return JsonResponse({'success': False, 'msg': 'Niste autor slike'})
    return JsonResponse({'success': False, 'msg': 'Invalid data'})
    


from django.http import JsonResponse

@login_required(login_url='user_login')
@require_POST
def create_discussion(request):
    """
    Funkcija za kreiranje diskusije. Predstavlja API poziv.
    
    **Argumenti:**
    
        - Argument zahteva je JSON objekat sa podacima o diskusiji.
        
    **Rezultat:**
    
        - Rezultat je JSON objekat sa statusom uspeha i porukom greske ako postoji
        - Diskusija je dodata u bazu ako je ishod uspesan
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        article_id = data.get('article_id')
        discussion_title = data.get('discussion_title', '')
        discussion_content = data.get('discussion_content','')
        discussion_title = discussion_title.strip() if discussion_title !='' else 'Nema naslova'
        discussion_content = discussion_content.strip() if discussion_content !='' else 'Nema sadrzaja'
        try:
            article = get_object_or_404(Clanak, id_clanka=article_id)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        if article is not None:
            new_discussion = Diskusija()
            new_discussion.id_clanka = article
            new_discussion.id_pokretaca = request.user
            new_discussion.naslov_diskusije = discussion_title
            new_discussion.sadrzaj = discussion_content
            new_discussion.save()
            # print(str(new_discussion))
            return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid data'})


#@login_required(login_url='user_login')
@require_GET
def get_discussions_for_article(request, article_id):
    """
    Funkcija za prikaz diskusija. Predstavlja API poziv.
    
    **Argumenti:**
    
        - Argument zahteva je ID clanka. Dostavlja se kroz url.
        
    **Rezultat:**
    
        - Rezultat je JSON objekat sa podacima o diskusiji i komentarima za trazeni clanak
    """
    discussions = Diskusija.objects.filter(id_clanka=article_id).order_by('-datum_vreme_kreiranja')
    discussions_data = []
    for discussion in discussions:
        discussion_data = {
            'id_diskusije': discussion.id_diskusije,
            'komentari': [],
            'autorDiskusije': discussion.id_pokretaca.username,
            'naslov': discussion.naslov_diskusije,
            'sadrzaj': discussion.sadrzaj,
            'datumVreme': timezone.localtime(discussion.datum_vreme_kreiranja).strftime('%d.%m.%Y. %H:%M')
        }
        comments = Komentar.objects.filter(
            id_diskusije=discussion).order_by('datum_vreme_postavljanja')
        for comment in comments:
            comment_data = {
                'id_komentara': comment.id_komentara,
                'autorKomentara': comment.id_korisnika.username,
                'sadrzaj': comment.sadrzaj,
                'datumVreme': timezone.localtime(comment.datum_vreme_postavljanja).strftime('%d.%m.%Y. %H:%M')
            }
            discussion_data['komentari'].append(comment_data)
        discussions_data.append(discussion_data)
    return JsonResponse(discussions_data, safe=False)
    
    
@require_GET
def get_gallery_for_article(request, article_id):
    """
    Funkcija za prikaz fotografija. Predstavlja API poziv.
    
    **Argumenti:**
    
        - Argument zahteva je ID clanka. Dostavlja se kroz url.
        
    **Rezultat:**
    
        - Rezultat je JSON objekat sa podacima o fotografijama iz galerije za trazeni clanak
    """
    article = Clanak.objects.get(id_clanka=article_id)
    images = FotografijaGalerija.objects.filter(id_clanka=article).order_by('-datum_vreme_postavljanja')
    images_data = []
    for image in images:
        image_data = {
            'id_fotografije': image.id_fotografije,
            'sadrzaj_slike': base64.b64encode(image.sadrzaj_slike).decode('utf-8'),
            'username_autora': image.id_autora.username,
            'datum_vreme':timezone.localtime(image.datum_vreme_postavljanja).strftime('%d.%m.%Y. %H:%M')
        }
        images_data.append(image_data)
    return JsonResponse(images_data, safe=False)

@login_required(login_url='user_login')
@require_POST
def create_comment(request):
    """
    Funkcija za kreiranje komentara na neku diskusiju. Predstavlja API poziv.

    **Argumenti:**

        - Argumenti zahteva su ID diskusije i sadrzaj komentara. Dostavlja se kroz JSON objekat.
        
    **Rezultat:**

        - Rezultat je JSON objekat sa statusom uspeha i porukom greske ako postoji
    """
    data = json.loads(request.body)
    discussion_id = data.get('discussion_id','')
    comment_content = data.get('comment_content', 'Nema sadrzaja')
    comment_content = comment_content if comment_content!='' else 'Nema sadrzaja'
    try:
        discussion = get_object_or_404(Diskusija, id_diskusije=discussion_id)
    except Exception:
        return JsonResponse({'success': False, 'error': 'Invalid data'})
    if discussion is not None:
        new_comment = Komentar()
        new_comment.id_diskusije = discussion
        new_comment.id_korisnika = request.user
        new_comment.sadrzaj = comment_content
        new_comment.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid data'})

@login_required(login_url='user_login')
@specific_users_only(['A', 'U'])
@require_POST
def delete_discussion(request):
    """
    Funkcija za brisanje neke diskusije. Predstavlja API poziv.

    **Argumenti:**

        - Argument zahteva je ID diskusije. Dostavlja se kroz JSON objekat.
        
    **Rezultat:**

        - Rezultat je JSON objekat sa statusom uspeha i porukom greske ako postoji
        - U slucaju uspeha obrisane su i sve prijave nepravilnosti i svi komentari vezani za tu diskusiju
    """
    data = json.loads(request.body)
    discussion_id = data.get('discussion_id')
    if discussion_id is not None:
        comments = Komentar.objects.filter(id_diskusije=discussion_id)
        for comment in comments:
            comment_id = comment.id_komentara
            messages = PrimljenePoruke.objects.filter(id_prijavljene_stvari=comment_id, tip_prijave='K')
            message_id = -1
            for message in messages:
                message_id = message.id_poruke.id_poruke
                message.delete()
            primary_message = Poruka.objects.filter(id_poruke=message_id)
            if primary_message:
                primary_message.delete()
        dicussion = Diskusija.objects.get(id_diskusije=discussion_id)
        discussion_id = dicussion.id_diskusije
        messages = PrimljenePoruke.objects.filter(id_prijavljene_stvari=discussion_id, tip_prijave='D')
        message_id = -1
        for message in messages:
            message_id = message.id_poruke.id_poruke
            message.delete()
        #print(message_id)
        primary_message = Poruka.objects.filter(id_poruke=message_id)
        if primary_message:
            primary_message.delete()
        dicussion.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid data'})

@login_required(login_url='user_login')
@specific_users_only(['A', 'U'])
@require_POST
def delete_comment(request):
    """
    Funkcija za brisanje komentara. Predstavlja API poziv.
    
    **Argumenti:**

        - Argument zahteva je ID komentara. Dostavlja se kroz JSON objekat.
        
    **Rezultat:**

        - Rezultat je JSON objekat sa statusom uspeha i porukom greske ako postoji
        - U slucaju uspeha obrisane su i sve prijave nepravilnosti vezane za taj komentar
    """
    data = json.loads(request.body)
    comment_id = data.get('comment_id')
    if comment_id is not None:
        comment = Komentar.objects.get(id_komentara=comment_id)
        comment_id = comment.id_komentara
        messages = PrimljenePoruke.objects.filter(id_prijavljene_stvari=comment_id, tip_prijave='K')
        message_id = -1
        for message in messages:
            message_id = message.id_poruke.id_poruke
            message.delete()
        #print(message_id)
        primary_message = Poruka.objects.filter(id_poruke=message_id)
        if primary_message:
            primary_message.delete()
        comment.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid data'})

@login_required(login_url='user_login')
@require_POST
def alter_rating(request):
    """
    Funkcija za ocenjivanje clanka. Predstavlja API poziv.
    Ukoliko ocena tog korisnika za dati clanak vec postoji, brise se stara i dodaje nova, u suprotnom se dodaje nova.

    **Argumenti:**

        - Argumenti zahteva su ID clanka i nova ocena. Dostavljaju se kroz JSON objekat.
        
    **Rezultat:**

        - Rezultat je JSON objekat sa statusom uspeha i novom prosecnom ocenom clanka
    """
    data = json.loads(request.body)
    article_id = data.get('article_id')
    new_grade_value = data.get('grade')
    if article_id is None:
        return JsonResponse({'success': False, 'error': 'Clanak ne postoji'})
    if int(new_grade_value) < 1 or int(new_grade_value) > 10:
        return JsonResponse({'success': False, 'error': 'Ocena mora biti izmedju 1 i 10'})
    article = Clanak.objects.get(id_clanka=article_id)
    old_grade = Ocena.objects.filter(id_korisnika=request.user, id_clanka=article)
    if not old_grade.exists():
        # prvi put se dodaje ocena
        new_grade = Ocena()
        new_grade.id_korisnika = request.user
        new_grade.id_clanka = article
        new_grade.ocena = new_grade_value
        article.zbir_ocena += new_grade_value
        article.broj_ocena += 1
    else:
        # prethodno data ocena se menja
        old_grade_value = old_grade[0].ocena
        article.zbir_ocena -= old_grade_value
        article.broj_ocena -= 1
        old_grade.delete()
        new_grade = Ocena()
        new_grade.id_korisnika = request.user
        new_grade.id_clanka = article
        new_grade.ocena = new_grade_value
        article.zbir_ocena += new_grade_value
        article.broj_ocena += 1
        
    new_grade.save()
    article.save()
    avg_rating = article.zbir_ocena*1.0 / article.broj_ocena
    return JsonResponse({'success': True, 'avg_rating': avg_rating})
   
def get_avg_rating(request, article_id):
    """
    Funkcija za dohvatanje prosecne ocene clanka. Predstavlja API poziv.
    
    **Argumenti:**

        - Argument zahteva je ID clanka. Dostavlja se kroz url.
        
    **Rezultat:**

        - Rezultat je JSON objekat sa prosecnom ocenom clanka i statusom uspeha. Prosecna ocena je 0 u slucaju neuspeha
    """
    try:
        article = Clanak.objects.get(id_clanka=article_id)
        if article is None or article.broj_ocena == 0:
            return JsonResponse({'avg_rating': 0,'success':True})
        avg_rating = article.zbir_ocena*1.0 / article.broj_ocena
        return JsonResponse({'avg_rating': avg_rating, 'success':True})
    except:
        return JsonResponse({'avg_rating': 0, 'success':False})
    
@login_required(login_url='user_login')
@require_POST
@specific_users_only(['A', 'U'])
def change_article_text(request):
    """
    Funkcija za izmenu sadrzaja clanka. Predstavlja API poziv.
    
    **Argumenti:**

        - Argumenti zahteva su ID clanka i novi sadrzaj. Dostavljaju se kroz JSON objekat.
        
    **Rezultat:**

        - Rezultat je JSON objekat sa statusom uspeha
        - Takodje se salju mejl obavestenja i poruke obavestenja koirsnicima koji prate izmene clanka
    """
    data = json.loads(request.body)
    article_id = data.get('article_id')
    new_text = data.get('new_text')
    if article_id is None:
        return JsonResponse({'success': False, 'error': 'Clanak ne postoji'})
    article = Clanak.objects.get(id_clanka=article_id)
    if article.id_autora != request.user and request.user.tip != 'A':
        return JsonResponse({'success': False, 'error': 'Niste autor clanka'})
    article.sadrzaj = new_text
    article.save()

    # slanje mejlova i obaveštenja

    users_to_send_email = PrijavljenNaObavestenja.objects.filter(id_clanka=article, primaj_na_mail=1)
    user_to_send_notification = PrijavljenNaObavestenja.objects.filter(id_clanka=article)

    subject = "Izmenjen tekst članka"
    url = "http://127.0.0.1:8000/pregled_clanka/" + str(article_id)
    type_of_reason = "Izmenjen tekst članka"
    title = PticaTabela.objects.get(id_clanka=article_id)
    title = title.vrsta

    context = {
        "type": type_of_reason,
        "id_article": article,
        "url": url,
        "title": title
    }

    mails = set()
    for user in users_to_send_email:
        usr = user.id_korisnika
        mails.add(usr.email)

    if len(mails) > 0:
        html_message = render_to_string("slobodna_enciklopedija_ptica_srbije/email_article_change_text.html", context)
        plain_message = strip_tags(html_message)
        email_thread = threading.Thread(target=send_email, args=(subject, plain_message, html_message, list(mails)))
        email_thread.start()

    send_to = set()
    message = Poruka()
    message.tekst = "Izmenjen je tekst sledećeg članka"
    message.save()
    for user_notif in user_to_send_notification:
        send_to.add(user_notif.id_korisnika.id)
        received_message = PrimljenePoruke()
        received_message.id_poruke = message
        received_message.id_korisnika = user_notif.id_korisnika
        received_message.procitana = 0
        received_message.id_prijavljene_stvari = article_id
        received_message.tip_prijave = 'C'
        received_message.save()

    return JsonResponse({'success': True})

@login_required(login_url='user_login')
@require_POST
@specific_users_only(['A', 'U'])
def change_article_table(request):
    """
    Funkcija za izmenu informacija o tabeli. Predstavlja API poziv.
    
    **Argumenti:**

        - Argumenti zahteva su ID clanka i novi sadrzaj tabele. Dostavljaju se kroz JSON objekat.
        
    **Rezultat:**

        - Rezultat je JSON objekat sa statusom uspeha
        - Takodje se salju mejl obavestenja i poruke obavestenja koirsnicima koji prate izmene clanka
    """
    data = json.loads(request.body)
    article_id = data.get('article_id')
    vrsta = data.get('vrsta')
    rod = data.get('rod')
    porodica = data.get('porodica')
    red = data.get('red')
    klasa = data.get('klasa')
    tip = data.get('tip')
    carstvo = data.get('carstvo')
    velicina = float(data.get('velicina') if data.get('velicina')!="" else 0.0)
    tezina = float(data.get('tezina') if data.get('tezina')!="" else 0.0)
    status_ugrozenosti = data.get('status')
    if article_id is None:
        return JsonResponse({'success': False, 'error': 'Clanak ne postoji'})
    article = Clanak.objects.get(id_clanka=article_id)
    if article.id_autora != request.user and request.user.tip != 'A':
        return JsonResponse({'success': False, 'error': 'Niste autor clanka'})
    tabela_informacija = PticaTabela.objects.get(id_clanka=article_id)
    tabela_informacija.vrsta = vrsta
    tabela_informacija.rod = rod
    tabela_informacija.porodica = porodica
    tabela_informacija.red = red
    tabela_informacija.klasa = klasa
    tabela_informacija.tip = tip
    tabela_informacija.carstvo = carstvo
    tabela_informacija.tezina = tezina
    tabela_informacija.velicina = velicina
    tabela_informacija.status_ugrozenosti = status_ugrozenosti
    tabela_informacija.save()

    # slanje mejlova i obaveštenja

    users_to_send_email = PrijavljenNaObavestenja.objects.filter(id_clanka=Clanak.objects.get(id_clanka=article_id), primaj_na_mail=1)
    user_to_send_notification = PrijavljenNaObavestenja.objects.filter(id_clanka=Clanak.objects.get(id_clanka=article_id))

    subject = "Izmenjene informacije u tabeli članka"
    url = "http://127.0.0.1:8000/pregled_clanka/" + str(article_id)
    type_of_reason = "Izmenjene informacije u tabeli članka"
    title = tabela_informacija.vrsta
    context = {
        "type": type_of_reason,
        "id_article": article_id,
        "url": url,
        "title": title
    }

    mails = set()
    for user in users_to_send_email:
        usr = user.id_korisnika
        mails.add(usr.email)

    if len(mails) > 0:
        html_message = render_to_string("slobodna_enciklopedija_ptica_srbije/email_article_change_text.html", context)
        plain_message = strip_tags(html_message)
        email_thread = threading.Thread(target=send_email, args=(subject, plain_message, html_message, list(mails)))
        email_thread.start()

    send_to = set()
    message = Poruka()
    message.tekst = "Izmenjene informacije u tabeli sledećeg članka"
    message.save()
    for user_notif in user_to_send_notification:
        send_to.add(user_notif.id_korisnika.id)
        received_message = PrimljenePoruke()
        received_message.id_poruke = message
        received_message.id_korisnika = user_notif.id_korisnika
        received_message.procitana = 0
        received_message.id_prijavljene_stvari = article_id
        received_message.tip_prijave = 'C'
        received_message.save()


    return JsonResponse({'success': True})


@login_required(login_url='user_login')
@require_POST
@specific_users_only(['A', 'U'])
def change_table_image(request):
    """
    Funkcija za izmenu slike u tabeli informacija. Predstavlja API poziv.
    
    **Argumenti:**

        - Argumenti zahteva su ID clanka i novi slika. Dostavljaju se kroz JSON objekat.

    **Rezultat:**

        - Rezultat je JSON objekat sa statusom uspeha i porukom greske ako postoji, ili osvezavanje stranice za pregled clanka, ako je uspesno
        - Takodje se salju mejl obavestenja i poruke obavestenja koirsnicima koji prate izmene clanka
    """
    data = request.POST
    article_id = data.get('article_id')
    file = request.FILES.get('image')
    image_file = file.read()
    if article_id is None:
        return JsonResponse({'success': False, 'error': 'Clanak ne postoji'})
    
    try:
        article = Clanak.objects.get(id_clanka=article_id)
        if article.id_autora != request.user and request.user.tip != 'A':
            return JsonResponse({'success': False, 'error': 'Niste autor clanka'})
        tabela_informacija = PticaTabela.objects.get(id_clanka=article_id)
        if is_valid_image(image_file):  
            tabela_informacija.slika_vrste = image_file
            tabela_informacija.save()


            # SEND EMAIL AND NOTIFICATIONS

            users_to_send_email = PrijavljenNaObavestenja.objects.filter(id_clanka=Clanak.objects.get(id_clanka=article_id),
                                                                         primaj_na_mail=1)
            user_to_send_notification = PrijavljenNaObavestenja.objects.filter(
                id_clanka=Clanak.objects.get(id_clanka=article_id))

            subject = "Izmenjena fotografija u tabeli članka"
            url = "http://127.0.0.1:8000/pregled_clanka/" + str(article_id)
            type_of_reason = "Izmenjena fotografija u tabeli članka"
            title = tabela_informacija.vrsta
            context = {
                "type": type_of_reason,
                "id_article": article_id,
                "url": url,
                "title": title
            }

            mails = set()
            for user in users_to_send_email:
                usr = user.id_korisnika
                mails.add(usr.email)

            if len(mails) > 0:
                html_message = render_to_string("slobodna_enciklopedija_ptica_srbije/email_article_change_text.html",
                                                context)
                plain_message = strip_tags(html_message)
                email_thread = threading.Thread(target=send_email, args=(subject, plain_message, html_message, list(mails)))
                email_thread.start()

            send_to = set()
            message = Poruka()
            message.tekst = "Izmenjena fotografija u tabeli članka"
            message.save()
            for user_notif in user_to_send_notification:
                send_to.add(user_notif.id_korisnika.id)
                received_message = PrimljenePoruke()
                received_message.id_poruke = message
                received_message.id_korisnika = user_notif.id_korisnika
                received_message.procitana = 0
                received_message.id_prijavljene_stvari = article_id
                received_message.tip_prijave = 'C'
                received_message.save()

            return redirect('show_article', article_id=article_id)
        else:
            return redirect('show_article', article_id=article_id)
            #return JsonResponse({'success': False, 'error': 'Nije validna slika'})
    except:
        return JsonResponse({'success': False, 'error': 'Clanak ne postoji'})
        


@login_required(login_url='user_login')
@require_POST
@specific_users_only(['A', 'U'])    
def delete_table_image(request):
    """
    Funkcija za brisanje slike u tabeli informacija. Predstavlja API poziv.
    
    **Argumenti:**

        - Argument zahteva je ID clanka. Dostavlja se kroz JSON objekat.

    **Rezultat:**

        - Rezultat je JSON objekat sa statusom uspeha i porukom greske ako postoji
        - Takodje se salju mejl obavestenja i poruke obavestenja korisnicima koji prate izmene clanka
    """
    data = json.loads(request.body)
    article_id = data.get('article_id')
    if article_id is None:
        return JsonResponse({'success': False, 'error': 'Clanak ne postoji'})
    article = Clanak.objects.get(id_clanka=article_id)
    if article.id_autora != request.user and request.user.tip != 'A':
        return JsonResponse({'success': False, 'error': 'Niste autor clanka'})
    tabela_informacija = PticaTabela.objects.get(id_clanka=article_id)
    tabela_informacija.slika_vrste = None
    tabela_informacija.save()
    
    # SEND EMAIL AND NOTIFICATIONS

    users_to_send_email = PrijavljenNaObavestenja.objects.filter(id_clanka=Clanak.objects.get(id_clanka=article_id),
                                                                    primaj_na_mail=1)
    user_to_send_notification = PrijavljenNaObavestenja.objects.filter(
        id_clanka=Clanak.objects.get(id_clanka=article_id))

    subject = "Izmenjena fotografija u tabeli članka"
    url = "http://127.0.0.1:8000/pregled_clanka/" + str(article_id)
    type_of_reason = "Izmenjena fotografija u tabeli članka"
    title = tabela_informacija.vrsta
    context = {
        "type": type_of_reason,
        "id_article": article_id,
        "url": url,
        "title": title
    }

    mails = set()
    for user in users_to_send_email:
        usr = user.id_korisnika
        mails.add(usr.email)

    if len(mails) > 0:
        html_message = render_to_string("slobodna_enciklopedija_ptica_srbije/email_article_change_text.html",
                                        context)
        plain_message = strip_tags(html_message)
        email_thread = threading.Thread(target=send_email, args=(subject, plain_message, html_message, list(mails)))
        email_thread.start()

    send_to = set()
    message = Poruka()
    message.tekst = "Izmenjena fotografija u tabeli članka"
    message.save()
    for user_notif in user_to_send_notification:
        send_to.add(user_notif.id_korisnika.id)
        received_message = PrimljenePoruke()
        received_message.id_poruke = message
        received_message.id_korisnika = user_notif.id_korisnika
        received_message.procitana = 0
        received_message.id_prijavljene_stvari = article_id
        received_message.tip_prijave = 'C'
        received_message.save()
    return JsonResponse({'success': True})

@login_required(login_url='user_login')
def report_irregularity_photograph_get(request, id_img):
    """
    Funkcija za prikaz stranice za prijavu nepravilnosti fotografije. Predstavlja API poziv.
    
    **Argumenti:**

        - Argument zahteva je ID fotografije. Dostavlja se kroz url.
        
    **Template:**

        - slobodna_enciklopedija_ptica_srbije/prijava_nepravilnosti_galerija.html

    **Rezultat:**

        - Rezultat je prikaz stranice za prijavu nepravilnosti fotografije.
    """
    reasons = RazlogPrijaveFotografije.objects.all()
    context={
        "idPhotograph":id_img,
        "reasons":reasons
    }
    return render(request, "slobodna_enciklopedija_ptica_srbije/prijava_nepravilnosti_galerija.html", context)

@login_required(login_url='user_login')
def report_irregularity_photograph_page(request):
    """
    Funckija za proveru da li slika za koju se prijavljuje nerpavilnost postoji. Predstavlja API poziv.
    
    **Argumenti:**

        - Argument zahteva je ID fotografije. Dostavlja se kroz JSON objekat.
        
    **Rezultat:**

        - JSON objekat sa statusom uspeha i porukom greske ako postoji
    """
    data = json.loads(request.body)
    id_ph = data.get('imageId')
    if id_ph is None:
        return JsonResponse({'success': False, 'error': 'Fotografija ne postoji'})
    else:
        return JsonResponse({'success': True})

@login_required(login_url='user_login')
@require_POST
def report_irregularity_photograph_confirm(request):
    """
    Funkcija za prijavu nepravilnosti fotografije. Predstavlja API poziv.
    
    **Argumenti:**

        - Argumenti zahteva su ID fotografije, razlog prijave i username korisnika. Dostavljaju se kroz JSON objekat.
        
    **Rezultat:**

        - Rezultat je JSON objekat sa statusom uspeha
        - U slucaju uspeha dodaju se nepravilnost fotografije i prijava nepravilnosti u bazu
        - U slucaju uspeha salju se mejl obavestenja i poruke obavestenja adminima i autoru clanka
    """
    try:
        data = json.loads(request.body)
        id_ph = data.get('imageId')
        id_reason = data.get("reason")
        id_user = data.get("username")
        if id_ph is None or id_reason is None:
            return JsonResponse({"success":False, 'error':'Fotografija ili razlog ili korisnicko ime ne postoji'})
        new_report = NepravilnostFotografija()
        ph = FotografijaGalerija.objects.get(id_fotografije=id_ph)
        reason = RazlogPrijaveFotografije.objects.get(id_razlog_fotografija=id_reason)
        user = Korisnik.objects.get(username=id_user)
        report = PrijavaNepravilnosti()
        report.id_korisnika = user
        report.save()
        new_report.id_prijave = report
        new_report.id_fotografije = ph
        new_report.id_razlog_fotografija = reason
        new_report.save()
        subject = "Prijavljena nepravilnost fotografije"

        photo = FotografijaGalerija.objects.get(id_fotografije=id_ph)
        article = photo.id_clanka
        id_article = article.id_clanka
        title = PticaTabela.objects.get(id_clanka=id_article)

        url = "http://127.0.0.1:8000/pregled_clanka/" + str(id_article)
        type_of_reason = "Prijavljena nepravilnost fotografije"
        context = {
            "type": type_of_reason,
            "id_article": article,
            "reason": reason,
            "url": url,
            "photo": photo,
            "title":title.vrsta
        }
        html_message = render_to_string("slobodna_enciklopedija_ptica_srbije/email_photo.html", context)
        editor_email = article.id_autora.email
        admins = Korisnik.objects.all().filter(tip='A')
        mails = set()

        mails.add(editor_email)
        for admin in admins:
            mails.add(admin.email)
        plain_message = strip_tags(html_message)
        email_thread = threading.Thread(target=send_email, args=(subject, plain_message, html_message, list(mails)))
        email_thread.start()

        send_to = set()

        message = Poruka()
        message.tekst = "Prijavljena je nepravilnost fotografije " + str(id_ph) + " sa razlogom " + str(reason.opis)
        message.save()
        for admin in admins:
            send_to.add(admin.id)
            received_message = PrimljenePoruke()
            received_message.id_poruke = message
            received_message.id_korisnika = admin
            received_message.procitana = 0
            received_message.id_prijavljene_stvari = id_ph
            received_message.tip_prijave = 'F'
            received_message.save()
        if article.id_autora.id not in send_to:
            editor_message = PrimljenePoruke()
            editor_message.id_poruke = message
            editor_message.id_korisnika = article.id_autora
            editor_message.procitana = 0
            editor_message.id_prijavljene_stvari = id_ph
            editor_message.tip_prijave = 'F'
            editor_message.save()

        return JsonResponse({'success': True})
    except:
        return JsonResponse({"success":False, 'error':'Fotografija ili razlog ili korisnicko ime ne postoji'})

@login_required(login_url='user_login')
def report_irregularity_comment_get(request, id_comm):
    """
    Funkcija za prikaz stranice za prijavu nepravilnosti komentara.
    
    **Argumenti:**

        - Argument je ID komentara. Dostavlja se kroz url.
        
    **Template:**
    
        - slobodna_enciklopedija_ptica_srbije/prijava_nepravilnosti_komentar.html
        
    **Rezultat:**
    
        - Rezultat je prikaz stranice za prijavu nepravilnosti komentara.
    """
    reasons = RazlogPrijaveKomentar.objects.all()
    numOfReasons=len(reasons)
    context={
        "idComm":id_comm,
        "idDiscuss":-1,
        "reasons":reasons,
        "num_of_reasons":numOfReasons
    }
    return render(request, "slobodna_enciklopedija_ptica_srbije/prijava_nepravilnosti_komentar.html", context)

@login_required(login_url='user_login')
def report_irregularity_comment_page(request):
    """
    Funkcija za proveru da li komentar za koji se prijavljuje nepravilnost postoji. Predstavlja API poziv.
    
    **Argumenti:**

        - Argument zahteva je ID komentara. Dostavlja se kroz JSON objekat.
        
    **Rezultat:**
    
        - JSON objekat sa statusom uspeha i porukom greske ako postoji.
    """
    data = json.loads(request.body)
    id_comm = data.get('idComm')
    if id_comm is None:
        return JsonResponse({'success': False, 'error': 'Komentar ne postoji'})
    else:
        return JsonResponse({'success': True})

@login_required(login_url='user_login')
@require_POST
def report_irregularity_comment_confirm(request):
    """
    Funkcija za prijavu nepravilnosti komentara. Predstavlja API poziv.
    
    **Argumenti:**

        - Argumenti zahteva su ID komentara, razlog prijave i korisnicko ime korisnika. Dostavljaju se kroz JSON objekat.
        
    **Rezultat:**
    
        - JSON objekat sa statusom uspeha i porukom greske ako postoji.
        - U slucaju uspeha dodaju se prijava nepravilnosti i nepravilnost komentara u bazu.
        - Takodje se salju mejl obavestenja i poruke obavestenja adminima i autoru clanka.
    """
    try:
        data = json.loads(request.body)
        id_comm = data.get('idComm')
        id_reason = data.get("reason")
        id_user = data.get("username")
        if id_comm is None or id_reason is None:
            return JsonResponse({"success":False, 'error':'Niste dostavili sve podatke!'})
        new_report = NepravilnostKomentar()
        comm = Komentar.objects.get(id_komentara=id_comm)
        reason = RazlogPrijaveKomentar.objects.get(id_razlog_komentar=id_reason)
        user = Korisnik.objects.get(username=id_user)
        report = PrijavaNepravilnosti()
        report.id_korisnika = user
        report.save()
        new_report.id_prijave = report
        new_report.id_komentara = comm
        new_report.id_razlog_komentar = reason
        new_report.save()
        subject = "Prijavljena nepravilnost komentara"

        comment = Komentar.objects.get(id_komentara=id_comm)
        article = comment.id_diskusije.id_clanka
        id_article = article.id_clanka
        url = "http://127.0.0.1:8000/pregled_clanka/" + str(id_article)
        type_of_reason = "Prijavljena nepravilnost komentara"
        title = PticaTabela.objects.get(id_clanka=id_article)
        context = {
            "type": type_of_reason,
            "id_article": article,
            "reason": reason,
            "url": url,
            "comment": comment,
            "title":title.vrsta
        }
        html_message = render_to_string("slobodna_enciklopedija_ptica_srbije/email_comment.html", context)
        editor_email = article.id_autora.email
        admins = Korisnik.objects.all().filter(tip='A')
        mails = set()
        mails.add(editor_email)
        for admin in admins:
            mails.add(admin.email)
        plain_message = strip_tags(html_message)
        email_thread = threading.Thread(target=send_email, args=(subject, plain_message, html_message, list(mails)))
        email_thread.start()

        send_to = set()

        message = Poruka()
        message.tekst = "Prijavljena je nepravilnost komentara " + str(comment.sadrzaj) + " sa razlogom " + str(reason.opis)
        message.save()
        for admin in admins:
            send_to.add(admin.id)
            received_message = PrimljenePoruke()
            received_message.id_poruke = message
            received_message.id_korisnika = admin
            received_message.procitana = 0
            received_message.id_prijavljene_stvari = id_comm
            received_message.tip_prijave = 'K'
            received_message.save()
        if article.id_autora.id not in send_to:
            editor_message = PrimljenePoruke()
            editor_message.id_poruke = message
            editor_message.id_korisnika = article.id_autora
            editor_message.procitana = 0
            editor_message.id_prijavljene_stvari = id_comm
            editor_message.tip_prijave = 'K'
            editor_message.save()

        return JsonResponse({'success': True})
    except:
        return JsonResponse({"success":False, 'error':'Niste dostavili sve podatke!'})


@login_required(login_url='user_login')
def report_irregularity_discussion_get(request, id_discuss):
    """
    Funkcija za prikaz stranice za prijavu nepravilnosti diskusije.
    
    **Argumenti:**

        - Argument zahteva je ID diskusije. Dostavlja se kroz url.
        
    **Template:**
    
        - slobodna_enciklopedija_ptica_srbije/prijava_nepravilnosti_komentar.html
        
    **Rezultat:**
    
        - Prikaz stranice za prijavu nepravilnosti diskusije.
    """
    reasons = RazlogPrijaveDiskusija.objects.all()

    numOfReasons = len(reasons)
    context = {
        "idComment": -1,
        "idDiscuss": id_discuss,
        "reasons": reasons,
        "num_of_reasons": numOfReasons
    }
    return render(request, "slobodna_enciklopedija_ptica_srbije/prijava_nepravilnosti_komentar.html", context)

@login_required(login_url='user_login')
def report_irregularity_discussion_page(request):
    """
    Funkcija za proveru da li diskusija za koju se prijavljuje nepravilnost postoji. Predstavlja API poziv.
    
    **Argumenti:**

        - Argument zahteva je ID diskusije. Dostavlja se kroz JSON objekat.
        
    **Rezultat:**
    
        - JSON objekat sa statusom uspeha i porukom greske ako postoji.
    """
    data = json.loads(request.body)
    id_discuss = data.get('idDiscuss')
    if id_discuss is None:
        return JsonResponse({'success': False, 'error': 'Diskusija ne postoji'})
    else:
        return JsonResponse({'success': True})

@login_required(login_url='user_login')
@require_POST
def report_irregularity_discussion_confirm(request):
    """
    Funkcija za potvrdu prijave nepravilnosti diskusije. Predstavlja API poziv.
    
    **Argumenti:**

        - Argumenti zahteva su ID diskusije, razlog prijave i username korisnika. Dostavljaju se kroz JSON objekat.
        
    **Rezultat:**
    
        - Rezultat je JSON objekat sa statusom uspeha
        - U slucaju uspeha dodaju se nepravilnost diskusije i prijava nepravilnosti u bazu.
        - Takodje se salju mejl obavestenja i poruke obavestenja adminima i autoru clanka.
    """
    try:
        data = json.loads(request.body)
        id_discuss = data.get('idDiscuss')
        id_reason = data.get("reason")
        id_user = data.get("username")
        if id_discuss is None or id_reason is None:
            return JsonResponse({"success":False, 'error':'Niste dostavili sve podatke!'})
        new_report = NepravilnostDiskusija()
        discuss = Diskusija.objects.get(id_diskusije=id_discuss)
        reason = RazlogPrijaveDiskusija.objects.get(id_razlog_diskusija=id_reason)
        user = Korisnik.objects.get(username=id_user)
        report = PrijavaNepravilnosti()
        report.id_korisnika = user
        report.save()
        new_report.id_prijave = report
        new_report.id_diskusije = discuss
        new_report.id_razlog_diskusija = reason
        new_report.save()
        # sending email to admins and to the editor of article

        subject = "Prijavljena nepravilnost diskusije"

        discussion = Diskusija.objects.get(id_diskusije=id_discuss)
        article = discussion.id_clanka
        id_article = article.id_clanka
        #print("HERE before email send")
        url = "http://127.0.0.1:8000/pregled_clanka/"+str(id_article)
        type_of_reason = "Prijavljena nepravilnost diskusije"
        title = PticaTabela.objects.get(id_clanka=id_article)
        context = {
            "type": type_of_reason,
            "id_article": id_article,
            "reason": reason,
            "url": url,
            "discussion": discussion,
            "title":title.vrsta
        }
        html_message = render_to_string("slobodna_enciklopedija_ptica_srbije/email_discussion.html", context)
        editor_email = article.id_autora.email
        admins = Korisnik.objects.all().filter(tip='A')
        mails = set()
        mails.add(editor_email)
        for admin in admins:
            mails.add(admin.email)
        plain_message = strip_tags(html_message)
        email_thread = threading.Thread(target=send_email, args=(subject, plain_message, html_message, list(mails)))
        email_thread.start()
        send_to = set()

        message = Poruka()
        message.tekst = "Prijavljena je nepravilnost diskusije " + str(discussion.naslov_diskusije) + " sa razlogom " + str(reason.opis)
        message.save()
        for admin in admins:
            send_to.add(admin.id)
            received_message = PrimljenePoruke()
            received_message.id_poruke = message
            received_message.id_korisnika = admin
            received_message.procitana = 0
            received_message.id_prijavljene_stvari = id_discuss
            received_message.tip_prijave = 'D'
            received_message.save()
        if article.id_autora.id not in send_to:
            editor_message = PrimljenePoruke()
            editor_message.id_poruke = message
            editor_message.id_korisnika = article.id_autora
            editor_message.procitana = 0
            editor_message.id_prijavljene_stvari = id_discuss
            editor_message.tip_prijave = 'D'
            editor_message.save()


        return JsonResponse({'success': True})
    except:
        return JsonResponse({"success":False, 'error':'Niste dostavili sve podatke!'})



@login_required(login_url='user_login')
def track_changes_on_article_page(request):
    """
    Funkcija za proveru da li clanak na cije pracenje korisnik zeli da se prijavi i dalje postoji. Predstavlja API poziv.
    
    **Argumenti:**

        - Argument zahteva je ID clanka. Dostavljaju se kroz JSON objekat.
        
    **Rezultat:**
    
        - Rezultat je JSON objekat sa statusom uspeha i porukom greske ako postoji
    """
    try:
        data = json.loads(request.body)
        id_article = data.get('article')
        if id_article is None:
            return JsonResponse({'success': False, 'error': 'Nedostaje ID clanka'})
        
        # Check if the article exists
        article = get_object_or_404(Clanak, id_clanka=id_article)
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required(login_url='user_login')
def track_changes_on_article(request, id_article):
    """
    Funckija za prikaz stranice za prijavu na obavestenja.
    
    **Argumenti:**

        - Argument zahteva je ID clanka. Dostavlja se kroz url.
        
    **Template:**
    
        - slobodna_enciklopedija_ptica_srbije/prijava_na_obavestenja.html
        
    **Rezultat:**
    
        - Prikaz stranice za prijavu na obavestenja.
    """
    if request.user.is_authenticated:
        if request.user.email:
            show_question = 1
        else:
            show_question = 0
    else:
        show_question = 0
    context = {
        "id_article": id_article,
        "show_question": show_question
    }
    return render(request, "slobodna_enciklopedija_ptica_srbije/prijava_na_obavestenja.html", context)


@login_required(login_url='user_login')
@require_POST
def track_changes_on_article_confirm(request):
    """
    Funkcija za prijavu na pracenje obavestenja za odgovarajuci clanak. Predstavlja API poziv.
    
    **Argumenti:**

        - Argumenti zahteva su ID clanka i informacija da li se primaju obavestenja i na mejl. Dostavljaju se kroz JSON objekat.
        
    **Rezultat:**
    
        - JSON objekat sa statusom uspeha i porukom greske ako postoji.
        - U slucaju uspeha prijava na obavestenja se dodaje u bazu.
    """
    data = json.loads(request.body)
    id_article = data.get('id_article')
    get_on_email = data.get("get_on_email")
    if id_article is None or get_on_email is None:
        return JsonResponse({"success": False, 'error': 'Clanak ne postoji, doslo je do greske'})
    try:
        article = get_object_or_404(Clanak, id_clanka=id_article)

        new_track = PrijavljenNaObavestenja()
        new_track.id_clanka = article
        new_track.primaj_na_mail=get_on_email
        new_track.id_korisnika = request.user
        new_track.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, 'error': str(e)})

def check_if_already_track(request):
    """
    Funkcija za proveru da li je korisnik vec prijavljen na pracenje obavestenja za odgovarajuci clanak. Predstavlja API poziv.
    
    **Argumenti:**

        - Argument zahteva je ID clanka. Dostavlja se kroz JSON objekat.
        
    **Rezultat:**
    
        - JSON objekat sa statusom uspeha i porukom greske ako postoji.
    """
    data = json.loads(request.body)
    article_id = data.get('article')
    try:
        article = get_object_or_404(Clanak, id_clanka=article_id)
        if request.user.is_authenticated:
            was_registered = PrijavljenNaObavestenja.objects.filter(id_korisnika=request.user, id_clanka=article)
            if was_registered.exists():
                show_want_to_register = 0
            else:
                show_want_to_register = 1
        else:
            show_want_to_register = 0

        if show_want_to_register==1:
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "You already follow changes"})
    except Exception as e:
        return JsonResponse({"success": False, 'error': str(e)})

@login_required(login_url='user_login')
def stop_tracking_article_changes(request):
    """
    Funckija za odjavljivanje korisnika sa prijavljenih na obavestenja. Predstavlja API poziv.
    
    **Argumenti:**

        - Argument zahteva je ID clanka. Dostavlja se kroz JSON objekat.
        
    **Rezultat:**
    
        - JSON objekat sa statusom uspeha i porukom greske ako postoji.
        - U slucaju uspeha prijava na obavestenja korisnika se brise iz baze.
    """
    data = json.loads(request.body)
    id_article = data.get('article')

    if id_article is None:
        return JsonResponse({'success': False, 'error': 'Pristupa sa nepostojecem clanku'})

    #PrijavljenNaObavestenja.objects.filter(id_clanka=id_article).get(id_korisnika=request.user.id).delete()
    subscription = PrijavljenNaObavestenja.objects.filter(id_clanka=id_article, id_korisnika=request.user)
    if subscription.exists():
        subscription.delete()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "error": "You don't follow changes"})


@login_required(login_url='user_login')
def report_irregularity_article_get(request, id_article):
    """
    Funckija za prikaz stranice za prijavu nepravilnosti clanka.
    
    **Argumenti:**

        - Argument zahteva je ID clanka. Dostavlja se kroz url.
        
    **Template:**
    
        - slobodna_enciklopedija_ptica_srbije/prijava_nepravilnosti_clanak.html
        
    **Rezultat:**
    
        - Prikaz stranice za prijavu nepravilnosti clanka.
    """
    context = {
        "id_article":id_article
    }
    return render(request, "slobodna_enciklopedija_ptica_srbije/prijava_nepravilnosti_clanak.html", context)

@login_required(login_url='user_login')
def report_irregularity_article_page(request):
    """
    Funkcija za proveru da li clanak za koji se prijavljuje nepravilnost postoji. Predstavlja API poziv.
    
    **Argumenti:**

        - Argument zahteva je ID clanka. Dostavlja se kroz JSON objekat.
        
    **Rezultat:**
    
        - JSON objekat sa statusom uspeha i porukom greske ako postoji.
    """
    data = json.loads(request.body)
    id_article = data.get('article')
    if id_article is None:
        return JsonResponse({'success': False, 'error': 'Artikal ne postoji'})
    else:
        return JsonResponse({'success': True})

@login_required(login_url='user_login')
@require_POST
def report_irregularity_article_confirm(request):
    """
    Funkcija za prijavu nepravilnosti sadrzaja clanka. Predstavlja API poziv.
    
    **Argumenti:**

        - Argumenti zahteva su ID clanka i razlog prijave. Dostavljaju se kroz JSON objekat.
        
    **Rezultat:**
    
        - JSON objekat sa statusom uspeha i porukom greske ako postoji.
        - Takodje se salju mejl obavestenja i poruke obavestenja adminima i autoru clanka.
    """

    try:
        data = json.loads(request.body)
        id_article = data.get('id_article')
        reason = data.get("reason")
        if id_article is None or reason is None:
            return JsonResponse({"success":False, 'error':'Clanak ili razlog prijave nije naveden'})
        new_report = NepravilnostClanak()
        article = Clanak.objects.get(id_clanka=id_article)
        report = PrijavaNepravilnosti()
        report.id_korisnika = request.user

        report.save()
        new_report.id_prijave  = report
        new_report.id_clanka = article
        new_report.opis = reason
        new_report.save()
        subject = "Prijavljena nepravilnost članka"
        url = "http://127.0.0.1:8000/pregled_clanka/"+str(id_article)
        type_of_reason = "Prijavljena nepravilnost članka"
        title = PticaTabela.objects.get(id_clanka=id_article)
        context = {
            "type": type_of_reason,
            "id_article": id_article,
            "reason": reason,
            "url": url,
            "title":title.vrsta
        }
        html_message = render_to_string("slobodna_enciklopedija_ptica_srbije/email_article.html", context)
        editor_email = article.id_autora.email
        admins = Korisnik.objects.all().filter(tip='A')
        mails = set()
        mails.add(editor_email)
        for admin in admins:
            mails.add(admin.email)
        plain_message = strip_tags(html_message)
        email_thread = threading.Thread(target=send_email, args=(subject, plain_message, html_message, list(mails)))
        email_thread.start()


        editor = article.id_autora
        admins = Korisnik.objects.all().filter(tip='A')
        send_to = set()
        message = Poruka()
        message.tekst = "Prijavljena je nepravilnost " + str(reason) + " za ovaj članak."
        message.save()
        for admin in admins:
            send_to.add(admin.id)
            received_message = PrimljenePoruke()
            received_message.id_poruke = message
            received_message.id_korisnika = admin
            received_message.procitana = 0
            received_message.id_prijavljene_stvari = id_article
            received_message.tip_prijave = 'C'
            received_message.save()
        if editor.id not in send_to:
            editor_message = PrimljenePoruke()
            editor_message.id_poruke = message
            editor_message.id_korisnika = editor
            editor_message.procitana = 0
            editor_message.id_prijavljene_stvari = id_article
            editor_message.tip_prijave = 'C'
            editor_message.save()

        return JsonResponse({'success': True})
    except: 
        return JsonResponse({'success': False})

@login_required(login_url='user_login')
def notifications(request):
    """
    Funkcija za prikaz obavestenja.
    
    **Argumenti:**

        - Implicitno se prenosi username ulogovanog korisnika.
        
    **Template:**
    
        - slobodna_enciklopedija_ptica_srbije/prikaz_obavestenja.html
        
    **Rezultat:**
    
        - Prikaz obavestenja za ulogovanog korisnika.
    """
    messages_from_PrimljenePoruke = PrimljenePoruke.objects.filter(id_korisnika=request.user.id)
    received_messages = []

    for message in messages_from_PrimljenePoruke:
        complete_message = message.id_poruke

        new_message_view = MessageView(path = f"/pregled_poruke/{complete_message.id_poruke}",
                                       date_time=complete_message.datum_vreme_kreiranja,
                                       type=message_type(message.tip_prijave, complete_message.tekst),
                                       content=complete_message.tekst[0:30]+"...",
                                       read=message.procitana,
                                       msg_id=complete_message.id_poruke
                                       )
        received_messages.append(new_message_view)

    context = {
        'messages': received_messages[::-1]
    }
    return render(request, 'slobodna_enciklopedija_ptica_srbije/prikaz_obavestenja.html', context)


@login_required(login_url='user_login')
def one_message_view(request, msg_id):
    """
    Funkcija za prikaz sireg pregleda jedne poruke obavestenja. Dodatno se prikazuju informacije o clanku za koji je vezana poruka
    
    **Argumenti:**
    
        - ID poruke, dostavlja se kroz url
        
    **Template:**
    
        - slobodna_enciklopedija_ptica_srbije/prikaz_jedne_poruke.html
        
    **Rezultat:**
    
        - Prikaz stranice za pregled jedne poruke
    """
    message = Poruka.objects.get(id_poruke=msg_id)
    receive_info = PrimljenePoruke.objects.get(id_poruke=msg_id, id_korisnika=request.user.id)

    receive_info.procitana = 1
    receive_info.save()

    image_view_final = None
    reported_discussion_title = ''
    reported_comment_content = ''
    article = None
    if message_type(receive_info.tip_prijave, message.tekst) == 'Nepravilnost - fotografija':
        image = FotografijaGalerija.objects.filter(id_fotografije=receive_info.id_prijavljene_stvari).first()
        if image is not None:
            image_view = base64.b64encode(image.sadrzaj_slike).decode('utf-8')
            image_view_final = f'data:image/png;base64,{image_view}'
            article = image.id_clanka
        else:
            article = None
            image_view_final = ''
    elif receive_info.tip_prijave == 'D':
        reported_discussion = Diskusija.objects.get(id_diskusije=receive_info.id_prijavljene_stvari)
        reported_discussion_title = reported_discussion.naslov_diskusije
        article = reported_discussion.id_clanka
    elif receive_info.tip_prijave == 'K':
        reported_comment = Komentar.objects.get(id_komentara=receive_info.id_prijavljene_stvari)
        reported_comment_content = reported_comment.sadrzaj
        reported_discussion_title = reported_comment.id_diskusije.naslov_diskusije
        article = reported_comment.id_diskusije.id_clanka
    else:
        article = Clanak.objects.get(id_clanka=receive_info.id_prijavljene_stvari)

    bird = None
    if article is not None:
        bird = PticaTabela.objects.get(id_clanka=article.id_clanka)

    msg_view = MessageView(
        path="#",
        date_time=message.datum_vreme_kreiranja,
        type=message_type(receive_info.tip_prijave, message.tekst),
        content=message.tekst,
        image=image_view_final,
        id_of_reported_thing=receive_info.id_prijavljene_stvari,
        msg_id=message.id_poruke
    )

    context = {
        'message': msg_view,
        'reported_discussion_title': reported_discussion_title,
        'reported_comment': reported_comment_content,
        'article_title': '' if (bird is None) else bird.vrsta,
        'article_path': '' if (article is None) else f'/pregled_clanka/{article.id_clanka}',
        'valid_msg': (bird is not None) and (article is not None)
    }

    return render(request, 'slobodna_enciklopedija_ptica_srbije/prikaz_jedne_poruke.html', context)

@login_required(login_url='user_login')
def delete_message(request, msg_id=None):
    """
    Funkcija za brisanje poruke obavestenja. Predstavlja API poziv.
    
    **Argumenti:**
    
        - ID poruke, dostavlja se kroz url
        
    **Rezultat:**
    
        - Rezultat je JSON objekat sa statusom uspeha
    """
    if msg_id is None:
        return JsonResponse({"success": False, "error": "msg_id is required"}, status=400)
    try:
        received_msg = get_object_or_404(PrimljenePoruke, id_poruke=msg_id, id_korisnika=request.user.id)
        received_msg.delete()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
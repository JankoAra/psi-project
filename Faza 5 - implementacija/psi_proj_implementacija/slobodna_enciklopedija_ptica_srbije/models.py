# Andjela Ciric 2021/0066
# Srdjan Lucic 2021/0260
# Janko Arandjelovic 2021/0328
# Jaroslav Veseli 2021/0480

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


class Korisnik(AbstractUser):
    """
    Ova klasa predstavlja korisnika u sistemu.
    Nasledjuje model AbstractUser i dodaje tip korisnika (R - registrovani korisnik, U - urednik, A - administrator).
    """
    tip = models.CharField(db_column='Tip', max_length=1, choices=[('R', 'Registrovani Korisnik'), ('U', 'Urednik'), ('A', 'Administrator')], default='A')

    def is_editor(self):
        # Korisnik se smatra urednikom ako njegov tip ima vrednost 'U' ili 'A'.
        return self.tip == 'U' or self.tip == 'A'

    def is_admin(self):
        # Korisnik se smatra administratorom ako njegov tip ima vrednost 'A'.
        return self.tip == 'A'

    def is_regular_user(self):
        # Korisnik se smatra obicnim korisnikom ako njegov tip ima vrednost 'R'.
        return self.tip == 'R'

    class Meta:
        managed = True
        db_table = 'Korisnik'
        
    def __str__(self):
        return f"Korisnik(id={self.id}, username='{self.username}', tip='{self.tip}')"



class Clanak(models.Model):
    """
    Prestavlja clanak. Sadrzi tekstualni sadrzaj clanka, datum kreiranja, broj ocena i zbir ocena.
    """
    id_clanka = models.AutoField(db_column='IDClanka', primary_key=True)
    id_autora = models.ForeignKey('Korisnik', models.PROTECT, db_column='IDAutora')
    sadrzaj = models.TextField(db_column='Sadrzaj', blank=True, null=True)
    datum_vreme_kreiranja = models.DateTimeField(db_column='DatumVremeKreiranja', default=timezone.localtime)
    broj_ocena = models.IntegerField(db_column='BrojOcena', default=0)
    zbir_ocena = models.IntegerField(db_column='ZbirOcena', default=0)

    class Meta:
        managed = True
        db_table = 'Clanak'
        
    def __str__(self):
        return f"Clanak(id={self.id_clanka}, id_autora={self.id_autora}, datum_vreme_kreiranja={self.datum_vreme_kreiranja}, broj_ocena={self.broj_ocena}, zbir_ocena={self.zbir_ocena})"



class PticaTabela(models.Model):
    """
    Tabela informacija vezana za tacno jedan clanak.
    
    Sadrzi dodatne informacije o ptici koje se prikazuju u tabeli prilikom pregleda nekog clanka.
    """
    id_clanka = models.OneToOneField(Clanak, models.PROTECT, db_column='IDClanka', primary_key=True)
    vrsta = models.CharField(db_column='Vrsta', max_length=60)
    rod = models.CharField(db_column='Rod', max_length=60, blank=True, null=True)
    porodica = models.CharField(db_column='Porodica', max_length=60, blank=True, null=True)
    red = models.CharField(db_column='Red', max_length=60, blank=True, null=True)
    klasa = models.CharField(db_column='Klasa', max_length=60, blank=True, null=True)
    tip = models.CharField(db_column='Tip', max_length=60, blank=True, null=True)
    carstvo = models.CharField(db_column='Carstvo', max_length=60, blank=True, null=True)
    tezina = models.DecimalField(db_column='Tezina', max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0.0)])
    velicina = models.DecimalField(db_column='Velicina', max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0.0)])
    status_ugrozenosti = models.CharField(db_column='StatusUgrozenosti', max_length=60, blank=True, null=True)
    slika_vrste = models.BinaryField(db_column="SlikaVrste", blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'PticaTabela'
        
    def __str__(self):
        return f"PticaTabela(id_clanka={self.id_clanka}, vrsta='{self.vrsta}')"



class FotografijaGalerija(models.Model):
    """
    Jedna fotografija u galeriji vezanoj za clanak.
    """
    id_fotografije = models.AutoField(db_column='IDFotografije', primary_key=True)
    id_clanka = models.ForeignKey('Clanak', models.PROTECT, db_column='IDClanka')
    id_autora = models.ForeignKey('Korisnik', models.PROTECT, db_column='IDAutora')
    sadrzaj_slike = models.BinaryField(db_column="SadrzajSlike")
    datum_vreme_postavljanja = models.DateTimeField(db_column='DatumVremePostavljanja', default=timezone.localtime)

    class Meta:
        managed = True
        db_table = 'FotografijaGalerija'
        
    def __str__(self):
        return f"FotografijaGalerija(id_fotografije={self.id_fotografije}, id_clanka={self.id_clanka}, id_autora={self.id_autora}, datum_vreme_postavljanja={self.datum_vreme_postavljanja})"



class Diskusija(models.Model):
    """
    Jedna diskusija za neki clanak. Sadrzi sadrzaj diskusije, datum kreiranja, id pokretaca i naslov diskusije.
    """
    id_diskusije = models.AutoField(db_column='IDDiskusije', primary_key=True)
    id_pokretaca = models.ForeignKey('Korisnik', models.PROTECT, db_column='IDPokretaca')
    sadrzaj = models.CharField(db_column='Sadrzaj', max_length=400)
    datum_vreme_kreiranja = models.DateTimeField(db_column='DatumVremeKreiranja', default=timezone.localtime)
    id_clanka = models.ForeignKey(Clanak, models.PROTECT, db_column='IDClanka')
    naslov_diskusije = models.CharField(db_column='NaslovDiskusije', max_length=60, default='Naslov')

    class Meta:
        managed = True
        db_table = 'Diskusija'
        
    def __str__(self):
        return f"Diskusija(id_diskusije={self.id_diskusije}, id_pokretaca={self.id_pokretaca}, id_clanka={self.id_clanka}, datum_vreme_kreiranja={self.datum_vreme_kreiranja}, naslov_diskusije='{self.naslov_diskusije}')"



class Komentar(models.Model):
    """
    Komentar na neku zapocetu diskusiju. Sadrzi sadrzaj komentara, datum kreiranja, id korisnika i id diskusije.
    """
    id_komentara = models.AutoField(db_column='IDKomentara', primary_key=True)
    id_diskusije = models.ForeignKey(Diskusija, models.CASCADE, db_column='IDDiskusije')
    id_korisnika = models.ForeignKey('Korisnik', models.PROTECT, db_column='IDKorisnika')
    sadrzaj = models.CharField(db_column='Sadrzaj', max_length=400)
    datum_vreme_postavljanja = models.DateTimeField(db_column='DatumVremePostavljanja', default=timezone.localtime)

    class Meta:
        managed = True
        db_table = 'Komentar'
        
    def __str__(self):
        return f"Komentar(id_komentara={self.id_komentara}, id_diskusije={self.id_diskusije}, id_korisnika={self.id_korisnika}, datum_vreme_postavljanja={self.datum_vreme_postavljanja})"
    


class Ocena(models.Model):
    """
    Ocena na neki clanak. Sadrzi vreme ocenjivanja i ocenu.
    """
    id_ocene = models.AutoField(db_column='IDOcene', primary_key=True)
    id_korisnika = models.ForeignKey(Korisnik, models.PROTECT, db_column='IDKorisnika')
    id_clanka = models.ForeignKey(Clanak, models.PROTECT, db_column='IDClanka')
    datum_vreme_ocenjivanja = models.DateTimeField(db_column='DatumVremeOcenjivanja', default=timezone.localtime)
    ocena = models.IntegerField(db_column='Ocena', validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        managed = True
        db_table = 'Ocena'
        constraints = [
            models.UniqueConstraint(
                fields=['id_korisnika', 'id_clanka'], name='idKor_idCla_unique'
            )
        ]
        
    def __str__(self):
        return f"Ocena(id_korisnika={self.id_korisnika}, id_clanka={self.id_clanka}, datum_vreme_ocenjivanja={self.datum_vreme_ocenjivanja}, ocena={self.ocena})"


class RazlogPrijaveDiskusija(models.Model):
    """
    Pomocna tabela koja poseduje sve moguce razloge za prijavu diskusije.
    """
    id_razlog_diskusija = models.AutoField(db_column='IDRazlogDiskusija', primary_key=True)
    opis = models.CharField(db_column='Opis', max_length=100)

    class Meta:
        managed = True
        db_table = 'RazlogPrijaveDiskusija'
        
    def __str__(self):
        return f"RazlogPrijaveDiskusija(id_razlog_diskusija={self.id_razlog_diskusija}, opis={self.opis})"


class RazlogPrijaveFotografije(models.Model):
    """
    Pomocna tabela koja poseduje sve moguce razloge za prijavu fotografije.
    """
    id_razlog_fotografija = models.AutoField(db_column='IDRazlogFotografija', primary_key=True)
    opis = models.CharField(db_column='Opis', max_length=100)

    class Meta:
        managed = True
        db_table = 'RazlogPrijaveFotografije'
        
    def __str__(self):
        return f"RazlogPrijaveFotografije(id_razlog_fotografija={self.id_razlog_fotografija}, opis={self.opis})"


class RazlogPrijaveKomentar(models.Model):
    """
    Pomocna tabela koja poseduje sve moguce razloge za prijavu komentara.
    """
    id_razlog_komentar = models.AutoField(db_column='IDRazlogKomentar', primary_key=True)
    opis = models.CharField(db_column='Opis', max_length=100)

    class Meta:
        managed = True
        db_table = 'RazlogPrijaveKomentar'
        
    def __str__(self):
        return f"RazlogPrijaveKomentar(id_razlog_komentar={self.id_razlog_komentar}, opis={self.opis})"


class PrijavaNepravilnosti(models.Model):
    """
    Informacije o prijavi nekog korisnika.
    """
    id_prijave = models.AutoField(db_column='IDPrijave', primary_key=True)
    id_korisnika = models.ForeignKey(Korisnik, models.PROTECT, db_column='IDKorisnika')
    datum_vreme_prijave = models.DateTimeField(db_column='DatumVremePrijave', default=timezone.localtime)

    class Meta:
        managed = True
        db_table = 'PrijavaNepravilnosti'
        
    def __str__(self):
        return f"PrijavaNepravilnosti(id_prijave={self.id_prijave}, id_korisnika={self.id_korisnika}, datum_vreme_prijave={self.datum_vreme_prijave})"


class NepravilnostClanak(models.Model):
    """
    Dodatne informacije o prijavama na clanke.
    """
    id_prijave = models.OneToOneField('PrijavaNepravilnosti', models.CASCADE, db_column='IDPrijave', primary_key=True)
    id_clanka = models.ForeignKey(Clanak, models.CASCADE, db_column='IDClanka')
    opis = models.CharField(db_column='Opis', max_length=400)

    class Meta:
        managed = True
        db_table = 'NepravilnostClanak'
        
    def __str__(self):
        return f"NepravilnostClanak(id_prijave={self.id_prijave}, id_clanka={self.id_clanka}, opis={self.opis})"


class NepravilnostDiskusija(models.Model):
    """
    Dodatne informacije o prijavama na diskusije.
    """
    id_prijave = models.OneToOneField('PrijavaNepravilnosti', models.CASCADE, db_column='IDPrijave', primary_key=True)
    id_razlog_diskusija = models.ForeignKey('RazlogPrijaveDiskusija', models.PROTECT, db_column='IDRazlogDiskusija')
    id_diskusije = models.ForeignKey(Diskusija, models.CASCADE, db_column='IDDiskusije')

    class Meta:
        managed = True
        db_table = 'NepravilnostDiskusija'
        
    def __str__(self):
        return f"NepravilnostDiskusija(id_prijave={self.id_prijave}, id_razlog_diskusija={self.id_razlog_diskusija}, id_diskusije={self.id_diskusije})"


class NepravilnostFotografija(models.Model):
    """
    Dodatne informacije o prijavama na fotografije.
    """
    id_prijave = models.OneToOneField('PrijavaNepravilnosti', models.CASCADE, db_column='IDPrijave', primary_key=True)
    id_razlog_fotografija = models.ForeignKey('RazlogPrijaveFotografije', models.PROTECT, db_column='IDRazlogFotografija')
    id_fotografije = models.ForeignKey('FotografijaGalerija', models.CASCADE, db_column='IDFotografije')

    class Meta:
        managed = True
        db_table = 'NepravilnostFotografija'
        
    def __str__(self):
        return f"NepravilnostFotografija(id_prijave={self.id_prijave}, id_razlog_fotografija={self.id_razlog_fotografija}, id_fotografije={self.id_fotografije})"


class NepravilnostKomentar(models.Model):
    """
    Dodatne informacije o prijavama na komentare.
    """
    id_prijave = models.OneToOneField('PrijavaNepravilnosti', models.CASCADE, db_column='IDPrijave', primary_key=True)
    id_razlog_komentar = models.ForeignKey('RazlogPrijaveKomentar', models.PROTECT, db_column='IDRazlogKomentar')
    id_komentara = models.ForeignKey(Komentar, models.CASCADE, db_column='IDKomentara')

    class Meta:
        managed = True
        db_table = 'NepravilnostKomentar'
        
    def __str__(self):
        return f"NepravilnostKomentar(id_prijave={self.id_prijave}, id_razlog_komentar={self.id_razlog_komentar}, id_komentara={self.id_komentara})"


class Poruka(models.Model):
    """
    Poruke obavestenja koje se salju korisnicima.
    """
    id_poruke = models.AutoField(db_column='IDPoruke', primary_key=True)
    tekst = models.CharField(db_column='Tekst', max_length=400)
    datum_vreme_kreiranja = models.DateTimeField(db_column='DatumVremeKreiranja', default=timezone.localtime)

    class Meta:
        managed = True
        db_table = 'Poruka'
        
    def __str__(self):
        return f"Poruka(id_poruke={self.id_poruke}, tekst={self.tekst}, datum_vreme_kreiranja={self.datum_vreme_kreiranja})"


class PrijavljenNaObavestenja(models.Model):
    """
    Informacije o tome koji korisnik se prijavio na pracenje kojih clanaka i da li se poruke primaju i na mejl.
    """
    id_prijava_obavestenja = models.AutoField(db_column='IDPrijavaObavestenja', primary_key=True)
    id_korisnika = models.ForeignKey(Korisnik, models.PROTECT, db_column='IDKorisnika')
    id_clanka = models.ForeignKey(Clanak, models.CASCADE, db_column='IDClanka')
    datum_vreme_prijave = models.DateTimeField(db_column='DatumVremePrijave', default=timezone.localtime)
    primaj_na_mail = models.IntegerField(db_column='PrimajNaMail')

    class Meta:
        managed = True
        db_table = 'PrijavljenNaObavestenja'
        constraints = [
            models.UniqueConstraint(
                fields=['id_korisnika', 'id_clanka'], name='combination_pks'
            )
        ]

    def __str__(self):
        return f"PrijavljenNaObavestenja(id_korisnika={self.id_korisnika}, id_clanka={self.id_clanka}, datum_vreme_prijave={self.datum_vreme_prijave}, primaj_na_mail={self.primaj_na_mail})"


class PrimljenePoruke(models.Model):
    """
    Poruke poslate pojedinacnim korisnicima, sa informacijom o tome da li je poruka procitana u sanducetu.
    """
    id_primljena_poruka = models.AutoField(db_column='IDPrimljenaPoruka', primary_key=True)
    id_poruke = models.ForeignKey(Poruka, models.CASCADE, db_column='IDPoruke')
    id_korisnika = models.ForeignKey(Korisnik, models.PROTECT, db_column='IDKorisnika')
    procitana = models.IntegerField(db_column='Procitana')

    tip_prijave = models.CharField(db_column='TipPrijave', max_length=1, choices=[('D', 'Diskusija'), ('K', 'Komentar'), ('F', 'Fotografija'), ('C', 'Clanak')], default='C')
    id_prijavljene_stvari = models.IntegerField(db_column='IDPrijavljeneStvari', default=0)

    class Meta:
        managed = True
        db_table = 'PrimljenePoruke'
        constraints = [
            models.UniqueConstraint(
                fields=['id_poruke', 'id_korisnika'], name='combination_pks_primljena_poruka'
            )
        ]

    def __str__(self):
        return f"PrimljenePoruke(id_poruke={self.id_poruke}, id_korisnika={self.id_korisnika}, procitana={self.procitana})"

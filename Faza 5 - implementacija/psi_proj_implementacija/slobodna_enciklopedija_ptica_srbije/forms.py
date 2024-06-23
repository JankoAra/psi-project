# Janko Arandjelovic 2021/0328
# Jaroslav Veseli 2021/0480


from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import Korisnik


# Ova forma je napravljena jer ugradjen UserCreationForm radi sa defaultnim django Korisnikom.
# To je ovde override-ovano preko nested Meta klase, jer mi imamo prilagodjen model za Korisnika.
class KorisnikCreationForm(UserCreationForm):
    def clean(self):
        super().clean()
        if (self.cleaned_data.get('email') is not None) and (self.cleaned_data.get('email').strip() == ''):
            self.add_error("email", "Ovo polje mora da se popuni.")
        elif (self.cleaned_data.get('email') is not None) and (Korisnik.objects.filter(email=self.cleaned_data.get('email')).exists()):
            self.add_error("email", "Korisnik sa tom email adresom već postoji!")
        return self.cleaned_data

    class Meta:
        model = Korisnik
        fields = ['username', 'email', 'password1', 'password2']


class UploadImageToGalleryForm(forms.Form):
    """
    Forma za unos nove slike u galeriju.
    """
    image = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control mb-3', 'accept': 'image/jpeg, image/png, image/jpg'}),required=False)
    article_id = forms.IntegerField(widget=forms.HiddenInput())

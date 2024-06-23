# Jaroslav Veseli 2021/0480


from django.contrib import admin
from .models import *

# Registrovani su svi modeli kako bi neko mogao da pristupi njima preko admin panela.
admin.site.register(Korisnik)
admin.site.register(Clanak)
admin.site.register(PticaTabela)
admin.site.register(FotografijaGalerija)
admin.site.register(Diskusija)
admin.site.register(Komentar)
admin.site.register(Ocena)

admin.site.register(RazlogPrijaveDiskusija)
admin.site.register(RazlogPrijaveFotografije)
admin.site.register(RazlogPrijaveKomentar)
admin.site.register(PrijavaNepravilnosti)
admin.site.register(NepravilnostClanak)
admin.site.register(NepravilnostDiskusija)
admin.site.register(NepravilnostFotografija)
admin.site.register(NepravilnostKomentar)

admin.site.register(Poruka)
admin.site.register(PrijavljenNaObavestenja)
admin.site.register(PrimljenePoruke)

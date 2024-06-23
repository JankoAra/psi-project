# Andjela Ciric 2021/0066
# Srdjan Lucic 2021/0260
# Janko Arandjelovic 2021/0328
# Jaroslav Veseli 2021/0480


from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('api/index_ucitaj_vise/', index_load_more, name='index_load_more'),
    path('prijava/', user_login, name='user_login'),
    path('registracija/', user_register, name='user_register'),
    path('registracija_urednika/', editor_register, name='editor_register'),
    path('odjava/', user_logout, name='user_logout'),
    path('brisanje_korisnika/', user_deletion, name='user_deletion'),
    path('kreiranje_clanka/', create_article, name='create_article'),
    path('obrisi_korisnika/<int:user_id>/', delete_user_endpoint, name='delete_user'),
    path('pregled_clanka/<int:article_id>', show_article, name='show_article'),
    path('dodavanje_u_galeriju/', add_image_to_gallery, name='add_image_to_gallery'),
    path('api/napravi_diskusiju/', create_discussion, name='create_discussion'),
    path('api/dohvati_diskusije/<int:article_id>', get_discussions_for_article, name='get_discussions_for_article'),
    path('api/dohvati_slike_u_galeriji/<int:article_id>', get_gallery_for_article, name='get_gallery_for_article'),
    path('api/obrisi_sliku_u_galeriji/<int:image_id>', delete_image_from_gallery, name='delete_image_from_gallery'),
    path('api/dodaj_komentar/', create_comment, name='create_comment'),
    path('api/obrisi_diskusiju/', delete_discussion, name='delete_discussion'),
    path('api/obrisi_komentar/', delete_comment, name='delete_comment'),
    path('api/izmena_ocena/', alter_rating, name='alter_rating'),
    path('api/prosecna_ocena/<int:article_id>', get_avg_rating, name='get_avg_rating'),
    path('api/izmena_teksta_clanka/', change_article_text, name='change_article_text'),
    path('api/izmena_tabele/', change_article_table, name='change_article_table'),
    path('izmena_slike_tabele/', change_table_image, name='change_table_image'),
    path('api/obrisi_sliku_u_tabeli/', delete_table_image, name='delete_table_image'),
    path('pregled_clanka/prijavi_nepravilnost_slike_prelaz/', report_irregularity_photograph_page, name='report_irregularity_photogrpah_page'),
    path('prijavi_nepravilnost_slike/<int:id_img>', report_irregularity_photograph_get, name='report_irregularity_photograph_get'),
    path('prijavi_nepravilnost_slike/api/prijavi_nepravilnost_slike_potvrda/', report_irregularity_photograph_confirm, name='report_irregularity_photograph_confirm'),
    path('pregled_clanka/prijavi_nepravilnost_komentara_prelaz/', report_irregularity_comment_page, name='report_irregularity_comment_page'),
    path('prijavi_nepravilnost_komentara/<int:id_comm>', report_irregularity_comment_get, name='report_irregularity_comment_get'),
    path('prijavi_nepravilnost_komentara/api/prijavi_nepravilnost_komentara_potvrda/', report_irregularity_comment_confirm, name='report_irregularity_comment_confirm'),
    path('pregled_clanka/prijavi_nepravilnost_diskusije_prelaz/', report_irregularity_discussion_page, name='report_irregularity_discussion_page'),
    path('prijavi_nepravilnost_diskusije/<int:id_discuss>', report_irregularity_discussion_get, name='report_irregularity_discussion_get'),
    path('prijavi_nepravilnost_diskusije/api/prijavi_nepravilnost_diskusije_potvrda/', report_irregularity_discussion_confirm, name='report_irregularity_discussion_confirm'),
    path('pregled_clanka/prijavi_se_na_pracenje_obavestenja_prelaz/', track_changes_on_article_page,
         name='track_changes_on_article_page'),
    path('prijavi_se_na_pracenje_obavestenja/<int:id_article>', track_changes_on_article,
         name='track_changes_on_article'),
    path('prijavi_se_na_pracenje_obavestenja/api/prijavi_se_na_pracenje_obavestenja_potvrda/',
         track_changes_on_article_confirm, name='track_changes_on_article_confirm'),
    path('api/dohvati_prijavljen_na_obavestenja/', check_if_already_track, name = 'check_if_already_track'),
    path('pregled_clanka/prijavi_nepravilnost_clanka_prelaz/', report_irregularity_article_page, name='report_irregularity_article_page'),
    path('prijavi_nepravilnost_clanka/<int:id_article>', report_irregularity_article_get, name='report_irregularity_article_get'),
    path('prijavi_nepravilnost_clanka/api/prijavi_nepravilnost_clanka_potvrda/', report_irregularity_article_confirm, name='report_irregularity_article_confirm'),
    path('api/odjavi_se_sa_pracenja_obavjestenja/', stop_tracking_article_changes, name='stop_tracking_article_changes'),
    path('pregled_obavestenja/', notifications, name='notifications'),
    path('pregled_poruke/<int:msg_id>', one_message_view, name='one_message_view'),
    path('api/obrisi_poruku/<int:msg_id>', delete_message, name='delete_message')
]

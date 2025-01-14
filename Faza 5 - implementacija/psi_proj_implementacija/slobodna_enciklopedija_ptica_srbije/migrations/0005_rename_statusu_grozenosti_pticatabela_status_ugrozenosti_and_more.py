# Generated by Django 5.0.6 on 2024-05-14 11:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slobodna_enciklopedija_ptica_srbije', '0004_alter_korisnik_tip'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pticatabela',
            old_name='statusu_grozenosti',
            new_name='status_ugrozenosti',
        ),
        migrations.AlterField(
            model_name='clanak',
            name='datum_vreme_kreiranja',
            field=models.DateTimeField(db_column='DatumVremeKreiranja', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='diskusija',
            name='datum_vreme_kreiranja',
            field=models.DateTimeField(db_column='DatumVremeKreiranja', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='fotografijagalerija',
            name='datum_vreme_postavljanja',
            field=models.DateTimeField(db_column='DatumVremePostavljanja', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='komentar',
            name='datum_vreme_postavljanja',
            field=models.DateTimeField(db_column='DatumVremePostavljanja', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='ocena',
            name='datum_vreme_ocenjivanja',
            field=models.DateTimeField(db_column='DatumVremeOcenjivanja', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='poruka',
            name='datum_vreme_kreiranja',
            field=models.DateTimeField(db_column='DatumVremeKreiranja', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='prijavanepravilnosti',
            name='datum_vreme_prijave',
            field=models.DateTimeField(db_column='DatumVremePrijave', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='prijavljennaobavestenja',
            name='datum_vreme_prijave',
            field=models.DateTimeField(db_column='DatumVremePrijave', default=django.utils.timezone.now),
        ),
    ]

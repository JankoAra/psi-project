# Generated by Django 5.0.6 on 2024-05-14 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slobodna_enciklopedija_ptica_srbije', '0005_rename_statusu_grozenosti_pticatabela_status_ugrozenosti_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='diskusija',
            name='naslov_diskusije',
            field=models.CharField(db_column='NaslovDiskusije', default='Naslov', max_length=60),
        ),
    ]
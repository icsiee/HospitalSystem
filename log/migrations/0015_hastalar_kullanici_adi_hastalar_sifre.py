# Generated by Django 5.0.5 on 2024-05-17 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0014_remove_doktorlar_user_remove_hastalar_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='hastalar',
            name='kullanici_adi',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
        migrations.AddField(
            model_name='hastalar',
            name='sifre',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]

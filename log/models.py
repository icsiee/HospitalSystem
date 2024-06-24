from django.contrib.auth.models import User
from django.db import models
import json
import os
from django.conf import settings
from django.utils.crypto import get_random_string

class Hastalar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hasta')
    ad = models.CharField(max_length=50)
    soyad = models.CharField(max_length=50)
    dogum_tarihi = models.DateField()
    cinsiyet = models.CharField(max_length=10)
    telefon = models.CharField(max_length=15)
    adres = models.CharField(max_length=100)
    kullanici_adi = models.CharField(max_length=50, blank=True, null=True)
    sifre = models.CharField(max_length=15, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.kullanici_adi:
            self.kullanici_adi = self.ad
        if not self.sifre:
            self.sifre = get_random_string(10)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ad} {self.soyad}"

class Doktorlar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doktor')
    ad = models.CharField(max_length=50)
    soyad = models.CharField(max_length=50)
    uzmanlik_alani = models.CharField(max_length=100)
    calistigi_hastane = models.CharField(max_length=100)
    kullanici_adi = models.CharField(max_length=50, blank=True, null=True)
    sifre = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.kullanici_adi:
            self.kullanici_adi = self.ad
        if not self.sifre:
            self.sifre = get_random_string(10)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ad} {self.soyad}"

class Yonetici(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='yonetici')

class Randevular(models.Model):
    hasta = models.ForeignKey(Hastalar, on_delete=models.CASCADE)
    doktor = models.ForeignKey(Doktorlar, on_delete=models.CASCADE)
    randevu_tarihi = models.DateField()
    randevu_saati = models.TimeField()

class TıbbiRaporlar(models.Model):
    hasta = models.ForeignKey(Hastalar, on_delete=models.CASCADE)
    doktor = models.ForeignKey(Doktorlar, on_delete=models.CASCADE)
    rapor_tarihi = models.DateField()
    rapor_icerigi = models.TextField()
    rapor_gorseli = models.ImageField(upload_to='raporlar/', blank=True, null=True)
    rapor_json = models.JSONField(null=True, blank=True)
    rapor_url = models.URLField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:  # Check if this is a new object
            super().save(*args, **kwargs)

        json_data = {
            "hasta": self.hasta.ad,
            "doktor": self.doktor.ad,
            "rapor_tarihi": self.rapor_tarihi.strftime("%Y-%m-%d"),
            "rapor_icerigi": self.rapor_icerigi,
        }

        if self.rapor_gorseli:
            self.rapor_url = self.rapor_gorseli.url
            json_data["rapor_gorseli_url"] = self.rapor_url
        else:
            self.rapor_url = ''

        self.rapor_json = json_data

        json_file_path = os.path.join(settings.MEDIA_ROOT, 'raporlar', f'rapor_{self.id}.json')
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

        self.rapor_url = settings.MEDIA_URL + f'raporlar/rapor_{self.id}.json'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Rapor ID: {self.id} - {self.rapor_tarihi}"

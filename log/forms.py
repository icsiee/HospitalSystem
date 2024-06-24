from django import forms
from .models import Hastalar, Doktorlar, Randevular, TıbbiRaporlar, Yonetici

class HastalarForm(forms.ModelForm):
    class Meta:
        model = Hastalar
        fields = ['ad', 'soyad', 'dogum_tarihi', 'cinsiyet', 'telefon', 'adres']
        widgets = {
            'dogum_tarihi': forms.DateInput(attrs={'type': 'date'}),
            'cinsiyet': forms.Select(choices=[('Kadın', 'Kadın'), ('Erkek', 'Erkek')]),
        }

class DoktorlarForm(forms.ModelForm):
    class Meta:
        model = Doktorlar
        fields = ['ad', 'soyad', 'uzmanlik_alani', 'calistigi_hastane']




class YoneticiForm(forms.ModelForm):
    class Meta:
        model = Yonetici
        fields = ['user']

from django import forms
from .models import Randevular

class RandevularForm(forms.ModelForm):
    class Meta:
        model = Randevular
        fields = ['doktor', 'randevu_tarihi', 'randevu_saati']
        widgets = {
            'randevu_tarihi': forms.DateInput(attrs={'type': 'date'}),
            'randevu_saati': forms.TimeInput(attrs={'type': 'time'}),
        }


class TibbiRaporlarForm(forms.ModelForm):
    hasta = forms.ModelChoiceField(queryset=Hastalar.objects.all(), label="Hasta", widget=forms.Select)
    doktor = forms.ModelChoiceField(queryset=Doktorlar.objects.all(), label="Doktor", widget=forms.Select)

    class Meta:
        model = TıbbiRaporlar
        fields = ['hasta', 'doktor', 'rapor_tarihi', 'rapor_icerigi', 'rapor_gorseli']
        widgets = {
            'rapor_tarihi': forms.DateInput(attrs={'type': 'date'}),
            'rapor_gorseli': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super(TibbiRaporlarForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['rapor_tarihi'].widget = forms.HiddenInput()


class HastaGirisForm(forms.Form):
    username = forms.CharField(label='Kullanıcı Adı', max_length=50)
    password = forms.CharField(label='Şifre', widget=forms.PasswordInput)


class DoktorTibbiRaporEkleForm(forms.ModelForm):
    class Meta:
        model = TıbbiRaporlar
        fields = ['hasta', 'rapor_tarihi', 'rapor_icerigi', 'rapor_gorseli']
        widgets = {
            'rapor_tarihi': forms.DateInput(attrs={'type': 'date'}),
            'rapor_gorseli': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
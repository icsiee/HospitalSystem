import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
import json
import os
from .models import TıbbiRaporlar
from .forms import TibbiRaporlarForm
from django.conf import settings
from django.http import HttpResponse
from .models import Doktorlar, Randevular
from django.contrib.auth.decorators import login_required
from .models import Hastalar,Doktorlar,Randevular
from .forms import HastalarForm,DoktorlarForm,RandevularForm, HastaGirisForm, TibbiRaporlarForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Hastalar
from .models import Randevular

from django.shortcuts import get_object_or_404


def randevu_sil(request, randevu_id):
    if request.method == 'POST':
        try:
            # Veritabanından hastayı bul ve sil
            randevu = Randevular.objects.get(id=randevu_id)
            randevu.delete()
            return HttpResponse("Randevu başarıyla silindi!", status=200)
        except Randevular.DoesNotExist:
            return HttpResponse("Randevu bulunamadı!", status=404)
    else:
        return HttpResponse("Geçersiz istek!", status=400)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'hasta'):
                return redirect('hasta_dashboard')
            elif hasattr(user, 'doktor'):
                return redirect('doktor_dashboard')
    return render(request, 'login.html')

@login_required
def randevu_liste(request):
    randevular = Randevular.objects.filter(hasta=request.user.hasta)
    return render(request, 'log/randevu_liste.html', {'randevular': randevular})

@login_required
def randevu_al(request):
    try:
        hasta = request.user.hasta
    except Hastalar.DoesNotExist:
        messages.error(request, 'Randevu alabilmek için hasta kaydınız olmalı.')
        return redirect('hasta_paneli')

    if request.method == 'POST':
        form = RandevularForm(request.POST)
        if form.is_valid():
            doktor = form.cleaned_data['doktor']
            randevu_tarihi = form.cleaned_data['randevu_tarihi']
            randevu_saati = form.cleaned_data['randevu_saati']

            # Aynı doktor, tarih ve saat için başka randevu olup olmadığını kontrol et
            if Randevular.objects.filter(doktor=doktor, randevu_tarihi=randevu_tarihi, randevu_saati=randevu_saati).exists():
                messages.error(request, 'Bu tarih ve saatte, seçtiğiniz doktordan randevu alınamaz. Lütfen başka bir saat seçin.')
            else:
                # Randevuyu kaydet
                randevu = form.save(commit=False)
                randevu.hasta = hasta
                randevu.save()
                messages.success(request, 'Randevunuz başarıyla oluşturuldu.')
                return redirect('randevu_liste')
    else:
        form = RandevularForm()

    return render(request, 'log/randevu_al.html', {'form': form})

def hasta_giris(request):
    if request.method == 'POST':
        form = HastaGirisForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                try:
                    hasta = user.hasta
                    login(request, user)
                    messages.success(request, 'Giriş başarılı!')
                    return redirect('hasta_paneli')  # Hastanın giriş yaptıktan sonra yönlendirileceği sayfa
                except Hastalar.DoesNotExist:
                    messages.error(request, 'Hasta bilgisi bulunamadı.')
            else:
                messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
    else:
        form = HastaGirisForm()

    return render(request, 'log/hasta_giris.html', {'form': form})


def doktor_giris(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Kullanıcı adı ve şifre ile doğrulama
        user = authenticate(request, username=username, password=password)

        if user is not None and user.doktor:
            # Doğrulama başarılı, kullanıcıyı oturum açık olarak işaretle
            login(request, user)
            messages.success(request, 'Giriş başarılı!')
            return redirect('doktor_paneli')  # Doğru kullanıcı ise doktor paneline yönlendir
        else:
            # Doğrulama başarısız
            messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')

    return render(request, 'log/doktor_giris.html')
def doktor_paneli(request):
    if not request.user.is_authenticated:
        return redirect('doktor_giris')

    try:
        doktor = request.user.doktor
    except Doktorlar.DoesNotExist:
        messages.error(request, 'Doktor bilgisi bulunamadı.')
        return redirect('doktor_giris')

    return render(request, 'log/doktor_paneli.html', {'doktor': doktor})


@login_required
def hasta_paneli(request):
    try:
        hasta = request.user.hasta
        return render(request, 'log/hasta_paneli.html', {'hasta': hasta})
    except Hastalar.DoesNotExist:
        messages.error(request, 'Hasta bilgisi bulunamadı.')
        return redirect('hasta_giris')

def yonetici_giris(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('yonetici_paneli')  # Yönetici paneline yönlendir
    return render(request, 'log/yonetici_giris.html')

def yonetici_paneli(request):
    return render(request, 'log/yonetici_paneli.html')



def blogs(request):
    return render(request, "log/blogs.html")


import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Hastalar, Doktorlar
from .forms import HastalarForm, DoktorlarForm

def hasta_ekle(request):
    if request.method == 'POST':
        form = HastalarForm(request.POST)
        if form.is_valid():
            ad = form.cleaned_data['ad']
            soyad = form.cleaned_data['soyad']
            telefon = form.cleaned_data['telefon']

            if Hastalar.objects.filter(ad=ad, soyad=soyad, telefon=telefon).exists():
                messages.error(request, 'Bu bilgilere sahip bir hasta zaten mevcut.')
            else:
                # Benzersiz bir kullanıcı adı oluştur
                username = f"{ad}_{uuid.uuid4().hex[:6]}"
                password = telefon  # Telefon numarasını şifre olarak kullan

                user = User.objects.create_user(username=username, password=password)

                hasta = form.save(commit=False)
                hasta.user = user
                hasta.kullanici_adi = username
                hasta.sifre = password
                hasta.save()

                messages.success(request, 'Hasta başarıyla eklendi.')
                return redirect('yonetici_paneli')
    else:
        form = HastalarForm()

    return render(request, 'log/hasta_ekle.html', {'form': form})

def doktor_ekle(request):
    if request.method == 'POST':
        form = DoktorlarForm(request.POST)
        if form.is_valid():
            ad = form.cleaned_data['ad']
            soyad = form.cleaned_data['soyad']
            calistigi_hastane = form.cleaned_data['calistigi_hastane']

            if Doktorlar.objects.filter(ad=ad, soyad=soyad, calistigi_hastane=calistigi_hastane).exists():
                messages.error(request, 'Bu bilgilere sahip bir doktor zaten mevcut.')
            else:
                # Benzersiz bir kullanıcı adı oluştur
                username = f"{ad}_{uuid.uuid4().hex[:6]}"
                password = soyad  # Soyadı şifre olarak kullan

                user = User.objects.create_user(username=username, password=password)

                doktor = form.save(commit=False)
                doktor.user = user
                doktor.kullanici_adi = username
                doktor.sifre = password
                doktor.save()

                messages.success(request, 'Doktor başarıyla eklendi.')
                return redirect('yonetici_paneli')
    else:
        form = DoktorlarForm()

    return render(request, 'log/doktor_ekle.html', {'form': form})


def hasta_liste(request):
    hastalar = Hastalar.objects.all()
    return render(request, 'log/hasta_liste.html', {'hastalar': hastalar})

from django.http import HttpResponse, JsonResponse

def hasta_sil(request, hasta_id):
    if request.method == 'POST':
        try:
            # Veritabanından hastayı bul ve sil
            hasta = Hastalar.objects.get(id=hasta_id)
            hasta.delete()
            return HttpResponse("Hasta başarıyla silindi!", status=200)
        except Hastalar.DoesNotExist:
            return HttpResponse("Hasta bulunamadı!", status=404)
    else:
        return HttpResponse("Geçersiz istek!", status=400)

def doktor_liste(request):
        doktorlar = Doktorlar.objects.all()
        return render(request, 'log/doktor_liste.html', {'doktorlar': doktorlar})

def doktor_sil(request, doktor_id):
    if request.method == 'POST':
        doktor = get_object_or_404(Doktorlar, id=doktor_id)

        # Doktorun randevularını kontrol et
        aktif_randevular = Randevular.objects.filter(doktor=doktor)

        if aktif_randevular.exists():
            return HttpResponse("Doktorun bir randevusu var bu yüzden silinemez.", status=403)

        # Doktoru sil
        doktor.delete()
        return HttpResponse("Doktor başarıyla silindi!", status=200)
    else:
        return HttpResponse("Geçersiz istek!", status=400)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TıbbiRaporlar
from .forms import TibbiRaporlarForm

@login_required
def yonetici_tibbirapor_ekle(request):
    if request.method == 'POST':
        form = TibbiRaporlarForm(request.POST, request.FILES)
        if form.is_valid():
            rapor = form.save(commit=False)
            rapor.save()
            return redirect('yonetici_tibbirapor_liste')
    else:
        form = TibbiRaporlarForm()
    return render(request, 'log/yonetici_tibbirapor_ekle.html', {'form': form})

@login_required
def yonetici_tibbirapor_liste(request):
    raporlar = TıbbiRaporlar.objects.all()
    return render(request, 'log/yonetici_tibbirapor_liste.html', {'raporlar': raporlar})

@login_required
def yonetici_tibbirapor_json_goruntule(request, rapor_id):
    rapor = get_object_or_404(TıbbiRaporlar, id=rapor_id)
    return JsonResponse(rapor.rapor_json)

@login_required
def tum_raporlar_json(request):
    raporlar = TıbbiRaporlar.objects.all()
    tum_raporlar = [rapor.rapor_json for rapor in raporlar]
    return JsonResponse(tum_raporlar, safe=False)

@login_required
def yonetici_tibbirapor_sil(request, rapor_id):
    rapor = get_object_or_404(TıbbiRaporlar, id=rapor_id)
    if request.method == 'POST':
        rapor.delete()
        return redirect('yonetici_tibbirapor_liste')
    return render(request, 'log/yonetici_tibbirapor_sil.html', {'rapor': rapor})

@login_required
def yonetici_tibbirapor_indir(request, rapor_id):
    rapor = get_object_or_404(TıbbiRaporlar, id=rapor_id)
    response = HttpResponse(json.dumps(rapor.rapor_json, ensure_ascii=False, indent=4), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename=rapor_{rapor_id}.json'
    return response

@login_required
def yonetici_tibbirapor_duzenle(request, rapor_id):
    rapor = get_object_or_404(TıbbiRaporlar, id=rapor_id)
    if request.method == 'POST':
        form = TibbiRaporlarForm(request.POST, request.FILES, instance=rapor)
        if form.is_valid():
            form.save()
            return redirect('yonetici_tibbirapor_liste')
    else:
        form = TibbiRaporlarForm(instance=rapor)
    return render(request, 'log/yonetici_tibbirapor_duzenle.html', {'form': form, 'rapor': rapor})

@login_required
def yonetici_tibbirapor_duzenle(request, rapor_id):
    rapor = get_object_or_404(TıbbiRaporlar, id=rapor_id)
    if request.method == 'POST':
        form = TibbiRaporlarForm(request.POST, request.FILES, instance=rapor)
        if form.is_valid():
            form.save()
            return redirect('yonetici_tibbirapor_liste')
    else:
        form = TibbiRaporlarForm(instance=rapor)
    return render(request, 'log/yonetici_tibbirapor_duzenle.html', {'form': form, 'rapor': rapor})

@login_required
def hasta_raporlar(request, hasta_id):
    raporlar = TıbbiRaporlar.objects.filter(hasta_id=hasta_id).values('id', 'rapor_tarihi', 'rapor_icerigi')
    raporlar_list = list(raporlar)
    return JsonResponse({'raporlar': raporlar_list})

@login_required
def hasta_bilgileri(request, hasta_id):
    hasta = get_object_or_404(Hastalar, id=hasta_id)
    data = {
        'id': hasta.id,
        'ad': hasta.ad,
        'soyad': hasta.soyad,
        'cinsiyet': hasta.cinsiyet,
        'telefon': hasta.telefon,
        'adres': hasta.adres
    }
    return JsonResponse(data)

@login_required
def hasta_guncelle(request, hasta_id):
    if request.method == 'POST':
        hasta = get_object_or_404(Hastalar, id=hasta_id)
        hasta.ad = request.POST.get('ad')
        hasta.soyad = request.POST.get('soyad')
        hasta.cinsiyet = request.POST.get('cinsiyet')
        hasta.telefon = request.POST.get('telefon')
        hasta.adres = request.POST.get('adres')
        hasta.save()
        return JsonResponse({'success': True, 'message': 'Hasta bilgileri başarıyla güncellendi.'})
    return JsonResponse({'success': False, 'message': 'Geçersiz istek.'})

def doktor_duzenle(request, doktor_id):
    doktor = get_object_or_404(Doktorlar, id=doktor_id)
    if request.method == 'POST':
        form = DoktorlarForm(request.POST, instance=doktor)
        if form.is_valid():
            form.save()
            return redirect('doktor_liste')  # Düzenleme işlemi tamamlandığında yönlendirilecek URL
    else:
        form = DoktorlarForm(instance=doktor)
    return render(request, 'log/doktor_duzenle.html', {'form': form})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Hastalar, Randevular, TıbbiRaporlar
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Randevular, TıbbiRaporlar

@login_required
def hasta_tibbirapor_ekle(request):
    if request.method == 'POST':
        form = TibbiRaporlarForm(request.POST, request.FILES)
        if form.is_valid():
            rapor = form.save(commit=False)
            rapor.hasta = request.user.hasta  # Oturum açmış olan hastaya atanıyor
            rapor.save()
            return redirect('hasta_tibbirapor_liste')
    else:
        form = TibbiRaporlarForm()
    return render(request, 'log/hasta_tibbirapor_ekle.html', {'form': form})

@login_required
def hasta_tibbirapor_liste(request):
    raporlar = TıbbiRaporlar.objects.filter(hasta=request.user.hasta)
    return render(request, 'log/hasta_tibbirapor_liste.html', {'raporlar': raporlar})


@login_required
def hasta_tibbirapor_json_goruntule(request, rapor_id):
    rapor = get_object_or_404(TıbbiRaporlar, id=rapor_id, hasta=request.user.hasta)
    return JsonResponse(rapor.rapor_json)

@login_required
def hasta_tumraporlar_json(request):
    raporlar = TıbbiRaporlar.objects.filter(hasta=request.user.hasta)
    tum_raporlar = [rapor.rapor_json for rapor in raporlar]
    return JsonResponse(tum_raporlar, safe=False)

@login_required
def hasta_tibbirapor_sil(request, rapor_id):
    rapor = get_object_or_404(TıbbiRaporlar, id=rapor_id, hasta=request.user.hasta)
    if request.method == 'POST':
        rapor.delete()
        return redirect('hasta_tibbirapor_liste')
    return render(request, 'log/hasta_tibbirapor_sil.html', {'rapor': rapor})

@login_required
def hasta_tibbirapor_indir(request, rapor_id):
    rapor = get_object_or_404(TıbbiRaporlar, id=rapor_id, hasta=request.user.hasta)
    response = HttpResponse(json.dumps(rapor.rapor_json, ensure_ascii=False, indent=4), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename=rapor_{rapor_id}.json'
    return response

@login_required
def hasta_tibbirapor_duzenle(request, rapor_id):
    rapor = get_object_or_404(TıbbiRaporlar, id=rapor_id, hasta=request.user.hasta)
    if request.method == 'POST':
        form = TibbiRaporlarForm(request.POST, request.FILES, instance=rapor)
        if form.is_valid():
            form.save()
            return redirect('hasta_tibbirapor_liste')
    else:
        form = TibbiRaporlarForm(instance=rapor)
    return render(request, 'log/hasta_tibbirapor_duzenle.html', {'form': form, 'rapor': rapor})

from .forms import DoktorTibbiRaporEkleForm


@login_required
def doktor_hasta_listesi(request):
    doktor = request.user.doktor  # Giriş yapmış doktoru al
    # Doktora ait tıbbi raporları bul
    tibbi_raporlar = TıbbiRaporlar.objects.filter(doktor=doktor)

    hastalar = []
    # Her bir tıbbi raporu tarayarak hastaları bul
    for rapor in tibbi_raporlar:
        hastalar.append(rapor.hasta)

    context = {
        'doktor': doktor,
        'hastalar': hastalar,
    }
    return render(request, 'log/doktor_hasta_listesi.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json
from .models import TıbbiRaporlar
from .forms import DoktorTibbiRaporEkleForm


@login_required
def doktor_tibbirapor_ekle(request):
    if request.method == 'POST':
        form = DoktorTibbiRaporEkleForm(request.POST, request.FILES)
        if form.is_valid():
            rapor = form.save(commit=False)
            rapor.doktor = request.user.doktor  # Oturum açmış olan doktora atanıyor
            rapor.save()
            return redirect('doktor_paneli')
    else:
        form = DoktorTibbiRaporEkleForm()
    return render(request, 'log/doktor_tibbirapor_ekle.html', {'form': form})

@login_required
def doktor_tibbirapor_liste(request):
    raporlar = TıbbiRaporlar.objects.filter(doktor=request.user.doktor)
    return render(request, 'log/doktor_tibbirapor_liste.html', {'raporlar': raporlar})


@login_required
def doktor_tibbirapor_json_goruntule(request, rapor_id):
    rapor = get_object_or_404(TıbbiRaporlar, id=rapor_id, doktor=request.user.doktor)
    return JsonResponse(rapor.rapor_json)


@login_required
def doktor_tibbirapor_sil(request, rapor_id):
    rapor = get_object_or_404(TıbbiRaporlar, id=rapor_id, doktor=request.user.doktor)
    if request.method == 'POST':
        rapor.delete()
        return redirect('doktor_tibbirapor_liste')
    return render(request, 'log/doktor_tibbirapor_sil.html', {'rapor': rapor})

@login_required
def doktor_tibbirapor_indir(request, rapor_id):
    rapor = get_object_or_404(TıbbiRaporlar, id=rapor_id, doktor=request.user.doktor)
    response = HttpResponse(json.dumps(rapor.rapor_json, ensure_ascii=False, indent=4), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename=rapor_{rapor_id}.json'
    return response

@login_required
def doktor_tibbirapor_duzenle(request, rapor_id):
    rapor = get_object_or_404(TıbbiRaporlar, id=rapor_id, doktor=request.user.doktor)
    if request.method == 'POST':
        form = DoktorTibbiRaporEkleForm(request.POST, request.FILES, instance=rapor)
        if form.is_valid():
            form.save()
            return redirect('doktor_tibbirapor_liste')
    else:
        form = DoktorTibbiRaporEkleForm(instance=rapor)
    return render(request, 'log/doktor_tibbirapor_duzenle.html', {'form': form, 'rapor': rapor})




from django.http import HttpResponse, JsonResponse

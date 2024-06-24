from django.urls import path
from . import views
from .views import hasta_sil, hasta_raporlar,hasta_bilgileri, hasta_guncelle
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.blogs),
    path('admin/', admin.site.urls),
    path('yonetici_giris/', views.yonetici_giris, name='yonetici_giris'),
    path('yonetici_paneli/', views.yonetici_paneli, name='yonetici_paneli'),
    path('hasta_giris/', views.hasta_giris, name='hasta_giris'),
    path('hasta_paneli/', views.hasta_paneli, name='hasta_paneli'),
    path('hasta_ekle/', views.hasta_ekle, name='hasta_ekle'),
    path('doktor_ekle/', views.doktor_ekle, name='doktor_ekle'),
    path('hasta_liste/', views.hasta_liste, name='hasta_liste'),
    path('doktor_liste/', views.doktor_liste, name='doktor_liste'),
    path('doktor_sil/<int:doktor_id>/', views.doktor_sil, name='doktor_sil'),
    path('randevu_al/', views.randevu_al, name='randevu_al'),
    path('hasta_sil/<int:hasta_id>/', views.hasta_sil, name='hasta_sil'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='log/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('randevu_liste/', views.randevu_liste, name='randevu_liste'),
    path('randevu_sil/<int:randevu_id>/', views.randevu_sil, name='randevu_sil'),
    path('doktor_giris/', views.doktor_giris, name='doktor_giris'),
    path('doktor_paneli/', views.doktor_paneli, name='doktor_paneli'),
    path('doktor/hasta-listesi/', views.doktor_hasta_listesi, name='doktor_hasta_listesi'),
    path('yonetici/tibbi-rapor-ekle/', views.yonetici_tibbirapor_ekle, name='yonetici_tibbirapor_ekle'),
    path('yonetici/tibbi-rapor-liste/', views.yonetici_tibbirapor_liste, name='yonetici_tibbirapor_liste'),
    path('yonetici/tibbi-rapor/<int:rapor_id>/json/', views.yonetici_tibbirapor_json_goruntule,name='yonetici_tibbirapor_json_goruntule'),
    path('yonetici/tum-raporlar-json/', views.tum_raporlar_json, name='tum_raporlar_json'),
    path('yonetici/tibbi-rapor-sil/<int:rapor_id>/', views.yonetici_tibbirapor_sil,name='yonetici_tibbirapor_sil'),
    path('yonetici/tibbi-rapor-indir/<int:rapor_id>/', views.yonetici_tibbirapor_indir,name='yonetici_tibbirapor_indir'),
    path('yonetici/tibbi-rapor-duzenle/<int:rapor_id>/', views.yonetici_tibbirapor_duzenle,name='yonetici_tibbirapor_duzenle'),
    path('hasta_raporlar/<int:hasta_id>/', hasta_raporlar, name='hasta_raporlar'),
    path('hasta_bilgileri/<int:hasta_id>/', hasta_bilgileri, name='hasta_bilgileri'),
    path('hasta_guncelle/<int:hasta_id>/', hasta_guncelle, name='hasta_guncelle'),

    path('doktor_duzenle/<int:doktor_id>/', views.doktor_duzenle, name='doktor_duzenle'),

    path('hasta/tibbi-rapor-ekle/', views.hasta_tibbirapor_ekle, name='hasta_tibbirapor_ekle'),
    path('hasta/tibbi-rapor-liste/', views.hasta_tibbirapor_liste,name='hasta_tibbirapor_liste'),
    path('hasta/tibbi-rapor/<int:rapor_id>/json/', views.hasta_tibbirapor_json_goruntule,name='hasta_tibbirapor_json_goruntule'),
    path('hasta/tum-raporlar-json/', views.tum_raporlar_json, name='tum_raporlar_json'),
    path('hasta/tibbi-rapor-sil/<int:rapor_id>/', views.hasta_tibbirapor_sil,name='hasta_tibbirapor_sil'),
    path('hasta/tibbi-rapor-indir/<int:rapor_id>/', views.hasta_tibbirapor_indir,name='hasta_tibbirapor_indir'),
    path('hasta/tibbi-rapor-duzenle/<int:rapor_id>/', views.hasta_tibbirapor_duzenle,name='hasta_tibbirapor_duzenle'),


    path('doktor/tibbirapor-ekle/', views.doktor_tibbirapor_ekle, name='doktor_tibbirapor_ekle'),
    path('doktor/tibbirapor-liste/', views.doktor_tibbirapor_liste, name='doktor_tibbirapor_liste'),
    path('doktor/tibbi-rapor/<int:rapor_id>/json/', views.doktor_tibbirapor_json_goruntule, name='doktor_tibbirapor_json_goruntule'),
    path('doktor/tum-raporlar-json/', views.tum_raporlar_json, name='tum_raporlar_json'),
    path('doktor/tibbi-rapor-sil/<int:rapor_id>/', views.doktor_tibbirapor_sil, name='doktor_tibbirapor_sil'),
    path('doktor/tibbi-rapor-indir/<int:rapor_id>/', views.doktor_tibbirapor_indir, name='doktor_tibbirapor_indir'),
    path('doktor/tibbi-rapor-duzenle/<int:rapor_id>/', views.doktor_tibbirapor_duzenle, name='doktor_tibbirapor_duzenle'),

    path('doktor_hasta_listesi/', views.doktor_hasta_listesi, name='doktor_hasta_listesi'),

              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

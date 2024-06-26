# Hospital Management System

## Overview

KOCAELİ ÜNİVERSİTESİ - BİLGİSAYAR MÜHENDİSLİĞİ BÖLÜMÜ 2023-2024
BLM210 PROGRAMLAMA LAB. II - PROJE 3

Bu proje, hastane yönetim sistemi olarak tasarlanmış bir web uygulamasıdır. Hastaların kayıt oluşturabileceği, doktorlarla randevu alabileceği, tıbbi raporları saklayabileceği ve genel olarak sağlıkla ilgili işlemleri yönetebileceği bir platform sunmayı amaçlamaktadır.

## Features

1. **Hasta Yönetimi:**
   - Hasta ekleme, silme ve güncelleme işlemleri yapılabilir.
   - Hastaların temel bilgileri saklanır: HastaID, Ad, Soyad, Doğum Tarihi, Cinsiyet, Telefon Numarası, Adres vb.

2. **Doktor Yönetimi:**
   - Doktor ekleme, silme ve güncelleme işlemleri yapılabilir.
   - Doktorların temel bilgileri saklanır: DoktorID, Ad, Soyad, Uzmanlık Alanı, Çalıştığı Hastane vb.

3. **Randevu Yönetimi:**
   - Hastaların doktorlarla randevu alabileceği ve randevularını iptal edebileceği bir sistem.
   - Randevuların temel bilgileri saklanır: RandevuID, Randevu Tarihi, Randevu Saati vb.

4. **Tıbbi Rapor Yönetimi:**
   - Hastaların tıbbi raporlarını ekleyip görüntüleyebileceği bir sistem.
   - Tıbbi raporlar JSON formatında ve resim dosyaları olarak saklanır.
   - Raporların temel bilgileri saklanır: RaporID, Rapor Tarihi, Rapor İçeriği vb.

5. **Kullanıcı Arayüzü:**
   - Kullanıcı dostu bir arayüz üzerinden tüm işlemler yapılabilir.
   - Dinamik bileşenler ve AJAX kullanımı ile sayfa yenilemeden dosya yükleme ve indirme işlemleri gerçekleştirilebilir.

6. **Bildirim Sistemi:**
   - Kullanıcılara yeni laboratuvar sonuçları yüklendiğinde veya güncellendiğinde bildirim gönderen bir sistem.

## Database Design

Veritabanı tasarımı aşağıdaki tabloları içerir:
- Hastalar: HastaID, Ad, Soyad, Doğum Tarihi, Cinsiyet, Telefon Numarası, Adres 
- Doktorlar: DoktorID, Ad, Soyad, Uzmanlık Alanı, Çalıştığı Hastane 
- Yönetici: YoneticiID
- Randevular: RandevuID, Randevu Tarihi, Randevu Saati 
- Tıbbi Raporlar: RaporID, Rapor Tarihi, Rapor İçeriği 

### Normalization
Veritabanı 1NF, 2NF ve 3NF kurallarına göre normalize edilmiştir.

## Technologies Used

- **Backend:** Python
- **Frontend:** HTML
- **Database:** MySQL

## Setup and Installation

### Clone the repository
```sh
git clone https://github.com/icsiee/HospitalSystem.git
cd HospitalSystem

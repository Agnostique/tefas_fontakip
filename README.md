# TEFAS Portföy Takip Telegram Botu

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Bu proje, Türkiye Elektronik Fon Dağıtım Platformu (TEFAS) verilerini kullanarak kişisel yatırım fonu portföyünüzü takip eden bir Telegram botudur. Belirlediğiniz fonların anlık fiyatlarını çeker, maliyetlerinize göre kar/zarar durumunu, yatırım süresini ve günlük performansı hesaplayarak size özel bir analiz sunar.

## Örnek Ekran Görüntüsü

Botun `/portfoyum` komutuna verdiği yanıt aşağıdakine benzer olacaktır:

```
📈 Portföyünüzün Güncel Durumu 📈

*MKG* - AKTİF PORTFÖY ALTIN KATILIM FONU
  Adet: 76047
  Maliyet: 11.7016 TL
  Güncel Fiyat: 11.8500 TL
  Alım Tarihi: 2025-07-23
  Geçen Süre: 7 gün
  Toplam K/Z: +11264.44 TL (%1.27) ✅
  Günlük K/Z: +1609.21 TL

*IDL* - AKTİF PORTFÖY PARA PİYASASI (TL) FONU
  Adet: 566457
  Maliyet: 3.9814 TL
  Güncel Fiyat: 4.1000 TL
  Toplam K/Z: +67185.76 TL (%2.98) ✅
  Günlük K/Z: +9597.97 TL

-----------------------------------
📊 Toplam Portföy Özeti 📊
  Toplam Maliyet: 3145678.90 TL
  Güncel Değer: 3224499.10 TL
  Toplam Kar/Zarar: +78420.20 TL (%2.50) ✅
```

## Özellikler

- **Anlık Veri:** TEFAS'tan güncel fon fiyatlarını çeker.
- **Detaylı Analiz:** Her bir fon için aşağıdaki metrikleri hesaplar:
  - Toplam Kar/Zarar (Tutar ve Yüzde)
  - Alım tarihinden itibaren geçen gün sayısı
  - Günlük ortalama Kar/Zarar tutarı
- **Portföy Özeti:** Tüm varlıkların toplam maliyetini, güncel değerini ve genel kar/zarar durumunu özetler.
- **Kolay Kurulum:** Birkaç adımla kolayca kendi sunucunuzda çalıştırılabilir.
- **Kişiselleştirilebilir:** Kendi portföy bilgilerinizi (fon kodu, adet, maliyet, tarih) kod içerisinden kolayca güncelleyebilirsiniz.

## Kurulum

Projeyi kendi sunucunuzda çalıştırmak için aşağıdaki adımları izleyin.

1.  **Projeyi Klonlayın:**
    ```bash
    git clone https://github.com/Agnostique/tefas_fontakip.git
    cd tefas_fontakip
    ```

2.  **Gerekli Kütüphaneleri Yükleyin:**
    Aşağıdaki tek satır komut, botun çalışması için gerekli tüm Python kütüphanelerini kuracaktır.
    ```bash
    pip install python-telegram-bot tefas-crawler pandas
    ```

## Yapılandırma

Botu çalıştırmadan önce `fon_bot.py` dosyasında birkaç temel yapılandırma yapmanız gerekmektedir.

1.  **Telegram Bot Token:**
    - Telegram'da `BotFather` ile konuşarak yeni bir bot oluşturun ve size verdiği API Token'ını alın.
    - `fon_bot.py` dosyasındaki `TELEGRAM_API_TOKEN` değişkenine bu token'ı atayın.

    > **⚠️ Güvenlik Uyarısı:**
    > API Token'ınız botunuzun şifresidir. **Asla** bu token'ı halka açık bir GitHub reposunda veya başkalarıyla paylaşmayın! Profesyonel projelerde bu tür gizli bilgileri "Environment Variables" (Ortam Değişkenleri) veya `.env` dosyaları ile yönetmek en iyi pratiktir.

2.  **Portföy Bilgileri:**
    - `fon_bot.py` dosyasının en üstündeki `PORTFOY` listesini kendi fonlarınıza göre düzenleyin.
    - Her bir fon için `kod`, `adet`, `maliyet` ve `tarih` bilgilerini doğru formatta girin.
    - **Unutmayın:** Ondalık sayılarda nokta (`.`), tarihlerde ise `YYYY-AA-GG` formatını kullanın.

## Kullanım

1.  **Botu Başlatma:**
    Yapılandırmayı tamamladıktan sonra, sunucunuzun terminalinde aşağıdaki komutu çalıştırın:
    ```bash
    python3 fon_bot.py
    ```

2.  **Telegram Komutları:**
    - `/start`: Bota hoşgeldin mesajı attırır.
    - `/portfoyum`: Portföyünüzün detaylı analizini getirir.

## Veri Kaynağı

Bu bot, tüm fon verilerini Türkiye Elektronik Fon Dağıtım Platformu (TEFAS) üzerinden anlık olarak çekmektedir. Botun çalışması, TEFAS'ın altyapısının ve veri sunum şeklinin devamlılığına bağlıdır.

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.

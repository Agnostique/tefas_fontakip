# TEFAS Portföy Takip Telegram Botu

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Bu proje, Türkiye Elektronik Fon Dağıtım Platformu (TEFAS) verilerini kullanarak kişisel yatırım fonu portföyünüzü takip eden bir Telegram botudur. Belirlediğiniz fonların anlık fiyatlarını çeker, maliyetlerinize göre kar/zarar durumunu, yatırım süresini ve günlük performansı hesaplayarak size özel bir analiz sunar.

## Örnek Ekran Görüntüsü

Botun `/portfoyum` komutuna verdiği yanıt, tüm yeni özelliklerle birlikte aşağıdakine benzer olacaktır:

```
📈 Portföyünüzün Güncel Durumu 📈

*TGE* - İŞ PORTFÖY EMTİA YABANCI BYF FON SEPETİ FONU
  Adet: `50`
  Maliyet: `15.2500` TL
  Güncel Fiyat: `22.5000` TL
  Toplam Değer: `1.125,00` TL
  Alım Tarihi: `2024-11-01`
  Geçen Süre: `278 gün`
  Toplam K/Z: `+362,50 TL (%47.54)` ✅
  Günlük K/Z: `+1,30 TL`

-----------------------------------
📊 Toplam Portföy Özeti 📊
  Toplam Maliyet: `889.375,12 TL`
  Güncel Değer: `901.156,95 TL`
  Toplam Kar/Zarar: `+11.781,83 TL (%1.32)` ✅
```

## Özellikler

- **Anlık Veri:** TEFAS'tan güncel fon fiyatlarını çeker.
- **Detaylı Analiz:** Her bir fon için aşağıdaki metrikleri hesaplar:
  - Fonun güncel toplam değeri.
  - Alım tarihinden itibaren geçen gün sayısı.
  - Toplam Kar/Zarar (Tutar ve Yüzde).
  - Günlük ortalama Kar/Zarar tutarı.
- **Okunaklı Raporlama:** Tüm parasal değerleri, okumayı kolaylaştırmak için Türkçe formatında (`1.234,56 TL`) gösterir.
- **Portföy Özeti:** Tüm varlıkların toplam maliyetini, güncel değerini ve genel kar/zarar durumunu özetler.
- **Sağlam ve Güvenilir:** `tefas-crawler` kütüphanesi sayesinde TEFAS'taki altyapı değişikliklerine karşı dayanıklıdır.
- **Hata Yönetimi:** Bir fonun verisi alınamazsa bile diğer fonların analizine devam eder.

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
    > API Token'ınız botunuzun şifresidir. **Asla** bu token'ı halka açık bir GitHub reposunda veya başkalarıyla paylaşmayın!

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

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.

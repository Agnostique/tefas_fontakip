# -*- coding: utf-8 -*-
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from tefas import Crawler
import pandas as pd
from datetime import date, datetime

# --- YAPILANDIRMA (CONFIGURATION) ---
# 1. GÜVENLİK UYARISI: GERÇEK TOKEN'INIZI GITHUB'A YÜKLEMEYİN!
# Botu kendi sunucunuzda çalıştırırken buraya BotFather'dan aldığınız token'ı yazın.
TELEGRAM_API_TOKEN = "BURAYA_KENDİ_TELEGRAM_TOKENINIZI_GİRİN"

# 2. PORTFÖYÜNÜZÜ BURAYA GİRİN
#    ÖNEMLİ: Ondalık sayılarda NOKTA (.) kullanın. Tarihleri 'YYYY-AA-GG' formatında yazın.
#    Aşağıdaki örnekleri silip kendi fonlarınızı ekleyebilirsiniz.
PORTFOY = [
    # {'kod': 'TGE', 'adet': 50, 'maliyet': 15.25, 'tarih': '2024-11-01'},
    # {'kod': 'AFA', 'adet': 200, 'maliyet': 1.80, 'tarih': '2025-07-01'},
]
# --- YAPILANDIRMA SONU ---


def format_currency_tr(value):
    """
    Bir sayıyı Türkçe para formatına (1.234.567,89) çevirir.
    """
    try:
        formatted_str = "{:,.2f}".format(float(value))
        formatted_str = formatted_str.replace(',', '#').replace('.', ',')
        formatted_str = formatted_str.replace('#', '.')
        return formatted_str
    except (ValueError, TypeError):
        return str(value)

def tefas_verilerini_cek():
    """
    'tefas-crawler' kütüphanesini kullanarak tüm fonların güncel verilerini çeker.
    """
    try:
        today_str = date.today().strftime('%Y-%m-%d')
        tefas = Crawler()
        data = tefas.fetch(start=today_str, end=today_str, columns=['code', 'title', 'price'])
        print(f"TEFAS verileri ({today_str}) başarıyla çekildi.")
        data.columns = ['Kod', 'Ad', 'Fiyat']
        data['Fiyat'] = pd.to_numeric(data['Fiyat'].astype(str).str.replace(',', '.'), errors='coerce')
        return data
    except Exception as e:
        print(f"Hata: 'tefas-crawler' ile veri çekilirken bir sorun oluştu: {e}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start komutuna yanıt verir."""
    user = update.effective_user
    await update.message.reply_html(
        f"Merhaba {user.mention_html()}! 👋\n\n"
        "Portföyünün güncel durumunu, kar/zarar analizi ile görmek için /portfoyum komutunu kullanabilirsin."
    )

async def portfoy_sorgula(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/portfoyum komutuyla portföydeki fonların kar/zarar analizini yapar."""
    await update.message.reply_text('Portföy analizi için TEFAS\'tan güncel veriler alınıyor, lütfen bekleyin...')
    
    fon_verileri_df = tefas_verilerini_cek()
    
    if fon_verileri_df is None or fon_verileri_df.empty:
        await update.message.reply_text('❌ TEFAS\'tan bugün için veri alınamadı. Muhtemelen piyasalar kapalı (hafta sonu/resmi tatil).')
        return
            
    mesaj = "📈 **Portföyünüzün Güncel Durumu** 📈\n\n"
    toplam_maliyet = 0
    toplam_guncel_deger = 0
    
    bugun = date.today()
    for fon_portfoy in PORTFOY:
        try:
            fon_kodu = fon_portfoy['kod']
            adet = fon_portfoy['adet']
            maliyet_fiyati = fon_portfoy['maliyet']
            alim_tarihi_str = fon_portfoy['tarih']
            
            fon_bilgisi = fon_verileri_df[fon_verileri_df['Kod'].str.upper() == fon_kodu.upper()]
            
            if not fon_bilgisi.empty and pd.notna(fon_bilgisi['Fiyat'].iloc[0]):
                guncel_fiyat = float(fon_bilgisi['Fiyat'].iloc[0])
                fon_adi = fon_bilgisi['Ad'].iloc[0]
                
                alim_tarihi = datetime.strptime(alim_tarihi_str, '%Y-%m-%d').date()
                gecen_gun = (bugun - alim_tarihi).days
                gecen_gun = max(1, gecen_gun) 
                
                maliyet_toplam = adet * maliyet_fiyati
                guncel_deger_toplam = adet * guncel_fiyat
                kar_zarar_tutar = guncel_deger_toplam - maliyet_toplam
                kar_zarar_yuzde = (kar_zarar_tutar / maliyet_toplam) * 100 if maliyet_toplam > 0 else 0
                gunluk_kar_zarar = kar_zarar_tutar / gecen_gun
                
                toplam_maliyet += maliyet_toplam
                toplam_guncel_deger += guncel_deger_toplam

                mesaj += f"*{fon_kodu}* - {fon_adi}\n"
                mesaj += f"  Adet: `{adet}`\n"
                mesaj += f"  Maliyet: `{maliyet_fiyati:.4f}` TL\n"
                mesaj += f"  Güncel Fiyat: `{guncel_fiyat:.4f}` TL\n"
                mesaj += f"  Toplam Değer: `{format_currency_tr(guncel_deger_toplam)}` TL\n"
                mesaj += f"  Alım Tarihi: `{alim_tarihi_str}`\n"
                mesaj += f"  Geçen Süre: `{gecen_gun} gün`\n"

                if kar_zarar_tutar >= 0:
                    mesaj += f"  Toplam K/Z: `+{format_currency_tr(kar_zarar_tutar)} TL (%{kar_zarar_yuzde:.2f})` ✅\n"
                    mesaj += f"  Günlük K/Z: `+{format_currency_tr(gunluk_kar_zarar)} TL`\n\n"
                else:
                    mesaj += f"  Toplam K/Z: `{format_currency_tr(kar_zarar_tutar)} TL (%{kar_zarar_yuzde:.2f})` 🔻\n"
                    mesaj += f"  Günlük K/Z: `{format_currency_tr(gunluk_kar_zarar)} TL`\n\n"
            else:
                mesaj += f"*{fon_kodu}*: Bu kodla eşleşen fon bulunamadı veya fiyatı geçersiz.\n\n"
        except Exception as e:
            fon_kodu_hata = fon_portfoy.get('kod', 'Bilinmeyen Fon')
            mesaj += f"*{fon_kodu_hata}*: Bu fon işlenirken bir hata oluştu: `{e}`\n\n"

    # Eğer hiç fon girilmemişse veya hiçbiri işlenememişse özet gösterme
    if toplam_maliyet > 0:
        toplam_kar_zarar = toplam_guncel_deger - toplam_maliyet
        toplam_kar_zarar_yuzde = (toplam_kar_zarar / toplam_maliyet) * 100
        
        mesaj += "-----------------------------------\n"
        mesaj += "📊 **Toplam Portföy Özeti** 📊\n"
        mesaj += f"  Toplam Maliyet: `{format_currency_tr(toplam_maliyet)} TL`\n"
        mesaj += f"  Güncel Değer: `{format_currency_tr(toplam_guncel_deger)} TL`\n"
        
        if toplam_kar_zarar >= 0:
            mesaj += f"  Toplam Kar/Zarar: `+{format_currency_tr(toplam_kar_zarar)} TL (%{toplam_kar_zarar_yuzde:.2f})` ✅\n"
        else:
            mesaj += f"  Toplam Kar/Zarar: `{format_currency_tr(toplam_kar_zarar)} TL (%{toplam_kar_zarar_yuzde:.2f})` 🔻\n"

    await update.message.reply_text(mesaj, parse_mode='Markdown')

def main() -> None:
    """Botu başlatır ve çalıştırır."""
    print("Gelişmiş Portföy Botu başlatılıyor...")
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("portfoyum", portfoy_sorgula))
    application.run_polling()
    print("Bot durduruldu.")

if __name__ == '__main__':
    main()

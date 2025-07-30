from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from tefas import Crawler
import pandas as pd
from datetime import date, datetime

# --- BURAYI DÜZENLEYİN ---
# 1. GÜVENLİK UYARISI: Bu token'ı BotFather'dan yenileyip gizli tutmanız önemlidir.
TELEGRAM_API_TOKEN = "BURAYA_KENDİ_TELEGRAM_TOKENINIZI_GİRİN"

# 2. PORTFÖYÜNÜZÜ BURAYA GİRİN
#    İstediğiniz üzerine portföyünüz güncellenmiştir.
#    Yeni fon eklemek isterseniz aşağıdaki formatta ekleyebilirsiniz.
#    ÖNEMLİ: Ondalık sayılarda NOKTA (.) kullanın. Tarihleri 'YYYY-AA-GG' formatında yazın.
PORTFOY = [
    {'kod': 'MKG', 'adet': 1,    'maliyet': 11.701644, 'tarih': '2025-01-01'},
    {'kod': 'IDL', 'adet': 1,   'maliyet': 3.981394,  'tarih': '2025-01-01'},
]
# --- DÜZENLEME SONU ---


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
        data['Fiyat'] = pd.to_numeric(data['Fiyat'], errors='coerce')
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
        await update.message.reply_text('❌ TEFAS\'tan bugün için veri alınamadı. Muhtemelen piyasalar kapalı (hafta sonu/resmi tatil). Lütfen daha sonra tekrar deneyin.')
        return
            
    mesaj = "📈 **Portföyünüzün Güncel Durumu** 📈\n\n"
    toplam_maliyet = 0
    toplam_guncel_deger = 0
    
    try:
        bugun = date.today()
        for fon_portfoy in PORTFOY:
            fon_kodu = fon_portfoy['kod']
            adet = fon_portfoy['adet']
            maliyet_fiyati = fon_portfoy['maliyet']
            alim_tarihi_str = fon_portfoy['tarih']
            
            fon_bilgisi = fon_verileri_df[fon_verileri_df['Kod'].str.upper() == fon_kodu.upper()]
            
            if not fon_bilgisi.empty and pd.notna(fon_bilgisi['Fiyat'].iloc[0]):
                guncel_fiyat = fon_bilgisi['Fiyat'].iloc[0]
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
                mesaj += f"  Alım Tarihi: `{alim_tarihi_str}`\n"
                mesaj += f"  Geçen Süre: `{gecen_gun} gün`\n"

                if kar_zarar_tutar >= 0:
                    mesaj += f"  Toplam K/Z: `+{kar_zarar_tutar:.2f} TL (%{kar_zarar_yuzde:.2f})` ✅\n"
                    mesaj += f"  Günlük K/Z: `+{gunluk_kar_zarar:.2f} TL`\n\n"
                else:
                    mesaj += f"  Toplam K/Z: `{kar_zarar_tutar:.2f} TL (%{kar_zarar_yuzde:.2f})` 🔻\n"
                    mesaj += f"  Günlük K/Z: `{gunluk_kar_zarar:.2f} TL`\n\n"
            else:
                mesaj += f"*{fon_kodu}*: Bu kodla eşleşen fon bulunamadı veya fiyatı geçersiz.\n\n"
        
        toplam_kar_zarar = toplam_guncel_deger - toplam_maliyet
        toplam_kar_zarar_yuzde = (toplam_kar_zarar / toplam_maliyet) * 100 if toplam_maliyet > 0 else 0
        
        mesaj += "-----------------------------------\n"
        mesaj += "📊 **Toplam Portföy Özeti** 📊\n"
        mesaj += f"  Toplam Maliyet: `{toplam_maliyet:.2f} TL`\n"
        mesaj += f"  Güncel Değer: `{toplam_guncel_deger:.2f} TL`\n"
        
        if toplam_kar_zarar >= 0:
            mesaj += f"  Toplam Kar/Zarar: `+{toplam_kar_zarar:.2f} TL (%{toplam_kar_zarar_yuzde:.2f})` ✅\n"
        else:
            mesaj += f"  Toplam Kar/Zarar: `{toplam_kar_zarar:.2f} TL (%{toplam_kar_zarar_yuzde:.2f})` 🔻\n"

    except Exception as e:
        await update.message.reply_text(f'❌ Hata: Veriler işlenirken bir sorun oluştu: {e}')
        return

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

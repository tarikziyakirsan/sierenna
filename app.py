import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

# Sayfa Yapılandırması
st.set_page_config(page_title="BIST Tüm Evren Analizi", layout="wide")

st.title("📊 BIST Tüm Şirketler Master Analiz Paneli")
st.write("Teknik Momentum, Temel Değerleme ve 6 Aylık Performans Denetimi")

# 1. TÜM BİST LİSTESİ (Benzersiz hale getirilmiş ~560 Hisse)
bist_full_list = sorted(list(set([
    "A1CAP.IS", "ACSEL.IS", "ADEZ.IS", "ADESE.IS", "AEFES.IS", "AFYON.IS", "AGESA.IS", "AGHOL.IS", "AGROT.IS", "AKBNK.IS",
    "AKCNS.IS", "AKENR.IS", "AKFGY.IS", "AKFYE.IS", "AKGRT.IS", "AKMGY.IS", "AKSA.IS", "AKSEN.IS", "ALARK.IS", "ALBRK.IS",
    "ALCTL.IS", "ALFAS.IS", "ALGYO.IS", "ALKA.IS", "ALKIM.IS", "ALMAD.IS", "ANELE.IS", "ANGEN.IS", "ANHYT.IS", "ANSGR.IS",
    "ARCLK.IS", "ARDYZ.IS", "ARENA.IS", "ARSAN.IS", "ASCEG.IS", "ASELS.IS", "ASGYO.IS", "ASTOR.IS", "ASUZU.IS", "ATAKP.IS",
    "ATATP.IS", "AYDEM.IS", "AYEN.IS", "AYGAZ.IS", "AZTEK.IS", "BAGFS.IS", "BAKAB.IS", "BANVT.IS", "BARMA.IS", "BASGZ.IS",
    "BERA.IS", "BEYAZ.IS", "BIENP.IS", "BIGCH.IS", "BIMAS.IS", "BIOEN.IS", "BIZIM.IS", "BJKAS.IS", "BLCYT.IS", "BMTKS.IS",
    "BNTAS.IS", "BOBET.IS", "BORLS.IS", "BOSSA.IS", "BRISA.IS", "BRSAN.IS", "BRYAT.IS", "BSOKE.IS", "BTCIM.IS", "BUCIM.IS",
    "BURCE.IS", "BVSAN.IS", "BYDNR.IS", "CANTE.IS", "CATES.IS", "CCOLA.IS", "CELHA.IS", "CEMAS.IS", "CEMTS.IS", "CEOEM.IS",
    "CIMSA.IS", "CLEBI.IS", "CONSE.IS", "CVKMD.IS", "CWENE.IS", "DAGHL.IS", "DAGI.IS", "DAPGM.IS", "DARDL.IS", "DGATE.IS",
    "DGGYO.IS", "DGNMO.IS", "DITAS.IS", "DMSAS.IS", "DNISI.IS", "DOAS.IS", "DOCO.IS", "DOGUB.IS", "DOHOL.IS", "DOKTA.IS",
    "DURDO.IS", "DYOBY.IS", "DZGYO.IS", "EBEBK.IS", "ECILC.IS", "ECZYT.IS", "EDATA.IS", "EGEEN.IS", "EGGUB.IS", "EGPRO.IS",
    "EGSER.IS", "EKGYO.IS", "EKOS.IS", "EKSUN.IS", "ELITE.IS", "EMKEL.IS", "ENERY.IS", "ENJSA.IS", "ENKAI.IS", "ENSRI.IS",
    "ERBOS.IS", "EREGL.IS", "ERSU.IS", "ESCOM.IS", "ESEN.IS", "EUPWR.IS", "EUREN.IS", "EYGYO.IS", "FENER.IS", "FLAP.IS",
    "FMIZP.IS", "FONET.IS", "FORMT.IS", "FORTE.IS", "FRIGO.IS", "FROTO.IS", "FZLGY.IS", "GARAN.IS", "GEDIK.IS", "GEDZA.IS",
    "GENIL.IS", "GENTS.IS", "GEREL.IS", "GESAN.IS", "GIPTA.IS", "GLBMD.IS", "GLRYH.IS", "GLYHO.IS", "GOKNR.IS", "GOLTS.IS",
    "GOODY.IS", "GOZDE.IS", "GSDHO.IS", "GSRAY.IS", "GUBRF.IS", "GWIND.IS", "GZNMI.IS", "HALKB.IS", "HATEK.IS", "HATSN.IS",
    "HEDEF.IS", "HEKTS.IS", "HKTM.IS", "HLGYO.IS", "HTTBT.IS", "HUNER.IS", "HURGZ.IS", "ICBCT.IS", "IEYHO.IS", "IHAAS.IS",
    "IHEVA.IS", "IHGZT.IS", "IHLAS.IS", "IHLGM.IS", "IMASM.IS", "INDES.IS", "INFO.IS", "INGRM.IS", "INVEO.IS", "INVES.IS",
    "IPEKE.IS", "ISCTR.IS", "ISFIN.IS", "ISGSY.IS", "ISGYO.IS", "ISKPL.IS", "ISMEN.IS", "ISSEN.IS", "ISYAT.IS", "IZENR.IS",
    "IZMDC.IS", "JANTS.IS", "KAPLM.IS", "KARYE.IS", "KATMR.IS", "KAYSE.IS", "KCAER.IS", "KCHOL.IS", "KENT.IS", "KERVT.IS",
    "KFEIN.IS", "KGYO.IS", "KIMMR.IS", "KLGYO.IS", "KLMSN.IS", "KLNMA.IS", "KLRHO.IS", "KLSYN.IS", "KNFRT.IS", "KONKA.IS",
    "KONTR.IS", "KONYA.IS", "KORDS.IS", "KOZAA.IS", "KOZAL.IS", "KRDMA.IS", "KRDMB.IS", "KRDMD.IS", "KRGYO.IS", "KRONT.IS",
    "KRPLS.IS", "KRSTL.IS", "KRTEK.IS", "KRVGD.IS", "KTSKR.IS", "KUTPO.IS", "KUYAS.IS", "KZBGY.IS", "KZGYO.IS", "LIDER.IS",
    "LIDFA.IS", "LINK.IS", "LKMNH.IS", "LOGOS.IS", "LUKSK.IS", "MAALT.IS", "MACKO.IS", "MAGEN.IS", "MAKIM.IS", "MAKTK.IS",
    "MANAS.IS", "MARTI.IS", "MAVI.IS", "MEDTR.IS", "MEGAP.IS", "MEKAG.IS", "MEPET.IS", "MERCN.IS", "MERKO.IS", "METRO.IS",
    "METUR.IS", "MHRGY.IS", "MIATK.IS", "MIPAZ.IS", "MNDRS.IS", "MOBTL.IS", "MGROS.IS", "MPARK.IS", "MRGYO.IS", "MRSHL.IS",
    "MSGYO.IS", "MTRKS.IS", "MZHLD.IS", "NATEN.IS", "NETAS.IS", "NIBAS.IS", "NTGAZ.IS", "NUGYO.IS", "NUHCM.IS", "OBAMS.IS",
    "ODAS.IS", "ONCSM.IS", "ORCAY.IS", "ORGE.IS", "OTKAR.IS", "OYAKC.IS", "OYAYO.IS", "OYLUM.IS", "OYYAT.IS", "OZGYO.IS",
    "OZKGY.IS", "OZRDN.IS", "OZSUB.IS", "PAGYO.IS", "PAMEL.IS", "PAPIL.IS", "PARSN.IS", "PASEU.IS", "PATEK.IS", "PCILT.IS",
    "PEGYO.IS", "PEKGY.IS", "PENTA.IS", "PETKM.IS", "PETUN.IS", "PGSUS.IS", "PINSU.IS", "PKART.IS", "PKENT.IS", "PNLSN.IS",
    "PNSUT.IS", "POLHO.IS", "POLTK.IS", "PRKAB.IS", "PRKME.IS", "PRZMA.IS", "PSDTC.IS", "QUAGR.IS", "RALYH.IS", "RAYYS.IS",
    "REEDR.IS", "RNPOL.IS", "RODRG.IS", "RTALB.IS", "RUBNS.IS", "RYGYO.IS", "RYSAS.IS", "SAFKR.IS", "SAHOL.IS", "SAMAT.IS",
    "SANEL.IS", "SANKO.IS", "SARKY.IS", "SASA.IS", "SAYAS.IS", "SDTTR.IS", "SEKFK.IS", "SEKUR.IS", "SELEC.IS", "SELVA.IS",
    "SEYKM.IS", "SILVR.IS", "SISE.IS", "SKBNK.IS", "SKTAS.IS", "SKYMD.IS", "SMART.IS", "SMRTG.IS", "SNGYO.IS", "SOKM.IS",
    "SONME.IS", "SRVGY.IS", "SUMAS.IS", "SUNTK.IS", "SURGY.IS", "SUWEN.IS", "TABGD.IS", "TARKM.IS", "TATGD.IS", "TAVHL.IS",
    "TCELL.IS", "TDGYO.IS", "TEKTU.IS", "TERA.IS", "TETMT.IS", "TGSAS.IS", "THYAO.IS", "TIRE.IS", "TKFEN.IS", "TKNSA.IS",
    "TMSN.IS", "TOASO.IS", "TRCAS.IS", "TRGYO.IS", "TRILC.IS", "TSKB.IS", "TSPOR.IS", "TTKOM.IS", "TTRAK.IS", "TUCLK.IS",
    "TUKAS.IS", "TUPRS.IS", "TUREX.IS", "TURGG.IS", "TURSG.IS", "UFUK.IS", "ULAS.IS", "ULKER.IS", "ULLY.IS", "ULUFA.IS",
    "ULUSE.IS", "ULUUN.IS", "USAK.IS", "VAKBN.IS", "VAKFN.IS", "VAKKO.IS", "VANGD.IS", "VBTYZ.IS", "VERTU.IS", "VERUS.IS",
    "VESBE.IS", "VESTL.IS", "VKGYO.IS", "VKING.IS", "VRGYO.IS", "YAPRK.IS", "YAYLA.IS", "YEOTK.IS", "YESIL.IS", "YGGYO.IS",
    "YKBNK.IS", "YONGA.IS", "YUNSA.IS", "YYLGD.IS", "ZEDUR.IS", "ZOREN.IS", "ZRGYO.IS"
])))

@st.cache_data(ttl=3600)
def fetch_master_data(tickers):
    # 10 aylık veri çekiyoruz (6 aylık performans ve SMA hesaplamaları için)
    data = yf.download(tickers, period="10mo", interval="1d", group_by='ticker', progress=False)
    return data

# Yan Panel - Filtreleme
st.sidebar.header("🔍 Analiz Ayarları")
score_threshold = st.sidebar.slider("Minimum Skor Eşiği", 0, 100, 50)
st.sidebar.info(f"Toplam {len(bist_full_list)} hisse taranacak.")

if st.sidebar.button("Analizi Başlat / Güncelle"):
    raw_data = fetch_master_data(bist_full_list)
    results = []
    
    # İlerleme çubuğu
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_tickers = len(bist_full_list)
    
    for i, ticker in enumerate(bist_full_list):
        try:
            # Durum güncelleme
            status_text.text(f"Analiz ediliyor: {ticker} ({i+1}/{total_tickers})")
            
            df = raw_data[ticker].copy().dropna()
            if len(df) < 130: continue

            # --- TEKNİK & MOMENTUM ---
            cp = df['Close'].iloc[-1]
            prev_p = df['Close'].iloc[-2]
            
            day_chg = ((cp - prev_p) / prev_p) * 100
            ret_1w = ((cp - df['Close'].iloc[-6]) / df['Close'].iloc[-6]) * 100
            ret_1m = ((cp - df['Close'].iloc[-22]) / df['Close'].iloc[-22]) * 100
            ret_6m = ((cp - df['Close'].iloc[-127]) / df['Close'].iloc[-127]) * 100
            
            # RSI & SMA
            df['RSI'] = ta.rsi(df['Close'], length=14)
            rsi = df['RSI'].iloc[-1]
            sma50 = ta.sma(df['Close'], length=50).iloc[-1]
            
            # --- TEMEL VERİLER ---
            # Not: Fundamental verileri çekmek hızı yavaşlatabilir.
            info = yf.Ticker(ticker).info
            sektor = info.get('sector', 'Diğer')
            fk = info.get('trailingPE', None)
            pddd = info.get('priceToBook', None)

            # --- SKORLAMA (0-100) ---
            skor = 0
            if 30 < rsi < 45: skor += 20       # Alım bölgesi RSI
            if cp > sma50: skor += 20         # Trend yönü olumlu
            if fk and 0 < fk < 15: skor += 30  # Makul F/K
            if ret_1m > 0: skor += 30         # Momentum var

            # --- SİNYAL BELİRLEME ---
            if day_chg >= 9.5: sinyal = "🚀 TAVAN"
            elif rsi < 30: sinyal = "💎 GÜÇLÜ AL"
            elif rsi > 70: sinyal = "🔥 GÜÇLÜ SAT"
            elif skor >= 70: sinyal = "✅ AL"
            elif skor >= 40: sinyal = "⌛ BEKLE"
            else: sinyal = "⚠️ RİSKLİ / SAT"

            results.append({
                "Sektör": sektor, 
                "Hisse": ticker.replace(".IS", ""), 
                "Fiyat": round(cp, 2),
                "Günlük %": round(day_chg, 2), 
                "1H %": round(ret_1w, 1), 
                "1A %": round(ret_1m, 1),
                "6A %": round(ret_6m, 1), 
                "RSI": round(rsi, 1), 
                "F/K": round(fk, 1) if fk else "N/A",
                "PD/DD": round(pddd, 1) if pddd else "N/A",
                "Skor": skor, 
                "Sinyal": sinyal
            })
            
            # İlerleme çubuğunu güncelle
            progress_bar.progress((i + 1) / total_tickers)
            
        except: 
            continue

    # Analiz tamamlandı mesajı
    status_text.text("Analiz Tamamlandı!")
    
    # Veriyi DataFrame'e dök
    res_df = pd.DataFrame(results)
    
    # Filtreleme: Kullanıcının belirlediği skorun üzerindekileri getir
    final_df = res_df[res_df['Skor'] >= score_threshold].sort_values(by=["Sektör", "Skor"], ascending=[True, False])
    
    # Görselleştirme
    st.success(f"Analiz bitti. Şartları sağlayan {len(final_df)} hisse bulundu.")
    
    # Renkli Tablo
    st.dataframe(
        final_df.style.background_gradient(subset=['Skor'], cmap='RdYlGn'), 
        use_container_width=True
    )
    
    # Excel/CSV İndirme Butonu
    csv = final_df.to_csv(index=False).encode('utf-8')
    st.download_button("Sonuçları İndir (CSV)", csv, "bist_analiz_sonuclari.csv", "text/csv")

else:
    st.info("Lütfen sol paneldeki 'Analizi Başlat' butonuna tıklayarak işlemi başlatın. 500+ hissenin taranması birkaç dakika sürebilir.")
    # Tablonun hemen altına eklenecek grafik kodu
st.markdown("---")
st.subheader("📈 Hisse Detay Analizi")
selected_ticker = st.selectbox("Grafiğini görmek istediğiniz hisseyi seçin:", bist_full_list)

if selected_ticker:
    detail_data = yf.download(selected_ticker, period="6mo", interval="1d", progress=False)
    detail_data['SMA50'] = ta.sma(detail_data['Close'], length=50)
    detail_data['SMA200'] = ta.sma(detail_data['Close'], length=200)
    
    # Grafik çizimi
    st.line_chart(detail_data[['Close', 'SMA50', 'SMA200']])
    st.write(f"{selected_ticker} için son 6 aylık fiyat ve ortalama grafiği.")

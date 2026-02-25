import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import feedparser
import pytz  # Saat dilimi yönetimi için
from urllib.parse import quote
from datetime import datetime
from email.utils import parsedate_to_datetime

# --- 1. SAYFA AYARLARI VE SAAT DİLİMİ ---
st.set_page_config(page_title="BIST Analiz Terminali", layout="wide", initial_sidebar_state="collapsed")

# Türkiye Saat Dilimi Tanımlama
TR_TZ = pytz.timezone('Europe/Istanbul')

# Sidebar'ı tamamen gizleyen CSS
st.markdown("""
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarNav"], .css-1dp56ee, .css-yk4q2l {
            display: none !important;
        }
        .stApp { margin-left: 0px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. BAŞLIK VE YASAL UYARI ---
st.title("📊 BIST Analiz Terminali")
st.markdown("""
    <div style="
        background-color: #ffca28; 
        color: #5d4037; 
        padding: 8px 20px; 
        border-radius: 50px; 
        border: 1px solid #f57f17; 
        width: fit-content; 
        margin: 10px auto; 
        font-size: 15px; 
        font-weight: 500;
        text-align: center;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
    ">
        <strong>⚠️ Yasal Bilgilendirme:</strong> 
        Bu terminal ve veriler bilgilendirme amaçlıdır, yatırım tavsiyesi değildir. Tüm sorumluluk kullanıcıya aittir.
    </div>
""", unsafe_allow_html=True)

# --- 3. HİSSE LİSTESİ ---
bist_full_list = sorted(list(set([
    "A1CAP.IS", "ACSEL.IS", "ADEZ.IS", "ADESE.IS", "AEFES.IS", "AFYON.IS", "AGESA.IS", "AGHOL.IS", "AGROT.IS", "AHGAZ.IS",
    "AKBNK.IS", "AKCNS.IS", "AKENR.IS", "AKFGY.IS", "AKFYE.IS", "AKGRT.IS", "AKMGY.IS", "AKSA.IS", "AKSEN.IS", "ALARK.IS",
    "ALBRK.IS", "ALCTL.IS", "ALFAS.IS", "ALGYO.IS", "ALKA.IS", "ALKIM.IS", "ALMAD.IS", "ALTNY.IS", "ANELE.IS", "ANGEN.IS",
    "ANHYT.IS", "ANSGR.IS", "ARCLK.IS", "ARDYZ.IS", "ARENA.IS", "ARSAN.IS", "ASCEG.IS", "ASELS.IS", "ASGYO.IS", "ASTOR.IS",
    "ASUZU.IS", "ATAKP.IS", "ATATP.IS", "AVHOL.IS", "AVOD.IS", "AVPGY.IS", "AVTUR.IS", "AYDEM.IS", "AYEN.IS", "AYGAZ.IS",
    "AZTEK.IS", "BAGFS.IS", "BAKAB.IS", "BANVT.IS", "BARMA.IS", "BASGZ.IS", "BAYRK.IS", "BEGYO.IS", "BERA.IS", "BEYAZ.IS",
    "BFREN.IS", "BIENP.IS", "BIGCH.IS", "BIMAS.IS", "BINHO.IS", "BIOEN.IS", "BIZIM.IS", "BJKAS.IS", "BLCYT.IS", "BMTKS.IS",
    "BNTAS.IS", "BOBET.IS", "BORLS.IS", "BOSSA.IS", "BRISA.IS", "BRKSN.IS", "BRMEN.IS", "BRSAN.IS", "BRYAT.IS", "BSOKE.IS",
    "BTCIM.IS", "BUCIM.IS", "BURCE.IS", "BURVA.IS", "BVSAN.IS", "BYDNR.IS", "CANTE.IS", "CATES.IS", "CCOLA.IS", "CELHA.IS",
    "CEMAS.IS", "CEMTS.IS", "CEOEM.IS", "CIMSA.IS", "CLEBI.IS", "CONSE.IS", "CVKMD.IS", "CWENE.IS", "DAGHL.IS", "DAGI.IS",
    "DAPGM.IS", "DARDL.IS", "DENGE.IS", "DERIM.IS", "DERHL.IS", "DESA.IS", "DESPC.IS", "DGATE.IS", "DGGYO.IS", "DGNMO.IS",
    "DIRIT.IS", "DITAS.IS", "DMSAS.IS", "DNISI.IS", "DOAS.IS", "DOCO.IS", "DOGUB.IS", "DOHOL.IS", "DOKTA.IS", "DURDO.IS",
    "DYOBY.IS", "DZGYO.IS", "EBEBK.IS", "ECILC.IS", "ECZYT.IS", "EDATA.IS", "EDIP.IS", "EGEEN.IS", "EGGUB.IS", "EGPRO.IS",
    "EGSER.IS", "EKGYO.IS", "EKOS.IS", "EKSUN.IS", "ELITE.IS", "EMKEL.IS", "ENERY.IS", "ENJSA.IS", "ENKAI.IS", "ENSRI.IS",
    "EPLAS.IS", "ERBOS.IS", "EREGL.IS", "ERSU.IS", "ESCOM.IS", "ESEN.IS", "ETILR.IS", "EUPWR.IS", "EUREN.IS", "EYGYO.IS",
    "FENER.IS", "FLAP.IS", "FMIZP.IS", "FONET.IS", "FORMT.IS", "FORTE.IS", "FRIGO.IS", "FROTO.IS", "FZLGY.IS", "GARAN.IS",
    "GEDIK.IS", "GEDZA.IS", "GENIL.IS", "GENTS.IS", "GEREL.IS", "GESAN.IS", "GIPTA.IS", "GLBMD.IS", "GLRYH.IS", "GLYHO.IS",
    "GOKNR.IS", "GOLTS.IS", "GOODY.IS", "GOZDE.IS", "GSDDE.IS", "GSDHO.IS", "GSRAY.IS", "GUBRF.IS", "GWIND.IS", "GZNMI.IS",
    "HALKB.IS", "HATEK.IS", "HATSN.IS", "HEDEF.IS", "HEKTS.IS", "HKTM.IS", "HLGYO.IS", "HRKET.IS", "HTTBT.IS", "HUNER.IS",
    "HURGZ.IS", "ICBCT.IS", "IDGYO.IS", "IEYHO.IS", "IHAAS.IS", "IHEVA.IS", "IHGZT.IS", "IHLAS.IS", "IHLGM.IS", "IKLGT.IS",
    "IMASM.IS", "INDES.IS", "INFO.IS", "INGRM.IS", "INVEO.IS", "INVES.IS", "IPEKE.IS", "ISATR.IS", "ISBTR.IS", "ISCTR.IS",
    "ISFIN.IS", "ISGSY.IS", "ISGYO.IS", "ISKPL.IS", "ISMEN.IS", "ISSEN.IS", "ISYAT.IS", "IZENR.IS", "IZMDC.IS", "IZINV.IS",
    "JANTS.IS", "KAPLM.IS", "KARYE.IS", "KATMR.IS", "KAYSE.IS", "KCAER.IS", "KCHOL.IS", "KENT.IS", "KERVT.IS", "KFEIN.IS",
    "KGYO.IS", "KIMMR.IS", "KLGYO.IS", "KLMSN.IS", "KLNMA.IS", "KLRHO.IS", "KLSYN.IS", "KMPUR.IS", "KNFRT.IS", "KONKA.IS",
    "KONTR.IS", "KONYA.IS", "KORDS.IS", "KOZAA.IS", "KOZAL.IS", "KRDMA.IS", "KRDMB.IS", "KRDMD.IS", "KRGYO.IS", "KRONT.IS",
    "KRPLS.IS", "KRSTL.IS", "KRTEK.IS", "KRVGD.IS", "KTSKR.IS", "KUTPO.IS", "KUYAS.IS", "KZBGY.IS", "KZGYO.IS", "LIDER.IS",
    "LIDFA.IS", "LINK.IS", "LKMNH.IS", "LOGOS.IS", "LUKSK.IS", "MAALT.IS", "MACKO.IS", "MAGEN.IS", "MAKIM.IS", "MAKTK.IS",
    "MANAS.IS", "MARBL.IS", "MARTI.IS", "MAVI.IS", "MEDTR.IS", "MEGAP.IS", "MEKAG.IS", "MEPET.IS", "MERCN.IS", "MERKO.IS",
    "METRO.IS", "METUR.IS", "MHRGY.IS", "MIATK.IS", "MIPAZ.IS", "MNDRS.IS", "MOBTL.IS", "MGROS.IS", "MOGAN.IS", "MPARK.IS",
    "MRGYO.IS", "MRSHL.IS", "MSGYO.IS", "MTRKS.IS", "MZHLD.IS", "NATEN.IS", "NETAS.IS", "NIBAS.IS", "NTGAZ.IS", "NUGYO.IS",
    "NUHCM.IS", "OBAMS.IS", "OBASE.IS", "ODAS.IS", "ONCSM.IS", "ORCAY.IS", "ORGE.IS", "ORMA.IS", "OSMEN.IS", "OSTIM.IS",
    "OTKAR.IS", "OYAKC.IS", "OYAYO.IS", "OYLUM.IS", "OYYAT.IS", "OZGYO.IS", "OZKGY.IS", "OZRDN.IS", "OZSUB.IS", "PAGYO.IS",
    "PAMEL.IS", "PAPIL.IS", "PARSN.IS", "PASEU.IS", "PATEK.IS", "PCILT.IS", "PEGYO.IS", "PEKGY.IS", "PENTA.IS", "PETKM.IS",
    "PETUN.IS", "PGSUS.IS", "PINSU.IS", "PKART.IS", "PKENT.IS", "PLTUR.IS", "PNLSN.IS", "PNSUT.IS", "POLHO.IS", "POLTK.IS",
    "PRKAB.IS", "PRKME.IS", "PRZMA.IS", "PSDTC.IS", "QUAGR.IS", "RALYH.IS", "RAYYS.IS", "REEDR.IS", "RNPOL.IS", "RODRG.IS",
    "RTALB.IS", "RUBNS.IS", "RYGYO.IS", "RYSAS.IS", "SAFKR.IS", "SAHOL.IS", "SAMAT.IS", "SANEL.IS", "SANFM.IS", "SANKO.IS",
    "SARKY.IS", "SASA.IS", "SAYAS.IS", "SDTTR.IS", "SEKFK.IS", "SEKUR.IS", "SELEC.IS", "SELVA.IS", "SEYKM.IS", "SILVR.IS",
    "SISE.IS", "SKBNK.IS", "SKTAS.IS", "SKYMD.IS", "SMART.IS", "SMRTG.IS", "SNGYO.IS", "SNICA.IS", "SOKM.IS", "SONME.IS",
    "SRVGY.IS", "SUMAS.IS", "SUNTK.IS", "SURGY.IS", "SUWEN.IS", "TABGD.IS", "TARKM.IS", "TATGD.IS", "TAVHL.IS", "TCELL.IS",
    "TDGYO.IS", "TEKTU.IS", "TERA.IS", "TETMT.IS", "TGSAS.IS", "THYAO.IS", "TIRE.IS", "TKFEN.IS", "TKNSA.IS", "TMSN.IS",
    "TOASO.IS", "TRCAS.IS", "TRGYO.IS", "TRILC.IS", "TSKB.IS", "TSPOR.IS", "TTKOM.IS", "TTRAK.IS", "TUCLK.IS", "TUKAS.IS",
    "TUPRS.IS", "TUREX.IS", "TURGG.IS", "TURSG.IS", "UFUK.IS", "ULAS.IS", "ULKER.IS", "ULLY.IS", "ULUFA.IS", "ULUSE.IS",
    "ULUUN.IS", "USAK.IS", "VAKBN.IS", "VAKFN.IS", "VAKKO.IS", "VANGD.IS", "VBTYZ.IS", "VERTU.IS", "VERUS.IS", "VESBE.IS",
    "VESTL.IS", "VKGYO.IS", "VKING.IS", "VRGYO.IS", "YAPRK.IS", "YATAS.IS", "YAYLA.IS", "YEOTK.IS", "YESIL.IS", "YGGYO.IS",
    "YKBNK.IS", "YONGA.IS", "YOTAS.IS", "YUNSA.IS", "YYLGD.IS", "ZEDUR.IS", "ZOREN.IS", "ZRGYO.IS"
])))

@st.cache_data(ttl=3600)
def fetch_master_data(tickers):
    return yf.download(tickers, period="10mo", interval="1d", group_by='ticker', progress=False)

# --- 4. SEKMELER ---
tab1, tab2, tab3 = st.tabs(["🚀 Pazar Analizi", "💰 Portföyüm", "📰 Haberler"])

# --- TAB 1: PAZAR ANALİZİ (Değiştirilmedi) ---
with tab1:
    st.subheader("🔍 Tarama Ayarları")
    col1, col2 = st.columns([2, 1])
    with col1:
        score_threshold = st.slider("Minimum Skor Eşiği", 0, 100, 50)
    with col2:
        start_button = st.button("Analizi Başlat / Güncelle", use_container_width=True)

    if start_button:
        raw_data = fetch_master_data(bist_full_list)
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        total_tickers = len(bist_full_list)
        
        for i, ticker in enumerate(bist_full_list):
            try:
                status_text.text(f"Analiz ediliyor: {ticker} ({i+1}/{total_tickers})")
                df = raw_data[ticker].copy().dropna()
                if len(df) < 130: continue
                cp = df['Close'].iloc[-1]
                prev_p = df['Close'].iloc[-2]
                day_chg = ((cp - prev_p) / prev_p) * 100
                ret_1m = ((cp - df['Close'].iloc[-22]) / df['Close'].iloc[-22]) * 100
                df['RSI'] = ta.rsi(df['Close'], length=14)
                rsi = df['RSI'].iloc[-1]
                sma50 = ta.sma(df['Close'], length=50).iloc[-1]
                info = yf.Ticker(ticker).info
                fk = info.get('trailingPE', None)
                skor = 0
                if 30 < rsi < 45: skor += 20
                if cp > sma50: skor += 20
                if fk and 0 < fk < 15: skor += 30
                if ret_1m > 0: skor += 30

                if day_chg >= 9.5: sinyal = "🚀 TAVAN"
                elif rsi < 30: sinyal = "💎 GÜÇLÜ AL"
                elif rsi > 70: sinyal = "🔥 GÜÇLÜ SAT"
                elif skor >= 70: sinyal = "✅ AL"
                elif skor >= 40: sinyal = "⌛ BEKLE"
                else: sinyal = "⚠️ SAT"

                results.append({
                    "Hisse": ticker.replace(".IS", ""), "Fiyat": round(cp, 2),
                    "Günlük %": round(day_chg, 2), "1A %": round(ret_1m, 1),
                    "RSI": round(rsi, 1), "F/K": round(fk, 1) if fk else "N/A", "Skor": skor, "Sinyal": sinyal
                })
                progress_bar.progress((i + 1) / total_tickers)
            except: continue

        status_text.text("Analiz Tamamlandı!")
        res_df = pd.DataFrame(results)
        final_df = res_df[res_df['Skor'] >= score_threshold].sort_values(by=["Skor"], ascending=False)
        st.success(f"Şartları sağlayan {len(final_df)} hisse bulundu.")
        st.dataframe(final_df.style.background_gradient(subset=['Skor'], cmap='RdYlGn'), use_container_width=True, hide_index=True)
        csv = final_df.to_csv(index=False).encode('utf-8')
        st.download_button("Sonuçları İndir (CSV)", csv, "bist_analiz_sonuclari.csv", "text/csv")
    
    st.markdown("---")
    st.subheader("📈 Hisse Teknik Grafik İnceleme")
    selected_ticker = st.selectbox("Grafiğini görmek istediğiniz hisseyi seçin:", bist_full_list, key="detail_select")
    if selected_ticker:
        try:
            hisse_obj = yf.Ticker(selected_ticker)
            detail_data = hisse_obj.history(period="2y")
            if not detail_data.empty:
                detail_data['SMA50'] = ta.sma(detail_data['Close'], length=50)
                detail_data['SMA200'] = ta.sma(detail_data['Close'], length=200)
                st.line_chart(detail_data[['Close', 'SMA50', 'SMA200']].tail(150))
        except: st.error("Grafik yüklenirken bir hata oluştu.")

# --- TAB 2: PORTFÖYÜM ---
with tab2:
    st.subheader("💼 Portföy Yönetimi")

    # Portföyü session_state üzerinde saklayalım
    if 'my_portfolio' not in st.session_state:
        st.session_state.my_portfolio = []

    # --- HİSSE EKLEME ALANI ---
    with st.expander("➕ Yeni Hisse Ekle", expanded=True):
        col1, col2, col3 = st.columns([3, 2, 2])
        
        with col1:
            # Otomatik tamamlama özelliği burada devreye giriyor
            selected_stock = st.selectbox("Hisse Seçin (Örn: THY yazabilirsiniz)", 
                                         options=bist_full_list, 
                                         index=None,
                                         placeholder="Hisse kodu arayın...")
        with col2:
            lot_size = st.number_input("Adet", min_value=1, step=1, value=1)
        with col3:
            buy_price = st.number_input("Maliyet (TL)", min_value=0.01, step=0.01, format="%.2f")
            
        if st.button("Portföye Ekle", use_container_width=True):
            if selected_stock:
                st.session_state.my_portfolio.append({
                    "Hisse": selected_stock,
                    "Adet": lot_size,
                    "Maliyet": buy_price
                })
                st.toast(f"{selected_stock} portföye eklendi!")
                st.rerun()

    # --- PORTFÖY LİSTELEME VE HESAPLAMA ---
    if st.session_state.my_portfolio:
        portfolio_df = pd.DataFrame(st.session_state.my_portfolio)
        unique_stocks = portfolio_df["Hisse"].unique().tolist()
        
        try:
            # Güncel fiyatları toplu çekelim (Hız için)
            current_data = yf.download(unique_stocks, period="1d", interval="1m", progress=False)['Close'].iloc[-1]
            
            # DataFrame üzerinde hesaplamalar
            def calculate_metrics(row):
                # Tek bir hisse varsa Seri, çok varsa DataFrame döner; ona göre kontrol edelim
                c_price = current_data[row['Hisse']] if len(unique_stocks) > 1 else current_data
                current_val = c_price * row['Adet']
                total_cost = row['Maliyet'] * row['Adet']
                p_l = current_val - total_cost
                p_l_percent = (p_l / total_cost) * 100 if total_cost > 0 else 0
                return pd.Series([round(c_price, 2), round(current_val, 2), round(p_l, 2), round(p_l_percent, 2)])

            portfolio_df[['Güncel Fiyat', 'Toplam Değer', 'Kar/Zarar', '% Değişim']] = portfolio_df.apply(calculate_metrics, axis=1)

            # Görselleştirme ve Tablo
            st.write("### Mevcut Durum")
            
            # Toplam Özet Metrikleri
            total_pl = portfolio_df['Kar/Zarar'].sum()
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("Toplam Portföy Değeri", f"{portfolio_df['Toplam Değer'].sum():,.2f} TL")
            col_m2.metric("Toplam Kar/Zarar", f"{total_pl:,.2f} TL", delta=f"{total_pl:,.2f} TL")

            # Renkli Tablo Gösterimi
            def color_pl(val):
                color = '#2ecc71' if val > 0 else '#e74c3c' if val < 0 else '#f39c12'
                return f'color: {color}; font-weight: bold'

            st.dataframe(
                portfolio_df.style.applymap(color_pl, subset=['Kar/Zarar', '% Değişim']),
                use_container_width=True,
                hide_index=True
            )

            if st.button("Portföyü Temizle"):
                st.session_state.my_portfolio = []
                st.rerun()

        except Exception as e:
            st.warning("Veriler güncellenirken bir sorun oluştu. Lütfen biraz bekleyin.")
    else:
        st.info("Portföyünüz henüz boş. Yukarıdaki bölümden hisse ekleyebilirsiniz.")
    
    # Haber Sorgusu İyileştirildi (Bugünkü tüm KAP ve Borsa hareketlerini yakalar)
    if news_ticker == "Canlı Akış (Tüm Şirketler)":
        query_text = "(hisse OR borsa OR kap OR bist) when:1d"
    else:
        hisse_sade = news_ticker.replace(".IS", "")
        query_text = f"{hisse_sade} (hisse OR kap OR borsa)"
    
    rss_url = f"https://news.google.com/rss/search?q={quote(query_text)}&hl=tr&gl=TR&ceid=TR:tr"
    feed = feedparser.parse(rss_url)
    
    if feed.entries:
        processed_entries = []
        for entry in feed.entries:
            try:
                # 1. Haberin yayınlanma tarihini al (UTC)
                utc_dt = parsedate_to_datetime(entry.published)
                # 2. Türkiye saatine (TR_TZ) çevir
                tr_dt = utc_dt.astimezone(TR_TZ)
                entry.sort_time = tr_dt
                processed_entries.append(entry)
            except: continue
        
        # 3. En yeniden en eskiye (Descending) kesin sıralama
        processed_entries.sort(key=lambda x: x.sort_time, reverse=True)
        
        for entry in processed_entries[:20]: # En güncel 20 haber
            with st.container():
                clean_date = entry.sort_time.strftime("%d %b %Y %H:%M")
                st.markdown(f"### [{entry.title}]({entry.link})")
                st.caption(f"🕒 **{clean_date}** | 🏢 Kaynak: {entry.source.title}")
                st.divider()
    else:
        st.info("Son 24 saat içinde yeni bir haber akışı bulunamadı.")

st.markdown("---")
# Alt bilgi saatini Türkiye saatine sabitledik
st.caption(f"BIST Analiz Terminali | Son Güncelleme: {datetime.now(TR_TZ).strftime('%d.%m.%Y %H:%M')}")

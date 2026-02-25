import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import feedparser
import pytz
from urllib.parse import quote
from datetime import datetime
from email.utils import parsedate_to_datetime

# --- 1. SAYFA AYARLARI VE TASARIM ---
st.set_page_config(page_title="BIST Analiz Terminali", layout="wide", initial_sidebar_state="collapsed")

# Türkiye Saat Dilimi
TR_TZ = pytz.timezone('Europe/Istanbul')

# Sidebar Gizleme ve Genel Stil
st.markdown("""
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] {display: none !important;}
        .stApp { margin-left: 0px; }
        /* Tabloyu daha okunaklı yap */
        .stDataFrame {border: 1px solid #f0f2f6; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

# --- 2. BAŞLIK VE KÜÇÜK YASAL UYARI ---
st.title("📊 BIST Analiz Terminali")

# İstediğin küçük, koyu sarı, ortalanmış yasal uyarı
st.markdown("""
    <div style="
        background-color: #ffca28; 
        color: #5d4037; 
        padding: 8px 20px; 
        border-radius: 50px; 
        border: 1px solid #f57f17; 
        width: fit-content; 
        margin: 0 auto 20px auto; 
        font-size: 14px; 
        font-weight: 500;
        text-align: center;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
    ">
        <strong>⚠️ Yasal Bilgilendirme:</strong> Veriler yatırım tavsiyesi değildir. Tüm sorumluluk kullanıcıya aittir.
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

# --- TAB 1: PAZAR ANALİZİ ---
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

# --- TAB 2: PORTFÖYÜM (GÜNCEL & HATASIZ) ---
with tab2:
    st.subheader("💼 Portföy Yönetimi")
    
    if 'my_portfolio' not in st.session_state:
        st.session_state.my_portfolio = []

    # Hisse Ekleme Bölümü
    with st.expander("➕ Portföye Hisse Ekle", expanded=True):
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            # Otomatik tamamlama burada: "thy" yazarsan THYAO.IS'yi seçebilirsin
            selected_stock = st.selectbox("Hisse Ara/Seç:", options=bist_full_list, index=None, placeholder="Örn: THY...", key="port_select")
        with c2:
            lot = st.number_input("Adet", min_value=1, value=1)
        with c3:
            maliyet = st.number_input("Maliyet (TL)", min_value=0.0, value=0.0, step=0.01)
        
        if st.button("Listeye Ekle", use_container_width=True):
            if selected_stock:
                st.session_state.my_portfolio.append({"Hisse": selected_stock, "Adet": lot, "Maliyet": maliyet})
                st.rerun()

    # Portföy Tablosu ve Kâr/Zarar Hesabı
    if st.session_state.my_portfolio:
        df_p = pd.DataFrame(st.session_state.my_portfolio)
        unique_stocks = df_p['Hisse'].unique().tolist()
        
        try:
            # Güncel fiyatları çek (Toplu çekim)
            price_data = yf.download(unique_stocks, period="1d", interval="1m", progress=False)['Close'].iloc[-1]
            
            def calculate_row(row):
                # Tek bir hisse varken Yahoo Finance farklı format dönebilir, kontrol ediyoruz
                curr_p = price_data[row['Hisse']] if len(unique_stocks) > 1 else price_data
                total_val = curr_p * row['Adet']
                total_cost = row['Maliyet'] * row['Adet']
                pl = total_val - total_cost
                pl_perc = (pl / total_cost * 100) if total_cost > 0 else 0
                return pd.Series([round(curr_p, 2), round(total_val, 2), round(pl, 2), round(pl_perc, 2)])

            df_p[['Güncel Fiyat', 'Toplam Değer', 'Kâr/Zarar', 'Değişim %']] = df_p.apply(calculate_row, axis=1)
            
            # Özet Bilgiler
            m1, m2 = st.columns(2)
            m1.metric("Toplam Portföy Değeri", f"{df_p['Toplam Değer'].sum():,.2f} TL")
            net_pl = df_p['Kâr/Zarar'].sum()
            m2.metric("Toplam Net Kâr/Zarar", f"{net_pl:,.2f} TL", delta=f"{net_pl:,.2f}")

            # Renklendirme Fonksiyonu
            def color_pl(val):
                color = 'green' if val > 0 else 'red' if val < 0 else 'black'
                return f'color: {color}'

            st.dataframe(df_p.style.applymap(color_pl, subset=['Kâr/Zarar', 'Değişim %']), use_container_width=True, hide_index=True)
            
            if st.button("Portföyü Sıfırla"):
                st.session_state.my_portfolio = []
                st.rerun()
        except Exception as e:
            st.warning("Fiyat verileri alınırken bir hata oluştu. Borsa kapalı veya internet bağlantısı zayıf olabilir.")
    else:
        st.info("Portföyünüz henüz boş.")

# --- TAB 3: CANLI HABER TERMİNALİ (HATASIZ) ---
with tab3:
    st.subheader("📰 Canlı Haber Terminali")
    
    # news_ticker tanımını en başa aldık (Hata almamak için)
    news_options = ["Canlı Akış (Tüm Şirketler)"] + bist_full_list
    news_ticker = st.selectbox("Hisse Filtrele:", news_options, key="news_filter_box")
    
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
                utc_dt = parsedate_to_datetime(entry.published)
                tr_dt = utc_dt.astimezone(TR_TZ)
                entry.sort_time = tr_dt
                processed_entries.append(entry)
            except: continue
        
        processed_entries.sort(key=lambda x: x.sort_time, reverse=True)
        
        for entry in processed_entries[:20]:
            with st.container():
                st.markdown(f"### [{entry.title}]({entry.link})")
                st.caption(f"🕒 {entry.sort_time.strftime('%H:%M')} | {entry.source.title}")
                st.divider()
    else:
        st.info("Son 24 saatte yeni haber akışı bulunamadı.")

# --- ALT BİLGİ ---
st.markdown("---")
st.caption(f"BIST Analiz Terminali | Son Güncelleme: {datetime.now(TR_TZ).strftime('%d.%m.%Y %H:%M')}")

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

TR_TZ = pytz.timezone('Europe/Istanbul')

st.markdown("""
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] {display: none !important;}
        .stApp { margin-left: 0px; }
        .stDataFrame {border: 1px solid #f0f2f6; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

# --- 2. BAŞLIK VE YASAL UYARI ---
st.title("📊 BIST Analiz Terminali")

st.markdown("""
    <div style="
        background-color: #ffca28; color: #4e342e; padding: 10px 30px; border-radius: 50px; 
        border: 1px solid #f57f17; width: fit-content; margin: 0 auto 20px auto; 
        font-size: 14.5px; font-weight: 500; text-align: center; line-height: 1.4;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
    ">
        ⚠️ <strong>Bilgilendirme:</strong> Bu terminaldeki veri ve analizler yatırım tavsiyesi değildir ve profesyonel bir kullanım amacı taşımamaktadır. 
        Tüm sorumluluğun kullanıcıya ait olduğunu hatırlatmak isteriz.
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
    # 3 ve 6 aylık verileri kapsamak için 1 yıllık veri çekiyoruz
    return yf.download(tickers, period="1y", interval="1d", group_by='ticker', progress=False)

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

    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None

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
                
                # Değişim Hesaplamaları
                day_chg = ((cp - prev_p) / prev_p) * 100
                ret_1m = ((cp - df['Close'].iloc[-22]) / df['Close'].iloc[-22]) * 100
                ret_3m = ((cp - df['Close'].iloc[-66]) / df['Close'].iloc[-66]) * 100 if len(df) > 66 else 0
                ret_6m = ((cp - df['Close'].iloc[-126]) / df['Close'].iloc[-126]) * 100 if len(df) > 126 else 0
                
                # Teknik Göstergeler
                df['RSI'] = ta.rsi(df['Close'], length=14)
                rsi = df['RSI'].iloc[-1]
                sma50 = ta.sma(df['Close'], length=50).iloc[-1]
                
                # Skorlama
                skor = 0
                if 30 < rsi < 45: skor += 20
                if cp > sma50: skor += 20
                if ret_1m > 0: skor += 30
                if day_chg > 0: skor += 30

                # Sinyal Mantığı
                if day_chg >= 9.5: sinyal = "🚀 TAVAN"
                elif rsi < 30: sinyal = "💎 GÜÇLÜ AL"
                elif rsi > 70: sinyal = "🔥 GÜÇLÜ SAT"
                elif skor >= 70: sinyal = "✅ AL"
                elif skor >= 40: sinyal = "⌛ BEKLE"
                else: sinyal = "⚠️ SAT"

                results.append({
                    "Hisse": ticker.replace(".IS", ""), "Fiyat": round(cp, 2),
                    "Günlük %": round(day_chg, 2), "1A %": round(ret_1m, 1),
                    "3A %": round(ret_3m, 1), "6A %": round(ret_6m, 1),
                    "RSI": round(rsi, 1), "Skor": skor, "Sinyal": sinyal
                })
                progress_bar.progress((i + 1) / total_tickers)
            except: continue

        status_text.text("Analiz Tamamlandı!")
        st.session_state.analysis_results = pd.DataFrame(results)

    # --- FİLTRELEME VE GÖSTERİM ---
    if st.session_state.analysis_results is not None:
        df_res = st.session_state.analysis_results.copy()
        
        # Sinyal Filtresi (Multiselect)
        st.markdown("---")
        col_f1, col_f2 = st.columns([2,1])
        with col_f1:
            all_signals = df_res["Sinyal"].unique().tolist()
            selected_signals = st.multiselect("Sinyale Göre Filtrele:", options=all_signals, default=all_signals)
        
        # Filtreyi Uygula
        filtered_df = df_res[
            (df_res["Skor"] >= score_threshold) & 
            (df_res["Sinyal"].isin(selected_signals))
        ].sort_values(by=["Skor"], ascending=False)
        
        st.success(f"Şartları sağlayan {len(filtered_df)} hisse bulundu.")
        st.dataframe(
            filtered_df.style.background_gradient(subset=['Skor'], cmap='RdYlGn'), 
            use_container_width=True, 
            hide_index=True
        )

    # --- GRAFİK BÖLÜMÜ ---
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
    if 'my_portfolio' not in st.session_state:
        st.session_state.my_portfolio = []

    with st.expander("➕ Portföye Hisse Ekle", expanded=True):
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            selected_stock = st.selectbox("Hisse Ara/Seç:", options=bist_full_list, index=None, placeholder="Örn: THY...", key="port_select")
        with c2:
            lot = st.number_input("Adet", min_value=1, value=1)
        with c3:
            maliyet = st.number_input("Maliyet (TL)", min_value=0.0, value=0.0, step=0.01)
        if st.button("Listeye Ekle", use_container_width=True):
            if selected_stock:
                st.session_state.my_portfolio.append({"Hisse": selected_stock, "Adet": lot, "Maliyet": maliyet})
                st.rerun()

    if st.session_state.my_portfolio:
        df_p = pd.DataFrame(st.session_state.my_portfolio)
        unique_stocks = df_p['Hisse'].unique().tolist()
        try:
            price_data = yf.download(unique_stocks, period="1d", interval="1m", progress=False)['Close'].iloc[-1]
            def calculate_row(row):
                curr_p = price_data[row['Hisse']] if len(unique_stocks) > 1 else price_data
                total_val = curr_p * row['Adet']
                total_cost = row['Maliyet'] * row['Adet']
                pl = total_val - total_cost
                pl_perc = (pl / total_cost * 100) if total_cost > 0 else 0
                return pd.Series([round(curr_p, 2), round(total_val, 2), round(pl, 2), round(pl_perc, 2)])
            df_p[['Güncel Fiyat', 'Toplam Değer', 'Kâr/Zarar', 'Değişim %']] = df_p.apply(calculate_row, axis=1)
            m1, m2 = st.columns(2)
            m1.metric("Toplam Değer", f"{df_p['Toplam Değer'].sum():,.2f} TL")
            m2.metric("Toplam K/Z", f"{df_p['Kâr/Zarar'].sum():,.2f} TL", delta=f"{df_p['Kâr/Zarar'].sum():,.2f}")
            st.dataframe(df_p, use_container_width=True, hide_index=True)
            if st.button("Sıfırla"):
                st.session_state.my_portfolio = []
                st.rerun()
        except: st.warning("Fiyat verileri alınamadı.")

# --- TAB 3: HABERLER ---
with tab3:
    st.subheader("📰 Canlı Haber Terminali")
    news_options = ["Canlı Akış (Tüm Şirketler)"] + bist_full_list
    news_ticker = st.selectbox("Hisse Filtrele:", news_options, key="news_filter_box")
    
    query_text = "(hisse OR borsa OR kap OR bist) when:1d" if news_ticker == "Canlı Akış (Tüm Şirketler)" else f"{news_ticker.replace('.IS', '')} (hisse OR kap OR borsa)"
    
    rss_url = f"https://news.google.com/rss/search?q={quote(query_text)}&hl=tr&gl=TR&ceid=TR:tr"
    feed = feedparser.parse(rss_url)
    
    if feed.entries:
        processed = []
        for e in feed.entries:
            try:
                dt = parsedate_to_datetime(e.published).astimezone(TR_TZ)
                e.sort_time = dt
                processed.append(e)
            except: continue
        processed.sort(key=lambda x: x.sort_time, reverse=True)
        for e in processed[:20]:
            st.markdown(f"### [{e.title}]({e.link})")
            st.caption(f"🕒 {e.sort_time.strftime('%d.%m.%Y %H:%M')} | {e.source.title}")
            st.divider()
    else: st.info("Haber bulunamadı.")

# --- ALT BİLGİ ---
st.markdown("---")
st.caption(f"BIST Analiz Terminali | Son Güncelleme: {datetime.now(TR_TZ).strftime('%d.%m.%Y %H:%M')}")

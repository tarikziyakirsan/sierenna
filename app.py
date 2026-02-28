import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import feedparser
import pytz
import google.generativeai as genai
from urllib.parse import quote
from datetime import datetime
from email.utils import parsedate_to_datetime

# --- 1. AI AYARLARI (Gemini) ---
genai.configure(api_key="AIzaSyBa4qF36wC3-WMiBkCRf7mdwWijTcOYb-E")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. SAYFA AYARLARI VE TASARIM ---
st.set_page_config(page_title="BIST Analiz Terminali", layout="wide", initial_sidebar_state="collapsed")
TR_TZ = pytz.timezone('Europe/Istanbul')

# CSS: Sidebar ve "Running" bildirimlerini gizleme
st.markdown("""
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] {display: none !important;}
        .stApp { margin-left: 0px; }
        .stDataFrame {border: 1px solid #f0f2f6; border-radius: 10px;}
        [data-testid="stStatusWidget"], .stStatusWidget {display: none !important;}
    </style>
""", unsafe_allow_html=True)

# --- 3. BAŞLIK VE NAZİK YASAL UYARI ---
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

# --- 4. HİSSE LİSTESİ ---
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

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_master_data(tickers):
    return yf.download(tickers, period="1y", interval="1d", group_by='ticker', progress=False)

# --- AI ANALİZ FONKSİYONU ---
def get_ai_insight(ticker_name, tech_row, news_entries):
    news_text = "\n".join([f"- {e.title}" for e in news_entries[:5]])
    prompt = f"""
    Sen uzman bir borsa analistisin. {ticker_name} hissesini analiz et.
    TEKNİK: Fiyat:{tech_row['Fiyat']}, RSI:{tech_row['RSI']}, 1A:%{tech_row['1A %']}, Sinyal:{tech_row['Sinyal']}
    HABERLER/KAP: {news_text}
    GÖREV: Teknik ve haberleri sentezle. Riskleri ve fırsatları belirt. 
    Kısa, net ve yatırımcıyı aydınlatan bir tavsiye ver.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "Analiz şu an yapılamıyor."

# --- 5. SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Pazar Analizi", "💰 Portföyüm", "📰 Haberler", "🤖 Gemini AI"])

# --- TAB 1: PAZAR ANALİZİ ---
with tab1:
    st.subheader("🔍 Tarama Ayarları")
    col1, col2 = st.columns([3, 1])
    with col1:
        score_threshold = st.slider("Minimum Skor Eşiği", 0, 100, 50)
    with col2:
        start_button = st.button("Analizi Başlat / Güncelle", use_container_width=True)

    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
    
    if "selected_chart_ticker" not in st.session_state:
        st.session_state.selected_chart_ticker = "THYAO.IS"

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
                ret_3m = ((cp - df['Close'].iloc[-63]) / df['Close'].iloc[-63]) * 100
                ret_6m = ((cp - df['Close'].iloc[-126]) / df['Close'].iloc[-126]) * 100
                
                df['RSI'] = ta.rsi(df['Close'], length=14)
                rsi = df['RSI'].iloc[-1]
                sma50 = ta.sma(df['Close'], length=50).iloc[-1]
                
                skor = 0
                if 30 < rsi < 45: skor += 20
                if cp > sma50: skor += 20
                if ret_1m > 0: skor += 30
                if day_chg > 0: skor += 30

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

    # --- ANINDA ARAMA VE TABLO ---
    if st.session_state.analysis_results is not None:
        search_ticker = st.selectbox(
            "🔍 Listeden Hisseye Git / Ara:", 
            options=st.session_state.analysis_results["Hisse"].tolist(),
            index=None,
            placeholder="Hisse kodu yazın...",
            key="instant_search"
        )
        
        df_display = st.session_state.analysis_results.copy()
        if search_ticker:
            df_display = df_display[df_display["Hisse"] == search_ticker]
            st.session_state.selected_chart_ticker = search_ticker + ".IS"
        else:
            df_display = df_display[df_display["Skor"] >= score_threshold]

        st.success(f"Listelenen hisse sayısı: {len(df_display)}. Tıklayarak grafiği ve AI yorumunu güncelleyin.")
        
        selection_event = st.dataframe(
            df_display.sort_values(by="Skor", ascending=False),
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            column_config={
                "Skor": st.column_config.ProgressColumn("Skor", min_value=0, max_value=100, format="%d"),
                "Fiyat": st.column_config.NumberColumn("Fiyat", format="%.2f TL"),
                "Günlük %": st.column_config.NumberColumn("Günlük %", format="%.2f"),
                "3A %": st.column_config.NumberColumn("3A %", format="%.1f"),
                "6A %": st.column_config.NumberColumn("6A %", format="%.1f")
            }
        )

        if selection_event.selection.rows:
            idx = selection_event.selection.rows[0]
            curr_sorted = df_display.sort_values(by="Skor", ascending=False)
            clicked = curr_sorted.iloc[idx]["Hisse"]
            st.session_state.selected_chart_ticker = clicked + ".IS"

    st.markdown("---")
    st.subheader("📈 Teknik Grafik")
    try:
        current_list_idx = bist_full_list.index(st.session_state.selected_chart_ticker)
    except: current_list_idx = 0

    selected_ticker_final = st.selectbox("İncele:", bist_full_list, index=current_list_idx, key="detail_select")
    if selected_ticker_final:
        st.session_state.selected_chart_ticker = selected_ticker_final
        h_obj = yf.Ticker(selected_ticker_final)
        d_data = h_obj.history(period="2y")
        if not d_data.empty:
            d_data['SMA50'] = ta.sma(d_data['Close'], length=50)
            d_data['SMA200'] = ta.sma(d_data['Close'], length=200)
            st.line_chart(d_data[['Close', 'SMA50', 'SMA200']].tail(150))

# --- TAB 4: GEMINI AI ---
with tab4:
    st.subheader("🤖 Gemini Yapay Zeka Analizi")
    ai_hisse = st.session_state.selected_chart_ticker.replace(".IS", "")
    st.info(f"Seçili Hisse: **{ai_hisse}**")
    
    if st.button(f"{ai_hisse} İçin AI Raporu Oluştur"):
        if st.session_state.analysis_results is not None:
            # Teknik Veriyi Al
            row = st.session_state.analysis_results[st.session_state.analysis_results["Hisse"] == ai_hisse].iloc[0]
            # Haberleri Al
            q = f"{ai_hisse} (hisse OR kap OR borsa)"
            f = feedparser.parse(f"https://news.google.com/rss/search?q={quote(q)}&hl=tr&gl=TR&ceid=TR:tr")
            
            with st.status("Gemini verileri analiz ediyor...", expanded=True):
                ai_text = get_ai_insight(ai_hisse, row, f.entries)
                st.write(ai_text)
        else:
            st.warning("Önce Pazar Analizi sekmesinden tarama yapmalısınız.")

# --- TAB 2 & 3 (Kısa halleri) ---
with tab2:
    st.subheader("💼 Portföy")
    if 'my_portfolio' not in st.session_state: st.session_state.my_portfolio = []
    # (Portföy kodların burada devam ediyor...)

with tab3:
    st.subheader("📰 Haber Akışı")
    # (Haber kodların burada devam ediyor...)

st.markdown("---")
st.caption(f"BIST Analiz Terminali | Son Güncelleme: {datetime.now(TR_TZ).strftime('%d.%m.%Y %H:%M')}")

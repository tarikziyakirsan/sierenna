import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

# --- 1. SAYFA AYARLARI VE SIDEBAR'I TAMAMEN GİZLEME ---
st.set_page_config(page_title="BIST Master Analiz Terminali", layout="wide", initial_sidebar_state="collapsed")

# Sidebar'ı ve açılır kapanır oku tamamen ortadan kaldıran CSS
st.markdown("""
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarNav"], .css-1dp56ee, .css-yk4q2l {
            display: none !important;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { margin-left: 0px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. BAŞLIK VE ESKİ SARI UYARI YAZISI ---
st.title("Bist Master Analiz Terminali")

# Sayfa Yapılandırması
st.set_page_config(page_title="BIST Tüm Evren Analizi", layout="wide")

st.title("📊 BIST Tüm Şirketler Master Analiz Paneli")
st.write("Teknik Momentum, Temel Değerleme ve Performans Denetimi")

# Yasal Uyarı Bölümü
st.warning("⚠️ **Yasal Uyarı:** Bu uygulama bilgilendirme amaçlıdır. Burada yer alan veriler, analizler ve skorlar kesinlikle **yatırım tavsiyesi değildir.** Piyasa verileri gecikmeli olabilir ve analiz sonuçları hata payı içerebilir. Yapılan tüm işlemlerin riski ve sorumluluğu tamamen kullanıcıya aittir.")

st.markdown("---")

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
    "DIRIT.IS", "DITAS.IS", "DMSAS.IS", "DNISI.IS", "DOAS.IS", "DOCO.IS", "DOGUB.IS", "DOHOL.IS", "DOKTA.IS",
    "DURDO.IS", "DYOBY.IS", "DZGYO.IS", "EBEBK.IS", "ECILC.IS", "ECZYT.IS", "EDATA.IS", "EDIP.IS", "EGEEN.IS", "EGGUB.IS",
    "EGPRO.IS", "EGSER.IS", "EKGYO.IS", "EKOS.IS", "EKSUN.IS", "ELITE.IS", "EMKEL.IS", "ENERY.IS", "ENJSA.IS", "ENKAI.IS",
    "ENSRI.IS", "EPLAS.IS", "ERBOS.IS", "EREGL.IS", "ERSU.IS", "ESCOM.IS", "ESEN.IS", "ETILR.IS", "EUPWR.IS", "EUREN.IS",
    "EYGYO.IS", "FENER.IS", "FLAP.IS", "FMIZP.IS", "FONET.IS", "FORMT.IS", "FORTE.IS", "FRIGO.IS", "FROTO.IS", "FZLGY.IS",
    "GARAN.IS", "GEDIK.IS", "GEDZA.IS", "GENIL.IS", "GENTS.IS", "GEREL.IS", "GESAN.IS", "GIPTA.IS", "GLBMD.IS", "GLRYH.IS",
    "GLYHO.IS", "GOKNR.IS", "GOLTS.IS", "GOODY.IS", "GOZDE.IS", "GSDDE.IS", "GSDHO.IS", "GSRAY.IS", "GUBRF.IS", "GWIND.IS",
    "GZNMI.IS", "HALKB.IS", "HATEK.IS", "HATSN.IS", "HEDEF.IS", "HEKTS.IS", "HKTM.IS", "HLGYO.IS", "HRKET.IS", "HTTBT.IS",
    "HUNER.IS", "HURGZ.IS", "ICBCT.IS", "IDGYO.IS", "IEYHO.IS", "IHAAS.IS", "IHEVA.IS", "IHGZT.IS", "IHLAS.IS", "IHLGM.IS",
    "IKLGT.IS", "IMASM.IS", "INDES.IS", "INFO.IS", "INGRM.IS", "INVEO.IS", "INVES.IS", "IPEKE.IS", "ISATR.IS", "ISBTR.IS",
    "ISCTR.IS", "ISFIN.IS", "ISGSY.IS", "ISGYO.IS", "ISKPL.IS", "ISMEN.IS", "ISSEN.IS", "ISYAT.IS", "IZENR.IS", "IZMDC.IS",
    "IZINV.IS", "JANTS.IS", "KAPLM.IS", "KARYE.IS", "KATMR.IS", "KAYSE.IS", "KCAER.IS", "KCHOL.IS", "KENT.IS", "KERVT.IS",
    "KFEIN.IS", "KGYO.IS", "KIMMR.IS", "KLGYO.IS", "KLMSN.IS", "KLNMA.IS", "KLRHO.IS", "KLSYN.IS", "KMPUR.IS", "KNFRT.IS",
    "KONKA.IS", "KONTR.IS", "KONYA.IS", "KORDS.IS", "KOZAA.IS", "KOZAL.IS", "KRDMA.IS", "KRDMB.IS", "KRDMD.IS", "KRGYO.IS",
    "KRONT.IS", "KRPLS.IS", "KRSTL.IS", "KRTEK.IS", "KRVGD.IS", "KTSKR.IS", "KUTPO.IS", "KUYAS.IS", "KZBGY.IS", "KZGYO.IS",
    "LIDER.IS", "LIDFA.IS", "LINK.IS", "LKMNH.IS", "LOGOS.IS", "LUKSK.IS", "MAALT.IS", "MACKO.IS", "MAGEN.IS", "MAKIM.IS",
    "MAKTK.IS", "MANAS.IS", "MARBL.IS", "MARTI.IS", "MAVI.IS", "MEDTR.IS", "MEGAP.IS", "MEKAG.IS", "MEPET.IS", "MERCN.IS",
    "MERKO.IS", "METRO.IS", "METUR.IS", "MHRGY.IS", "MIATK.IS", "MIPAZ.IS", "MNDRS.IS", "MOBTL.IS", "MGROS.IS", "MOGAN.IS",
    "MPARK.IS", "MRGYO.IS", "MRSHL.IS", "MSGYO.IS", "MTRKS.IS", "MZHLD.IS", "NATEN.IS", "NETAS.IS", "NIBAS.IS", "NTGAZ.IS",
    "NUGYO.IS", "NUHCM.IS", "OBAMS.IS", "OBASE.IS", "ODAS.IS", "ONCSM.IS", "ORCAY.IS", "ORGE.IS", "ORMA.IS", "OSMEN.IS",
    "OSTIM.IS", "OTKAR.IS", "OYAKC.IS", "OYAYO.IS", "OYLUM.IS", "OYYAT.IS", "OZGYO.IS", "OZKGY.IS", "OZRDN.IS", "OZSUB.IS",
    "PAGYO.IS", "PAMEL.IS", "PAPIL.IS", "PARSN.IS", "PASEU.IS", "PATEK.IS", "PCILT.IS", "PEGYO.IS", "PEKGY.IS", "PENTA.IS",
    "PETKM.IS", "PETUN.IS", "PGSUS.IS", "PINSU.IS", "PKART.IS", "PKENT.IS", "PLTUR.IS", "PNLSN.IS", "PNSUT.IS", "POLHO.IS",
    "POLTK.IS", "PRKAB.IS", "PRKME.IS", "PRZMA.IS", "PSDTC.IS", "QUAGR.IS", "RALYH.IS", "RAYYS.IS", "REEDR.IS", "RNPOL.IS",
    "RODRG.IS", "RTALB.IS", "RUBNS.IS", "RYGYO.IS", "RYSAS.IS", "SAFKR.IS", "SAHOL.IS", "SAMAT.IS", "SANEL.IS", "SANFM.IS",
    "SANKO.IS", "SARKY.IS", "SASA.IS", "SAYAS.IS", "SDTTR.IS", "SEKFK.IS", "SEKUR.IS", "SELEC.IS", "SELVA.IS", "SEYKM.IS",
    "SILVR.IS", "SISE.IS", "SKBNK.IS", "SKTAS.IS", "SKYMD.IS", "SMART.IS", "SMRTG.IS", "SNGYO.IS", "SNICA.IS", "SOKM.IS",
    "SONME.IS", "SRVGY.IS", "SUMAS.IS", "SUNTK.IS", "SURGY.IS", "SUWEN.IS", "TABGD.IS", "TARKM.IS", "TATGD.IS", "TAVHL.IS",
    "TCELL.IS", "TDGYO.IS", "TEKTU.IS", "TERA.IS", "TETMT.IS", "TGSAS.IS", "THYAO.IS", "TIRE.IS", "TKFEN.IS", "TKNSA.IS",
    "TMSN.IS", "TOASO.IS", "TRCAS.IS", "TRGYO.IS", "TRILC.IS", "TSKB.IS", "TSPOR.IS", "TTKOM.IS", "TTRAK.IS", "TUCLK.IS",
    "TUKAS.IS", "TUPRS.IS", "TUREX.IS", "TURGG.IS", "TURSG.IS", "UFUK.IS", "ULAS.IS", "ULKER.IS", "ULLY.IS", "ULUFA.IS",
    "ULUSE.IS", "ULUUN.IS", "USAK.IS", "VAKBN.IS", "VAKFN.IS", "VAKKO.IS", "VANGD.IS", "VBTYZ.IS", "VERTU.IS", "VERUS.IS",
    "VESBE.IS", "VESTL.IS", "VKGYO.IS", "VKING.IS", "VRGYO.IS", "YAPRK.IS", "YATAS.IS", "YAYLA.IS", "YEOTK.IS", "YESIL.IS",
    "YGGYO.IS", "YKBNK.IS", "YONGA.IS", "YOTAS.IS", "YUNSA.IS", "YYLGD.IS", "ZEDUR.IS", "ZOREN.IS", "ZRGYO.IS"
])))

@st.cache_data(ttl=3600)
def fetch_master_data(tickers):
    return yf.download(tickers, period="10mo", interval="1d", group_by='ticker', progress=False)

# --- 4. SEKMELER ---
tab1, tab2, tab3 = st.tabs(["🚀 Pazar Analizi", "💰 Portföyüm", "📰 Haberler & Detay"])

# --- TAB 1: PAZAR ANALİZİ ---
with tab1:
    # "Global" kelimesi kaldırıldı
    st.subheader("🔥 BIST Taraması")
    
    # Skor eşiği ve buton (vibe filter yazısı kaldırıldı)
    score_threshold = st.slider("🎯 Minimum skor eşiği", 0, 100, 50)
    
    if st.button("🔄 Analizi Başlat / Güncelle"):
        st.session_state.last_run = True

    if 'last_run' in st.session_state:
        raw_data = fetch_master_data(bist_full_list)
        results = []
        progress_bar = st.progress(0)
        
        for i, ticker in enumerate(bist_full_list):
            try:
                df = raw_data[ticker].copy().dropna()
                if len(df) < 130: continue
                
                cp = df['Close'].iloc[-1]
                prev_p = df['Close'].iloc[-2]
                day_chg = ((cp - prev_p) / prev_p) * 100
                ret_1m = ((cp - df['Close'].iloc[-22]) / df['Close'].iloc[-22]) * 100
                
                df['RSI'] = ta.rsi(df['Close'], length=14)
                rsi = df['RSI'].iloc[-1]
                sma50 = ta.sma(df['Close'], length=50).iloc[-1]
                
                # Sektör bilgisi kaldırıldı, sadece temel finansal veri
                info = yf.Ticker(ticker).info
                fk = info.get('trailingPE', None)

                skor = 0
                if 30 < rsi < 45: skor += 20
                if cp > sma50: skor += 20
                if fk and 0 < fk < 15: skor += 30
                if ret_1m > 0: skor += 30

                results.append({
                    "Hisse": ticker.replace(".IS", ""), "Fiyat": round(cp, 2),
                    "Günlük %": round(day_chg, 2), "1A %": round(ret_1m, 1), "RSI": round(rsi, 1),
                    "F/K": round(fk, 1) if fk else "N/A", "Skor": skor
                })
                progress_bar.progress((i + 1) / len(bist_full_list))
            except: continue
            
        res_df = pd.DataFrame(results)
        final_df = res_df[res_df['Skor'] >= score_threshold].sort_values(by="Skor", ascending=False)
        st.dataframe(final_df.style.background_gradient(subset=['Skor'], cmap='RdYlGn'), use_container_width=True)
    else:
        st.info("Pazar taramasını başlatmak için 'Analizi Başlat' butonuna tıklayın.")

# --- TAB 2: PORTFÖYÜM ---
with tab2:
    st.subheader("💼 Portföy Durumu")
    if 'portfolio_data' not in st.session_state:
        st.session_state.portfolio_data = pd.DataFrame([{"Hisse Kodu": "THYAO", "Adet": 1, "Maliyet": 300.0}])

    edited_df = st.data_editor(st.session_state.portfolio_data, num_rows="dynamic", use_container_width=True)
    st.session_state.portfolio_data = edited_df

    if st.button("💸 Portföyü Hesapla"):
        p_results = []
        for _, row in edited_df.iterrows():
            h = str(row['Hisse Kodu']).upper().strip()
            if not h: continue
            t = f"{h}.IS" if not h.endswith(".IS") else h
            try:
                price = yf.Ticker(t).history(period="1d")['Close'].iloc[-1]
                kz = (price - row['Maliyet']) * row['Adet']
                p_results.append({"Hisse": h, "Fiyat": round(price, 2), "Kâr/Zarar TL": round(kz, 2)})
            except: pass
        
        if p_results:
            st.dataframe(pd.DataFrame(p_results), use_container_width=True)
            total = sum(x['Kâr/Zarar TL'] for x in p_results)
            st.metric("Net Durum", f"{total:,.2f} TL", delta=f"{total:,.2f} TL")
            if total > 0: st.balloons()

# --- TAB 3: HABERLER & GRAFİK ---
with tab3:
    st.subheader("📈 Hisse Detay Analizi")
    selected_ticker = st.selectbox("Hisse Seçin:", bist_full_list, key="detail_select")

    if selected_ticker:
        try:
            hisse_obj = yf.Ticker(selected_ticker)
            # Grafik
            detail_data = hisse_obj.history(period="2y")
            if not detail_data.empty:
                detail_data['SMA50'] = ta.sma(detail_data['Close'], length=50)
                detail_data['SMA200'] = ta.sma(detail_data['Close'], length=200)
                plot_df = detail_data[['Close', 'SMA50', 'SMA200']].tail(130).dropna()
                st.line_chart(plot_df)
            
            # Haberler
            st.markdown("---")
            st.write("📰 **Son Haberler**")
            news = hisse_obj.news
            for item in news[:3]:
                st.write(f"🔗 **[{item['title']}]({item['link']})**")
        except Exception as e:
            st.error(f"Veri yüklenirken hata: {e}")

st.markdown("---")
st.caption("BIST Master Analiz Terminali | Veriler teknik momentum ve temel analiz çarpanları ile hesaplanır.")

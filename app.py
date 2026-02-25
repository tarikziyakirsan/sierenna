import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import feedparser
from urllib.parse import quote

# --- 1. SAYFA AYARLARI VE SIDEBAR'I TAMAMEN GİZLEME ---
st.set_page_config(page_title="BIST Analiz Terminali", layout="wide", initial_sidebar_state="collapsed")

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

# --- 2. BAŞLIK VE YASAL UYARI ---
st.title("📊 BIST Analiz Paneli")
st.write("Teknik Momentum, Temel Değerleme ve Performans Denetimi")

st.warning("⚠️ **Yasal Uyarı:** Bu uygulama bilgilendirme amaçlıdır. Burada yer alan veriler, analizler ve skorlar kesinlikle yatırım tavsiyesi değildir. Piyasa verileri gecikmeli olabilir ve analiz sonuçları hata payı içerebilir. Yapılan tüm işlemlerin riski ve sorumluluğu tamamen kullanıcıya aittir.")

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
    "KONTR.IS", "KONYA.IS", "KORDS.IS", "KOZAA.IS", "KOZAL.IS", "KRDMA.IS", "KRDMB.IS", "KRDMD.IS", "

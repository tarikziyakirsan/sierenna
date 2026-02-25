import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import feedparser
from urllib.parse import quote

# --- 1. SAYFA AYARLARI VE SIDEBAR'I TAMAMEN GİZLEME ---
st.set_page_config(page_title="BIST Analiz Terminali", layout="wide", initial_sidebar_state="collapsed")

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

# --- 2. BAŞLIK VE YASAL UYARI ---
st.title("📊 BIST Analiz Paneli")
st.write("Teknik Momentum, Temel Değerleme ve Performans Denetimi")

st.warning("⚠️ **Yasal Uyarı:** Bu uygulama bilgilendirme amaçlıdır. Burada yer alan veriler, analizler ve skorlar kesinlikle yatırım tavsiyesi değildir. Piyasa verileri gecikmeli olabilir ve analiz sonuçları hata payı içerebilir. Yapılan tüm işlemlerin riski ve sorumluluğu tamamen kullanıcıya aittir.")

st.markdown("---")

# --- 3. HİSSE LİSTESİ (Hatasız Tam Liste) ---
bist_full_list = sorted(list(set([
    "A1CAP.IS", "ACSEL.IS", "ADEZ.IS", "ADESE.IS", "AEFES.IS", "AFYON.IS", "AGESA.IS", "AGHOL.IS", "AGROT.IS", "AHGAZ.IS",
    "AKBNK.IS", "AKCNS.IS", "AKENR.IS", "AKFGY.IS", "AKFYE.IS", "AKGRT.IS", "AKMGY.IS", "AKSA.IS", "AKSEN.IS", "ALARK.IS",
    "ALBRK.IS", "ALCTL.IS", "ALFAS.IS", "ALGYO.IS", "ALKA.IS", "ALKIM.IS", "ALMAD.IS", "ALTNY.IS", "ANELE.IS", "ANGEN.IS",
    "ANHYT.IS", "ANSGR.IS", "ARCLK.IS", "ARDYZ.IS", "ARENA.IS", "ARSAN.IS", "ASCEG.IS", "ASELS.IS", "ASGYO.IS", "ASTOR.IS",
    "ASUZU.IS", "ATAKP.IS", "ATATP.IS", "AVHOL.IS", "AVOD.IS", "AVPGY.IS", "AVTUR.IS", "AYDEM.IS", "AYEN.IS", "AYGAZ.IS",
    "AZTEK.IS", "BAGFS.IS", "BAKAB.IS", "BANVT.IS", "BARMA.IS", "BASGZ.IS", "BAYRK.IS", "BEGYO.IS", "BERA.IS", "BEYAZ.IS",
    "BFREN.IS", "BIENP.IS", "BIGCH.IS", "BIMAS.IS", "BINHO.IS", "BIOEN.IS", "BIZIM.IS", "BJKAS.IS", "BLCYT.IS", "BMTKS.IS",
    "BNTAS.IS", "BOBET.IS", "BORLS.IS", "BOSSA.IS", "BRISA.IS", "BRKSN.IS", "BRMEN.IS", "BRSAN.IS", "BRY

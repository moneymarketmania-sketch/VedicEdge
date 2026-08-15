import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta, date
import math
import requests
import io
import plotly.graph_objects as go

st.set_page_config(page_title="VedicEdge", page_icon="🔵", layout="wide")

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');
:root{--bg:#060810;--bg2:#0d1117;--border:rgba(255,255,255,0.07);--text:#e8edf5;--muted:#64748b;--gold:#f59e0b;--green:#10b981;--red:#ef4444;--blue:#3b82f6;--purple:#8b5cf6;--cyan:#06b6d4;}
html,body,.stApp{background:var(--bg)!important;color:var(--text);font-family:'Space Grotesk',sans-serif;}
h1,h2,h3,h4,h5{font-family:'Space Grotesk',sans-serif;color:var(--text);}
.gc{background:linear-gradient(135deg,rgba(255,255,255,0.04),rgba(255,255,255,0.01));border:1px solid var(--border);border-radius:20px;padding:24px;margin-bottom:16px;backdrop-filter:blur(12px);box-shadow:0 4px 24px rgba(0,0,0,0.4),inset 0 1px 0 rgba(255,255,255,0.06);transition:box-shadow .25s;}
.gc:hover{box-shadow:0 8px 32px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.08);}
.gc-gold{border-color:rgba(245,158,11,.3);box-shadow:0 4px 24px rgba(245,158,11,.08);}
.gc-green{border-color:rgba(16,185,129,.3);box-shadow:0 4px 24px rgba(16,185,129,.08);}
.gc-red{border-color:rgba(239,68,68,.3);box-shadow:0 4px 24px rgba(239,68,68,.08);}
.gc-blue{border-color:rgba(59,130,246,.3);box-shadow:0 4px 24px rgba(59,130,246,.08);}
.gc-purple{border-color:rgba(139,92,246,.3);box-shadow:0 4px 24px rgba(139,92,246,.08);}
.gc-cyan{border-color:rgba(6,182,212,.3);box-shadow:0 4px 24px rgba(6,182,212,.08);}
.lc{border-left:3px solid;border-radius:12px;padding:12px 16px;margin-bottom:8px;}
.lc-gold{border-color:var(--gold);background:linear-gradient(90deg,rgba(245,158,11,.07),transparent);}
.lc-green{border-color:var(--green);background:linear-gradient(90deg,rgba(16,185,129,.07),transparent);}
.lc-red{border-color:var(--red);background:linear-gradient(90deg,rgba(239,68,68,.07),transparent);}
.lc-blue{border-color:var(--blue);background:linear-gradient(90deg,rgba(59,130,246,.07),transparent);}
.lc-purple{border-color:var(--purple);background:linear-gradient(90deg,rgba(139,92,246,.07),transparent);}
.lc-cyan{border-color:var(--cyan);background:linear-gradient(90deg,rgba(6,182,212,.07),transparent);}
.verdict-banner{border-radius:16px;padding:18px 24px;margin:12px 0;font-size:20px;font-weight:800;letter-spacing:-.5px;}
.vb-buy{background:linear-gradient(135deg,rgba(16,185,129,.18),rgba(16,185,129,.05));border:1px solid rgba(16,185,129,.4);color:#10b981;}
.vb-caution{background:linear-gradient(135deg,rgba(245,158,11,.18),rgba(245,158,11,.05));border:1px solid rgba(245,158,11,.4);color:#f59e0b;}
.vb-avoid{background:linear-gradient(135deg,rgba(239,68,68,.18),rgba(239,68,68,.05));border:1px solid rgba(239,68,68,.4);color:#ef4444;}
.score-ring{font-size:56px;font-weight:900;font-family:'JetBrains Mono',monospace;line-height:1;}
.pb-wrap{background:rgba(255,255,255,.06);border-radius:100px;height:7px;margin:5px 0 10px;overflow:hidden;}
.pb-fill{border-radius:100px;height:7px;}
.kpi{border-radius:16px;padding:16px 18px;text-align:center;background:linear-gradient(135deg,rgba(255,255,255,.04),rgba(255,255,255,.01));border:1px solid var(--border);}
.kpi-label{font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:var(--muted);margin-bottom:5px;}
.kpi-val{font-size:26px;font-weight:800;font-family:'JetBrains Mono',monospace;}
.sec-title{font-size:1.3rem;font-weight:700;margin:24px 0 14px;display:flex;align-items:center;gap:10px;}
.sec-title::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(255,255,255,.1),transparent);}
div[data-testid="stTextInput"] input{background:rgba(255,255,255,.04)!important;border:1px solid rgba(255,255,255,.12)!important;border-radius:50px!important;color:#e8edf5!important;font-family:'Space Grotesk',sans-serif!important;font-size:14px!important;padding:10px 20px!important;letter-spacing:.3px;box-shadow:0 2px 16px rgba(0,0,0,.3),inset 0 1px 0 rgba(255,255,255,.06)!important;transition:all .2s!important;}
div[data-testid="stTextInput"] input:focus{border-color:rgba(245,158,11,.5)!important;box-shadow:0 0 0 3px rgba(245,158,11,.1),0 2px 16px rgba(0,0,0,.3)!important;outline:none!important;}
div[data-testid="stTextInput"] input::placeholder{color:#475569!important;}
div[data-testid="stTextInput"] label{display:none!important;}
.stButton>button{background:linear-gradient(135deg,rgba(255,255,255,.06),rgba(255,255,255,.02))!important;border:1px solid rgba(255,255,255,.1)!important;border-radius:14px!important;color:var(--text)!important;font-family:'Space Grotesk',sans-serif!important;font-weight:600!important;transition:all .2s!important;}
.stButton>button:hover{background:linear-gradient(135deg,rgba(255,255,255,.1),rgba(255,255,255,.04))!important;border-color:rgba(255,255,255,.2)!important;transform:translateY(-1px)!important;}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#1d4ed8,#7c3aed)!important;border-color:transparent!important;}
.stTabs [data-baseweb="tab-list"]{background:var(--bg2)!important;border-radius:16px;padding:4px;gap:4px;}
.stTabs [data-baseweb="tab"]{border-radius:12px!important;color:var(--muted)!important;font-family:'Space Grotesk',sans-serif!important;font-weight:600!important;}
.stTabs [aria-selected="true"]{background:rgba(255,255,255,.08)!important;color:var(--text)!important;}
hr{border-color:rgba(255,255,255,.06)!important;}
</style>
""",
    unsafe_allow_html=True,
)

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown(
    """
<div style="display:flex;align-items:center;gap:14px;margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid rgba(255,255,255,0.06)">
    <div style="font-size:2.2rem;font-weight:900;letter-spacing:-2px;background:linear-gradient(135deg,#f59e0b,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent">VedicEdge</div>
    <div style="font-size:12px;color:#475569;border:1px solid rgba(255,255,255,0.07);border-radius:20px;padding:3px 12px;letter-spacing:.5px">Sarvatobhadra Chakra · Real-Time NSE</div>
</div>
""",
    unsafe_allow_html=True,
)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for k, v in [
    ("selected_symbol", None), ("scan_results", []), ("scan_ran", False),
    ("analyze_triggered", False), ("last_symbol", ""),
]:
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def pb(val, max_val, color):
    pct = min(100, max(0, val / max_val * 100))
    return f'<div class="pb-wrap"><div class="pb-fill" style="width:{pct}%;background:{color}"></div></div>'

def kpi(label, val, color="#e8edf5", sub=None):
    sub_h = f'<div style="font-size:11px;color:#64748b;margin-top:3px">{sub}</div>' if sub else ""
    return f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-val" style="color:{color}">{val}</div>{sub_h}</div>'

def safe_html(text):
    return str(text).replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def _strip_timezone(hist):
    if hist is None or hist.empty:
        return hist
    try:
        if hist.index.tzinfo is not None:
            hist.index = hist.index.tz_convert(None)
    except Exception:
        try:
            hist.index = hist.index.tz_localize(None)
        except Exception:
            pass
    return hist

# ══════════════════════════════════════════════════════════════════════════════
# INDEX MAP — ALL NSE INDICES
# ══════════════════════════════════════════════════════════════════════════════
INDEX_MAP = {
    # ── Broad Market ──────────────────────────────────────────────────────────
    "Nifty 50":         {"tickers": ["^NSEI", "^NSEI"],         "label": "Nifty 50",         "color": "#3b82f6"},
    "Sensex":           {"tickers": ["^BSESN", "^BSESN"],       "label": "Sensex",           "color": "#f59e0b"},
    "Nifty Next 50":    {"tickers": ["^NSENIFTY50", "^NSEMIDCAP"], "label": "Nifty Next 50",  "color": "#8b5cf6"},
    "Nifty 100":        {"tickers": ["^NSE100", "^CRSMID"],     "label": "Nifty 100",        "color": "#06b6d4"},
    "Nifty 200":        {"tickers": ["^NSE200", "^NSEMIDCAP"],  "label": "Nifty 200",        "color": "#10b981"},
    "Nifty 500":        {"tickers": ["^CRSNXD", "^NSE500"],     "label": "Nifty 500",        "color": "#a855f7"},
    "Nifty Total Market": {"tickers": ["^NSTMTM", "^NSTTMC"],   "label": "Nifty Total Mkt",  "color": "#ec4899"},
    # ── Mid & Small Cap ──────────────────────────────────────────────────────
    "Nifty Midcap 50":    {"tickers": ["^NSMIDCP50", "^NSEMID50"],   "label": "Nifty Midcap 50",    "color": "#f97316"},
    "Nifty Midcap 100":   {"tickers": ["^NSEMIDCAP100", "^NSEMID100"], "label": "Nifty Midcap 100", "color": "#fb923c"},
    "Nifty Midcap 150":   {"tickers": ["^NSEMIDCAP150", "^NSEMID150"], "label": "Nifty Midcap 150", "color": "#fdba74"},
    "Nifty Smallcap 50":  {"tickers": ["^NSESCAP50", "^NSESC50"],     "label": "Nifty Smallcap 50", "color": "#14b8a6"},
    "Nifty Smallcap 100": {"tickers": ["^NSESCAP100", "^NSESC100"],   "label": "Nifty Smallcap 100","color": "#2dd4bf"},
    "Nifty Smallcap 250": {"tickers": ["^NSESCAP250", "^NSESC250"],   "label": "Nifty Smallcap 250","color": "#5eead4"},
    "Nifty MidSmallcap 400": {"tickers": ["^NSEMIDSMALL400", "^NSEMS400"], "label": "Nifty MidSmall 400", "color": "#fbbf24"},
    "Nifty LargeMidcap 250": {"tickers": ["^NSELRGMID250", "^NSELM250"], "label": "Nifty LargeMid 250", "color": "#facc15"},
    # ── Sector Indices ───────────────────────────────────────────────────────
    "Bank Nifty":            {"tickers": ["^NSEBANK", "^NSEBANK"],       "label": "Bank Nifty",       "color": "#ef4444"},
    "Nifty IT":              {"tickers": ["^NSEIT", "^CNXIT"],           "label": "Nifty IT",         "color": "#3b82f6"},
    "Nifty Pharma":          {"tickers": ["^NSEPHARMA", "^CNXPHARMA"],   "label": "Nifty Pharma",     "color": "#10b981"},
    "Nifty Auto":            {"tickers": ["^NSEAUTO", "^CNXAUTO"],       "label": "Nifty Auto",       "color": "#f59e0b"},
    "Nifty FMCG":            {"tickers": ["^NSEFMCG", "^CNXFMCG"],       "label": "Nifty FMCG",       "color": "#8b5cf6"},
    "Nifty Metal":           {"tickers": ["^NSEMETAL", "^CNXMETAL"],     "label": "Nifty Metal",      "color": "#06b6d4"},
    "Nifty Realty":          {"tickers": ["^NSEREALTY", "^CNXREALTY"],   "label": "Nifty Realty",     "color": "#a855f7"},
    "Nifty Energy":          {"tickers": ["^NSEENERGY", "^CNXENERGY"],   "label": "Nifty Energy",     "color": "#f97316"},
    "Nifty Infrastructure":  {"tickers": ["^NSEINFRA", "^CNXINFRA"],     "label": "Nifty Infra",      "color": "#14b8a6"},
    "Nifty Media":           {"tickers": ["^NSEMEDIA", "^CNXMEDIA"],     "label": "Nifty Media",      "color": "#ec4899"},
    "Nifty Healthcare":      {"tickers": ["^NSEHEALTH", "^CNXHEALTH"],   "label": "Nifty Healthcare", "color": "#22d3ee"},
    "Nifty Consumer Durables": {"tickers": ["^NSECONSDUR", "^CNXCONSDUR"], "label": "Nifty Cons Durable", "color": "#fbbf24"},
    "Nifty Oil & Gas":       {"tickers": ["^NSEOILGAS", "^CNXOILGAS"],   "label": "Nifty Oil & Gas",  "color": "#fb923c"},
    "Nifty PSU Bank":        {"tickers": ["^NSEPSUBANK", "^CNXPSUBANK"], "label": "Nifty PSU Bank",   "color": "#dc2626"},
    "Nifty Pvt Bank":        {"tickers": ["^NSEPBANK", "^CNXPBANK"],     "label": "Nifty Pvt Bank",   "color": "#b91c1c"},
    "Nifty Financial Services": {"tickers": ["^NSEFIN", "^CNXFIN"],       "label": "Nifty Fin Serv",   "color": "#7c3aed"},
    "Nifty Financial Services 25": {"tickers": ["^NSEFIN25", "^CNXFIN25"], "label": "Nifty Fin25",     "color": "#6d28d9"},
    "Nifty Commodities":     {"tickers": ["^NSECOMMOD", "^CNXCOMMOD"],   "label": "Nifty Commodities","color": "#ca8a04"},
    "Nifty CPSE":            {"tickers": ["^NSECPSE", "^CNXCPSE"],       "label": "Nifty CPSE",      "color": "#65a30d"},
    # ── Thematic / Strategy ──────────────────────────────────────────────────
    "Nifty MNC":             {"tickers": ["^NSEMNC", "^CNXMNC"],         "label": "Nifty MNC",       "color": "#0ea5e9"},
    "Nifty PSE":             {"tickers": ["^NSEPSE", "^CNXPSE"],         "label": "Nifty PSE",       "color": "#0891b2"},
    "Nifty Services Sector": {"tickers": ["^NSESRV", "^CNXSRV"],         "label": "Nifty Services",  "color": "#7dd3fc"},
    "Nifty India Consumption": {"tickers": ["^NSECONSUM", "^CNXCONSUM"], "label": "Nifty Consum",    "color": "#fcd34d"},
    "Nifty India Manufacturing": {"tickers": ["^NSEMANUF", "^CNXMANUF"], "label": "Nifty Manuf",     "color": "#f472b6"},
    "Nifty Digital India":   {"tickers": ["^NSEDIGITAL", "^CNXDIGITAL"], "label": "Nifty Digital",   "color": "#818cf8"},
    "Nifty India Growth 50": {"tickers": ["^NSEIGROWTH50", "^CNXIG50"],  "label": "Nifty Growth 50","color": "#c084fc"},
    "Nifty100 ESG":          {"tickers": ["^NSE100ESG", "^CNX100ESG"],   "label": "Nifty100 ESG",   "color": "#34d399"},
    "Nifty200 Quality 30":   {"tickers": ["^NSE200Q30", "^CNX200Q30"],   "label": "Nifty200 Q30",   "color": "#4ade80"},
    "Nifty50 Value 20":      {"tickers": ["^NSE50V20", "^CNX50V20"],     "label": "Nifty50 Val 20", "color": "#86efac"},
    "Nifty50 Equal Weight":  {"tickers": ["^NSE50EW", "^CNX50EW"],       "label": "Nifty50 EW",     "color": "#a7f3d0"},
    "Nifty100 Equal Weight": {"tickers": ["^NSE100EW", "^CNX100EW"],     "label": "Nifty100 EW",    "color": "#bef264"},
    "Nifty200 Momentum 30":  {"tickers": ["^NSE200M30", "^CNX200M30"],   "label": "Nifty200 Mom30", "color": "#fde047"},
    "Nifty Alpha 50":        {"tickers": ["^NSEALPHA50", "^CNXALPHA50"], "label": "Nifty Alpha 50", "color": "#fca5a5"},
    "Nifty High Beta 50":    {"tickers": ["^NSEHBETA50", "^CNXHB50"],    "label": "Nifty HiBeta50", "color": "#f87171"},
    "Nifty Low Volatility 50": {"tickers": ["^NSELVOL50", "^CNXLV50"],   "label": "Nifty LoVol50",  "color": "#93c5fd"},
    "Nifty Shariah 25":      {"tickers": ["^NSESHARIAH25", "^CNXSH25"],  "label": "Nifty Shariah25","color": "#d8b4fe"},
    # ── BSE Indices ──────────────────────────────────────────────────────────
    "BSE Sensex 30":   {"tickers": ["^BSESN", "^BSE30"],        "label": "BSE Sensex",    "color": "#f59e0b"},
    "BSE 100":         {"tickers": ["^BSE100", "^BSE100"],       "label": "BSE 100",       "color": "#fb923c"},
    "BSE 200":         {"tickers": ["^BSE200", "^BSE200"],       "label": "BSE 200",       "color": "#fdba74"},
    "BSE 500":         {"tickers": ["^BSE500", "^BSE500"],       "label": "BSE 500",       "color": "#fbbf24"},
    "BSE Midcap":      {"tickers": ["^BSEMIDCAP", "^BSEMID"],    "label": "BSE Midcap",    "color": "#f97316"},
    "BSE Smallcap":    {"tickers": ["^BSESMALLCAP", "^BSESMALL"], "label": "BSE Smallcap", "color": "#14b8a6"},
    "BSE Bankex":      {"tickers": ["^BSEBANK", "^BSEBK"],       "label": "BSE Bankex",    "color": "#ef4444"},
    "BSE IT":          {"tickers": ["^BSEIT", "^BSEIT"],         "label": "BSE IT",        "color": "#3b82f6"},
    "BSE Auto":        {"tickers": ["^BSEAUTO", "^BSEAUTO"],     "label": "BSE Auto",      "color": "#10b981"},
    "BSE Pharma":      {"tickers": ["^BSEPHARMA", "^BSEPH"],     "label": "BSE Pharma",    "color": "#a855f7"},
    "BSE Power":       {"tickers": ["^BSEPOWER", "^BSEPOW"],     "label": "BSE Power",     "color": "#06b6d4"},
    "BSE Realty":      {"tickers": ["^BSEREALTY", "^BSEREAL"],   "label": "BSE Realty",    "color": "#ec4899"},
    "BSE Metal":       {"tickers": ["^BSEMETAL", "^BSEMET"],     "label": "BSE Metal",     "color": "#ca8a04"},
    "BSE Oil & Gas":   {"tickers": ["^BSEOIL", "^BSEOILG"],      "label": "BSE Oil&Gas",   "color": "#65a30d"},
    "BSE Consumer Durable": {"tickers": ["^BSECD", "^BSECONSDUR"], "label": "BSE Cons Dur", "color": "#0ea5e9"},
    "BSE Capital Goods":     {"tickers": ["^BSECG", "^BSECAPGOOD"], "label": "BSE Cap Goods","color": "#8b5cf6"},
    "BSE Teck":        {"tickers": ["^BSETECK", "^BSETECK"],     "label": "BSE Teck",      "color": "#7c3aed"},
    "BSE PSU":         {"tickers": ["^BSEPSU", "^BSEPSU"],       "label": "BSE PSU",       "color": "#dc2626"},
}

# ══════════════════════════════════════════════════════════════════════════════
# NIFTY 500 FETCH
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=86400, show_spinner=False)
def fetch_nifty500_symbols():
    try:
        url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
        headers = {"User-Agent": "Mozilla/5.0", "Accept": "text/html,application/xhtml+xml"}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        df = pd.read_csv(io.StringIO(r.text))
        symbols = df["Symbol"].dropna().str.strip().tolist()
        if len(symbols) > 100:
            seen = set(); unique = []
            for s in symbols:
                if s not in seen: seen.add(s); unique.append(s)
            return unique
    except Exception:
        pass
    raw = [
        "RELIANCE","TCS","HDFCBANK","INFY","ICICIBANK","SBIN","LT","BHARTIARTL",
        "AXISBANK","KOTAKBANK","MARUTI","SUNPHARMA","HINDUNILVR","ITC","ULTRACEMCO",
        "WIPRO","HCLTECH","NTPC","POWERGRID","ONGC","BAJFINANCE","TATAMOTORS",
        "TATASTEEL","JSWSTEEL","HINDALCO","TITAN","ASIANPAINT","DMART","ADANIENT",
        "NESTLEIND","BAJAJFINSV","TECHM","INDUSINDBK","GRASIM","ADANIPORTS",
        "COALINDIA","BPCL","BRITANNIA","CIPLA","DRREDDY","EICHERMOT","HEROMOTOCO",
        "DIVISLAB","APOLLOHOSP","TATACONSUM","LTIM","SBILIFE","HDFCLIFE","BAJAJ-AUTO","M&M",
        "SHRIRAMFIN","PIDILITIND","BERGEPAINT","MUTHOOTFIN","CHOLAFIN","MANAPPURAM",
        "ABCAPITAL","ICICIGI","NAUKRI","PERSISTENT","COFORGE","MPHASIS","TATACOMM",
        "OFSS","KPITTECH","ZOMATO","PAYTM","NYKAA","POLICYBZR","DELHIVERY","IRCTC",
        "CONCOR","SIEMENS","ABB","BHEL","CUMMINSIND","THERMAX","KECL","KALPATPOWR",
        "APLAPOLLO","HFCL","RAILTEL","RVNL","IRFC","RECLTD","PFC","SJVN","NHPC",
        "INDIANB","BANKINDIA","CANBK","UNIONBANK","FEDERALBNK","IDFCFIRSTB",
        "BANDHANBNK","RBLBANK","LICHSGFIN","PNBHOUSING","AAVAS","HOMEFIRST",
        "BIOCON","ALKEM","LUPIN","TORNTPHARM","AUROPHARMA","IPCALAB","LALPATHLAB",
        "METROPOLIS","MAXHEALTH","FORTIS","SYNGENE","NATCOPHARM","GRANULES","GLAND",
        "LAURUSLABS","PFIZER","ABBOTINDIA","GLAXO","AJANTPHARM",
        "TVSMOTOR","ASHOKLEY","MOTHERSON","BOSCHLTD","BHARATFORG","SUPRAJIT",
        "APOLLOTYRE","MRF","CEATLTD","BALKRISIND","ENDURANCE","SUNDRMFAST",
        "EXIDEIND","AMARAJABAT","WABCOINDIA","MINDAIND","GABRIEL","SUBROS",
        "MARICO","DABUR","GODREJCP","EMAMILTD","COLPAL","VBL","RADICO",
        "PGHH","JYOTHYLAB","BIKAJI","PATANJALI","VARUN","WONDERLA","DEVYANI",
        "LTTS","CYIENT","ZENSAR","HEXAWARE","BIRLASOFT","MASTEK","NIITTECH",
        "RAMSYSTEMS","TANLA","INTELLECT","NEWGEN","NUCLEUS","TATAELXSI",
        "NMDC","SAIL","NATIONALUM","HINDCOPPER","GMRINFRA","WELCORP","RATNAMANI",
        "JINDALSAW","JINDALSTEL","JSPL","MOIL","VEDL","HINDZINC","AIAENG",
        "TORNTPOWER","TATAPOWER","ADANIGREEN","ADANIPOWER","CESC","IEX",
        "MAHAGENCO","RPOWER","SUZLON","INOXWIND","GREENKO","ACME",
        "ENGINERSIN","NBCC","RITES","IRCON","NCC","PNCINFRA","KNRCON",
        "GPPL","MAHINDCIE","JKCEMENT","HEIDELBERG","RAMCOCEM","SHREECEM","JKIL",
        "DLF","GODREJPROP","OBEROIRLTY","PRESTIGE","PHOENIXLTD","BRIGADE","KOLTEPATIL",
        "MAHLIFE","LODHA","SUNTECK","SOBHA","ANANTRAJ","NESCO",
        "KARURVYSYA","DCBBANK","SOUTHBANK","LAKSHVILAS","TMB","EQUITASBNK","UJJIVAN",
        "SURYODAY","ESAFSFB","AUBANK","CREDITACC","AROHAN",
        "STARHEALTH","NIACL","GICRE","MAXFIN",
        "ATUL","DEEPAKNITRITE","NAVINFLUOR","SUDARSCHEM","GALAXYSURF",
        "VINATIORG","NOCIL","BALCHEMICALS","TATACHEM","GNFC","GSFC","CHAMBALFERT",
        "COROMANDEL","RALLIS","PIIND","BAYER","DHANUKA","INSECTICID",
        "PAGEIND","RAYMOND","ARVIND","TRIDENT","VARDHMAN","GOKEX","WELSPUNIND",
        "NITIN","ALOKTEXT","SPANDEX",
        "BLUEDART","MAHLOG","GATI","TCI","ALLCARGO","AEGISLOG",
        "ZEEL","SUNTV","PVRINOX","INOXLEISURE","TIPS","SAREGAMA","NAZARA",
        "IDEA","STLTECH","TEJAS",
        "INDHOTEL","EIHHOTEL","LEMONTREE","CHALET","MAHINDHOLIDAY",
        "MCDOWELL-N","UNITEDSPIRITS","GLOBUSSPR","ABFRL","TRENT","VMART",
        "SHOPERSTOP","AVENUESUP","MEESHO","CARTRADE","EASEMYTRIP",
        "RATEGAIN","JUSTDIAL","INFOEDGE","MATRIMONY","INDIAMART",
        "MCLEODRUS","WESTLIFE","JUBLFOOD","SAPPHIRE","BARBEQUE",
        "EQUITAS","SPANDANA","FUSION","UJJFIN",
    ]
    seen = set(); unique = []
    for s in raw:
        if s not in seen: seen.add(s); unique.append(s)
    return unique

# ══════════════════════════════════════════════════════════════════════════════
# DATA FETCH — STOCK
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=180, show_spinner=False)
def fetch_stock_data(symbol):
    try:
        tk = yf.Ticker(f"{symbol}.NS")
        hist = tk.history(period="1y", auto_adjust=True)
        if not hist.empty: hist = _strip_timezone(hist)
        if hist.empty or len(hist) < 10: raise ValueError("Empty")
        try:
            fi = tk.fast_info
            price = float(fi.last_price or fi.regular_market_price or hist["Close"].iloc[-1])
            prev  = float(fi.previous_close or hist["Close"].iloc[-2])
        except Exception:
            price = float(hist["Close"].iloc[-1]); prev = float(hist["Close"].iloc[-2])
        chg = round((price - prev) / prev * 100, 2)
        try:
            info = tk.info
            beta = float(info.get("beta") or 1.0)
            pe = float(info.get("trailingPE") or 0)
            pb_val = float(info.get("priceToBook") or 3.5)
            sector = info.get("sector", "Unknown") or "Unknown"
            name = info.get("longName", symbol) or symbol
            volume = int(info.get("volume") or hist["Volume"].iloc[-1])
        except Exception:
            beta=1.0; pe=0.0; pb_val=3.5; sector="Unknown"; name=symbol; volume=int(hist["Volume"].iloc[-1])
        pe = round(pe, 1) if pe and pe > 0 else 25.0; pb_val = round(pb_val, 2)
        delta = hist["Close"].diff()
        g = delta.clip(lower=0).ewm(alpha=1/14, min_periods=14, adjust=False).mean()
        l = (-delta.clip(upper=0)).ewm(alpha=1/14, min_periods=14, adjust=False).mean()
        rsi_raw = 100 - 100 / (1 + g / l)
        rsi = round(float(rsi_raw.iloc[-1]), 1) if not math.isnan(rsi_raw.iloc[-1]) else 50.0
        tr = pd.concat([hist["High"]-hist["Low"], (hist["High"]-hist["Close"].shift()).abs(), (hist["Low"]-hist["Close"].shift()).abs()], axis=1).max(axis=1)
        atr = round(float(tr.rolling(14).mean().iloc[-1]), 2)
        atr_pct = round(atr/price*100, 2) if price > 0 else 0
        w52h = round(float(hist["High"].max()), 2); w52l = round(float(hist["Low"].min()), 2)
        return dict(price=round(price,2), change_pct=chg, rsi=rsi, atr=atr, atr_pct=atr_pct, beta=beta, volume=volume, pe=pe, pb=pb_val, hist=hist, source="LIVE", sector=sector, name=name, w52h=w52h, w52l=w52l)
    except Exception as e:
        return dict(price=334.55, change_pct=3.46, rsi=58.4, atr=8.2, atr_pct=2.45, beta=1.06, volume=18310000, pe=25.0, pb=3.70, hist=None, source="DEMO", sector="Unknown", name=symbol, w52h=420.0, w52l=240.0)

# ══════════════════════════════════════════════════════════════════════════════
# DATA FETCH — INDEX
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=180, show_spinner=False)
def fetch_index_data(index_name):
    """Try each ticker in INDEX_MAP until one works."""
    cfg = INDEX_MAP.get(index_name)
    if not cfg: return None
    for ticker in cfg["tickers"]:
        try:
            tk = yf.Ticker(ticker)
            hist = tk.history(period="1y", auto_adjust=True)
            if hist.empty or len(hist) < 10: continue
            hist = _strip_timezone(hist)
            try:
                fi = tk.fast_info
                price = float(fi.last_price or fi.regular_market_price or hist["Close"].iloc[-1])
                prev = float(fi.previous_close or hist["Close"].iloc[-2])
            except Exception:
                price = float(hist["Close"].iloc[-1]); prev = float(hist["Close"].iloc[-2])
            chg = round((price-prev)/prev*100, 2)
            c = hist["Close"]
            delta = c.diff()
            g = delta.clip(lower=0).ewm(alpha=1/14, min_periods=14, adjust=False).mean()
            l = (-delta.clip(upper=0)).ewm(alpha=1/14, min_periods=14, adjust=False).mean()
            rsi_raw = 100 - 100/(1+g/l)
            rsi = round(float(rsi_raw.iloc[-1]),1) if not math.isnan(rsi_raw.iloc[-1]) else 50.0
            tr = pd.concat([hist["High"]-hist["Low"], (hist["High"]-hist["Close"].shift()).abs(), (hist["Low"]-hist["Close"].shift()).abs()], axis=1).max(axis=1)
            atr = round(float(tr.rolling(14).mean().iloc[-1]), 2)
            atr_pct = round(atr/price*100,2) if price>0 else 0
            w52h = round(float(hist["High"].max()),2); w52l = round(float(hist["Low"].min()),2)
            # EMAs & oscillators for index
            ema21 = round(float(c.ewm(span=21, adjust=False).mean().iloc[-1]), 2)
            ema50 = round(float(c.ewm(span=50, adjust=False).mean().iloc[-1]), 2)
            ema200 = round(float(c.ewm(span=200, adjust=False).mean().iloc[-1]), 2)
            ml = c.ewm(span=12, adjust=False).mean() - c.ewm(span=26, adjust=False).mean()
            ms = ml.ewm(span=9, adjust=False).mean()
            macd_hist = round(float(ml.iloc[-1]) - float(ms.iloc[-1]), 2)
            bm = c.rolling(20).mean(); bs = c.rolling(20).std()
            bb_upper = round(float((bm+2*bs).iloc[-1]),2)
            bb_lower = round(float((bm-2*bs).iloc[-1]),2)
            # ADX
            atr14 = tr.ewm(alpha=1/14, min_periods=14, adjust=False).mean()
            dmp_raw = hist["High"].diff().clip(lower=0)
            dmn_raw = (-hist["Low"].diff()).clip(lower=0)
            dmp = dmp_raw.where(dmp_raw > dmn_raw, 0)
            dmn = dmn_raw.where(dmn_raw > dmp_raw, 0)
            di_pos_s = dmp.ewm(alpha=1/14, min_periods=14, adjust=False).mean()
            di_neg_s = dmn.ewm(alpha=1/14, min_periods=14, adjust=False).mean()
            atr14_safe = atr14.replace(0, np.nan)
            di_pos_v = (di_pos_s/atr14_safe*100).iloc[-1]
            di_neg_v = (di_neg_s/atr14_safe*100).iloc[-1]
            di_pos = round(float(di_pos_v),1) if not math.isnan(di_pos_v) else 0.0
            di_neg = round(float(di_neg_v),1) if not math.isnan(di_neg_v) else 0.0
            dx = (abs(di_pos-di_neg)/(di_pos+di_neg+0.01)*100)
            adx = round(float(dx.ewm(alpha=1/14, min_periods=14, adjust=False).mean().iloc[-1] if isinstance(dx, pd.Series) else dx), 1)
            # Pivots
            h_copy = hist.copy(); h_copy.index = pd.to_datetime(h_copy.index)
            weekly = h_copy.resample("W").agg({"High":"max","Low":"min","Close":"last"}).dropna()
            if len(weekly)>=2:
                wph,wpl,wpc = round(float(weekly["High"].iloc[-2]),2), round(float(weekly["Low"].iloc[-2]),2), round(float(weekly["Close"].iloc[-2]),2)
            else:
                wph,wpl,wpc = round(float(hist["High"].iloc[-2]),2), round(float(hist["Low"].iloc[-2]),2), round(float(hist["Close"].iloc[-2]),2)
            w_pivot = round((wph+wpl+wpc)/3,2); w_r1=round(2*w_pivot-wpl,2); w_s1=round(2*w_pivot-wph,2)
            w_r2=round(w_pivot+(wph-wpl),2); w_s2=round(w_pivot-(wph-wpl),2)
            monthly = h_copy.resample("ME").agg({"High":"max","Low":"min","Close":"last"}).dropna()
            if len(monthly)>=2:
                mph,mpl,mpc = round(float(monthly["High"].iloc[-2]),2), round(float(monthly["Low"].iloc[-2]),2), round(float(monthly["Close"].iloc[-2]),2)
            else:
                mph,mpl,mpc = wph,wpl,wpc
            m_pivot=round((mph+mpl+mpc)/3,2); m_r1=round(2*m_pivot-mpl,2); m_s1=round(2*m_pivot-mph,2)
            m_r2=round(m_pivot+(mph-mpl),2); m_s2=round(m_pivot-(mph-mpl),2)
            return dict(price=round(price,2), change_pct=chg, rsi=rsi, atr=atr, atr_pct=atr_pct,
                        hist=hist, w52h=w52h, w52l=w52l, ema21=ema21, ema50=ema50, ema200=ema200,
                        macd_hist=macd_hist, bb_upper=bb_upper, bb_lower=bb_lower,
                        adx=adx, di_pos=di_pos, di_neg=di_neg,
                        w_pivot=w_pivot, w_r1=w_r1, w_s1=w_s1, w_r2=w_r2, w_s2=w_s2,
                        m_pivot=m_pivot, m_r1=m_r1, m_s1=m_s1, m_r2=m_r2, m_s2=m_s2)
        except Exception:
            continue
    return None

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_index_long_history(index_name):
    cfg = INDEX_MAP.get(index_name)
    if not cfg: return None
    for ticker in cfg["tickers"]:
        try:
            h = yf.Ticker(ticker).history(period="10y")
            if h.empty: h = yf.Ticker(ticker).history(period="5y")
            if not h.empty: h = _strip_timezone(h)
            return h if not h.empty else None
        except Exception:
            continue
    return None

# ══════════════════════════════════════════════════════════════════════════════
# TECHNICALS (STOCK)
# ══════════════════════════════════════════════════════════════════════════════
def compute_technicals(data):
    p = data["price"]
    if data.get("hist") is not None and len(data["hist"]) >= 20:
        h = data["hist"]; c = h["Close"]
        ema9=round(float(c.ewm(span=9,adjust=False).mean().iloc[-1]),2)
        ema21=round(float(c.ewm(span=21,adjust=False).mean().iloc[-1]),2)
        ema55=round(float(c.ewm(span=55,adjust=False).mean().iloc[-1]),2)
        ema200=round(float(c.ewm(span=200,adjust=False).mean().iloc[-1]),2)
        ml=c.ewm(span=12,adjust=False).mean()-c.ewm(span=26,adjust=False).mean()
        ms=ml.ewm(span=9,adjust=False).mean()
        macd_val=round(float(ml.iloc[-1]),2); macd_sig=round(float(ms.iloc[-1]),2); macd_hist=round(macd_val-macd_sig,2)
        bm=c.rolling(20).mean(); bs=c.rolling(20).std()
        bb_upper=round(float((bm+2*bs).iloc[-1]),2); bb_lower=round(float((bm-2*bs).iloc[-1]),2); bb_mid=round(float(bm.iloc[-1]),2)
        lo14=h["Low"].rolling(14).min(); hi14=h["High"].rolling(14).max()
        denom=(hi14-lo14).replace(0,np.nan); stoch_raw=((c-lo14)/denom*100)
        stoch_k=round(float(stoch_raw.iloc[-1]),1) if not math.isnan(stoch_raw.iloc[-1]) else 50.0
        stoch_d=round(float(stoch_raw.rolling(3).mean().iloc[-1]),1) if not math.isnan(stoch_raw.rolling(3).mean().iloc[-1]) else 50.0
        vol20=round(float(h["Volume"].rolling(20).mean().iloc[-1])); volr=round(data["volume"]/max(vol20,1),2)
        tr_s=pd.concat([h["High"]-h["Low"],(h["High"]-h["Close"].shift()).abs(),(h["Low"]-h["Close"].shift()).abs()],axis=1).max(axis=1)
        atr14=tr_s.ewm(alpha=1/14,min_periods=14,adjust=False).mean()
        dmp_raw=h["High"].diff().clip(lower=0); dmn_raw=(-h["Low"].diff()).clip(lower=0)
        dmp=dmp_raw.where(dmp_raw>dmn_raw,0); dmn=dmn_raw.where(dmn_raw>dmp_raw,0)
        di_pos_s=dmp.ewm(alpha=1/14,min_periods=14,adjust=False).mean(); di_neg_s=dmn.ewm(alpha=1/14,min_periods=14,adjust=False).mean()
        atr14_safe=atr14.replace(0,np.nan)
        di_pos_v=(di_pos_s/atr14_safe*100).iloc[-1]; di_neg_v=(di_neg_s/atr14_safe*100).iloc[-1]
        di_pos=round(float(di_pos_v),1) if not math.isnan(di_pos_v) else 0.0
        di_neg=round(float(di_neg_v),1) if not math.isnan(di_neg_v) else 0.0
        di_pos_ser=di_pos_s/atr14_safe*100; di_neg_ser=di_neg_s/atr14_safe*100
        dx_s=(di_pos_ser-di_neg_ser).abs()/(di_pos_ser+di_neg_ser).clip(lower=0.01)*100
        adx_v=dx_s.ewm(alpha=1/14,min_periods=14,adjust=False).mean().iloc[-1]
        adx=round(float(adx_v),1) if not math.isnan(adx_v) else 0.0
        h_copy=h.copy(); h_copy.index=pd.to_datetime(h_copy.index)
        weekly=h_copy.resample("W").agg({"High":"max","Low":"min","Close":"last"}).dropna()
        if len(weekly)>=2: wph=round(float(weekly["High"].iloc[-2]),2); wpl=round(float(weekly["Low"].iloc[-2]),2); wpc=round(float(weekly["Close"].iloc[-2]),2)
        else: wph=round(float(h["High"].iloc[-2]),2); wpl=round(float(h["Low"].iloc[-2]),2); wpc=round(float(h["Close"].iloc[-2]),2)
        w_pivot=round((wph+wpl+wpc)/3,2); w_r1=round(2*w_pivot-wpl,2); w_s1=round(2*w_pivot-wph,2)
        w_r2=round(w_pivot+(wph-wpl),2); w_s2=round(w_pivot-(wph-wpl),2); w_cpr_pct=round((w_r1-w_s1)/max(p,0.01)*100,2)
        monthly=h_copy.resample("ME").agg({"High":"max","Low":"min","Close":"last"}).dropna()
        if len(monthly)>=2: mph=round(float(monthly["High"].iloc[-2]),2); mpl=round(float(monthly["Low"].iloc[-2]),2); mpc=round(float(monthly["Close"].iloc[-2]),2)
        else: mph,mpl,mpc=wph,wpl,wpc
        m_pivot=round((mph+mpl+mpc)/3,2); m_r1=round(2*m_pivot-mpl,2); m_s1=round(2*m_pivot-mph,2)
        m_r2=round(m_pivot+(mph-mpl),2); m_s2=round(m_pivot-(mph-mpl),2); m_cpr_pct=round((m_r1-m_s1)/max(p,0.01)*100,2)
        swing_highs=[]; swing_lows=[]; roll_win=10
        for i in range(roll_win,len(h)-roll_win):
            if h["High"].iloc[i]==h["High"].iloc[i-roll_win:i+roll_win].max(): swing_highs.append(round(float(h["High"].iloc[i]),2))
            if h["Low"].iloc[i]==h["Low"].iloc[i-roll_win:i+roll_win].min(): swing_lows.append(round(float(h["Low"].iloc[i]),2))
        key_res=sorted([x for x in swing_highs if x>p])[:3]; key_sup=sorted([x for x in swing_lows if x<p],reverse=True)[:3]
        mag=10**max(0,int(math.log10(max(p,1)))-1); rounds=[]; base=round(p*0.85/mag)*mag
        while base<=p*1.15: rounds.append(round(base,2)); base+=mag
        w52h=data["w52h"]; w52l=data["w52l"]; w52h_prox=round((w52h-p)/max(p,0.01)*100,1); w52l_prox=round((p-w52l)/max(p,0.01)*100,1)
    else:
        ema9=ema21=ema55=ema200=p; macd_val=0.0; macd_sig=0.0; macd_hist=0.0
        bb_upper=round(p*1.04,2); bb_lower=round(p*0.96,2); bb_mid=p
        stoch_k=50.0; stoch_d=50.0; vol20=data["volume"]; volr=1.0
        di_pos=0.0; di_neg=0.0; adx=0.0
        w_pivot=p; w_r1=round(p*1.02,2); w_s1=round(p*0.98,2); w_r2=round(p*1.04,2); w_s2=round(p*0.96,2); w_cpr_pct=2.0
        m_pivot=p; m_r1=round(p*1.04,2); m_s1=round(p*0.96,2); m_r2=round(p*1.08,2); m_s2=round(p*0.92,2); m_cpr_pct=4.0
        key_res=[round(p*1.03,2),round(p*1.06,2),round(p*1.10,2)]; key_sup=[round(p*0.97,2),round(p*0.94,2),round(p*0.90,2)]; rounds=[]
        w52h=data.get("w52h",p*1.2); w52l=data.get("w52l",p*0.8); w52h_prox=round((w52h-p)/max(p,0.01)*100,1); w52l_prox=round((p-w52l)/max(p,0.01)*100,1)
    return dict(ema9=ema9,ema21=ema21,ema55=ema55,ema200=ema200,macd_val=macd_val,macd_sig=macd_sig,macd_hist=macd_hist,
                bb_upper=bb_upper,bb_lower=bb_lower,bb_mid=bb_mid,stoch_k=stoch_k,stoch_d=stoch_d,vol20=vol20,volr=volr,
                di_pos=di_pos,di_neg=di_neg,adx=adx,w_pivot=w_pivot,w_r1=w_r1,w_s1=w_s1,w_r2=w_r2,w_s2=w_s2,w_cpr_pct=w_cpr_pct,
                m_pivot=m_pivot,m_r1=m_r1,m_s1=m_s1,m_r2=m_r2,m_s2=m_s2,m_cpr_pct=m_cpr_pct,
                key_res=key_res,key_sup=key_sup,rounds=rounds,w52h=w52h,w52l=w52l,w52h_prox=w52h_prox,w52l_prox=w52l_prox)

def compute_tech_score(data, tech):
    p=data["price"]; ts=0; bull=[]; bear=[]
    if p>tech["ema9"] and p>tech["ema21"] and p>tech["ema55"]: ts+=2; bull.append("Above EMA9/21/55 ✅")
    elif p>tech["ema9"] and p>tech["ema21"]: ts+=1; bull.append("Above EMA9/21")
    else: ts-=1; bear.append("Below key EMAs")
    if p>tech["ema200"]: ts+=1; bull.append("Above 200 EMA ✅")
    else: ts-=1; bear.append("Below 200 EMA")
    if 40<data["rsi"]<70: ts+=1; bull.append(f"RSI {data['rsi']} healthy ✅")
    elif data["rsi"]>=70: ts-=1; bear.append(f"RSI {data['rsi']} overbought ⚠️")
    else: ts+=1; bull.append(f"RSI {data['rsi']} oversold bounce ✅")
    if tech["macd_hist"]>0: ts+=1; bull.append("MACD hist positive ✅")
    else: ts-=1; bear.append("MACD hist negative")
    if tech["volr"]>1.3: ts+=1; bull.append(f"Volume {tech['volr']}x ✅")
    elif tech["volr"]<0.7: ts-=1; bear.append("Low volume")
    if tech["adx"]>25 and tech["di_pos"]>tech["di_neg"]: ts+=1; bull.append(f"ADX {tech['adx']} +DI ✅")
    elif tech["adx"]>25 and tech["di_pos"]<tech["di_neg"]: ts-=1; bear.append("Strong downtrend")
    if tech["bb_mid"]<p<tech["bb_upper"]: ts+=1; bull.append("Mid-upper BB ✅")
    elif p>tech["bb_upper"]: bear.append("Above upper BB")
    elif p<tech["bb_lower"]: ts+=1; bull.append("Lower BB bounce ✅")
    if data["pe"]<25 and data["pb"]<4: ts+=1; bull.append(f"PE {data['pe']} ✅")
    elif data["pe"]>45: bear.append(f"PE {data['pe']} stretched")
    return ts, bull, bear

# ══════════════════════════════════════════════════════════════════════════════
# GANN CORE
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_long_history(symbol):
    try:
        tk=yf.Ticker(f"{symbol}.NS"); h=tk.history(period="10y")
        if h.empty: h=tk.history(period="5y")
        if not h.empty: h=_strip_timezone(h)
        return h if not h.empty else None
    except Exception: return None

def _find_significant_anchor(hist):
    if hist is None or len(hist)<50: return None
    candidates=[]; win=20
    for i in range(win,len(hist)-win):
        bar_low=float(hist["Low"].iloc[i]); window_min=float(hist["Low"].iloc[i-win:i+win].min())
        if bar_low==window_min:
            vol=float(hist["Volume"].iloc[i]); subsequent_high=float(hist["High"].iloc[i:].max())
            move_pct=(subsequent_high-bar_low)/max(bar_low,1)*100
            candidates.append((move_pct,vol,bar_low,hist.index[i]))
    if not candidates:
        idx=hist["Low"].idxmin(); high_idx=hist["High"].idxmax()
        return (round(float(hist["Low"].min()),2), idx.date() if hasattr(idx,"date") else idx,
                round(float(hist["High"].max()),2), high_idx.date() if hasattr(high_idx,"date") else high_idx)
    candidates.sort(key=lambda x:x[0],reverse=True)
    _,_,best_low,best_date=candidates[0]
    after=hist[hist.index>=best_date]; anchor_high=round(float(after["High"].max()),2)
    anchor_high_date=after["High"].idxmax()
    return (round(best_low,2), best_date.date() if hasattr(best_date,"date") else best_date,
            anchor_high, anchor_high_date.date() if hasattr(anchor_high_date,"date") else anchor_high_date)

def _sq9_levels(price):
    if price<=0: return []
    root=math.sqrt(price); levels=[]
    for offset in [-2,-1.5,-1,-0.5,0.5,1,1.5,2,2.5,3]:
        new_root=root+offset
        if new_root<=0: continue
        lv_price=round(new_root**2,2); spoke="Cardinal" if offset==round(offset) else "Diagonal"
        direction="Support" if offset<0 else "Resistance"; step_label=f"{'+' if offset>0 else ''}{offset}"
        levels.append((f"{direction} ({step_label} {spoke})",lv_price,spoke))
    return sorted(levels,key=lambda x:x[1])

def _time_cycle_confluence(anchor_low_date, today):
    days_from_low=max((today-anchor_low_date).days,0); window=5
    n=int(math.sqrt(days_from_low)); sq_prev=n*n; sq_next=(n+1)*(n+1)
    days_to_sq=sq_next-days_from_low
    t1_next=anchor_low_date+timedelta(days=sq_next); t1_prev=anchor_low_date+timedelta(days=sq_prev)
    t1_upcoming=t1_next if days_to_sq>0 else t1_prev; tool1_active=abs((today-t1_upcoming).days)<=window
    gann_divs=[45,90,135,144,180,225,270,315,360,450,504,720]
    t2_dates=[]
    for base in gann_divs:
        mult=1
        while True:
            d=base*mult; dt=anchor_low_date+timedelta(days=d)
            if dt>=today-timedelta(days=window): t2_dates.append(dt); break
            mult+=1
            if d>days_from_low+720: break
    t2_next=min(t2_dates,key=lambda dt:abs((dt-today).days)) if t2_dates else today+timedelta(days=90)
    tool2_active=any(abs((today-dt).days)<=window for dt in t2_dates)
    nearest_div=min(gann_divs,key=lambda d:abs(days_from_low%d) if d>0 else 9999)
    days_to_div=nearest_div-(days_from_low%nearest_div) if nearest_div>0 else 9999
    t3_upcoming=None; tool3_active=False
    for yr in range(1,15):
        try:
            anniv=anchor_low_date.replace(year=anchor_low_date.year+yr); days_away=(anniv-today).days
            if -window<=days_away<=window: tool3_active=True; t3_upcoming=anniv; break
            if 0<days_away<=365:
                if t3_upcoming is None or days_away<(t3_upcoming-today).days: t3_upcoming=anniv
        except Exception: pass
    if t3_upcoming is None:
        try: t3_upcoming=anchor_low_date.replace(year=today.year+1)
        except Exception: t3_upcoming=today+timedelta(days=365)
    seasonal=[date(today.year,3,20),date(today.year,6,21),date(today.year,9,22),date(today.year,12,21),
              date(today.year+1,3,20),date(today.year+1,6,21)]
    tool4_active=any(abs((today-sd).days)<=window for sd in seasonal)
    valid_s=[sd for sd in seasonal if sd>=today-timedelta(days=window)]
    t4_upcoming=min(valid_s,key=lambda d:abs((d-today).days)) if valid_s else seasonal[-1]
    upcoming={"sq":t1_upcoming,"div":t2_next,"anniv":t3_upcoming,"seasonal":t4_upcoming}
    active_flags={"sq":tool1_active,"div":tool2_active,"anniv":tool3_active,"seasonal":tool4_active}
    same_window_pairs=0; pair_labels=[]; keys=list(upcoming.keys())
    for i in range(len(keys)):
        for j in range(i+1,len(keys)):
            k1,k2=keys[i],keys[j]
            if active_flags[k1] and active_flags[k2]:
                delta=abs((upcoming[k1]-upcoming[k2]).days)
                if delta<=window*2: same_window_pairs+=1; pair_labels.append(f"{k1}+{k2} within {delta}d")
    total_active=sum(active_flags.values())
    if same_window_pairs>=3 or (same_window_pairs>=2 and total_active>=3): active_tools=3
    elif same_window_pairs>=1 and total_active>=2: active_tools=2
    elif total_active>=2: active_tools=1
    else: active_tools=0
    details={"tool1_active":tool1_active,"tool2_active":tool2_active,"tool3_active":tool3_active,"tool4_active":tool4_active,
             "active_tools":active_tools,"same_window_pairs":same_window_pairs,"pair_labels":pair_labels,
             "days_to_sq":days_to_sq,"sq_prev":sq_prev,"sq_next":sq_next,"nearest_div":nearest_div,"days_to_div":days_to_div,
             "next_sq_date":t1_upcoming,"next_div_date":t2_next,"next_anniv_date":t3_upcoming,"next_seasonal_date":t4_upcoming,
             "days_from_low":days_from_low}
    return active_tools, details

def compute_gann_confluence(data, symbol=None):
    price=data["price"]; today=datetime.now().date()
    long_hist=fetch_long_history(symbol) if symbol else None
    hist=long_hist if (long_hist is not None and not long_hist.empty) else data.get("hist")
    if hist is not None and len(hist)>=50:
        anchor_result=_find_significant_anchor(hist)
        if anchor_result: anchor_low,anchor_low_date,anchor_high,anchor_high_date=anchor_result
        else:
            anchor_low=round(float(hist["Low"].min()),2); anchor_high=round(float(hist["High"].max()),2)
            low_idx=hist["Low"].idxmin(); high_idx=hist["High"].idxmax()
            anchor_low_date=low_idx.date() if hasattr(low_idx,"date") else low_idx
            anchor_high_date=high_idx.date() if hasattr(high_idx,"date") else high_idx
        hl_range=round(anchor_high-anchor_low,2)
    else:
        anchor_low=round(price*0.72,2); anchor_high=round(price*1.22,2)
        anchor_low_date=today-timedelta(days=500); anchor_high_date=today-timedelta(days=90); hl_range=round(anchor_high-anchor_low,2)
    if isinstance(anchor_low_date,datetime): anchor_low_date=anchor_low_date.date()
    if isinstance(anchor_high_date,datetime): anchor_high_date=anchor_high_date.date()
    days_from_low=max((today-anchor_low_date).days,1); days_from_high=max((today-anchor_high_date).days,0)
    price_range=max(anchor_high-anchor_low,1.0); time_range=max(days_from_low,1)
    scale=round(price_range/time_range,4)
    angle_4x1=round(anchor_low+days_from_low*scale*4,2); angle_2x1=round(anchor_low+days_from_low*scale*2,2)
    angle_1x1=round(anchor_low+days_from_low*scale*1,2); angle_1x2=round(anchor_low+days_from_low*scale*0.5,2)
    angle_1x4=round(anchor_low+days_from_low*scale*0.25,2)
    angles={"4×1":angle_4x1,"2×1":angle_2x1,"1×1":angle_1x1,"1×2":angle_1x2,"1×4":angle_1x4}
    closest_angle=min(angles,key=lambda k:abs(angles[k]-price)); price_vs_1x1=(price-angle_1x1)/max(angle_1x1,1)*100
    if price>=angle_2x1: angle_label="Above 2×1 (Very Strong Bull)"; angle_color="#10b981"
    elif price>=angle_1x1: angle_label="1×1–2×1 (Bull Zone)"; angle_color="#10b981"
    elif price>=angle_1x2: angle_label="1×2–1×1 (Weak / Caution)"; angle_color="#f59e0b"
    else: angle_label="Below 1×2 (Bear)"; angle_color="#ef4444"
    sq9_all=_sq9_levels(price)
    sq9_sup=[(l,p2,s) for l,p2,s in sq9_all if p2<price]; sq9_res=[(l,p2,s) for l,p2,s in sq9_all if p2>price]
    sq9_s1=sq9_sup[-1] if sq9_sup else ("—",price,"—"); sq9_s2=sq9_sup[-2] if len(sq9_sup)>=2 else sq9_s1
    sq9_r1=sq9_res[0] if sq9_res else ("—",price,"—"); sq9_r2=sq9_res[1] if len(sq9_res)>=2 else sq9_r1
    gann_t1=sq9_r1[1]; gann_t2=sq9_r2[1]; gann_sl=sq9_s2[1]
    sq_display=[["⚪ Current",price,"—"]]+[[f"🔴 {l}",p2,s] for l,p2,s in sq9_sup[-3:]]+[[f"🟢 {l}",p2,s] for l,p2,s in sq9_res[:3]]
    sq_display=sorted(sq_display,key=lambda x:x[1])
    active_tools,cycle_details=_time_cycle_confluence(anchor_low_date,today)
    sqrt_days=round(math.sqrt(days_from_low),4); n_low=int(sqrt_days); nearest_sq=n_low*n_low; next_sq=(n_low+1)*(n_low+1); days_to_next=next_sq-days_from_low
    sq9_prices=[p2 for _,p2,_ in sq9_all]; nearest_sq9_price=min(sq9_prices,key=lambda x:abs(x-price)) if sq9_prices else price
    price_sq9_dev=abs(nearest_sq9_price-price)/max(price,0.01)*100
    at_sq9_tight=price_sq9_dev<=0.5; at_sq9_moderate=price_sq9_dev<=1.5; at_1x1=abs(price-angle_1x1)/max(price,0.01)*100<=1.0
    time_strong=active_tools>=3; time_moderate=active_tools>=2
    confluence=0; reasons=[]
    if at_sq9_tight and at_1x1 and time_strong: confluence=5; reasons.append("🔥 TIER 1: Sq9 tight + 1×1 + 3/3 time")
    elif (at_sq9_tight or at_sq9_moderate) and time_strong: confluence=4; reasons.append("✅ TIER 2: Sq9 + strong time")
    elif at_sq9_tight and (at_1x1 or time_moderate): confluence=4; reasons.append("✅ TIER 2: Sq9 tight + angle/time")
    elif at_sq9_moderate and time_moderate: confluence=3; reasons.append("✅ TIER 3: Sq9 moderate + 2/3 time")
    elif at_sq9_moderate or time_moderate or at_1x1: confluence=2; reasons.append("⚡ TIER 4: Single confluence")
    else: confluence=1; reasons.append("⚪ No meaningful confluence")
    reasons.append(f"   Sq9 nearest ₹{nearest_sq9_price:,.2f} · dev {price_sq9_dev:.2f}%")
    reasons.append(f"   1×1 ₹{angle_1x1:,.2f} · dev {abs(price_vs_1x1):.1f}%")
    sw=cycle_details["same_window_pairs"]; pi=" · ".join(cycle_details["pair_labels"]) if cycle_details["pair_labels"] else "no pairs"
    reasons.append(f"   Time tools: {active_tools}/3 · Same-window: {sw} ({pi})")
    gann_time_units=[45,90,135,144,180,225,270,315,360,450,504,720]; gann_future=[]
    for t in gann_time_units:
        fd=anchor_low_date+timedelta(days=t)
        if fd>=today: gann_future.append((t,fd,(fd-today).days))
        if len(gann_future)>=6: break
    sq_dates=[]; n_start=int(math.sqrt(days_from_low))+1
    for i in range(n_start,n_start+6):
        d=i*i; sd=anchor_low_date+timedelta(days=d)
        if sd>=today: sq_dates.append((d,sd,(sd-today).days,i))
    anniv_dates=[]
    for yr in [1,2,3,5,7,10]:
        try:
            ad=anchor_low_date.replace(year=anchor_low_date.year+yr)
            if ad>=today: anniv_dates.append((yr,ad,(ad-today).days))
        except Exception: pass
    scaled_time=days_from_low*scale; squaring_pct=round(abs(price-scaled_time)/max(price,0.01)*100,1); is_squared=squaring_pct<3.0
    anchor_sq9_root=round(math.sqrt(max(anchor_low,0.01)),4); range_sqrt=round(math.sqrt(max(hl_range,0.01)),4)
    range_sq_target=round((math.ceil(range_sqrt)+1)**2,2); active_cycle=next((t for t in gann_time_units if days_from_low<=t),720)
    return (confluence,angle_label,angle_color,is_squared,squaring_pct,
            dict(anchor_low=anchor_low,anchor_high=anchor_high,anchor_low_date=anchor_low_date,anchor_high_date=anchor_high_date,
                 days_from_low=days_from_low,days_from_high=days_from_high,hl_range=hl_range,scale=scale,
                 angle_4x1=angle_4x1,angle_2x1=angle_2x1,angle_1x1=angle_1x1,angle_1x2=angle_1x2,angle_1x4=angle_1x4,
                 closest_angle=closest_angle,price_vs_1x1=round(price_vs_1x1,1),
                 sq9_root=round(math.sqrt(max(price,0.01)),4),sq9_s1=sq9_s1,sq9_s2=sq9_s2,sq9_r1=sq9_r1,sq9_r2=sq9_r2,
                 nearest_sq9_price=nearest_sq9_price,price_sq9_dev=price_sq9_dev,sq_levels=sq_display,
                 gann_t1=gann_t1,gann_t2=gann_t2,gann_sl=gann_sl,
                 sqrt_days=sqrt_days,n_low=n_low,nearest_sq=nearest_sq,next_sq=next_sq,days_to_next=days_to_next,
                 cycle_details=cycle_details,active_tools=active_tools,
                 gann_future=gann_future,sq_dates=sq_dates,anniv_dates=anniv_dates,
                 scaled_time=round(scaled_time,2),anchor_sq9_root=anchor_sq9_root,
                 range_sqrt=range_sqrt,range_sq_target=range_sq_target,active_cycle=active_cycle,reasons=reasons))

# ══════════════════════════════════════════════════════════════════════════════
# INDEX-SPECIFIC GANN HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def _get_all_anchors(hist):
    """Compute 3 anchor strategies from index history."""
    if hist is None or len(hist)<50: return {}
    anchors = {}
    # Strategy 1: Deepest swing low (most significant)
    anchor1 = _find_significant_anchor(hist)
    if anchor1:
        anchors["Deepest Significant Low"] = dict(
            anchor_low=anchor1[0], anchor_low_date=anchor1[1],
            anchor_high=anchor1[2], anchor_high_date=anchor1[3])
    # Strategy 2: Most recent major swing low (within last 2 years)
    two_yr_ago = hist.index[-1] - pd.Timedelta(days=730)
    recent = hist[hist.index >= two_yr_ago]
    if len(recent) >= 50:
        anchor2 = _find_significant_anchor(recent)
        if anchor2:
            anchors["Recent Major Low (2Y)"] = dict(
                anchor_low=anchor2[0], anchor_low_date=anchor2[1],
                anchor_high=anchor2[2], anchor_high_date=anchor2[3])
    # Strategy 3: Absolute all-time low
    if len(hist) >= 100:
        idx = hist["Low"].idxmin()
        al = round(float(hist["Low"].min()), 2)
        ald = idx.date() if hasattr(idx, "date") else idx
        after = hist[hist.index >= idx]
        ah = round(float(after["High"].max()), 2)
        ahd = after["High"].idxmax()
        ahd = ahd.date() if hasattr(ahd, "date") else ahd
        anchors["All-Time Low"] = dict(anchor_low=al, anchor_low_date=ald, anchor_high=ah, anchor_high_date=ahd)
    return anchors

def _compute_gann_from_anchor(price, anchor_low, anchor_low_date, anchor_high, hist, anchor_high_date=None):
    """Pure-math Gann computation from a chosen anchor. No network calls."""
    today = datetime.now().date()
    if isinstance(anchor_low_date, datetime): anchor_low_date = anchor_low_date.date()
    if anchor_high_date and isinstance(anchor_high_date, datetime): anchor_high_date = anchor_high_date.date()
    days_from_low = max((today - anchor_low_date).days, 1)
    price_range = max(anchor_high - anchor_low, 1.0)
    scale = round(price_range / days_from_low, 4)
    angle_4x1 = round(anchor_low + days_from_low * scale * 4, 2)
    angle_2x1 = round(anchor_low + days_from_low * scale * 2, 2)
    angle_1x1 = round(anchor_low + days_from_low * scale * 1, 2)
    angle_1x2 = round(anchor_low + days_from_low * scale * 0.5, 2)
    angle_1x4 = round(anchor_low + days_from_low * scale * 0.25, 2)
    angles = {"4×1": angle_4x1, "2×1": angle_2x1, "1×1": angle_1x1, "1×2": angle_1x2, "1×4": angle_1x4}
    closest_angle = min(angles, key=lambda k: abs(angles[k] - price))
    price_vs_1x1 = (price - angle_1x1) / max(angle_1x1, 1) * 100
    if price >= angle_2x1: angle_label = "Above 2×1 (Very Strong Bull)"; angle_color = "#10b981"
    elif price >= angle_1x1: angle_label = "1×1–2×1 (Bull Zone)"; angle_color = "#10b981"
    elif price >= angle_1x2: angle_label = "1×2–1×1 (Weak / Caution)"; angle_color = "#f59e0b"
    else: angle_label = "Below 1×2 (Bear)"; angle_color = "#ef4444"
    sq9_all = _sq9_levels(price)
    sq9_sup = [(l, p2, s) for l, p2, s in sq9_all if p2 < price]
    sq9_res = [(l, p2, s) for l, p2, s in sq9_all if p2 > price]
    sq9_s1 = sq9_sup[-1] if sq9_sup else ("—", price, "—")
    sq9_s2 = sq9_sup[-2] if len(sq9_sup) >= 2 else sq9_s1
    sq9_r1 = sq9_res[0] if sq9_res else ("—", price, "—")
    sq9_r2 = sq9_res[1] if len(sq9_res) >= 2 else sq9_r1
    active_tools, cycle_details = _time_cycle_confluence(anchor_low_date, today)
    sq9_prices = [p2 for _, p2, _ in sq9_all]
    nearest_sq9 = min(sq9_prices, key=lambda x: abs(x - price)) if sq9_prices else price
    price_sq9_dev = abs(nearest_sq9 - price) / max(price, 0.01) * 100
    at_sq9_tight = price_sq9_dev <= 0.5; at_sq9_moderate = price_sq9_dev <= 1.5
    at_1x1 = abs(price - angle_1x1) / max(price, 0.01) * 100 <= 1.0
    time_strong = active_tools >= 3; time_moderate = active_tools >= 2
    confluence = 0; reasons = []
    if at_sq9_tight and at_1x1 and time_strong: confluence = 5; reasons.append("🔥 TIER 1")
    elif (at_sq9_tight or at_sq9_moderate) and time_strong: confluence = 4; reasons.append("✅ TIER 2")
    elif at_sq9_tight and (at_1x1 or time_moderate): confluence = 4; reasons.append("✅ TIER 2")
    elif at_sq9_moderate and time_moderate: confluence = 3; reasons.append("✅ TIER 3")
    elif at_sq9_moderate or time_moderate or at_1x1: confluence = 2; reasons.append("⚡ TIER 4")
    else: confluence = 1; reasons.append("⚪ No confluence")
    reasons.append(f"   Sq9 dev {price_sq9_dev:.2f}% · 1×1 dev {abs(price_vs_1x1):.1f}% · Time {active_tools}/3")
    scaled_time = days_from_low * scale
    squaring_pct = round(abs(price - scaled_time) / max(price, 0.01) * 100, 1)
    is_squared = squaring_pct < 3.0
    gann_time_units = [45, 90, 135, 144, 180, 225, 270, 315, 360, 450, 504, 720]
    gann_future = []
    for t in gann_time_units:
        fd = anchor_low_date + timedelta(days=t)
        if fd >= today: gann_future.append((t, fd, (fd - today).days))
        if len(gann_future) >= 6: break
    return dict(
        anchor_low=anchor_low, anchor_high=anchor_high, anchor_low_date=anchor_low_date,
        days_from_low=days_from_low, scale=scale, hl_range=round(anchor_high-anchor_low,2),
        angle_4x1=angle_4x1, angle_2x1=angle_2x1, angle_1x1=angle_1x1, angle_1x2=angle_1x2, angle_1x4=angle_1x4,
        closest_angle=closest_angle, price_vs_1x1=round(price_vs_1x1,1),
        angle_label=angle_label, angle_color=angle_color,
        sq9_root=round(math.sqrt(max(price,0.01)),4),
        sq9_s1=sq9_s1, sq9_s2=sq9_s2, sq9_r1=sq9_r1, sq9_r2=sq9_r2,
        nearest_sq9=nearest_sq9, price_sq9_dev=price_sq9_dev,
        gann_t1=sq9_r1[1], gann_t2=sq9_r2[1], gann_sl=sq9_s2[1],
        confluence=confluence, reasons=reasons,
        active_tools=active_tools, cycle_details=cycle_details,
        is_squared=is_squared, squaring_pct=squaring_pct, scaled_time=round(scaled_time,2),
        gann_future=gann_future,
    )

def detect_reversal_candle(o, h, l, c, prev_c, direction="any"):
    """Detect common reversal candlestick patterns. Returns (name, strength, type) or None."""
    body = abs(c - o); total = h - l
    if total <= 0: return None
    body_ratio = body / total
    upper_wick = h - max(c, o); lower_wick = min(c, o) - l
    is_up = c > o; is_down = c < o
    # Hammer (bullish)
    if lower_wick >= body * 2 and upper_wick <= body * 0.5 and body_ratio < 0.4:
        if direction in ("any", "bull"): return ("Hammer", 2, "bull")
    # Inverted hammer (bullish)
    if upper_wick >= body * 2 and lower_wick <= body * 0.5 and body_ratio < 0.4:
        if direction in ("any", "bull"): return ("Inv Hammer", 1, "bull")
    # Shooting star (bearish)
    if upper_wick >= body * 2 and lower_wick <= body * 0.5 and body_ratio < 0.4 and is_down:
        if direction in ("any", "bear"): return ("Shooting Star", 2, "bear")
    # Doji
    if body_ratio < 0.1:
        return ("Doji", 2, "neutral")
    # Bullish engulfing
    prev_body = abs(prev_c - o)
    if is_up and c > prev_c and o < prev_c and body > prev_body * 1.2:
        if direction in ("any", "bull"): return ("Bull Engulf", 3, "bull")
    # Bearish engulfing
    if is_down and c < prev_c and o > prev_c and body > prev_body * 1.2:
        if direction in ("any", "bear"): return ("Bear Engulf", 3, "bear")
    return None

def _build_forecast_table(price, gd, timeframe_opt, days_forward):
    """Build forward forecast with bull/bear angle fans + time cycle events."""
    anchor_low = gd["anchor_low"]; anchor_low_date = gd["anchor_low_date"]
    anchor_high = gd["anchor_high"]; scale = gd["scale"]; today = datetime.now().date()
    # Sq9 levels for current price
    sq9_all = _sq9_levels(price)
    sq9_res = sorted([p2 for _, p2, _ in sq9_all if p2 > price])
    sq9_sup = sorted([p2 for _, p2, _ in sq9_all if p2 < price], reverse=True)
    sq9_r1 = sq9_res[0] if sq9_res else price * 1.02
    sq9_r2 = sq9_res[1] if len(sq9_res) >= 2 else sq9_r1
    sq9_s1 = sq9_sup[0] if sq9_sup else price * 0.98
    sq9_s2 = sq9_sup[1] if len(sq9_sup) >= 2 else sq9_s1
    # Zone classification
    bull_1x1_now = gd["angle_1x1"]
    # Bear 1×1 from anchor high (descending)
    days_from_high = max((today - gd.get("anchor_high_date", today - timedelta(days=365))).days, 1) if gd.get("anchor_high_date") else days_forward
    bear_1x1_now = anchor_high - days_from_high * scale
    if price > bull_1x1_now:
        zone = "STRONG_BULL"
    elif price < bear_1x1_now:
        zone = "BEAR"
    else:
        zone = "CAUTION"
    # Collect time events for each future day
    gann_divs = [45, 90, 135, 144, 180, 225, 270, 315, 360, 450, 504, 720]
    seasonal_months = [(3, 20), (6, 21), (9, 22), (12, 21)]
    rows = []
    for d in range(1, days_forward + 1):
        future_date = today + timedelta(days=d)
        total_days = gd["days_from_low"] + d
        events = []
        # Natural squares
        sqrt_val = math.sqrt(total_days)
        if abs(sqrt_val - round(sqrt_val)) < 0.05:
            events.append(f"Square {round(sqrt_val)}²={total_days}")
        # Gann divisions
        for div in gann_divs:
            if total_days % div == 0:
                events.append(f"Gann {div}d (×{total_days//div})")
        # Anniversaries
        try:
            for yr in range(1, 15):
                anniv = anchor_low_date.replace(year=anchor_low_date.year + yr)
                if anniv == future_date:
                    events.append(f"Anniv {yr}yr")
                    break
        except Exception:
            pass
        # Seasonal
        for m, s_day in seasonal_months:
            if future_date.month == m and future_date.day == s_day:
                events.append("Seasonal")
        # Time confluence score
        n_events = len(events)
        if n_events >= 3: time_cs = 3
        elif n_events >= 2: time_cs = 2
        elif n_events >= 1: time_cs = 1
        else: time_cs = 0
        if time_cs == 0: continue  # skip days with no time events
        # Compute Sq9 levels for each future day's approximate price
        # Bull 1×1 on this date
        bull_1x1_on_date = anchor_low + total_days * scale
        # Bear 1×1 from anchor high on this date
        days_from_high_f = total_days - (days_from_high - gd["days_from_low"]) if days_from_high > 0 else total_days
        bear_1x1_on_date = anchor_high - max(days_from_high_f, 0) * scale if days_from_high_f > 0 else None
        # Primary direction
        primary_dir = "Bull" if zone != "BEAR" else "Bear"
        rows.append(dict(
            date=future_date, days_away=d, events=events, n_events=n_events,
            time_cs=time_cs, time_conf="HIGH" if time_cs>=3 else "MOD" if time_cs>=2 else "LOW",
            bull_1x1_on_date=round(bull_1x1_on_date, 2),
            bear_1x1_on_date=round(bear_1x1_on_date, 2) if bear_1x1_on_date else None,
            primary_dir=primary_dir,
            sq9_r1=sq9_r1, sq9_r2=sq9_r2, sq9_s1=sq9_s1, sq9_s2=sq9_s2,
        ))
    return rows, zone, sq9_r1, sq9_r2, sq9_s1, sq9_s2

def _build_gann_verdict(price, gd, forecast_rows, zone, sq9_r1, sq9_r2, sq9_s1, sq9_s2):
    """Extract key verdicts from forecast rows."""
    verdicts = []
    for row in forecast_rows:
        if row["time_cs"] < 2: continue  # Only MODERATE+ and HIGH
        watch_price = row["sq9_r1"] if zone != "BEAR" else row["sq9_s1"]
        diff_pct = round((watch_price - price) / price * 100, 2)
        if zone == "STRONG_BULL":
            dir_lbl = "📈 Watch for resistance / reaction"
            col = "#10b981"
        elif zone == "BEAR":
            dir_lbl = "📉 Watch for support / bounce"
            col = "#ef4444"
        else:
            dir_lbl = "⚡ Watch for reaction (either direction)"
            col = "#f59e0b"
        verdicts.append(dict(
            date=row["date"], days_away=row["days_away"],
            watch_price=watch_price, diff_pct=diff_pct,
            dir_lbl=dir_lbl, col=col,
            events=" + ".join(row["events"]),
            time_cs=row["time_cs"], zone=zone,
        ))
    verdicts.sort(key=lambda x: (x["time_cs"], x["days_away"]), reverse=True)
    return verdicts[:10]

def _backtest_proper(hist, gd, lookback_days=730):
    """3-layer backtest: raw hit rate, Sq9 filtered, candle confirmed."""
    if hist is None or len(hist) < 100: return None
    today = datetime.now().date()
    anchor_low = gd["anchor_low"]; anchor_low_date = gd["anchor_low_date"]; scale = gd["scale"]
    cutoff = today - timedelta(days=lookback_days)
    hist_cut = hist[hist.index >= pd.Timestamp(cutoff)]
    if len(hist_cut) < 50: return None
    gann_divs = [45, 90, 135, 144, 180, 225, 270, 315, 360]
    results = []
    for i in range(20, len(hist_cut) - 5):
        row_date = hist_cut.index[i].date() if hasattr(hist_cut.index[i], "date") else hist_cut.index[i]
        days_from = (row_date - anchor_low_date).days
        if days_from <= 0: continue
        # Count time events
        events = []
        sqrt_val = math.sqrt(days_from)
        if abs(sqrt_val - round(sqrt_val)) < 0.05: events.append(f"sq{round(sqrt_val)}")
        for div in gann_divs:
            if days_from % div == 0: events.append(f"{div}d")
        try:
            for yr in [1, 2, 3, 5, 7]:
                anniv = anchor_low_date.replace(year=anchor_low_date.year + yr)
                if anniv == row_date: events.append(f"ann{yr}"); break
        except Exception: pass
        if len(events) < 2: continue  # Only HIGH-confidence signals
        sig_close = float(hist_cut["Close"].iloc[i])
        # Sq9 proximity
        sq9_all = _sq9_levels(sig_close)
        sq9_prices = [p2 for _, p2, _ in sq9_all]
        nearest_sq9 = min(sq9_prices, key=lambda x: abs(x - sig_close)) if sq9_prices else sig_close
        sq9_dev_pct = round(abs(nearest_sq9 - sig_close) / max(sig_close, 0.01) * 100, 2)
        at_sq9 = sq9_dev_pct <= 1.0
        # Candle pattern
        o = float(hist_cut["Open"].iloc[i]); h = float(hist_cut["High"].iloc[i])
        l = float(hist_cut["Low"].iloc[i]); c = float(hist_cut["Close"].iloc[i])
        prev_c = float(hist_cut["Close"].iloc[i - 1])
        candle = detect_reversal_candle(o, h, l, c, prev_c, "any")
        candle_str = f"{candle[0]} ({candle[2]})" if candle else "None"
        # Check 3-day move
        max_rev = 0; net_move = 0; turned = False
        for j in range(1, min(4, len(hist_cut) - i)):
            future_c = float(hist_cut["Close"].iloc[i + j])
            future_h = float(hist_cut["High"].iloc[i + j])
            future_l = float(hist_cut["Low"].iloc[i + j])
            reversal_up = (future_h - sig_close) / max(sig_close, 0.01) * 100
            reversal_dn = (sig_close - future_l) / max(sig_close, 0.01) * 100
            max_rev = max(max_rev, reversal_up, reversal_dn)
            net_move = (future_c - sig_close) / max(sig_close, 0.01) * 100
            if max_rev >= 1.5: turned = True
        results.append(dict(date=row_date, events=events, sig_close=sig_close,
                            nearest_sq9=nearest_sq9, sq9_dev_pct=sq9_dev_pct, at_sq9=at_sq9,
                            candle=candle, candle_str=candle_str,
                            turned=turned, reversal_pct=round(max_rev, 2),
                            net_move_pct=round(net_move, 2)))
    if not results: return dict(total=0)
    hits = [r for r in results if r["turned"]]
    sq9_total = sum(1 for r in results if r["at_sq9"])
    sq9_hits = [r for r in results if r["at_sq9"] and r["turned"]]
    conf_total = sum(1 for r in results if r["at_sq9"] and r["candle"] is not None)
    conf_hits = [r for r in results if r["at_sq9"] and r["candle"] is not None and r["turned"]]
    avg_rev = round(sum(r["reversal_pct"] for r in hits) / max(len(hits), 1), 2)
    return dict(total=len(results), hits=hits, hit_rate=round(len(hits)/max(len(results),1)*100,1),
                sq9_total=sq9_total, sq9_hits=sq9_hits, sq9_hit_rate=round(len(sq9_hits)/max(sq9_total,1)*100,1),
                conf_total=conf_total, conf_hits=conf_hits, conf_hit_rate=round(len(conf_hits)/max(conf_total,1)*100,1),
                avg_reversal=avg_rev, results=results)

def _build_index_gann_chart(hist, gd, price, label, forecast_rows=None):
    """Build Plotly chart with candlestick + angle fans + optional forecast markers."""
    if hist is None or len(hist) < 10: return None
    anchor_low = gd["anchor_low"]; anchor_low_date = gd["anchor_low_date"]; scale = gd["scale"]
    anchor_high = gd["anchor_high"]
    anchor_dt = pd.Timestamp(anchor_low_date)
    hist_after = hist[hist.index >= anchor_dt].copy()
    if hist_after.empty: return None
    dates_arr = hist_after.index.tolist()
    close_arr = hist_after["Close"].tolist(); high_arr = hist_after["High"].tolist(); low_arr = hist_after["Low"].tolist()
    days_arr = [(idx - anchor_dt).days for idx in dates_arr]
    if not days_arr: return None
    max_days = max(days_arr); proj_days = int(max_days * 1.05) + 1
    # Build date array for projections
    proj_dates = [anchor_dt + timedelta(days=d) for d in range(0, proj_days)]
    proj_days_arr = list(range(0, proj_days))
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=dates_arr, open=hist_after["Open"].tolist(), high=high_arr, low=low_arr, close=close_arr,
                                  name="Price", increasing_line_color="#10b981", decreasing_line_color="#ef4444", showlegend=False))
    # Bull angles from anchor low
    angle_specs = [(scale*4,"4×1","#ef4444","dash"),(scale*2,"2×1","#f59e0b","dash"),
                   (scale*1,"Bull 1×1","#10b981","solid"),(scale*0.5,"1×2","#f59e0b","dot"),(scale*0.25,"1×4","#ef4444","dot")]
    for rate,lbl,col,dash in angle_specs:
        y_vals = [anchor_low + d * rate for d in proj_days_arr]
        fig.add_trace(go.Scatter(x=proj_dates,y=y_vals,mode="lines",name=lbl,
                                  line=dict(color=col,width=1.5 if "1×1" in lbl else 1,dash=dash),opacity=0.7))
    # Bear 1×1 from anchor high
    ahd = gd.get("anchor_high_date")
    if ahd:
        if isinstance(ahd, datetime): ahd = ahd.date()
        days_from_high_start = max((anchor_dt.date() - ahd).days, 0) if hasattr(anchor_dt, 'date') else 0
        bear_y = [anchor_high - (days_from_high_start + d) * scale for d in proj_days_arr]
        fig.add_trace(go.Scatter(x=proj_dates,y=bear_y,mode="lines",name="Bear 1×1",
                                  line=dict(color="#ef4444",width=1.5,dash="solid"),opacity=0.7))
    # Forecast markers
    if forecast_rows:
        fx = [anchor_dt + timedelta(days=gd["days_from_low"] + r["days_away"]) for r in forecast_rows if r["time_cs"] >= 2]
        fy = [price for _ in fx]
        if fx:
            fig.add_trace(go.Scatter(x=fx,y=fy,mode="markers",name="Forecast",
                                      marker=dict(color="#f59e0b",size=10,symbol="diamond"),opacity=0.9))
    # Current price line
    fig.add_hline(y=price,line_color="#ffffff",line_width=1,line_dash="solid",opacity=0.7,
                   annotation_text=f"₹{price:,.2f}",annotation_font_size=10,annotation_font_color="#ffffff")
    fig.update_layout(height=520,paper_bgcolor="#060810",plot_bgcolor="#0d1117",
                       font=dict(family="Space Grotesk",color="#94a3b8",size=11),
                       title=dict(text=f"Gann Chart — {label} — Scale {scale:.4f} pts/day",font=dict(color="#f59e0b",size=13)),
                       xaxis=dict(title="Date",gridcolor="rgba(255,255,255,0.05)",color="#64748b"),
                       yaxis=dict(title="Price",gridcolor="rgba(255,255,255,0.05)",color="#64748b"),
                       legend=dict(orientation="h",yanchor="bottom",y=1.02,bgcolor="rgba(0,0,0,0)",font=dict(color="#94a3b8",size=10)),
                       xaxis_rangeslider_visible=False,margin=dict(l=60,r=40,t=60,b=40))
    return fig

def _build_gann_chart(hist, anchor_low, anchor_low_date, anchor_high,
                      scale, angle_1x1, angle_2x1, angle_1x2, angle_1x4,
                      sq9_levels, price, today):
    if hist is None or len(hist) < 10: return None
    anchor_dt = pd.Timestamp(anchor_low_date)
    hist_after = hist[hist.index >= anchor_dt].copy()
    if hist_after.empty: return None
    days_arr = [(idx - anchor_dt).days for idx in hist_after.index]
    close_arr = hist_after["Close"].tolist(); high_arr = hist_after["High"].tolist(); low_arr = hist_after["Low"].tolist()
    if not days_arr: return None
    max_days = max(days_arr); proj_days = int(max_days * 1.20) + 1
    angle_x = list(range(0, proj_days, 1))
    def angle_y(rate): return [anchor_low + d * rate for d in angle_x]
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=days_arr,open=hist_after["Open"].tolist(),high=high_arr,low=low_arr,close=close_arr,
                                  name="Price",increasing_line_color="#10b981",decreasing_line_color="#ef4444",showlegend=False))
    angle_specs = [(scale*4,"4×1","#ef4444","dash"),(scale*2,"2×1","#f59e0b","dash"),
                   (scale*1,"1×1","#10b981","solid"),(scale*0.5,"1×2","#f59e0b","dot"),(scale*0.25,"1×4","#ef4444","dot")]
    for rate,lbl,col,dash in angle_specs:
        fig.add_trace(go.Scatter(x=angle_x,y=angle_y(rate),mode="lines",name=lbl,
                                  line=dict(color=col,width=1.5 if lbl=="1×1" else 1,dash=dash),opacity=0.8))
    for lv in sq9_levels:
        lbl,lv_price,spoke=lv
        if not isinstance(lv_price,(int,float)): continue
        col="#3b82f6" if "Resistance" in lbl else "#8b5cf6" if "Support" in lbl else "#ffffff"
        fig.add_hline(y=lv_price,line_color=col,line_width=0.7,line_dash="dot",opacity=0.5,
                       annotation_text=f"₹{lv_price:,.0f}",annotation_font_size=9,annotation_font_color=col)
    fig.add_hline(y=price,line_color="#ffffff",line_width=1,line_dash="solid",opacity=0.9,
                   annotation_text=f"₹{price:,.2f}",annotation_font_size=10,annotation_font_color="#ffffff")
    fig.add_trace(go.Scatter(x=[0],y=[anchor_low],mode="markers+text",
                              marker=dict(color="#f59e0b",size=10,symbol="triangle-up"),
                              text=["Anchor"],textposition="bottom center",textfont=dict(color="#f59e0b",size=10),
                              name="Anchor Low",showlegend=False))
    fig.update_layout(height=520,paper_bgcolor="#060810",plot_bgcolor="#0d1117",
                       font=dict(family="Space Grotesk",color="#94a3b8",size=11),
                       title=dict(text=f"Gann Scaled Chart — 1 unit time = {scale:.4f} pts price",font=dict(color="#f59e0b",size=13)),
                       xaxis=dict(title="Days from Anchor Low",gridcolor="rgba(255,255,255,0.05)",color="#64748b"),
                       yaxis=dict(title="Price (₹)",gridcolor="rgba(255,255,255,0.05)",color="#64748b"),
                       legend=dict(orientation="h",yanchor="bottom",y=1.02,bgcolor="rgba(0,0,0,0)",font=dict(color="#94a3b8",size=10)),
                       xaxis_rangeslider_visible=False,margin=dict(l=60,r=40,t=60,b=40))
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# GANN INDEX SCANNER
# ══════════════════════════════════════════════════════════════════════════════
def run_gann_scan(symbols):
    results=[]; progress=st.progress(0,text="Initializing…"); total=len(symbols)
    for idx,sym in enumerate(symbols):
        progress.progress(int((idx+1)/total*100),text=f"Scanning {idx+1}/{total}: {sym}")
        try:
            data=fetch_stock_data(sym); tech=compute_technicals(data)
            ts,bull,bear=compute_tech_score(data,tech)
            gc,al,ac,isq,sp,gi=compute_gann_confluence(data,symbol=sym)
            tn=max(0,min(100,(ts+6)/14*100)); gn=max(0,min(100,(gc-1)/4*100))
            composite=round(tn*0.55+gn*0.45,1)
            results.append(dict(symbol=sym,name=data.get("name",sym),sector=data.get("sector","—"),
                                price=data["price"],change_pct=data["change_pct"],rsi=data["rsi"],pe=data["pe"],
                                tech_score=ts,gann_confluence=gc,angle_label=al,is_squared=isq,
                                squaring_pct=sp,active_tools=gi.get("active_tools",0),composite=composite,
                                gann_t1=gi.get("gann_t1",0),gann_sl=gi.get("gann_sl",0)))
        except Exception: continue
    progress.empty(); results.sort(key=lambda x:x["composite"],reverse=True); return results

def compute_verdict(tech_score, gann_confluence, data, tech, gann_info):
    tn=max(0,min(100,(tech_score+6)/14*100)); gn=max(0,min(100,(gann_confluence-1)/4*100))
    composite=round(tn*0.55+gn*0.45,1)
    if data["rsi"]>75: composite=max(0,composite-10)
    elif data["rsi"]<25: composite=min(100,composite+5)
    if composite>=70: return "STRONG BUY","vb-buy",composite
    elif composite>=55: return "BUY","vb-buy",composite
    elif composite>=40: return "CAUTION","vb-caution",composite
    elif composite>=25: return "AVOID","vb-avoid",composite
    else: return "STRONG AVOID","vb-avoid",composite

# ══════════════════════════════════════════════════════════════════════════════
# RENDER — SINGLE STOCK
# ══════════════════════════════════════════════════════════════════════════════
def render_analysis(symbol,data,tech,tech_score,bull,bear,gann_conf,angle_label,angle_color,is_squared,squaring_pct,gann_info,gann_chart):
    price=data["price"]
    kc=st.columns(7)
    with kc[0]: st.markdown(kpi("Price",f"₹{price:,.2f}","#e8edf5",data["name"]),unsafe_allow_html=True)
    with kc[1]: st.markdown(kpi("Change",f"{data['change_pct']:+.2f}%","#10b981" if data["change_pct"]>=0 else "#ef4444"),unsafe_allow_html=True)
    with kc[2]: st.markdown(kpi("RSI",f"{data['rsi']}","#10b981" if 40<=data["rsi"]<=70 else "#f59e0b"),unsafe_allow_html=True)
    with kc[3]: st.markdown(kpi("ATR%",f"{data['atr_pct']}%","#06b6d4"),unsafe_allow_html=True)
    with kc[4]: st.markdown(kpi("Beta",f"{data['beta']:.2f}","#8b5cf6"),unsafe_allow_html=True)
    with kc[5]: st.markdown(kpi("PE",f"{data['pe']}","#3b82f6"),unsafe_allow_html=True)
    with kc[6]: st.markdown(kpi("VolR",f"{tech['volr']}x","#10b981" if tech["volr"]>1 else "#64748b"),unsafe_allow_html=True)
    vt,vc,comp=compute_verdict(tech_score,gann_conf,data,tech,gann_info)
    st.markdown(f'<div class="verdict-banner {vc}"><span class="score-ring" style="color:inherit">{comp:.0f}</span>/100 &nbsp; {safe_html(vt)}</div>',unsafe_allow_html=True)
    tab_tech,tab_gann,tab_pivot,tab_sr=st.tabs(["📊 Technicals","🔷 Gann","📐 Pivots","🎯 S/R"])
    with tab_tech:
        sc="#10b981" if tech_score>0 else "#ef4444" if tech_score<0 else "#f59e0b"
        st.markdown(f'<div class="gc gc-{"green" if tech_score>0 else "red" if tech_score<0 else "gold"}"><div class="score-ring" style="color:{sc}">{tech_score:+d}</div>{pb(max(tech_score,0),8,sc)}</div>',unsafe_allow_html=True)
        if bull:
            st.markdown('<div class="sec-title">Bullish</div>',unsafe_allow_html=True)
            for b in bull: st.markdown(f'<div class="lc lc-green">{safe_html(b)}</div>',unsafe_allow_html=True)
        if bear:
            st.markdown('<div class="sec-title">Bearish</div>',unsafe_allow_html=True)
            for b in bear: st.markdown(f'<div class="lc lc-red">{safe_html(b)}</div>',unsafe_allow_html=True)
    with tab_gann:
        cc={5:"#10b981",4:"#10b981",3:"#f59e0b",2:"#f59e0b",1:"#64748b"}.get(gann_conf,"#64748b")
        cb={5:"green",4:"green",3:"gold",2:"gold",1:"blue"}.get(gann_conf,"blue")
        st.markdown(f'<div class="gc gc-{cb}"><div class="kpi-label">GANN CONFLUENCE</div><div class="score-ring" style="color:{cc}">{gann_conf}</div>/5{pb(gann_conf,5,cc)}</div>',unsafe_allow_html=True)
        for r in gann_info.get("reasons",[]):
            rc="lc-green" if "🔥" in r or "✅" in r else "lc-gold" if "⚡" in r else "lc-blue"
            st.markdown(f'<div class="lc {rc}">{safe_html(r)}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="lc lc-{"green" if "Bull" in angle_label else "red" if "Bear" in angle_label else "gold"}"><b style="color:{angle_color}">{safe_html(angle_label)}</b></div>',unsafe_allow_html=True)
        st.markdown(f'<div class="lc lc-{"green" if is_squared else "blue"}"><b>Price-Time {"SQUARED ⬢" if is_squared else "Not Squared"}</b> — dev {squaring_pct}%</div>',unsafe_allow_html=True)
        if gann_info.get("sq_levels"):
            st.dataframe(pd.DataFrame(gann_info["sq_levels"],columns=["Level","Price","Type"]),use_container_width=True,hide_index=True)
        tc=st.columns(3)
        with tc[0]: st.markdown(kpi("T1",f"₹{gann_info['gann_t1']:,.2f}","#10b981"),unsafe_allow_html=True)
        with tc[1]: st.markdown(kpi("T2",f"₹{gann_info['gann_t2']:,.2f}","#10b981"),unsafe_allow_html=True)
        with tc[2]: st.markdown(kpi("SL",f"₹{gann_info['gann_sl']:,.2f}","#ef4444"),unsafe_allow_html=True)
        if gann_chart: st.plotly_chart(gann_chart,use_container_width=True)
    with tab_pivot:
        pc=st.columns(2)
        with pc[0]:
            st.markdown(f'<div class="gc gc-gold"><div style="font-size:14px;font-weight:700;color:#f59e0b;margin-bottom:8px">Weekly</div>'
                        f'<div style="font-size:12px;color:#cbd5e1">R2: ₹{tech["w_r2"]:,.2f}<br>R1: ₹{tech["w_r1"]:,.2f}<br>'
                        f'<b>Pivot: ₹{tech["w_pivot"]:,.2f}</b><br>S1: ₹{tech["w_s1"]:,.2f}<br>S2: ₹{tech["w_s2"]:,.2f}</div></div>',unsafe_allow_html=True)
        with pc[1]:
            st.markdown(f'<div class="gc gc-purple"><div style="font-size:14px;font-weight:700;color:#8b5cf6;margin-bottom:8px">Monthly</div>'
                        f'<div style="font-size:12px;color:#cbd5e1">R2: ₹{tech["m_r2"]:,.2f}<br>R1: ₹{tech["m_r1"]:,.2f}<br>'
                        f'<b>Pivot: ₹{tech["m_pivot"]:,.2f}</b><br>S1: ₹{tech["m_s1"]:,.2f}<br>S2: ₹{tech["m_s2"]:,.2f}</div></div>',unsafe_allow_html=True)
    with tab_sr:
        for r in tech["key_res"]: st.markdown(f'<div class="lc lc-red">₹{r:,.2f} ({round((r-price)/max(price,0.01)*100,1):+.1f}%)</div>',unsafe_allow_html=True)
        for s in tech["key_sup"]: st.markdown(f'<div class="lc lc-green">₹{s:,.2f} ({round((price-s)/max(price,0.01)*100,1):+.1f}%)</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# RENDER — SCANNER
# ══════════════════════════════════════════════════════════════════════════════
def render_gann_index_analyzer_scanner(results):
    if not results:
        st.markdown('<div class="gc gc-blue" style="text-align:center;padding:32px"><div style="font-size:16px;color:#64748b">No results. Run a scan.</div></div>',unsafe_allow_html=True)
        return
    total=len(results); tier5=sum(1 for r in results if r["gann_confluence"]==5); tier4=sum(1 for r in results if r["gann_confluence"]>=4)
    squared=sum(1 for r in results if r["is_squared"]); avg_comp=round(sum(r["composite"] for r in results)/max(total,1),1)
    sc=st.columns(5)
    with sc[0]: st.markdown(kpi("Scanned",f"{total}","#06b6d4"),unsafe_allow_html=True)
    with sc[1]: st.markdown(kpi("Tier 5 🔥",f"{tier5}","#10b981"),unsafe_allow_html=True)
    with sc[2]: st.markdown(kpi("Tier 4+",f"{tier4}","#10b981"),unsafe_allow_html=True)
    with sc[3]: st.markdown(kpi("Squared",f"{squared}","#f59e0b"),unsafe_allow_html=True)
    with sc[4]: st.markdown(kpi("Avg Score",f"{avg_comp}","#8b5cf6"),unsafe_allow_html=True)
    fc=st.columns(4)
    with fc[0]: min_conf=st.selectbox("Min Conf",[1,2,3,4,5],index=0,key="sc_mc")
    with fc[1]: min_comp=st.slider("Min Composite",0,100,30,key="sc_mcm")
    with fc[2]: sort_by=st.selectbox("Sort",["Composite","Gann","Tech","RSI"],key="sc_sb")
    with fc[3]: show_n=st.selectbox("Top",[10,20,30,50,100],index=1,key="sc_sn")
    filtered=[r for r in results if r["gann_confluence"]>=min_conf and r["composite"]>=min_comp]
    sk={"Composite":lambda x:x["composite"],"Gann":lambda x:x["gann_confluence"],"Tech":lambda x:x["tech_score"],"RSI":lambda x:x["rsi"]}
    filtered.sort(key=sk.get(sort_by,lambda x:x["composite"]),reverse=True); filtered=filtered[:show_n]
    if filtered:
        rows=[]
        for r in filtered:
            ce={5:"🔥",4:"✅",3:"⚡",2:"⚠️",1:"⚪"}.get(r["gann_confluence"],"⚪")
            rr=round((r["gann_t1"]-r["price"])/max(r["price"]-r["gann_sl"],0.01),1) if r["gann_t1"]>0 and r["price"]>0 else 0.0
            rows.append({"Symbol":r["symbol"],"Price":f"₹{r['price']:,.2f}","Chg":f"{r['change_pct']:+.2f}%","RSI":r["rsi"],
                          "PE":r["pe"],"Tech":r["tech_score"],"Gann":f"{ce} {r['gann_confluence']}/5",
                          "Sq":"⬢" if r["is_squared"] else "—","R:R":f"{rr:.1f}","Score":r["composite"]})
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True,height=min(len(rows)*45+50,600))
        ds=st.selectbox("Drill down",options=[r["symbol"] for r in filtered],key="sc_dd")
        if st.button("🔍 Deep Analyze",key="sc_dd_btn"):
            st.session_state.selected_symbol=ds; st.session_state.analyze_triggered=True; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    all_symbols = fetch_nifty500_symbols()
    tab_single, tab_index, tab_scanner = st.tabs(["⚡ Single Stock", "🔷 Index Gann Analyzer", "🔍 Gann Stock Scanner"])

    # ── TAB 1: SINGLE STOCK ───────────────────────────────────────────────
    with tab_single:
        ic=st.columns([3,1])
        with ic[0]: query=st.text_input("symbol",placeholder="Search NSE — RELIANCE, TCS…")
        with ic[1]: ab=st.button("⚡ Analyze",use_container_width=True,key="s_ab")
        matched=[]
        if query and len(query.strip())>=1: matched=[s for s in all_symbols if query.strip().upper() in s][:20]
        selected=None
        if ab and matched: selected=matched[0]; st.session_state.selected_symbol=selected; st.session_state.analyze_triggered=True
        elif st.session_state.get("analyze_triggered") and st.session_state.get("selected_symbol"): selected=st.session_state.selected_symbol
        if matched and not selected:
            sc=st.columns(min(len(matched),5))
            for idx,sym in enumerate(matched[:10]):
                with sc[idx%len(sc)]:
                    if st.button(sym,key=f"sym_{sym}"): st.session_state.selected_symbol=sym; st.session_state.analyze_triggered=True; st.rerun()
        if selected:
            with st.spinner(f"Analyzing {selected}…"):
                data=fetch_stock_data(selected); tech=compute_technicals(data)
                ts,bull,bear=compute_tech_score(data,tech)
                gc,al,ac,isq,sp,gi=compute_gann_confluence(data,symbol=selected)
                chart=_build_gann_chart(data.get("hist"),gi["anchor_low"],gi["anchor_low_date"],gi["anchor_high"],
                                        gi["scale"],gi["angle_1x1"],gi["angle_2x1"],gi["angle_1x2"],gi["angle_1x4"],
                                        _sq9_levels(data["price"]),data["price"],datetime.now().date())
            render_analysis(selected,data,tech,ts,bull,bear,gc,al,ac,isq,sp,gi,chart)
        else:
            st.markdown('<div class="gc gc-gold" style="text-align:center;padding:40px"><div style="font-size:1.8rem;font-weight:800;background:linear-gradient(135deg,#f59e0b,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:12px">Search an NSE stock to begin</div><div style="font-size:14px;color:#64748b">VedicEdge combines Western technicals with Gann price-time theory</div></div>',unsafe_allow_html=True)

    # ── TAB 2: INDEX GANN ANALYZER ────────────────────────────────────────
    with tab_index:
        st.markdown('<div class="sec-title">📊 Index Gann Analyzer</div>',unsafe_allow_html=True)
        st.caption("All NSE/BSE Indices · Sq9 · Angles · Time Cycles · Forecast · Backtest")
        ic1,ic2,ic3=st.columns([2,2,1])
        with ic1: selected_index=st.selectbox("Index",list(INDEX_MAP.keys()),label_visibility="collapsed",key="idx_sel")
        with ic2: timeframe_opt=st.selectbox("Timeframe",["Intraday / Few Days (3–10d)","Swing Trade (2–8 weeks)"],label_visibility="collapsed",key="idx_tf")
        with ic3: analyze_index=st.button("Analyze",type="primary",use_container_width=True,key="btn_idx2")
        days_forward=15 if "Intraday" in timeframe_opt else 60
        if analyze_index and selected_index:
            cfg=INDEX_MAP[selected_index]
            with st.spinner(f"Fetching {cfg['label']}…"):
                _idata=fetch_index_data(selected_index)
            if _idata is None:
                st.error(f"❌ Could not fetch {cfg['label']}. Try again."); st.stop()
            with st.spinner("Fetching 10Y history…"):
                _long_hist=fetch_index_long_history(selected_index)
            _hist=_long_hist if _long_hist is not None else _idata["hist"]
            with st.spinner("Computing anchors…"):
                _anchors=_get_all_anchors(_hist)
            st.session_state["idx_idata"]=_idata; st.session_state["idx_hist"]=_hist
            st.session_state["idx_anchors"]=_anchors; st.session_state["idx_loaded_for"]=selected_index
            st.session_state["idx_timeframe_stored"]=timeframe_opt
        idata=st.session_state.get("idx_idata"); hist_for_gann=st.session_state.get("idx_hist")
        all_anchors=st.session_state.get("idx_anchors"); loaded_for=st.session_state.get("idx_loaded_for")
        if idata is not None and loaded_for!=selected_index:
            st.warning(f"⚠️ Results shown are for **{loaded_for}**. Click **Analyze** to load **{selected_index}**.")
        if idata is not None and all_anchors:
            cfg=INDEX_MAP[loaded_for]; ilabel=cfg["label"]; icolor=cfg["color"]
            price=idata["price"]; chg=idata["change_pct"]; c_col="#10b981" if chg>=0 else "#ef4444"
            st.markdown(f'<div style="background:linear-gradient(135deg,rgba(255,255,255,0.05),rgba(255,255,255,0.01));border:1px solid {icolor}44;border-radius:20px;padding:22px 28px;margin-bottom:16px"><div style="font-size:1.4rem;font-weight:900;color:{icolor};margin-bottom:2px">{ilabel}</div><div style="font-size:2.6rem;font-weight:900;font-family:JetBrains Mono,monospace;color:#e8edf5;line-height:1.1">{price:,.2f}</div><div style="color:{c_col};font-weight:700;font-size:14px;margin-top:2px">{"▲" if chg>=0 else "▼"} {abs(chg):.2f}%</div><div style="display:flex;gap:20px;margin-top:12px;flex-wrap:wrap"><div style="text-align:center"><div style="color:#94a3b8;font-size:11px;text-transform:uppercase;letter-spacing:1px">RSI</div><div style="font-size:22px;font-weight:700">{idata["rsi"]}</div></div><div style="text-align:center"><div style="color:#94a3b8;font-size:11px;text-transform:uppercase;letter-spacing:1px">ADX</div><div style="font-size:22px;font-weight:700;color:#f59e0b">{idata["adx"]:.0f}</div></div><div style="text-align:center"><div style="color:#94a3b8;font-size:11px;text-transform:uppercase;letter-spacing:1px">ATR</div><div style="font-size:22px;font-weight:700;color:#8b5cf6">{idata["atr"]:,.0f}</div></div></div></div>',unsafe_allow_html=True)
            anchor_names=list(all_anchors.keys())
            ac1,ac2,ac3=st.columns(3)
            for col,(aname,ainfo) in zip([ac1,ac2,ac3],all_anchors.items()):
                with col:
                    ds=(datetime.now().date()-ainfo["anchor_low_date"]).days; hlr=round(ainfo["anchor_high"]-ainfo["anchor_low"],2)
                    st.markdown(f'<div class="gc gc-gold" style="text-align:center;padding:14px"><div style="font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#64748b;margin-bottom:6px">{aname}</div><div style="font-size:1.3rem;font-weight:900;color:#f59e0b">{ainfo["anchor_low"]:,.2f}</div><div style="font-size:11px;color:#94a3b8;margin-top:4px">{ainfo["anchor_low_date"].strftime("%d %b %Y")}</div><div style="font-size:11px;color:#475569;margin-top:2px">{ds}d ago · Range {hlr:,.0f}</div></div>',unsafe_allow_html=True)
            selected_anchor_name=st.radio("Use anchor:",anchor_names,horizontal=True,key="anchor_radio")
            ainfo=all_anchors[selected_anchor_name]
            gd=_compute_gann_from_anchor(price,ainfo["anchor_low"],ainfo["anchor_low_date"],ainfo["anchor_high"],hist_for_gann,anchor_high_date=ainfo.get("anchor_high_date"))
            itab_tech,itab_gann,itab_forecast,itab_backtest=st.tabs(["📈 Technicals","🔶 Gann Now","🔮 Forecast","📋 Backtest"])
            # TECHNICALS
            with itab_tech:
                above200=price>idata["ema200"]; above50=price>idata["ema50"]; above21=price>idata["ema21"]
                trend_lbl="Strong Bull" if above200 and above50 and above21 else "Bull" if above200 and above50 else "Caution" if above200 else "Bear"
                trend_col="#10b981" if "Bull" in trend_lbl else "#f59e0b" if "Caution" in trend_lbl else "#ef4444"
                bb_pct=round((price-idata["bb_lower"])/max(idata["bb_upper"]-idata["bb_lower"],1)*100,1)
                st.markdown(f'<div class="gc gc-blue"><div style="font-size:14px;font-weight:700;margin-bottom:12px">📈 Technical Summary</div><div style="font-size:12px;color:#cbd5e1;line-height:1.8"><b style="color:#64748b">Trend:</b> <b style="color:{trend_col}">{trend_lbl}</b><br><b style="color:#64748b">RSI:</b> {idata["rsi"]} · <b style="color:#64748b">ADX:</b> {idata["adx"]:.1f} · <b style="color:#64748b">+DI/-DI:</b> {idata["di_pos"]}/{idata["di_neg"]} · <b style="color:#64748b">MACD:</b> {idata["macd_hist"]:+.1f} · <b style="color:#64748b">BB%B:</b> {bb_pct}%</div></div>',unsafe_allow_html=True)
                st.markdown(f'<div class="gc gc-gold"><div style="font-size:14px;font-weight:700;margin-bottom:12px">📐 Pivots</div><div style="font-size:12px;color:#cbd5e1"><b>Weekly:</b> R2 {idata["w_r2"]:,.2f} · R1 {idata["w_r1"]:,.2f} · <b style="color:#f59e0b">P {idata["w_pivot"]:,.2f}</b> · S1 {idata["w_s1"]:,.2f} · S2 {idata["w_s2"]:,.2f}<br><b>Monthly:</b> R2 {idata["m_r2"]:,.2f} · R1 {idata["m_r1"]:,.2f} · <b style="color:#f59e0b">P {idata["m_pivot"]:,.2f}</b> · S1 {idata["m_s1"]:,.2f} · S2 {idata["m_s2"]:,.2f}</div></div>',unsafe_allow_html=True)
            # GANN NOW
            with itab_gann:
                st.markdown(f'<div class="lc lc-gold" style="font-size:12px">⚓ <b>{selected_anchor_name}</b> · {ainfo["anchor_low"]:,.2f} · {ainfo["anchor_low_date"].strftime("%d %b %Y")} · {gd["days_from_low"]}d · Scale <b>{gd["scale"]:.4f}</b></div>',unsafe_allow_html=True)
                ang_rows=[]
                for ratio,aname,desc in [(8.0,"8×1","Very strong bull"),(4.0,"4×1","Strong bull"),(2.0,"2×1","Bull zone"),(1.0,"1×1","Master angle"),(0.5,"1×2","Caution"),(0.25,"1×4","Bear zone"),(0.125,"1×8","Strong bear")]:
                    val=round(ainfo["anchor_low"]+gd["days_from_low"]*gd["scale"]*ratio,2); diff=round((price-val)/max(val,1)*100,2)
                    ang_rows.append([aname,f"{val:,.2f}",desc,f"{'▲' if diff>=0 else '▼'} {abs(diff):.2f}%"])
                st.dataframe(pd.DataFrame(ang_rows,columns=["Angle","Level","Description","From CMP"]),use_container_width=True,hide_index=True)
                st.markdown(f'<div class="lc lc-{"green" if "Bull" in gd["angle_label"] else "gold" if "Caution" in gd["angle_label"] else "red"}"><b style="color:{gd["angle_color"]}">{gd["angle_label"]}</b> · Closest: {gd["closest_angle"]} · 1×1 dev: {gd["price_vs_1x1"]:+.2f}%</div>',unsafe_allow_html=True)
                sqc=st.columns(4)
                for col,(lab,val,vc) in zip(sqc,[("S2 (SL)",gd["sq9_s2"][1],"#ef4444"),("S1",gd["sq9_s1"][1],"#f97316"),("R1 (T1)",gd["sq9_r1

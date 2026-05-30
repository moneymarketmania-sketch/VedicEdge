import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import hashlib
import math
import requests
import io

st.set_page_config(page_title="VedicEdge", page_icon="🔵", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

:root {
    --bg:#060810; --bg2:#0d1117; --border:rgba(255,255,255,0.07);
    --text:#e8edf5; --muted:#64748b;
    --gold:#f59e0b; --green:#10b981; --red:#ef4444;
    --blue:#3b82f6; --purple:#8b5cf6; --cyan:#06b6d4;
}
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

div[data-testid="stTextInput"] input{
    background:rgba(255,255,255,.04)!important;
    border:1px solid rgba(255,255,255,.12)!important;
    border-radius:50px!important;
    color:#e8edf5!important;
    font-family:'Space Grotesk',sans-serif!important;
    font-size:14px!important;
    padding:10px 20px!important;
    letter-spacing:.3px;
    box-shadow:0 2px 16px rgba(0,0,0,.3),inset 0 1px 0 rgba(255,255,255,.06)!important;
    transition:all .2s!important;
}
div[data-testid="stTextInput"] input:focus{
    border-color:rgba(245,158,11,.5)!important;
    box-shadow:0 0 0 3px rgba(245,158,11,.1),0 2px 16px rgba(0,0,0,.3)!important;
    outline:none!important;
}
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
    ("selected_symbol", None),
    ("scan_results", []),
    ("scan_ran", False),
    ("analyze_triggered", False),
    ("last_symbol", ""),
]:
    if k not in st.session_state:
        st.session_state[k] = v


# ====================== HELPERS ==============================================
def pb(val, max_val, color):
    pct = min(100, max(0, val / max_val * 100))
    return f'<div class="pb-wrap"><div class="pb-fill" style="width:{pct}%;background:{color}"></div></div>'


def kpi(label, val, color="#e8edf5", sub=None):
    sub_h = (
        f'<div style="font-size:11px;color:#64748b;margin-top:3px">{sub}</div>'
        if sub
        else ""
    )
    return f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-val" style="color:{color}">{val}</div>{sub_h}</div>'


def safe_html(text):
    """Sanitize string for safe HTML injection."""
    return str(text).replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ====================== NIFTY 500 FETCH ======================================
@st.cache_data(ttl=86400, show_spinner=False)
def fetch_nifty500_symbols():
    """
    Fetch Nifty 500 constituent symbols from NSE's public CSV.
    Falls back to a hardcoded ~500 list if the endpoint is unreachable.
    """
    try:
        url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        df = pd.read_csv(io.StringIO(r.text))
        # NSE CSV has a "Symbol" column
        symbols = df["Symbol"].dropna().str.strip().tolist()
        if len(symbols) > 100:
            return symbols
    except Exception:
        pass

    # ── Fallback: hardcoded Nifty 500 symbols ────────────────────────────────
    return [
        # Nifty 50
        "RELIANCE","TCS","HDFCBANK","INFY","ICICIBANK","SBIN","LT","BHARTIARTL",
        "AXISBANK","KOTAKBANK","MARUTI","SUNPHARMA","HINDUNILVR","ITC","ULTRACEMCO",
        "WIPRO","HCLTECH","NTPC","POWERGRID","ONGC","BAJFINANCE","TATAMOTORS",
        "TATASTEEL","JSWSTEEL","HINDALCO","TITAN","ASIANPAINT","DMART","ADANIENT",
        "NESTLEIND","BAJAJFINSV","TECHM","INDUSINDBK","GRASIM","ADANIPORTS",
        "COALINDIA","BPCL","BRITANNIA","CIPLA","DRREDDY","EICHERMOT","HEROMOTOCO",
        "DIVISLAB","APOLLOHOSP","TATACONSUM","LTIM","SBILIFE","HDFCLIFE","BAJAJ-AUTO","M&M",
        # Nifty Next 50
        "SHRIRAMFIN","PIDILITIND","BERGEPAINT","MUTHOOTFIN","CHOLAFIN","MANAPPURAM",
        "ABCAPITAL","ICICIGI","NAUKRI","PERSISTENT","COFORGE","MPHASIS","TATACOMM",
        "OFSS","KPITTECH","ZOMATO","PAYTM","NYKAA","POLICYBZR","DELHIVERY","IRCTC",
        "CONCOR","SIEMENS","ABB","BHEL","CUMMINSIND","THERMAX","KECL","KALPATPOWR",
        "APLAPOLLO","HFCL","RAILTEL","RVNL","IRFC","RECLTD","PFC","SJVN","NHPC",
        "INDIANB","BANKINDIA","CANBK","UNIONBANK","FEDERALBNK","IDFCFIRSTB",
        "BANDHANBNK","RBLBANK","LICHSGFIN","PNBHOUSING","AAVAS","HOMEFIRST",
        # Pharma
        "BIOCON","ALKEM","LUPIN","TORNTPHARM","AUROPHARMA","IPCALAB","LALPATHLAB",
        "METROPOLIS","MAXHEALTH","FORTIS","SYNGENE","NATCOPHARM","GRANULES","GLAND",
        "LAURUSLABS","PFIZER","ABBOTINDIA","GLAXO","SUNPHARMA","AJANTPHARM",
        # Auto & Ancillaries
        "TVSMOTOR","ASHOKLEY","MOTHERSON","BOSCHLTD","BHARATFORG","SUPRAJIT",
        "APOLLOTYRE","MRF","CEATLTD","BALKRISIND","ENDURANCE","SUNDRMFAST",
        "EXIDEIND","AMARAJABAT","WABCOINDIA","MINDAIND","GABRIEL","SUBROS",
        # FMCG / Consumer
        "MARICO","DABUR","GODREJCP","EMAMILTD","COLPAL","VBL","RADICO","TATACONSUM",
        "PGHH","JYOTHYLAB","BIKAJI","PATANJALI","VARUN","WONDERLA","DEVYANI",
        # IT / Tech
        "LTTS","CYIENT","ZENSAR","HEXAWARE","BIRLASOFT","MASTEK","NIITTECH",
        "RAMSYSTEMS","TANLA","INTELLECT","NEWGEN","NUCLEUS","TATAELXSI",
        # Metals / Mining
        "NMDC","SAIL","NATIONALUM","HINDCOPPER","GMRINFRA","WELCORP","RATNAMANI",
        "JINDALSAW","JINDALSTEL","JSPL","MOIL","VEDL","HINDZINC","AIAENG",
        # Energy / Power
        "TORNTPOWER","TATAPOWER","ADANIGREEN","ADANIPOWER","CESC","JSPL","IEX",
        "MAHAGENCO","RPOWER","SUZLON","INOXWIND","GREENKO","ACME",
        # Infra / Capital Goods
        "ENGINERSIN","NBCC","RITES","IRCON","NCC","PNCINFRA","HG INFRA","KNRCON",
        "GPPL","MAHINDCIE","JKCEMENT","HEIDELBERG","RAMCOCEM","SHREECEM","JKIL",
        # Real Estate
        "DLF","GODREJPROP","OBEROIRLTY","PRESTIGE","PHOENIXLTD","BRIGADE","KOLTEPATIL",
        "MAHLIFE","LODHA","SUNTECK","SOBHA","ANANTRAJ","NESCO",
        # Banking extras
        "KARURVYSYA","DCBBANK","SOUTHBANK","LAKSHVILAS","TMB","EQUITASBNK","UJJIVAN",
        "SURYODAY","ESAFSFB","AUBANK","CREDITACC","AROHAN",
        # Insurance
        "STARHEALTH","NIACL","GICRE","ICICIGI","HDFCLIFE","SBILIFE","MAXFIN",
        # Chemicals
        "PIDILITIND","ATUL","DEEPAKNITRITE","NAVINFLUOR","SUDARSCHEM","GALAXYSURF",
        "VINATIORG","NOCIL","BALCHEMICALS","TATACHEM","GNFC","GSFC","CHAMBALFERT",
        "COROMANDEL","RALLIS","PIIND","BAYER","DHANUKA","INSECTICID",
        # Textile
        "PAGEIND","RAYMOND","ARVIND","TRIDENT","VARDHMAN","GOKEX","WELSPUNIND",
        "NITIN","ALOKTEXT","SPANDEX",
        # Logistics
        "BLUEDART","MAHLOG","GATI","TCI","ALLCARGO","SPANDEX","AEGISLOG",
        # Media / Entertainment
        "ZEEL","SUNTV","PVRINOX","INOXLEISURE","TIPS","SAREGAMA","NAZARA",
        # Telecom
        "IDEA","TATACOMM","HFCL","STLTECH","TEJAS",
        # Hotels / Travel
        "INDHOTEL","EIHHOTEL","LEMONTREE","CHALET","MAHINDHOLIDAY",
        # Miscellaneous
        "MCDOWELL-N","UNITEDSPIRITS","GLOBUSSPR","ABFRL","TRENT","VMART",
        "SHOPERSTOP","AVENUESUP","NYKAA","MEESHO","CARTRADE","EASEMYTRIP",
        "RATEGAIN","JUSTDIAL","INFOEDGE","MATRIMONY","INDIAMART",
        "MCLEODRUS","WESTLIFE","JUBLFOOD","SAPPHIRE","BARBEQUE",
        "EQUITAS","CREDITACC","SPANDANA","AROHAN","FUSION","UJJFIN",
    ]


# ====================== DATA FETCH ===========================================
@st.cache_data(ttl=180, show_spinner=False)
def fetch_stock_data(symbol):
    try:
        tk = yf.Ticker(f"{symbol}.NS")
        info = tk.info
        # Normalize timezone — strip tz from yfinance index
        hist = tk.history(period="1y")
        if not hist.empty:
            hist.index = hist.index.tz_localize(None) if hist.index.tzinfo is None else hist.index.tz_convert(None)

        if hist.empty or len(hist) < 10:
            raise ValueError("Empty history")

        price = float(
            info.get("currentPrice")
            or info.get("regularMarketPrice")
            or hist["Close"].iloc[-1]
        )
        prev = float(info.get("previousClose") or hist["Close"].iloc[-2])
        chg = round((price - prev) / prev * 100, 2)

        # RSI — Wilder's smoothing
        delta = hist["Close"].diff()
        g = delta.clip(lower=0).ewm(alpha=1/14, min_periods=14, adjust=False).mean()
        l = (-delta.clip(upper=0)).ewm(alpha=1/14, min_periods=14, adjust=False).mean()
        rsi_raw = 100 - 100 / (1 + g / l)
        rsi = round(float(rsi_raw.iloc[-1]), 1) if not math.isnan(rsi_raw.iloc[-1]) else 50.0

        tr = pd.concat([
            hist["High"] - hist["Low"],
            (hist["High"] - hist["Close"].shift()).abs(),
            (hist["Low"] - hist["Close"].shift()).abs(),
        ], axis=1).max(axis=1)
        atr = round(float(tr.rolling(14).mean().iloc[-1]), 2)
        atr_pct = round(atr / price * 100, 2) if price > 0 else 0

        beta = float(info.get("beta") or 1.0)
        volume = int(info.get("volume") or hist["Volume"].iloc[-1])
        pe = round(float(info.get("trailingPE") or 25), 1)
        pb_val = round(float(info.get("priceToBook") or 3.5), 2)
        sector = info.get("sector", "Unknown")
        name = info.get("longName", symbol)
        w52h = round(float(hist["High"].max()), 2)
        w52l = round(float(hist["Low"].min()), 2)

        return dict(
            price=round(price, 2), change_pct=chg, rsi=rsi, atr=atr,
            atr_pct=atr_pct, beta=beta, volume=volume, pe=pe, pb=pb_val,
            hist=hist, source="LIVE", sector=sector, name=name,
            w52h=w52h, w52l=w52l,
        )

    except Exception:
        st.warning(f"⚠️ Live data failed for {symbol} — using demo data")
        return dict(
            price=334.55, change_pct=3.46, rsi=58.4, atr=8.2, atr_pct=2.45,
            beta=1.06, volume=18310000, pe=6.85, pb=3.70, hist=None,
            source="DEMO", sector="Unknown", name=symbol, w52h=420.0, w52l=240.0,
        )


# ====================== TECHNICALS ===========================================
# NOTE: Not cached with @st.cache_data because dicts with DataFrames aren't
# reliably hashable. The upstream fetch_stock_data is cached instead.
def compute_technicals(data):
    p = data["price"]
    if data.get("hist") is not None:
        h = data["hist"]
        c = h["Close"]
        ema9   = round(float(c.ewm(span=9,   adjust=False).mean().iloc[-1]), 2)
        ema21  = round(float(c.ewm(span=21,  adjust=False).mean().iloc[-1]), 2)
        ema55  = round(float(c.ewm(span=55,  adjust=False).mean().iloc[-1]), 2)
        ema200 = round(float(c.ewm(span=200, adjust=False).mean().iloc[-1]), 2)
        ml = c.ewm(span=12, adjust=False).mean() - c.ewm(span=26, adjust=False).mean()
        ms = ml.ewm(span=9, adjust=False).mean()
        macd_val  = round(float(ml.iloc[-1]), 2)
        macd_sig  = round(float(ms.iloc[-1]), 2)
        macd_hist = round(macd_val - macd_sig, 2)
        bm = c.rolling(20).mean()
        bs = c.rolling(20).std()
        bb_upper = round(float((bm + 2*bs).iloc[-1]), 2)
        bb_lower = round(float((bm - 2*bs).iloc[-1]), 2)
        bb_mid   = round(float(bm.iloc[-1]), 2)
        lo14 = h["Low"].rolling(14).min()
        hi14 = h["High"].rolling(14).max()
        stoch_k = round(float(((c - lo14) / (hi14 - lo14) * 100).iloc[-1]), 1)
        stoch_d = round(float(((c - lo14) / (hi14 - lo14) * 100).rolling(3).mean().iloc[-1]), 1)
        vol20 = round(float(h["Volume"].rolling(20).mean().iloc[-1]))
        volr  = round(data["volume"] / max(vol20, 1), 2)
        tr_s = pd.concat([
            h["High"] - h["Low"],
            (h["High"] - h["Close"].shift()).abs(),
            (h["Low"]  - h["Close"].shift()).abs(),
        ], axis=1).max(axis=1)
        atr14 = tr_s.ewm(alpha=1/14, min_periods=14, adjust=False).mean()

        # ── BUG FIX: save originals before zeroing to avoid race condition ──
        dmp_raw = h["High"].diff().clip(lower=0)
        dmn_raw = (-h["Low"].diff()).clip(lower=0)
        dmp = dmp_raw.where(dmp_raw > dmn_raw, 0)
        dmn = dmn_raw.where(dmn_raw > dmp_raw, 0)

        di_pos_s = dmp.ewm(alpha=1/14, min_periods=14, adjust=False).mean()
        di_neg_s = dmn.ewm(alpha=1/14, min_periods=14, adjust=False).mean()
        di_pos = round(float((di_pos_s / atr14 * 100).iloc[-1]), 1)
        di_neg = round(float((di_neg_s / atr14 * 100).iloc[-1]), 1)
        di_pos_series = di_pos_s / atr14 * 100
        di_neg_series = di_neg_s / atr14 * 100
        dx_series = (
            (di_pos_series - di_neg_series).abs()
            / (di_pos_series + di_neg_series).clip(lower=0.01)
            * 100
        )
        adx = round(float(dx_series.ewm(alpha=1/14, min_periods=14, adjust=False).mean().iloc[-1]), 1)

        ph = round(float(h["High"].iloc[-2]), 2)
        pl = round(float(h["Low"].iloc[-2]), 2)
        pc = round(float(h["Close"].iloc[-2]), 2)
        pivot = round((ph + pl + pc) / 3, 2)
        r1 = round(2*pivot - pl, 2)
        s1 = round(2*pivot - ph, 2)
        r2 = round(pivot + (ph - pl), 2)
        s2 = round(pivot - (ph - pl), 2)
    else:
        ema9 = ema21 = ema55 = ema200 = p
        macd_val = 0.5; macd_sig = 0.2; macd_hist = 0.3
        bb_upper = round(p*1.04, 2); bb_lower = round(p*0.96, 2); bb_mid = p
        stoch_k = 55.0; stoch_d = 52.0
        vol20 = data["volume"]; volr = 1.0
        di_pos = 22.0; di_neg = 18.0; adx = 24.0
        pivot = p; r1 = round(p*1.02, 2); s1 = round(p*0.98, 2)
        r2 = round(p*1.04, 2); s2 = round(p*0.96, 2)

    return dict(
        ema9=ema9, ema21=ema21, ema55=ema55, ema200=ema200,
        macd_val=macd_val, macd_sig=macd_sig, macd_hist=macd_hist,
        bb_upper=bb_upper, bb_lower=bb_lower, bb_mid=bb_mid,
        stoch_k=stoch_k, stoch_d=stoch_d,
        vol20=vol20, volr=volr,
        di_pos=di_pos, di_neg=di_neg, adx=adx,
        pivot=pivot, r1=r1, s1=s1, r2=r2, s2=s2,
    )


def compute_tech_score(data, tech):
    p = data["price"]
    ts = 0
    bull = []
    bear = []
    if p > tech["ema9"] and p > tech["ema21"] and p > tech["ema55"]:
        ts += 2; bull.append("Above EMA9/21/55 — bullish structure ✅")
    elif p > tech["ema9"] and p > tech["ema21"]:
        ts += 1; bull.append("Above EMA9/21 — short-term bullish")
    else:
        ts -= 1; bear.append("Below key EMAs — bearish structure")
    if p > tech["ema200"]:
        ts += 1; bull.append("Above 200 EMA — long-term bull ✅")
    else:
        ts -= 1; bear.append("Below 200 EMA — long-term bear risk")
    if 40 < data["rsi"] < 70:
        ts += 1; bull.append(f"RSI {data['rsi']} — healthy zone ✅")
    elif data["rsi"] >= 70:
        ts -= 1; bear.append(f"RSI {data['rsi']} — overbought ⚠️")
    else:
        ts += 1; bull.append(f"RSI {data['rsi']} — oversold, bounce potential ✅")
    if tech["macd_hist"] > 0:
        ts += 1; bull.append("MACD histogram positive ✅")
    else:
        ts -= 1; bear.append("MACD histogram negative")
    if tech["volr"] > 1.3:
        ts += 1; bull.append(f"Volume {tech['volr']}x avg ✅")
    elif tech["volr"] < 0.7:
        ts -= 1; bear.append("Low volume — lacks conviction")
    if tech["adx"] > 25 and tech["di_pos"] > tech["di_neg"]:
        ts += 1; bull.append(f"ADX {tech['adx']} strong, +DI dominant ✅")
    elif tech["adx"] > 25 and tech["di_pos"] < tech["di_neg"]:
        ts -= 1; bear.append("Strong downtrend, −DI dominant")
    if tech["bb_mid"] < p < tech["bb_upper"]:
        ts += 1; bull.append("Between mid-upper Bollinger ✅")
    elif p > tech["bb_upper"]:
        bear.append("Above upper Bollinger — extended")
    elif p < tech["bb_lower"]:
        ts += 1; bull.append("At lower Bollinger — bounce zone ✅")
    if data["pe"] < 25 and data["pb"] < 4:
        ts += 1; bull.append(f"Good valuations PE {data['pe']} ✅")
    elif data["pe"] > 45:
        bear.append(f"Stretched PE {data['pe']}")
    return ts, bull, bear


# ====================== GANN =================================================
def compute_gann_confluence(data):
    price = data["price"]
    today = datetime.now().date()
    if data.get("hist") is not None:
        hist = data["hist"]
        anchor_low  = round(float(hist["Low"].min()), 2)
        anchor_high = round(float(hist["High"].max()), 2)
        # ── BUG FIX: handle both tz-aware and naive index ──
        low_idx  = hist["Low"].idxmin()
        high_idx = hist["High"].idxmax()
        anchor_low_date  = low_idx.date()  if hasattr(low_idx,  "date") else low_idx.to_pydatetime().date()
        anchor_high_date = high_idx.date() if hasattr(high_idx, "date") else high_idx.to_pydatetime().date()
        days_from_low  = (today - anchor_low_date).days
        days_from_high = (today - anchor_high_date).days
        hl_range = round(anchor_high - anchor_low, 2)
    else:
        anchor_low  = round(price * 0.72, 2)
        anchor_high = round(price * 1.22, 2)
        anchor_low_date  = today - timedelta(days=210)
        anchor_high_date = today - timedelta(days=90)
        days_from_low  = 210
        days_from_high = 90
        hl_range = round(anchor_high - anchor_low, 2)

    sqrt_days  = round(math.sqrt(days_from_low), 4)
    n_low      = round(sqrt_days)
    nearest_sq = n_low ** 2
    next_sq    = (n_low + 1) ** 2 if nearest_sq <= days_from_low else nearest_sq
    days_to_next = next_sq - days_from_low

    floor_root = math.floor(math.sqrt(price))
    ceil_root  = math.ceil(math.sqrt(price))
    angle_1x1  = round(anchor_low + days_from_low, 2)
    current_rate = (price - anchor_low) / max(days_from_low, 1)

    if current_rate >= 3.5:
        angle_label = "4×1 (Very Strong Bull)"; angle_color = "#ef4444"
    elif current_rate >= 1.8:
        angle_label = "2×1 (Strong Bull)";      angle_color = "#10b981"
    elif current_rate >= 0.8:
        angle_label = "1×1 (Balanced/Healthy)"; angle_color = "#10b981"
    elif current_rate >= 0.4:
        angle_label = "1×2 (Weak — Caution)";   angle_color = "#f59e0b"
    else:
        angle_label = "Below 1×2 (Bear)";       angle_color = "#ef4444"

    time_sq_of_price = round(math.sqrt(price), 2)
    squaring_pct = round(abs(time_sq_of_price - days_from_low) / max(days_from_low, 1) * 100, 1)
    is_squared   = squaring_pct < 5

    confluence = 0
    reasons = []
    if is_squared:
        confluence += 1; reasons.append(f"✅ Price-Time Squared ({squaring_pct}% dev)")
    if days_to_next <= 7:
        confluence += 1; reasons.append(f"✅ Perfect Square in {days_to_next} days")
    if abs(price - angle_1x1) / price < 0.05:
        confluence += 1; reasons.append("✅ Near 1×1 Master Angle (±5%)")
    if abs(price - round(ceil_root**2, 2)) / price < 0.03:
        confluence += 1; reasons.append("✅ Near Cardinal Sq9 level (±3%)")
    if abs(days_from_low % 90) <= 5 or days_from_low in [144, 180, 270, 360]:
        confluence += 1; reasons.append(f"✅ At major time division ({days_from_low} days)")
    if not reasons:
        reasons.append("⚪ No major confluence — wait for cycle maturity")

    anchor_sq9_root  = round(math.sqrt(anchor_low), 4)
    range_sqrt       = round(math.sqrt(hl_range), 4)
    range_sq_target  = round((math.ceil(range_sqrt) + 1) ** 2, 2)
    gann_t1 = round((ceil_root + 1) ** 2, 2)
    gann_t2 = round((ceil_root + 2) ** 2, 2)
    gann_sl = round((floor_root - 1) ** 2, 2)

    sq_levels = [
        ["🔴 Support S2", round((floor_root - 1)**2, 2),       "Cardinal ring below — stop-loss zone"],
        ["🟠 Support S1", round((math.sqrt(price) - 0.5)**2, 2),"Diagonal Sq9 — minor support"],
        ["⚪ Current",    price,                                  "Price now"],
        ["🟡 R1",         round((math.sqrt(price) + 0.5)**2, 2),"Diagonal — first resistance"],
        ["🟢 R2",         round(ceil_root**2, 2),                "Cardinal ring — immediate resistance"],
        ["🔵 Target T1",  gann_t1,                               "Primary swing target"],
        ["🔵 Target T2",  gann_t2,                               "Medium-term target"],
        ["🔵 Target T3",  round((ceil_root + 3)**2, 2),          "Positional/yearly target"],
    ]

    gann_time_units = [7, 9, 13, 21, 30, 45, 60, 90, 120, 144, 180, 270, 360]
    active_cycle = next((t for t in gann_time_units if days_from_low <= t), 360)
    gann_future = []
    for t in gann_time_units:
        fd = anchor_low_date + timedelta(days=t)
        if fd >= today:
            gann_future.append((t, fd, (fd - today).days))
        if len(gann_future) >= 6:
            break
    sq_dates = []
    n_start = int(math.sqrt(days_from_low)) + 1
    for i in range(n_start, n_start + 6):
        d = i * i
        sd = anchor_low_date + timedelta(days=d)
        if sd >= today:
            sq_dates.append((d, sd, (sd - today).days, i))
    anniv_dates = []
    for yr in [1, 2, 5, 7, 10]:
        try:
            ad = anchor_low_date.replace(year=anchor_low_date.year + yr)
            if ad >= today:
                anniv_dates.append((yr, ad, (ad - today).days))
        except Exception:
            pass

    return (
        confluence, angle_label, angle_color, is_squared, squaring_pct,
        dict(
            anchor_low=anchor_low, anchor_high=anchor_high,
            anchor_low_date=anchor_low_date, anchor_high_date=anchor_high_date,
            days_from_low=days_from_low, days_from_high=days_from_high,
            hl_range=hl_range, sqrt_days=sqrt_days, n_low=n_low,
            nearest_sq=nearest_sq, next_sq=next_sq, days_to_next=days_to_next,
            angle_1x1=round(anchor_low + days_from_low, 2),
            angle_2x1=round(anchor_low + days_from_low * 2, 2),
            angle_1x2=round(anchor_low + days_from_low * 0.5, 2),
            angle_4x1=round(anchor_low + days_from_low * 4, 2),
            current_rate=current_rate,
            anchor_sq9_root=anchor_sq9_root, time_sq_of_price=time_sq_of_price,
            is_squared=is_squared, squaring_pct=squaring_pct,
            confluence=confluence, reasons=reasons,
            floor_root=floor_root, ceil_root=ceil_root,
            sq_levels=sq_levels, sq9_root=round(math.sqrt(price), 4),
            range_sqrt=range_sqrt, range_sq_target=range_sq_target,
            gann_t1=gann_t1, gann_t2=gann_t2, gann_sl=gann_sl,
            active_cycle=active_cycle, gann_future=gann_future,
            sq_dates=sq_dates, anniv_dates=anniv_dates, today=today,
        ),
    )


# ====================== SBC ==================================================
def compute_sbc(symbol, data):
    import os
    from datetime import datetime, timezone

    try:
        import swisseph as swe
    except ImportError:
        return (
            50, "Neutral (swisseph not installed)", "#f59e0b", "Unknown", 0, 0,
            [("⚠️ Setup Required","—","—","—","—","—","—","—","—",
              "Install swisseph and place ephe/ folder to enable SBC.", 0)],
        )

    try:
        EPHE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "ephe")
        swe.set_ephe_path(EPHE_PATH)
    except Exception:
        swe.set_ephe_path(os.path.join(os.getcwd(), "ephe"))

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    FLAGS = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL

    nakshatras = [
        "Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra",
        "Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni",
        "Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha",
        "Jyeshtha","Moola","Purva Ashadha","Uttara Ashadha","Shravana",
        "Dhanishtha","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati",
    ]

    sym_hash = int(hashlib.md5(symbol.encode()).hexdigest(), 16)
    stock_nak_idx = sym_hash % 27
    stock_nak = nakshatras[stock_nak_idx]

    now = datetime.now(timezone.utc)
    jd  = swe.julday(now.year, now.month, now.day, now.hour + now.minute/60 + now.second/3600)

    def get_lon(pid):
        r = swe.calc_ut(jd, pid, FLAGS)
        return r[0][0] % 360, r[0][3]

    sun_lon,sun_speed   = get_lon(swe.SUN)
    moon_lon,moon_speed = get_lon(swe.MOON)
    mars_lon,mars_speed = get_lon(swe.MARS)
    mercury_lon,mer_speed = get_lon(swe.MERCURY)
    jupiter_lon,jup_speed = get_lon(swe.JUPITER)
    venus_lon,ven_speed   = get_lon(swe.VENUS)
    saturn_lon,sat_speed  = get_lon(swe.SATURN)
    rahu_lon,_  = get_lon(swe.MEAN_NODE)
    ketu_lon    = (rahu_lon + 180) % 360

    def lon_to_nak(lon):
        idx = int((lon % 360) / (360/27))
        return idx, nakshatras[idx]

    def lon_to_sign(lon):
        signs = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
                 "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
        return signs[int((lon % 360) / 30)]

    def check_vedha(p_idx, s_idx, name):
        diff = abs(p_idx - s_idx) % 27
        if diff == 0:   return "Strong Positive", 4 if name in ["Jupiter ♃","Venus ♀"] else 3
        if diff in [7,14]:  return "Positive", 2
        if diff in [10,19]: return "Negative", -3 if name in ["Saturn ♄","Mars ♂","Rahu ☊","Ketu ☋"] else -2
        if diff in [3,24]:  return "Mild Positive", 1
        if diff in [6,21]:  return "Mild Negative", -1
        if diff in [4,5,8,9,11,12,13,15,16,17,18,20,22,23,25,26]:
            if name in ["Jupiter ♃","Venus ♀"]: return "Mild Positive", 1
            if name in ["Saturn ♄","Mars ♂","Rahu ☊","Ketu ☋"]: return "Mild Negative", -1
        return "Neutral", 0

    def get_chakra_house(p_idx, s_idx):
        diff = (p_idx - s_idx) % 27
        if diff in [0,11,2]:   return "Strong House", "Highly supportive"
        if diff in [10,19,6,21]: return "Weak House", "Obstructive"
        return "Neutral House", "Balanced"

    def get_drishti(p_idx, s_idx, name):
        diff = (p_idx - s_idx) % 27
        if diff in [3,10,17]: return "Benefic Aspect", 2 if name in ["Jupiter ♃","Venus ♀"] else -1
        if diff in [7,14]:    return "Powerful Aspect", 1 if name in ["Jupiter ♃","Venus ♀"] else -2
        return "No Aspect", 0

    def get_special(name, lon, speed, all_lons):
        special = []
        my_key = name.split()[0].lower()
        if speed < 0 and my_key != "sun":
            special.append("Retrograde")
        if my_key != "sun":
            diff = abs(lon - all_lons["sun"])
            diff = min(diff, 360 - diff)
            if diff < 8.0:
                special.append("Combust")
        for o_key, o_lon in all_lons.items():
            if o_key == my_key:
                continue
            diff = abs(o_lon - lon)
            diff = min(diff, 360 - diff)
            if diff < 1.0:
                special.append("Planetary War")
                break
        if 276.0 <= (lon % 360) <= 280.0:
            special.append("Abhijit")
        my_nak_idx = int((lon % 360) / (360/27))
        count_same = sum(
            1 for o_key, o_lon in all_lons.items()
            if o_key != my_key and int((o_lon % 360) / (360/27)) == my_nak_idx
        )
        if count_same >= 1 and "Planetary War" not in special:
            special.append("Conjunction in Same Nakshatra")
        return " + ".join(special) if special else "Normal"

    sector = data.get("sector", "Unknown").lower()
    sector_keywords = {
        "technology":   ["Mercury ☿","Jupiter ♃"],
        "it":           ["Mercury ☿","Jupiter ♃"],
        "bank":         ["Venus ♀","Jupiter ♃"],
        "financial":    ["Venus ♀","Jupiter ♃"],
        "auto":         ["Mars ♂"],
        "pharmaceutical":["Moon ☽","Jupiter ♃"],
        "energy":       ["Sun ☉","Mars ♂"],
        "metal":        ["Saturn ♄","Mars ♂"],
        "telecom":      ["Mercury ☿"],
        "default":      ["Jupiter ♃","Venus ♀"],
    }
    key_planets = sector_keywords["default"]
    for kw, planets in sector_keywords.items():
        if kw != "default" and kw in sector:
            key_planets = planets
            break

    all_lons = {
        "sun": sun_lon,"moon": moon_lon,"mars": mars_lon,"mercury": mercury_lon,
        "jupiter": jupiter_lon,"venus": venus_lon,"saturn": saturn_lon,
        "rahu": rahu_lon,"ketu": ketu_lon,
    }

    planet_list = [
        ("Sun ☉",     sun_lon,     sun_speed),
        ("Moon ☽",    moon_lon,    moon_speed),
        ("Mars ♂",    mars_lon,    mars_speed),
        ("Mercury ☿", mercury_lon, mer_speed),
        ("Jupiter ♃", jupiter_lon, jup_speed),
        ("Venus ♀",   venus_lon,   ven_speed),
        ("Saturn ♄",  saturn_lon,  sat_speed),
        ("Rahu ☊",    rahu_lon,    -0.053),
        ("Ketu ☋",    ketu_lon,    -0.053),
    ]

    planet_data = []
    sbc_raw = 0

    for name, lon, speed in planet_list:
        p_idx, p_nak = lon_to_nak(lon)
        p_sign = lon_to_sign(lon)
        vedha, vedha_w = check_vedha(p_idx, stock_nak_idx, name)
        sbc_raw += vedha_w
        placement  = "Strong" if vedha_w > 1 else "Weak" if vedha_w < -1 else "Average"
        house_type, _ = get_chakra_house(p_idx, stock_nak_idx)
        drishti, drishti_w = get_drishti(p_idx, stock_nak_idx, name)
        sbc_raw += drishti_w
        special = get_special(name, lon, speed, all_lons)
        sector_match = "Strong Sector Alignment" if name in key_planets else "Neutral Sector"
        impact = f"{name} in {p_nak} ({p_sign}) — {house_type} • {placement} • {drishti} • {special} • {sector_match}"
        total_weight = vedha_w + drishti_w
        planet_data.append((name, p_sign, p_nak, vedha, placement, house_type,
                             drishti, special, sector_match, impact, total_weight))

    sbc_score = max(15, min(95, int(50 + sbc_raw * 3.0)))
    sbc_label = ("Strongly Bullish" if sbc_score >= 75
                 else "Bullish" if sbc_score >= 62
                 else "Neutral" if sbc_score >= 48
                 else "Bearish")
    sbc_color = "#10b981" if sbc_score >= 62 else "#f59e0b" if sbc_score >= 48 else "#ef4444"
    benefic = sum(1 for p in planet_data if p[10] > 0)
    malefic = sum(1 for p in planet_data if p[10] < 0)

    return sbc_score, sbc_label, sbc_color, stock_nak, benefic, malefic, planet_data


# ====================== COMBINED VERDICT =====================================
def combined_verdict(tech_score, gann_confluence, sbc_score):
    tech_norm = max(0, min(100, int((tech_score + 8) / 18 * 100)))
    gann_norm = max(0, min(100, int(gann_confluence / 5 * 100)))
    sbc_norm  = max(0, min(100, sbc_score))
    final = round(tech_norm * 0.60 + gann_norm * 0.25 + sbc_norm * 0.15)
    if final >= 72:  lbl, cls, icon = "STRONG BUY",         "vb-buy",     "🟢"
    elif final >= 58: lbl, cls, icon = "BUY / ACCUMULATE",  "vb-buy",     "🟢"
    elif final >= 45: lbl, cls, icon = "CAUTIOUS — WAIT",   "vb-caution", "🟡"
    elif final >= 35: lbl, cls, icon = "NEUTRAL",           "vb-caution", "🟡"
    elif final >= 25: lbl, cls, icon = "AVOID / REDUCE",    "vb-avoid",   "🔴"
    else:             lbl, cls, icon = "STRONG AVOID",      "vb-avoid",   "🔴"
    return final, lbl, cls, icon, tech_norm, gann_norm, sbc_norm


# ====================== TABS =================================================
tab_scanner, tab_analyzer = st.tabs(["🔍  Stock Scanner", "🔵  Analyzer"])


# ====================================================================
# SCANNER TAB
# ====================================================================
with tab_scanner:
    st.markdown('<div class="sec-title">🔍 VedicEdge Swing Stock Scanner</div>', unsafe_allow_html=True)
    st.caption("Screens Nifty 500 stocks for swing & short-term setups · Technical + Momentum + Valuation")

    # Load symbol universe
    with st.spinner("Loading Nifty 500 symbols..."):
        UNIVERSE = fetch_nifty500_symbols()
    st.caption(f"Universe: {len(UNIVERSE)} symbols loaded")

    with st.expander("⚙️  Filter Settings", expanded=True):
        fc1, fc2, fc3, fc4 = st.columns(4)
        with fc1:
            min_rsi   = st.slider("Min RSI", 20, 60, 35)
            max_rsi   = st.slider("Max RSI", 50, 85, 68)
        with fc2:
            min_atr   = st.slider("Min ATR%", 0.5, 5.0, 1.5, 0.1)
            max_pe    = st.slider("Max PE", 10, 80, 45)
        with fc3:
            f_momentum = st.checkbox("Above EMA21 (Momentum)", value=True)
            f_macd     = st.checkbox("MACD Bullish Crossover", value=True)
            f_volume   = st.checkbox("Volume > 1.2x Avg", value=True)
        with fc4:
            f_breakout = st.checkbox("Near 52W High (>85%)", value=False)
            f_ema200   = st.checkbox("Above 200 EMA (Long-term)", value=False)
            f_low_beta = st.checkbox("Low Beta (<1.3)", value=False)

        batch_size = st.select_slider(
            "Batch size (stocks per chunk)",
            options=[25, 50, 100, 150, 200],
            value=50,
        )

    col_run, col_clear = st.columns([3, 1])
    with col_run:
        run_scan = st.button("🔍  Run Swing Scan", type="primary", use_container_width=True)
    with col_clear:
        if st.button("🗑️  Clear Results", use_container_width=True):
            st.session_state["scan_results"] = []
            st.session_state["scan_ran"] = False
            st.rerun()

    if run_scan:
        st.session_state["scan_results"] = []
        st.session_state["scan_ran"] = True

        batches = [UNIVERSE[i:i+batch_size] for i in range(0, len(UNIVERSE), batch_size)]
        total   = len(UNIVERSE)

        prog         = st.progress(0, text="Starting scan...")
        batch_status = st.empty()
        results_area = st.container()
        scanned      = 0

        for b_idx, batch in enumerate(batches):
            batch_status.markdown(
                f'<div style="color:#f59e0b;font-size:13px">📦 Batch {b_idx+1}/{len(batches)} · '
                f'Scanning {batch[0]}→{batch[-1]}</div>',
                unsafe_allow_html=True,
            )

            for sym in batch:
                scanned += 1
                prog.progress(scanned / total, text=f"Scanning {sym} ({scanned}/{total})...")
                try:
                    d = fetch_stock_data(sym)
                    t = compute_technicals(d)
                    score   = 0
                    reasons = []
                    criteria = {}

                    ok = min_rsi <= d["rsi"] <= max_rsi
                    criteria["rsi"] = ok
                    if ok: score += 20; reasons.append(f"RSI {d['rsi']} in momentum zone")

                    ok = not f_momentum or d["price"] > t["ema21"]
                    criteria["ema"] = ok
                    if ok: score += 15; reasons.append("Price above EMA21")

                    ok = not f_macd or t["macd_hist"] > 0
                    criteria["macd"] = ok
                    if ok: score += 15; reasons.append("MACD bullish")

                    ok = not f_volume or t["volr"] >= 1.2
                    criteria["vol"] = ok
                    if ok: score += 10; reasons.append(f"Vol {t['volr']}x avg")

                    ok = d["atr_pct"] >= min_atr
                    criteria["atr"] = ok
                    if ok: score += 10; reasons.append(f"ATR {d['atr_pct']}% — swing-worthy")

                    ok = d["pe"] <= max_pe
                    criteria["val"] = ok
                    if ok: score += 10; reasons.append(f"PE {d['pe']} ≤ {max_pe}")

                    hi_prox = d["price"] / d["w52h"] * 100
                    ok = not f_breakout or hi_prox >= 85
                    criteria["hi52"] = ok
                    if ok and f_breakout: score += 10; reasons.append(f"Near 52W High ({hi_prox:.0f}%)")

                    ok = not f_ema200 or d["price"] > t["ema200"]
                    criteria["ema200"] = ok
                    if ok and f_ema200: score += 10; reasons.append("Above 200 EMA")

                    ok = not f_low_beta or d["beta"] < 1.3
                    criteria["beta"] = ok
                    if ok and f_low_beta: score += 5

                    # Bonuses — applied separately, score capped after
                    bonus = 0
                    if d["price"] > t["ema9"] > t["ema21"] > t["ema55"]: bonus += 5
                    if t["adx"] > 22 and t["di_pos"] > t["di_neg"]:      bonus += 5

                    sl  = round(d["price"] - d["atr"] * 1.5, 2)
                    tgt = round(d["price"] + d["atr"] * 3,   2)
                    rr  = round((tgt - d["price"]) / max(d["price"] - sl, 0.01), 1)

                    base_score = min(score, 100)   # cap base before bonus
                    final_score = min(base_score + bonus, 100)

                    if final_score >= 40:
                        entry = dict(
                            sym=sym, name=d["name"], price=d["price"],
                            change=d["change_pct"], score=final_score,
                            reasons=reasons, criteria=criteria,
                            rsi=d["rsi"], pe=d["pe"], pb=d["pb"],
                            atr_pct=d["atr_pct"], beta=d["beta"],
                            volr=t["volr"], macd_hist=t["macd_hist"],
                            ema21=t["ema21"], ema200=t["ema200"],
                            sector=d["sector"], w52h=d["w52h"], w52l=d["w52l"],
                            sl=sl, tgt=tgt, rr=rr,
                        )
                        # Insert in sorted order (descending score)
                        inserted = False
                        for i, ex in enumerate(st.session_state["scan_results"]):
                            if entry["score"] > ex["score"]:
                                st.session_state["scan_results"].insert(i, entry)
                                inserted = True
                                break
                        if not inserted:
                            st.session_state["scan_results"].append(entry)
                except Exception:
                    pass

            # ── Show results after each batch completes ──
            with results_area:
                if st.session_state["scan_results"]:
                    top20 = st.session_state["scan_results"][:20]
                    st.markdown(
                        f'<div style="color:#10b981;font-size:13px;margin-bottom:8px">'
                        f'✅ {len(st.session_state["scan_results"])} candidates so far '
                        f'(showing top 20) · Batch {b_idx+1}/{len(batches)} complete</div>',
                        unsafe_allow_html=True,
                    )
                    _render_scan_results(top20) if "render" in dir() else None

        prog.empty()
        batch_status.empty()

    # ── Always render persisted results ──────────────────────────────────────
    if st.session_state["scan_results"]:
        top20 = st.session_state["scan_results"][:20]

        st.success(
            f"✅ **{len(st.session_state['scan_results'])} swing candidates** found · "
            f"Showing top {len(top20)}"
        )
        st.code("Watchlist: " + " | ".join(s["sym"] for s in top20), language="text")

        for s in top20:
            sc     = s["score"]
            sc_col = "#10b981" if sc >= 70 else "#f59e0b" if sc >= 55 else "#3b82f6"
            ch_col = "#10b981" if s["change"] >= 0 else "#ef4444"

            def dot(v):
                if v is True:  return '<span style="color:#10b981">●</span>'
                if v is False: return '<span style="color:#374151">●</span>'
                return '<span style="color:#f59e0b">◐</span>'

            cr = s["criteria"]
            dots = (
                f'{dot(cr.get("rsi"))} RSI &nbsp;'
                f'{dot(cr.get("ema"))} EMA &nbsp;'
                f'{dot(cr.get("macd"))} MACD &nbsp;'
                f'{dot(cr.get("vol"))} Volume &nbsp;'
                f'{dot(cr.get("atr"))} ATR'
            )
            sector_safe = safe_html(s["sector"])
            sector_tag  = (
                f'<span style="background:rgba(59,130,246,.14);color:#3b82f6;border-radius:6px;'
                f'padding:2px 8px;font-size:11px">{sector_safe}</span>'
                if s["sector"] != "Unknown" else ""
            )

            col_c, col_b = st.columns([8, 1])
            with col_c:
                st.markdown(
                    f"""
                <div class="gc" style="margin-bottom:10px">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:8px">
                        <div>
                            <span style="font-size:19px;font-weight:800">{safe_html(s["sym"])}</span>
                            <span style="color:#64748b;font-size:12px;margin-left:8px">{safe_html(s["name"][:28])}</span>
                            &nbsp;{sector_tag}
                        </div>
                        <div>
                            <span style="font-size:20px;font-weight:700">₹{s["price"]:,.2f}</span>
                            <span style="color:{ch_col};margin-left:8px;font-weight:600">{'▲' if s['change']>=0 else '▼'} {s['change']:.2f}%</span>
                        </div>
                    </div>
                    <div style="font-size:13px;margin-bottom:8px">{dots}</div>
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
                        <div style="flex:1;background:rgba(255,255,255,.05);border-radius:100px;height:5px;overflow:hidden">
                            <div style="width:{sc}%;background:{sc_col};height:5px;border-radius:100px"></div>
                        </div>
                        <span style="color:{sc_col};font-weight:800;font-size:13px;font-family:'JetBrains Mono',monospace">{sc}pts</span>
                    </div>
                    <div style="display:flex;gap:20px;flex-wrap:wrap;font-size:12px;color:#64748b">
                        <span>🎯 SL ₹{s["sl"]:,.2f}</span>
                        <span>🟢 Tgt ₹{s["tgt"]:,.2f}</span>
                        <span>📊 R:R 1:{s["rr"]}</span>
                        <span>RSI {s["rsi"]} · PE {s["pe"]} · ATR {s["atr_pct"]}%</span>
                    </div>
                    <details style="margin-top:8px;cursor:pointer">
                        <summary style="color:#475569;font-size:12px">▸ Why this stock?</summary>
                        <div style="color:#94a3b8;font-size:12px;margin-top:6px;line-height:1.8">
                            {safe_html(', '.join(s["reasons"]))} · Beta {s["beta"]:.2f} · Vol {s["volr"]}x avg
                        </div>
                    </details>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            with col_b:
                if st.button("Analyze →", key=f"sc_{s['sym']}"):
                    st.session_state["selected_symbol"] = s["sym"]
                    st.session_state["analyze_triggered"] = True
                    st.rerun()
    elif st.session_state["scan_ran"]:
        st.warning("No stocks matched current filters. Try relaxing RSI range or unchecking some filters.")


# ====================================================================
# ANALYZER TAB
# ====================================================================
with tab_analyzer:

    sc1, sc2 = st.columns([5, 1])
    with sc1:
        # ── BUG FIX: pre-fill from scanner "Analyze →" button ──
        default_sym = st.session_state.get("selected_symbol") or ""
        symbol_input = st.text_input(
            "sym",
            value=default_sym,
            placeholder="🔍 NSE Symbol",
            label_visibility="collapsed",
        ).upper().strip()
    with sc2:
        st.markdown("<div style='margin-top:1px'></div>", unsafe_allow_html=True)
        search_clicked = st.button("Search", type="primary", use_container_width=True)

    # ── BUG FIX: only run analysis on explicit trigger, not every keystroke ──
    should_analyze = (
        search_clicked
        or st.session_state.get("analyze_triggered", False)
    )
    # Reset the trigger flag after consuming it
    if st.session_state.get("analyze_triggered"):
        st.session_state["analyze_triggered"] = False

    symbol = symbol_input.strip().upper()

    if symbol and should_analyze:
        st.session_state["last_symbol"] = symbol
        data = fetch_stock_data(symbol)

        tech = compute_technicals(data)
        gann_conf, angle_label, angle_color, is_squared, squaring_pct, gd = compute_gann_confluence(data)

        # ── BUG FIX: compute_sbc called once, results reused across all tabs ──
        sbc_score, sbc_label, sbc_color, stock_nak, benefic, malefic, planet_data = compute_sbc(symbol, data)
        tech_score, bull_pts, bear_pts = compute_tech_score(data, tech)
        cv_final, cv_lbl, cv_cls, cv_icon, tech_norm, gann_norm, sbc_norm = combined_verdict(tech_score, gann_conf, sbc_score)

        # ── PRICE HEADER ──
        c_col = "#10b981" if data["change_pct"] >= 0 else "#ef4444"
        st.markdown(
            f"""
        <div style="background:linear-gradient(135deg,rgba(255,255,255,0.05),rgba(255,255,255,0.01));border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:24px 28px;margin-bottom:20px;backdrop-filter:blur(12px);box-shadow:0 4px 32px rgba(0,0,0,0.5)">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <div>
                    <div style="font-size:2rem;font-weight:900;letter-spacing:-1px;background:linear-gradient(135deg,#f59e0b,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:4px">{safe_html(symbol)}</div>
                    <div style="font-size:2.6rem;font-weight:900;font-family:'JetBrains Mono',monospace;color:#e8edf5;line-height:1.1;margin-bottom:4px">₹{data["price"]:,.2f}</div>
                    <div style="color:{c_col};font-weight:700;font-size:15px">{data["change_pct"]:+.2f}%</div>
                </div>
                <div style="text-align:right">
                    <div style="color:#94a3b8;font-size:13px">RSI</div>
                    <div style="font-size:24px;font-weight:700;color:#e8edf5">{data["rsi"]}</div>
                    <div style="margin-top:8px;color:#94a3b8;font-size:13px">Volume</div>
                    <div style="font-weight:700;color:#e8edf5">{data["volume"]/1e6:.2f}M</div>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # ── QUICK METRICS ──
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        for col, (lab, val) in zip(
            [m1, m2, m3, m4, m5, m6],
            [("PE", data["pe"]), ("PB", data["pb"]),
             ("EMA21", round(tech["ema21"], 2)), ("EMA200", round(tech["ema200"], 2)),
             ("ADX", round(tech["adx"], 1)), ("ATR", round(data["atr"], 2))],
        ):
            with col:
                st.markdown(kpi(lab, val, "#38bdf8"), unsafe_allow_html=True)

        # ── TABS ──
        overview_tab, tech_tab, sbc_tab, gann_tab = st.tabs(
            ["📊 Overview", "📈 In-Depth Technical", "🔵 In-Depth SBC", "🔶 In-Depth Gann"]
        )

        # ── OVERVIEW ─────────────────────────────────────────────────────────
        with overview_tab:
            st.markdown(
                f'<div class="verdict-banner {cv_cls}">{cv_icon} {cv_lbl} — Combined Weighted Score: {cv_final}/100</div>',
                unsafe_allow_html=True,
            )
            oc1, oc2, oc3 = st.columns(3)
            trend_label = "Bullish" if tech_score > 0 else "Bearish"
            trend_col   = "#10b981" if tech_score > 0 else "#ef4444"
            with oc1:
                st.markdown(f"""
                <div class="gc gc-blue">
                    <div style="font-size:15px;font-weight:700;margin-bottom:12px">📈 Technical Snapshot</div>
                    <div style="font-size:13px;color:#cbd5e1;line-height:1">
                        <div style="padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05);display:flex;justify-content:space-between"><span style="color:#64748b">Tech Score</span><span style="font-weight:700;color:#e8edf5">{tech_score:+d}</span></div>
                        <div style="padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05);display:flex;justify-content:space-between"><span style="color:#64748b">RSI</span><span style="font-weight:700;color:#e8edf5">{data["rsi"]}</span></div>
                        <div style="padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05);display:flex;justify-content:space-between"><span style="color:#64748b">ADX</span><span style="font-weight:700;color:#e8edf5">{tech["adx"]:.1f}</span></div>
                        <div style="padding:6px 0;display:flex;justify-content:space-between"><span style="color:#64748b">Trend</span><span style="font-weight:700;color:{trend_col}">{trend_label}</span></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            with oc2:
                st.markdown(f"""
                <div class="gc gc-gold">
                    <div style="font-size:15px;font-weight:700;margin-bottom:12px">🔶 Gann Snapshot</div>
                    <div style="font-size:13px;color:#cbd5e1;line-height:1">
                        <div style="padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05);display:flex;justify-content:space-between"><span style="color:#64748b">Confluence</span><span style="font-weight:700;color:#e8edf5">{gann_conf}/5</span></div>
                        <div style="padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05);display:flex;justify-content:space-between"><span style="color:#64748b">Active Cycle</span><span style="font-weight:700;color:#e8edf5">{gd["active_cycle"]}d</span></div>
                        <div style="padding:6px 0;display:flex;justify-content:space-between"><span style="color:#64748b">Angle</span><span style="font-weight:700;color:{angle_color}">{angle_label}</span></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            sbc_val_col = "#10b981" if sbc_score >= 62 else "#f59e0b" if sbc_score >= 48 else "#ef4444"
            with oc3:
                st.markdown(f"""
                <div class="gc gc-purple">
                    <div style="font-size:15px;font-weight:700;margin-bottom:12px">🔵 SBC Snapshot</div>
                    <div style="font-size:13px;color:#cbd5e1;line-height:1">
                        <div style="padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05);display:flex;justify-content:space-between"><span style="color:#64748b">SBC Score</span><span style="font-weight:700;color:{sbc_val_col}">{sbc_score}</span></div>
                        <div style="padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05);display:flex;justify-content:space-between"><span style="color:#64748b">Label</span><span style="font-weight:700;color:{sbc_val_col}">{sbc_label}</span></div>
                        <div style="padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05);display:flex;justify-content:space-between"><span style="color:#64748b">Benefic</span><span style="font-weight:700;color:#10b981">{benefic}</span></div>
                        <div style="padding:6px 0;display:flex;justify-content:space-between"><span style="color:#64748b">Malefic</span><span style="font-weight:700;color:#ef4444">{malefic}</span></div>
                    </div>
                </div>""", unsafe_allow_html=True)

        # ── TECHNICAL TAB ────────────────────────────────────────────────────
        with tech_tab:
            price_t = data["price"]
            tech_cards = [
                ("1. Price Action & Structure",
                 f"₹{price_t:,.2f} ({'+' if data['change_pct']>=0 else ''}{data['change_pct']:.2f}% today). "
                 f"{'Higher highs/lows — uptrend.' if data['change_pct']>0 else 'Flat/declining structure.'} "
                 f"Beta {data['beta']:.2f}. ATR ₹{data['atr']} ({data['atr_pct']}%) daily range.", "gc-blue"),
                ("2. Pivots & S/R",
                 f"Pivot ₹{tech['pivot']:,.2f} | R1 ₹{tech['r1']:,.2f} | R2 ₹{tech['r2']:,.2f} | S1 ₹{tech['s1']:,.2f} | S2 ₹{tech['s2']:,.2f}. "
                 f"Price {'above pivot — bullish bias.' if price_t>tech['pivot'] else 'below pivot — bearish bias.'} "
                 f"CPR ₹{round(tech['r1']-tech['s1'],2)} — {'narrow: breakout likely.' if (tech['r1']-tech['s1'])/price_t<0.015 else 'wide: consolidation.'}", "gc-cyan"),
                ("3. Volume",
                 f"{data['volume']:,} vs 20-day avg {tech['vol20']:,} ({tech['volr']}x). "
                 f"{'🔥 Above avg — institutional confirmation.' if tech['volr']>1.5 else '⚠️ Below avg — low conviction.' if tech['volr']<0.8 else '✅ Near-average — steady.'}", "gc-green"),
                ("4. Trend (ADX)",
                 f"ADX {tech['adx']} | +DI {tech['di_pos']} | −DI {tech['di_neg']}. "
                 f"{'Strong trend.' if tech['adx']>25 else 'Weak/sideways — avoid breakout trades.' if tech['adx']<20 else 'Moderate trend.'} "
                 f"+DI {'dominant — bullish.' if tech['di_pos']>tech['di_neg'] else '< −DI — bearish.'}", "gc-gold"),
                ("5. EMAs (9/21/55/200)",
                 f"EMA9 ₹{tech['ema9']:,.2f} | EMA21 ₹{tech['ema21']:,.2f} | EMA55 ₹{tech['ema55']:,.2f} | EMA200 ₹{tech['ema200']:,.2f}. "
                 f"{'✅ Above all EMAs — full bull alignment.' if price_t>tech['ema200'] and price_t>tech['ema55'] else '⚠️ Below EMA55/200 — bounce in downtrend.' if price_t<tech['ema55'] else '⚡ Above EMA9/21/55 — watch EMA200.'} "
                 f"9/21 gap {'expanding — momentum rising.' if tech['ema9']>tech['ema21'] else 'compressing.'}", "gc-purple"),
                ("6. RSI / MACD / Stoch",
                 f"RSI {data['rsi']} — {'⚠️ Overbought.' if data['rsi']>70 else '✅ Oversold — bounce.' if data['rsi']<35 else '✅ Healthy.' if data['rsi']<60 else '⚡ Near overbought.'}. "
                 f"MACD {tech['macd_val']} / Sig {tech['macd_sig']} / Hist {tech['macd_hist']:+.2f} — {'Bullish ✅' if tech['macd_hist']>0 else 'Bearish ⚠️'}. "
                 f"Stoch %K {tech['stoch_k']} / %D {tech['stoch_d']} — {'Overbought.' if tech['stoch_k']>80 else 'Oversold.' if tech['stoch_k']<20 else 'Neutral.'}", "gc-blue"),
                ("7. Bollinger Bands",
                 f"Upper ₹{tech['bb_upper']:,.2f} | Mid ₹{tech['bb_mid']:,.2f} | Lower ₹{tech['bb_lower']:,.2f}. "
                 f"Width ₹{round(tech['bb_upper']-tech['bb_lower'],2)} — "
                 f"{'Expanding: move in progress.' if (tech['bb_upper']-tech['bb_lower'])/tech['bb_mid']>0.06 else 'Squeeze — explosive move imminent.'}. "
                 f"Price {'near upper — momentum, watch wicks.' if price_t>tech['bb_mid']+(tech['bb_upper']-tech['bb_mid'])*.7 else 'near lower — oversold bounce.' if price_t<tech['bb_mid']-(tech['bb_mid']-tech['bb_lower'])*.7 else 'near mid — consolidation.'}", "gc-cyan"),
                ("8. Volatility & Valuation",
                 f"ATR {data['atr_pct']}%. Beta {data['beta']:.2f}. SL buffer: ₹{round(data['atr']*1.5,2)} (1.5×ATR). "
                 f"PE {data['pe']} | PB {data['pb']}. "
                 f"{'Stretched PE >40.' if data['pe']>40 else 'Reasonable PE <25 ✅.' if data['pe']<25 else 'Moderate PE.'} "
                 f"VIX <15 = low fear (good for longs), >20 = caution.", "gc-gold"),
            ]
            for i in range(0, len(tech_cards), 2):
                ca, cb = st.columns(2)
                for col, (title, body, gc_cls) in zip([ca, cb], tech_cards[i:i+2]):
                    with col:
                        st.markdown(
                            f'<div class="gc {gc_cls}"><div style="font-size:14px;font-weight:700;margin-bottom:8px">{title}</div>'
                            f'<div style="color:#94a3b8;line-height:1.75;font-size:13px">{body}</div></div>',
                            unsafe_allow_html=True,
                        )

            st.markdown("---")
            st.markdown("#### 🏁 Technical Analysis — Final Verdict")
            ts = tech_score
            if ts >= 6:    tlbl, tcls, tsub = "STRONG BUY",      "vb-buy",     "Multiple factors aligned."
            elif ts >= 3:  tlbl, tcls, tsub = "BUY / ACCUMULATE","vb-buy",     "Majority bullish. Enter on dips with stop below key EMA."
            elif ts >= 1:  tlbl, tcls, tsub = "CAUTIOUS BUY",    "vb-caution", "Mixed signals. Wait for volume confirmation before entry."
            elif ts >= -1: tlbl, tcls, tsub = "NEUTRAL — WAIT",  "vb-caution", "No clear edge. Stay sidelines until cleaner setup."
            elif ts >= -3: tlbl, tcls, tsub = "AVOID / REDUCE",  "vb-avoid",   "More bearish than bullish. Hold off fresh longs."
            else:          tlbl, tcls, tsub = "STRONG AVOID",    "vb-avoid",   "Majority of indicators bearish. Do not initiate longs."

            tv1, tv2, tv3 = st.columns([1, 2, 2])
            with tv1:
                ts_col = "#10b981" if ts > 0 else "#ef4444"
                st.markdown(
                    f'<div class="gc" style="text-align:center"><div class="kpi-label">TECH SCORE</div>'
                    f'<div style="font-size:56px;font-weight:900;font-family:JetBrains Mono,monospace;color:{ts_col}">{ts:+d}</div>'
                    f'<div class="verdict-banner {tcls}" style="font-size:13px;padding:8px 12px;margin-top:8px">{tlbl}</div></div>',
                    unsafe_allow_html=True,
                )
            with tv2:
                bh = "".join([f'<div class="lc lc-green" style="font-size:12px;margin-bottom:5px">{p}</div>' for p in bull_pts]) or '<div style="color:#475569">None</div>'
                st.markdown(f'<div class="gc gc-green"><div style="font-weight:700;color:#10b981;margin-bottom:8px">✅ Bullish</div>{bh}</div>', unsafe_allow_html=True)
            with tv3:
                bea = "".join([f'<div class="lc lc-red" style="font-size:12px;margin-bottom:5px">{p}</div>' for p in bear_pts]) or '<div style="color:#475569">None</div>'
                st.markdown(f'<div class="gc gc-red"><div style="font-weight:700;color:#ef4444;margin-bottom:8px">❌ Bearish</div>{bea}</div>', unsafe_allow_html=True)

            # ── BUG FIX: single ATR trade plan block ──
            sl_tp  = round(price_t - data["atr"] * 1.5, 2)
            t1_tp  = round(price_t + data["atr"] * 3,   2)
            t2_tp  = round(price_t + data["atr"] * 5,   2)
            rr_tp  = round((t1_tp - price_t) / max(price_t - sl_tp, 0.01), 1)
            rr_col = "#10b981" if rr_tp >= 3 else "#f59e0b"
            st.markdown(
                f"""<div class="gc gc-gold"><div style="font-weight:700;margin-bottom:10px">📋 ATR-Based Trade Plan</div>
                <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px;text-align:center;font-size:12px">
                    <div><div class="kpi-label">Entry Zone</div><div style="color:#e8edf5;font-weight:700">₹{round(price_t-data['atr']*.3,2):,.2f}–₹{round(price_t+data['atr']*.3,2):,.2f}</div></div>
                    <div><div class="kpi-label">Stop (1.5×ATR)</div><div style="color:#ef4444;font-weight:700">₹{sl_tp:,.2f}</div></div>
                    <div><div class="kpi-label">Target 1 (3×ATR)</div><div style="color:#10b981;font-weight:700">₹{t1_tp:,.2f}</div></div>
                    <div><div class="kpi-label">Target 2 (5×ATR)</div><div style="color:#10b981;font-weight:700">₹{t2_tp:,.2f}</div></div>
                    <div><div class="kpi-label">R:R</div><div style="color:{rr_col};font-weight:700">1:{rr_tp}</div></div>
                </div></div>""",
                unsafe_allow_html=True,
            )

        # ── GANN TAB ─────────────────────────────────────────────────────────
        with gann_tab:
            price = data["price"]
            gk1, gk2, gk3, gk4, gk5 = st.columns(5)
            for col, (lbl, val, clr) in zip(
                [gk1, gk2, gk3, gk4, gk5],
                [("Price", f"₹{price:,.2f}", "#f59e0b"),
                 ("Sq9 Root", str(gd["sq9_root"]), "#8b5cf6"),
                 ("Anchor Low", f"₹{gd['anchor_low']:,.2f}", "#3b82f6"),
                 ("Days Low", str(gd["days_from_low"]), "#f59e0b"),
                 ("√Days", str(gd["sqrt_days"]), "#10b981")],
            ):
                with col:
                    st.markdown(kpi(lbl, val, clr), unsafe_allow_html=True)

            gs1, gs2 = st.columns(2)
            with gs1:
                st.markdown(
                    f"""<div class="gc gc-blue"><div style="color:#f59e0b;font-weight:700;margin-bottom:6px">📌 Step 1: Anchors</div>
                    <div style="font-size:13px;color:#94a3b8;line-height:2">
                    🔽 Swing Low: <b style="color:#3b82f6">₹{gd['anchor_low']:,.2f}</b> · {gd['anchor_low_date'].strftime('%d %b %Y')}<br>
                    🔼 Swing High: <b style="color:#ef4444">₹{gd['anchor_high']:,.2f}</b> · {gd['anchor_high_date'].strftime('%d %b %Y')}<br>
                    HL Range: <b style="color:#e8edf5">₹{gd['hl_range']:,.2f}</b> · √Range: <b style="color:#e8edf5">{gd['range_sqrt']}</b><br>
                    Range Sq Target: <b style="color:#10b981">₹{gd['range_sq_target']:,.2f}</b>
                    </div></div>""",
                    unsafe_allow_html=True,
                )
            with gs2:
                st.markdown(
                    f"""<div class="gc gc-gold"><div style="color:#f59e0b;font-weight:700;margin-bottom:6px">⏰ Step 2: Time Elapsed</div>
                    <div style="font-size:13px;color:#94a3b8;line-height:2">
                    Days from Low: <b style="color:#f59e0b;font-size:18px">{gd['days_from_low']}</b><br>
                    √{gd['days_from_low']} = <b style="color:#10b981">{gd['sqrt_days']}</b><br>
                    Next perfect square: <b style="color:#f59e0b">{gd['next_sq']} days</b> → {(gd['anchor_low_date']+timedelta(days=gd['next_sq'])).strftime('%d %b %Y')} ({gd['days_to_next']} days away)
                    </div></div>""",
                    unsafe_allow_html=True,
                )

            n_prev   = int(math.sqrt(gd["days_from_low"]))
            prev_sq  = n_prev ** 2
            pct_thru = round((gd["days_from_low"] - prev_sq) / max(gd["next_sq"] - prev_sq, 1) * 100, 1)
            sq3c     = "#10b981" if gd["days_to_next"] <= 5 else "#f59e0b" if gd["days_to_next"] <= 15 else "#64748b"
            st.markdown(
                f"""<div class="gc gc-purple"><div style="color:#f59e0b;font-weight:700;margin-bottom:6px">🔢 Step 3: Square of Time</div>
                <div style="font-size:13px;color:#94a3b8;line-height:2">
                Previous: <b style="color:#e8edf5">{n_prev}²={prev_sq} days</b> · Current: <b style="color:{sq3c}">{pct_thru}% through window</b><br>
                Next: <b style="color:{sq3c}">{int(math.sqrt(gd['next_sq']))}²={gd['next_sq']} days</b> → {(gd['anchor_low_date']+timedelta(days=gd['next_sq'])).strftime('%d %b %Y')} ({gd['days_to_next']} days)
                <br><span style="color:#f59e0b">{"⚡ APPROACHING perfect square!" if gd['days_to_next']<=7 else "Monitor ±3-7 days around the square date."}</span>
                </div></div>""",
                unsafe_allow_html=True,
            )

            st.markdown('<div style="font-size:13px;font-weight:700;color:#f59e0b;margin:16px 0 8px">⏱️ Step 4: Natural Time Divisions</div>', unsafe_allow_html=True)
            td1, td2 = st.columns(2)
            with td1:
                st.markdown("**Gann Natural Cycles**")
                for t, fd, da in gd["gann_future"]:
                    is_maj = t in [45, 90, 180, 360]
                    cls    = "lc-gold" if is_maj else "lc-blue"
                    tag    = ' <span style="color:#f59e0b;font-size:10px">★MAJOR</span>' if is_maj else ""
                    st.markdown(
                        f'<div class="lc {cls}" style="font-size:12px;margin-bottom:5px"><b style="color:#f59e0b">{t}d</b> → {fd.strftime("%d %b %Y")} <span style="color:#475569">({da}d away)</span>{tag}</div>',
                        unsafe_allow_html=True,
                    )
            with td2:
                st.markdown("**Perfect Squares & Anniversaries**")
                for d_sq, sd, da, nv in gd["sq_dates"][:5]:
                    st.markdown(
                        f'<div class="lc lc-purple" style="font-size:12px;margin-bottom:5px"><b style="color:#8b5cf6">{nv}²={d_sq}d</b> → {sd.strftime("%d %b %Y")} <span style="color:#475569">({da}d)</span></div>',
                        unsafe_allow_html=True,
                    )
                for yr, ad, da in gd["anniv_dates"][:3]:
                    st.markdown(
                        f'<div class="lc lc-green" style="font-size:12px;margin-bottom:5px"><b style="color:#10b981">{yr}yr</b> → {ad.strftime("%d %b %Y")} <span style="color:#475569">({da}d)</span></div>',
                        unsafe_allow_html=True,
                    )

            st.markdown('<div style="font-size:13px;font-weight:700;color:#f59e0b;margin:16px 0 8px">🌀 Step 5: Square of Nine — Price Levels</div>', unsafe_allow_html=True)
            st.dataframe(
                pd.DataFrame(gd["sq_levels"], columns=["Level", "Price (₹)", "Note"]),
                use_container_width=True, hide_index=True,
            )

            sq_col = "#10b981" if is_squared else "#f59e0b"
            st.markdown(
                f"""<div class="gc {'gc-green' if is_squared else 'gc-gold'}"><div style="color:#f59e0b;font-weight:700;margin-bottom:6px">⚖️ Step 6: Price Squared with Time</div>
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px">
                <div style="font-size:13px;color:#94a3b8;line-height:2">
                P=₹{price:,.2f} · t={gd['days_from_low']}d · √P={gd['time_sq_of_price']}d · Deviation: <b style="color:{sq_col}">{squaring_pct}%</b> {"✅ <5%" if is_squared else "⚠️ >5%"}<br>
                Anchor √Price: {gd['anchor_sq9_root']} → +2 ring: <b style="color:#10b981">₹{round((gd['anchor_sq9_root']+2)**2,2):,.2f}</b>
                </div>
                <div class="verdict-banner {'vb-buy' if is_squared else 'vb-caution'}" style="font-size:13px;padding:10px 16px;margin:0">{"🟢 SQUARED" if is_squared else "🟡 NOT SQUARED"}</div>
                </div></div>""",
                unsafe_allow_html=True,
            )

            ga1, ga2 = st.columns([2, 1])
            with ga1:
                st.markdown('<div style="font-size:13px;font-weight:700;color:#f59e0b;margin:16px 0 8px">📐 Step 7: Gann Angles</div>', unsafe_allow_html=True)
                st.dataframe(
                    pd.DataFrame([
                        ["4×1", f"₹{gd['angle_4x1']:,.2f}", "4 pts/day"],
                        ["2×1", f"₹{gd['angle_2x1']:,.2f}", "2 pts/day"],
                        ["1×1 ★", f"₹{gd['angle_1x1']:,.2f}", "1 pt/day — master angle"],
                        ["1×2", f"₹{gd['angle_1x2']:,.2f}", "0.5 pts/day — bear zone"],
                    ], columns=["Angle", "Level", "Meaning"]),
                    use_container_width=True, hide_index=True,
                )
            with ga2:
                st.markdown(
                    f'<div class="gc gc-gold" style="text-align:center;margin-top:32px"><div class="kpi-label">Current Angle</div>'
                    f'<div style="font-size:14px;font-weight:800;color:{angle_color};margin:8px 0">{angle_label}</div>'
                    f'<div style="color:#475569;font-size:12px">{round(gd["current_rate"],3)} pts/day</div></div>',
                    unsafe_allow_html=True,
                )

            hl_r  = gd["hl_range"]
            r_proj = (gd["anchor_low_date"] + timedelta(days=round(hl_r))).strftime("%d %b %Y")
            st.markdown(
                f"""<div class="gc gc-cyan"><div style="color:#f59e0b;font-weight:700;margin-bottom:6px">📏 Step 8: Range Squaring</div>
                <div style="font-size:13px;color:#94a3b8;line-height:2">
                HL Range ₹{hl_r:,.2f} · √Range {gd['range_sqrt']} · Time proj: {round(hl_r)}d → {r_proj}<br>
                Range Sq Target: <b style="color:#10b981;font-size:16px">₹{gd['range_sq_target']:,.2f}</b></div></div>""",
                unsafe_allow_html=True,
            )

            cg1, cg2 = st.columns([1, 2])
            with cg1:
                conf_c = "#10b981" if gann_conf >= 3 else "#f59e0b" if gann_conf >= 2 else "#ef4444"
                st.markdown(
                    f'<div class="gc" style="text-align:center"><div class="kpi-label">🎯 Step 9: Confluence</div>'
                    f'<div style="font-size:64px;font-weight:900;font-family:JetBrains Mono,monospace;color:{conf_c}">{gann_conf}/5</div>'
                    f'{pb(gann_conf,5,conf_c)}'
                    f'<div style="color:{conf_c};font-weight:700">{"🔥 HIGH PROB" if gann_conf>=3 else "⚡ MODERATE" if gann_conf>=2 else "⏳ LOW"}</div></div>',
                    unsafe_allow_html=True,
                )
            with cg2:
                r_html = "".join([
                    f'<div class="lc lc-{"green" if "✅" in r else "blue"}" style="font-size:12px;margin-bottom:5px">{r}</div>'
                    for r in gd["reasons"]
                ])
                st.markdown(
                    f'<div class="gc gc-gold"><div style="color:#f59e0b;font-weight:700;margin-bottom:8px">Active Confluences:</div>{r_html}'
                    f'<div style="color:#475569;font-size:11px;margin-top:8px">Min 2 confluences + volume + 1:3 R:R before entry.</div></div>',
                    unsafe_allow_html=True,
                )

            gv_rr  = round((gd["gann_t1"] - price) / max(price - gd["gann_sl"], 0.01), 2)
            gv_cls = "vb-buy" if gann_conf >= 3 and gd["current_rate"] >= 0.8 else "vb-caution" if gann_conf >= 2 else "vb-avoid"
            gv_txt = ("STRONG SETUP" if gann_conf >= 3 and gd["current_rate"] >= 0.8
                      else "WAIT — MORE CONFLUENCE NEEDED" if gann_conf >= 2
                      else "AVOID — CYCLES NOT ALIGNED")
            st.markdown(
                f"""<div class="gc gc-gold"><div class="verdict-banner {gv_cls}" style="margin-bottom:14px">🔶 {gv_txt}</div>
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:12px">
                    <div class="lc lc-blue" style="font-size:12px">📍 Anchor Low<br>₹{gd['anchor_low']:,.2f} · {gd['anchor_low_date'].strftime('%d %b %Y')}</div>
                    <div class="lc lc-gold" style="font-size:12px">📐 Gann Angle<br>{angle_label}</div>
                    <div class="lc {'lc-green' if is_squared else 'lc-gold'}" style="font-size:12px">⚖️ Price-Time<br>{"✅ Squared" if is_squared else "⚠️ Not Squared"} ({squaring_pct}%)</div>
                    <div class="lc lc-green" style="font-size:12px">🎯 T1: ₹{gd['gann_t1']:,.2f}</div>
                    <div class="lc lc-blue"  style="font-size:12px">🎯 T2: ₹{gd['gann_t2']:,.2f}</div>
                    <div class="lc lc-red"   style="font-size:12px">🛑 SL: ₹{gd['gann_sl']:,.2f}</div>
                </div>
                <div style="font-size:12px;color:#64748b">R:R 1:{gv_rr} {"✅" if gv_rr>=3 else "⚠️"} · Sq9 {gd['sq9_root']} · Range target ₹{gd['range_sq_target']:,.2f}</div>
                </div>""",
                unsafe_allow_html=True,
            )

        # ── SBC TAB ──────────────────────────────────────────────────────────
        with sbc_tab:
            # ── BUG FIX: reuse already-computed sbc values, no second call ──
            st.markdown(
                f'<div class="sec-title">🔵 Sarvatobhadra Chakra — {safe_html(symbol)} · {safe_html(stock_nak)} Nakshatra</div>',
                unsafe_allow_html=True,
            )
            st.caption(f"✅ Full 6-Layer SBC • Strict Layer 5 • {datetime.now().strftime('%d %b %Y')}")

            sb1, sb2, sb3 = st.columns(3)
            with sb1:
                st.markdown(
                    f'<div class="gc gc-purple" style="text-align:center"><div class="kpi-label">SBC Score</div>'
                    f'<div class="score-ring" style="color:{sbc_color}">{sbc_score}</div>'
                    f'<div style="color:{sbc_color};font-weight:700">{sbc_label}</div></div>',
                    unsafe_allow_html=True,
                )
            with sb2:
                st.markdown(
                    f'<div class="gc gc-green" style="text-align:center"><div class="kpi-label">Benefic</div>'
                    f'<div class="score-ring" style="color:#10b981">{benefic}</div></div>',
                    unsafe_allow_html=True,
                )
            with sb3:
                st.markdown(
                    f'<div class="gc gc-red" style="text-align:center"><div class="kpi-label">Malefic</div>'
                    f'<div class="score-ring" style="color:#ef4444">{malefic}</div></div>',
                    unsafe_allow_html=True,
                )

            st.markdown("#### Planetary Impact Analysis — Full 6 Layers")
            for i in range(0, len(planet_data), 4):
                cols = st.columns(4)
                for j, (name, sign, nak, vedha, placement, house_type,
                         drishti, special, sector_match, impact, weight) in enumerate(planet_data[i:i+4]):
                    color  = "#10b981" if weight > 0 else "#ef4444" if weight < 0 else "#f59e0b"
                    gc_cls = "gc-green" if weight > 1 else "gc-red" if weight < -1 else "gc-gold"
                    with cols[j]:
                        st.markdown(
                            f"""<div class="gc {gc_cls}">
                            <div style="font-size:22px;margin-bottom:4px">{safe_html(name)}</div>
                            <div style="color:#475569;font-size:11px">{safe_html(sign)} · {safe_html(nak)}</div>
                            <div style="color:{color};font-weight:700;margin:8px 0 4px">{safe_html(vedha)}</div>
                            <div style="font-size:12px;color:#64748b;margin-bottom:4px">
                                {safe_html(placement)} • {safe_html(house_type)} • {safe_html(drishti)}<br>
                                <span style="color:#f59e0b">{safe_html(special)}</span><br>
                                <span style="color:#8b5cf6">{safe_html(sector_match)}</span>
                            </div>
                            <div style="color:#94a3b8;line-height:1.6;font-size:12.5px">{safe_html(impact)}</div>
                            </div>""",
                            unsafe_allow_html=True,
                        )

    elif symbol and not should_analyze:
        st.info("Press **Search** to analyze this symbol.")
    else:
        st.markdown(
            '<div style="color:#475569;text-align:center;padding:40px 0">Enter an NSE symbol above and press Search</div>',
            unsafe_allow_html=True,
        )

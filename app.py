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


def _strip_timezone(hist):
    """Robustly strip timezone info from a DataFrame index."""
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


# ====================== NIFTY 500 FETCH ======================================
@st.cache_data(ttl=86400, show_spinner=False)
def fetch_nifty500_symbols():
    """
    Fetch Nifty 500 constituent symbols from NSE's public CSV.
    Falls back to a deduplicated hardcoded list if the endpoint is unreachable.
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
        symbols = df["Symbol"].dropna().str.strip().tolist()
        if len(symbols) > 100:
            # Deduplicate while preserving order
            seen = set()
            unique = []
            for s in symbols:
                if s not in seen:
                    seen.add(s)
                    unique.append(s)
            return unique
    except Exception:
        pass

    # ── Fallback: deduplicated Nifty 500 symbols ─────────────────────────────
    raw = [
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
        "LAURUSLABS","PFIZER","ABBOTINDIA","GLAXO","AJANTPHARM",
        # Auto & Ancillaries
        "TVSMOTOR","ASHOKLEY","MOTHERSON","BOSCHLTD","BHARATFORG","SUPRAJIT",
        "APOLLOTYRE","MRF","CEATLTD","BALKRISIND","ENDURANCE","SUNDRMFAST",
        "EXIDEIND","AMARAJABAT","WABCOINDIA","MINDAIND","GABRIEL","SUBROS",
        # FMCG / Consumer
        "MARICO","DABUR","GODREJCP","EMAMILTD","COLPAL","VBL","RADICO",
        "PGHH","JYOTHYLAB","BIKAJI","PATANJALI","VARUN","WONDERLA","DEVYANI",
        # IT / Tech
        "LTTS","CYIENT","ZENSAR","HEXAWARE","BIRLASOFT","MASTEK","NIITTECH",
        "RAMSYSTEMS","TANLA","INTELLECT","NEWGEN","NUCLEUS","TATAELXSI",
        # Metals / Mining
        "NMDC","SAIL","NATIONALUM","HINDCOPPER","GMRINFRA","WELCORP","RATNAMANI",
        "JINDALSAW","JINDALSTEL","JSPL","MOIL","VEDL","HINDZINC","AIAENG",
        # Energy / Power
        "TORNTPOWER","TATAPOWER","ADANIGREEN","ADANIPOWER","CESC","IEX",
        "MAHAGENCO","RPOWER","SUZLON","INOXWIND","GREENKO","ACME",
        # Infra / Capital Goods
        "ENGINERSIN","NBCC","RITES","IRCON","NCC","PNCINFRA","KNRCON",
        "GPPL","MAHINDCIE","JKCEMENT","HEIDELBERG","RAMCOCEM","SHREECEM","JKIL",
        # Real Estate
        "DLF","GODREJPROP","OBEROIRLTY","PRESTIGE","PHOENIXLTD","BRIGADE","KOLTEPATIL",
        "MAHLIFE","LODHA","SUNTECK","SOBHA","ANANTRAJ","NESCO",
        # Banking extras
        "KARURVYSYA","DCBBANK","SOUTHBANK","LAKSHVILAS","TMB","EQUITASBNK","UJJIVAN",
        "SURYODAY","ESAFSFB","AUBANK","CREDITACC","AROHAN",
        # Insurance
        "STARHEALTH","NIACL","GICRE","MAXFIN",
        # Chemicals
        "ATUL","DEEPAKNITRITE","NAVINFLUOR","SUDARSCHEM","GALAXYSURF",
        "VINATIORG","NOCIL","BALCHEMICALS","TATACHEM","GNFC","GSFC","CHAMBALFERT",
        "COROMANDEL","RALLIS","PIIND","BAYER","DHANUKA","INSECTICID",
        # Textile
        "PAGEIND","RAYMOND","ARVIND","TRIDENT","VARDHMAN","GOKEX","WELSPUNIND",
        "NITIN","ALOKTEXT","SPANDEX",
        # Logistics
        "BLUEDART","MAHLOG","GATI","TCI","ALLCARGO","AEGISLOG",
        # Media / Entertainment
        "ZEEL","SUNTV","PVRINOX","INOXLEISURE","TIPS","SAREGAMA","NAZARA",
        # Telecom
        "IDEA","STLTECH","TEJAS",
        # Hotels / Travel
        "INDHOTEL","EIHHOTEL","LEMONTREE","CHALET","MAHINDHOLIDAY",
        # Miscellaneous
        "MCDOWELL-N","UNITEDSPIRITS","GLOBUSSPR","ABFRL","TRENT","VMART",
        "SHOPERSTOP","AVENUESUP","MEESHO","CARTRADE","EASEMYTRIP",
        "RATEGAIN","JUSTDIAL","INFOEDGE","MATRIMONY","INDIAMART",
        "MCLEODRUS","WESTLIFE","JUBLFOOD","SAPPHIRE","BARBEQUE",
        "EQUITAS","SPANDANA","FUSION","UJJFIN",
    ]
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for s in raw:
        if s not in seen:
            seen.add(s)
            unique.append(s)
    return unique


# ====================== DATA FETCH ===========================================
# BUG FIX 1: Removed duplicate @st.cache_data decorator
@st.cache_data(ttl=180, show_spinner=False)
def fetch_stock_data(symbol):
    try:
        tk = yf.Ticker(f"{symbol}.NS")

        hist = tk.history(period="1y", auto_adjust=True)
        if not hist.empty:
            # BUG FIX 4: Use centralized timezone stripping
            hist = _strip_timezone(hist)

        if hist.empty or len(hist) < 10:
            raise ValueError("Empty history")

        # fast_info is lightweight — doesn't require full info dict
        try:
            fi = tk.fast_info
            price = float(fi.last_price or fi.regular_market_price or hist["Close"].iloc[-1])
            prev  = float(fi.previous_close or hist["Close"].iloc[-2])
        except Exception:
            price = float(hist["Close"].iloc[-1])
            prev  = float(hist["Close"].iloc[-2])

        chg = round((price - prev) / prev * 100, 2)

        # Slower metadata — wrap separately so price never fails
        try:
            info   = tk.info
            beta   = float(info.get("beta") or 1.0)
            pe     = float(info.get("trailingPE") or 0)
            pb_val = float(info.get("priceToBook") or 3.5)
            sector = info.get("sector", "Unknown") or "Unknown"
            name   = info.get("longName", symbol) or symbol
            volume = int(info.get("volume") or hist["Volume"].iloc[-1])
        except Exception:
            beta   = 1.0
            pe     = 0.0
            pb_val = 3.5
            sector = "Unknown"
            name   = symbol
            volume = int(hist["Volume"].iloc[-1])

        pe = round(pe, 1) if pe and pe > 0 else 25.0
        pb_val = round(pb_val, 2)

        # RSI — Wilder's smoothing
        delta = hist["Close"].diff()
        g = delta.clip(lower=0).ewm(alpha=1/14, min_periods=14, adjust=False).mean()
        l = (-delta.clip(upper=0)).ewm(alpha=1/14, min_periods=14, adjust=False).mean()
        rsi_raw = 100 - 100 / (1 + g / l)
        rsi = round(float(rsi_raw.iloc[-1]), 1) if not math.isnan(rsi_raw.iloc[-1]) else 50.0

        tr = pd.concat([
            hist["High"] - hist["Low"],
            (hist["High"] - hist["Close"].shift()).abs(),
            (hist["Low"]  - hist["Close"].shift()).abs(),
        ], axis=1).max(axis=1)
        atr     = round(float(tr.rolling(14).mean().iloc[-1]), 2)
        atr_pct = round(atr / price * 100, 2) if price > 0 else 0
        w52h    = round(float(hist["High"].max()), 2)
        w52l    = round(float(hist["Low"].min()),  2)

        return dict(
            price=round(price, 2), change_pct=chg, rsi=rsi, atr=atr,
            atr_pct=atr_pct, beta=beta, volume=volume, pe=pe, pb=pb_val,
            hist=hist, source="LIVE", sector=sector, name=name,
            w52h=w52h, w52l=w52l,
        )

    except Exception as e:
        st.warning(f"⚠️ Data fetch failed for {symbol} ({e}) — using demo data")
        # BUG FIX 5: Ensure fallback has ALL keys and consistent types
        return dict(
            price=334.55, change_pct=3.46, rsi=58.4, atr=8.2, atr_pct=2.45,
            beta=1.06, volume=18310000, pe=25.0, pb=3.70,
            hist=None,           # Explicitly None so compute_technicals handles correctly
            source="DEMO", sector="Unknown", name=symbol,
            w52h=420.0, w52l=240.0,
        )


# ====================== TECHNICALS ===========================================
def compute_technicals(data):
    p = data["price"]
    if data.get("hist") is not None and len(data["hist"]) >= 20:
        h = data["hist"]
        c = h["Close"]

        # ── Moving Averages ────────────────────────────────────────────────
        ema9   = round(float(c.ewm(span=9,   adjust=False).mean().iloc[-1]), 2)
        ema21  = round(float(c.ewm(span=21,  adjust=False).mean().iloc[-1]), 2)
        ema55  = round(float(c.ewm(span=55,  adjust=False).mean().iloc[-1]), 2)
        ema200 = round(float(c.ewm(span=200, adjust=False).mean().iloc[-1]), 2)

        # ── MACD ───────────────────────────────────────────────────────────
        ml = c.ewm(span=12, adjust=False).mean() - c.ewm(span=26, adjust=False).mean()
        ms = ml.ewm(span=9, adjust=False).mean()
        macd_val  = round(float(ml.iloc[-1]), 2)
        macd_sig  = round(float(ms.iloc[-1]), 2)
        macd_hist = round(macd_val - macd_sig, 2)

        # ── Bollinger Bands ────────────────────────────────────────────────
        bm = c.rolling(20).mean()
        bs = c.rolling(20).std()
        bb_upper = round(float((bm + 2*bs).iloc[-1]), 2)
        bb_lower = round(float((bm - 2*bs).iloc[-1]), 2)
        bb_mid   = round(float(bm.iloc[-1]), 2)

        # ── Stochastic ────────────────────────────────────────────────────
        lo14 = h["Low"].rolling(14).min()
        hi14 = h["High"].rolling(14).max()
        denom = (hi14 - lo14).replace(0, np.nan)
        stoch_raw = ((c - lo14) / denom * 100)
        stoch_k = round(float(stoch_raw.iloc[-1]), 1) if not math.isnan(stoch_raw.iloc[-1]) else 50.0
        stoch_d = round(float(stoch_raw.rolling(3).mean().iloc[-1]), 1) if not math.isnan(stoch_raw.rolling(3).mean().iloc[-1]) else 50.0

        # ── Volume ────────────────────────────────────────────────────────
        vol20 = round(float(h["Volume"].rolling(20).mean().iloc[-1]))
        volr  = round(data["volume"] / max(vol20, 1), 2)

        # ── ADX System ────────────────────────────────────────────────────
        tr_s = pd.concat([
            h["High"] - h["Low"],
            (h["High"] - h["Close"].shift()).abs(),
            (h["Low"]  - h["Close"].shift()).abs(),
        ], axis=1).max(axis=1)
        atr14 = tr_s.ewm(alpha=1/14, min_periods=14, adjust=False).mean()

        # BUG FIX 2 (verified correct): Save originals before conditional zeroing
        # to avoid race condition where modifying +DM corrupts -DM comparison
        dmp_raw = h["High"].diff().clip(lower=0)
        dmn_raw = (-h["Low"].diff()).clip(lower=0)
        dmp = dmp_raw.where(dmp_raw > dmn_raw, 0)
        dmn = dmn_raw.where(dmn_raw > dmp_raw, 0)

        di_pos_s = dmp.ewm(alpha=1/14, min_periods=14, adjust=False).mean()
        di_neg_s = dmn.ewm(alpha=1/14, min_periods=14, adjust=False).mean()

        # Guard against division by zero in ADX when ATR is zero
        atr14_safe = atr14.replace(0, np.nan)
        di_pos = round(float((di_pos_s / atr14_safe * 100).iloc[-1]), 1)
        di_neg = round(float((di_neg_s / atr14_safe * 100).iloc[-1]), 1)

        if math.isnan(di_pos):
            di_pos = 0.0
        if math.isnan(di_neg):
            di_neg = 0.0

        di_pos_series = di_pos_s / atr14_safe * 100
        di_neg_series = di_neg_s / atr14_safe * 100
        dx_series = (
            (di_pos_series - di_neg_series).abs()
            / (di_pos_series + di_neg_series).clip(lower=0.01)
            * 100
        )
        adx = round(float(dx_series.ewm(alpha=1/14, min_periods=14, adjust=False).mean().iloc[-1]), 1)
        if math.isnan(adx):
            adx = 0.0

        # ── WEEKLY PIVOT (last completed week) ──────────────────────────
        h_copy = h.copy()
        h_copy.index = pd.to_datetime(h_copy.index)
        weekly = h_copy.resample("W").agg({"High": "max", "Low": "min", "Close": "last"})
        weekly = weekly.dropna()
        if len(weekly) >= 2:
            wph = round(float(weekly["High"].iloc[-2]), 2)
            wpl = round(float(weekly["Low"].iloc[-2]),  2)
            wpc = round(float(weekly["Close"].iloc[-2]), 2)
        else:
            wph = round(float(h["High"].iloc[-2]), 2)
            wpl = round(float(h["Low"].iloc[-2]),  2)
            wpc = round(float(h["Close"].iloc[-2]), 2)

        w_pivot = round((wph + wpl + wpc) / 3, 2)
        w_r1    = round(2*w_pivot - wpl, 2)
        w_s1    = round(2*w_pivot - wph, 2)
        w_r2    = round(w_pivot + (wph - wpl), 2)
        w_s2    = round(w_pivot - (wph - wpl), 2)
        w_cpr_pct = round((w_r1 - w_s1) / max(p, 0.01) * 100, 2)

        # ── MONTHLY PIVOT (last completed month) ────────────────────────
        monthly = h_copy.resample("ME").agg({"High": "max", "Low": "min", "Close": "last"})
        monthly = monthly.dropna()
        if len(monthly) >= 2:
            mph = round(float(monthly["High"].iloc[-2]), 2)
            mpl = round(float(monthly["Low"].iloc[-2]),  2)
            mpc = round(float(monthly["Close"].iloc[-2]), 2)
        else:
            mph, mpl, mpc = wph, wpl, wpc

        m_pivot = round((mph + mpl + mpc) / 3, 2)
        m_r1    = round(2*m_pivot - mpl, 2)
        m_s1    = round(2*m_pivot - mph, 2)
        m_r2    = round(m_pivot + (mph - mpl), 2)
        m_s2    = round(m_pivot - (mph - mpl), 2)
        m_cpr_pct = round((m_r1 - m_s1) / max(p, 0.01) * 100, 2)

        # ── KEY S/R: swing highs/lows + round numbers + 52W ────────────
        swing_highs = []
        swing_lows  = []
        roll_win = 10
        for i in range(roll_win, len(h) - roll_win):
            if h["High"].iloc[i] == h["High"].iloc[i-roll_win:i+roll_win].max():
                swing_highs.append(round(float(h["High"].iloc[i]), 2))
            if h["Low"].iloc[i] == h["Low"].iloc[i-roll_win:i+roll_win].min():
                swing_lows.append(round(float(h["Low"].iloc[i]), 2))

        key_res = sorted([x for x in swing_highs if x > p])[:3]
        key_sup = sorted([x for x in swing_lows  if x < p], reverse=True)[:3]

        # Round number levels within ±15% of price
        mag = 10 ** max(0, int(math.log10(max(p, 1))) - 1)
        rounds = []
        base = round(p * 0.85 / mag) * mag
        while base <= p * 1.15:
            rounds.append(round(base, 2))
            base += mag

        w52h = data["w52h"]
        w52l = data["w52l"]
        w52h_prox = round((w52h - p) / max(p, 0.01) * 100, 1)
        w52l_prox = round((p - w52l) / max(p, 0.01) * 100, 1)

    else:
        # BUG FIX 5: Consistent fallback — all fields populated with sensible defaults
        ema9 = ema21 = ema55 = ema200 = p
        macd_val = 0.0; macd_sig = 0.0; macd_hist = 0.0
        bb_upper = round(p*1.04, 2); bb_lower = round(p*0.96, 2); bb_mid = p
        stoch_k = 50.0; stoch_d = 50.0
        vol20 = data["volume"]; volr = 1.0
        di_pos = 0.0; di_neg = 0.0; adx = 0.0
        w_pivot = p; w_r1 = round(p*1.02, 2); w_s1 = round(p*0.98, 2)
        w_r2 = round(p*1.04, 2); w_s2 = round(p*0.96, 2); w_cpr_pct = 2.0
        m_pivot = p; m_r1 = round(p*1.04, 2); m_s1 = round(p*0.96, 2)
        m_r2 = round(p*1.08, 2); m_s2 = round(p*0.92, 2); m_cpr_pct = 4.0
        key_res = [round(p*1.03, 2), round(p*1.06, 2), round(p*1.10, 2)]
        key_sup = [round(p*0.97, 2), round(p*0.94, 2), round(p*0.90, 2)]
        rounds  = []
        w52h = data.get("w52h", p * 1.2); w52l = data.get("w52l", p * 0.8)
        w52h_prox = round((w52h - p) / max(p, 0.01) * 100, 1)
        w52l_prox = round((p - w52l) / max(p, 0.01) * 100, 1)

    return dict(
        ema9=ema9, ema21=ema21, ema55=ema55, ema200=ema200,
        macd_val=macd_val, macd_sig=macd_sig, macd_hist=macd_hist,
        bb_upper=bb_upper, bb_lower=bb_lower, bb_mid=bb_mid,
        stoch_k=stoch_k, stoch_d=stoch_d,
        vol20=vol20, volr=volr,
        di_pos=di_pos, di_neg=di_neg, adx=adx,
        w_pivot=w_pivot, w_r1=w_r1, w_s1=w_s1, w_r2=w_r2, w_s2=w_s2, w_cpr_pct=w_cpr_pct,
        m_pivot=m_pivot, m_r1=m_r1, m_s1=m_s1, m_r2=m_r2, m_s2=m_s2, m_cpr_pct=m_cpr_pct,
        key_res=key_res, key_sup=key_sup, rounds=rounds,
        w52h=w52h, w52l=w52l, w52h_prox=w52h_prox, w52l_prox=w52l_prox,
    )


def compute_tech_score(data, tech):
    p = data["price"]
    ts = 0
    bull = []
    bear = []

    # EMA structure
    if p > tech["ema9"] and p > tech["ema21"] and p > tech["ema55"]:
        ts += 2; bull.append("Above EMA9/21/55 — bullish structure ✅")
    elif p > tech["ema9"] and p > tech["ema21"]:
        ts += 1; bull.append("Above EMA9/21 — short-term bullish")
    else:
        ts -= 1; bear.append("Below key EMAs — bearish structure")

    # 200 EMA
    if p > tech["ema200"]:
        ts += 1; bull.append("Above 200 EMA — long-term bull ✅")
    else:
        ts -= 1; bear.append("Below 200 EMA — long-term bear risk")

    # RSI
    if 40 < data["rsi"] < 70:
        ts += 1; bull.append(f"RSI {data['rsi']} — healthy zone ✅")
    elif data["rsi"] >= 70:
        ts -= 1; bear.append(f"RSI {data['rsi']} — overbought ⚠️")
    else:
        ts += 1; bull.append(f"RSI {data['rsi']} — oversold, bounce potential ✅")

    # MACD
    if tech["macd_hist"] > 0:
        ts += 1; bull.append("MACD histogram positive ✅")
    else:
        ts -= 1; bear.append("MACD histogram negative")

    # Volume
    if tech["volr"] > 1.3:
        ts += 1; bull.append(f"Volume {tech['volr']}x avg ✅")
    elif tech["volr"] < 0.7:
        ts -= 1; bear.append("Low volume — lacks conviction")

    # ADX
    if tech["adx"] > 25 and tech["di_pos"] > tech["di_neg"]:
        ts += 1; bull.append(f"ADX {tech['adx']} strong, +DI dominant ✅")
    elif tech["adx"] > 25 and tech["di_pos"] < tech["di_neg"]:
        ts -= 1; bear.append("Strong downtrend, −DI dominant")

    # Bollinger
    if tech["bb_mid"] < p < tech["bb_upper"]:
        ts += 1; bull.append("Between mid-upper Bollinger ✅")
    elif p > tech["bb_upper"]:
        bear.append("Above upper Bollinger — extended")
    elif p < tech["bb_lower"]:
        ts += 1; bull.append("At lower Bollinger — bounce zone ✅")

    # Valuations
    if data["pe"] < 25 and data["pb"] < 4:
        ts += 1; bull.append(f"Good valuations PE {data['pe']} ✅")
    elif data["pe"] > 45:
        bear.append(f"Stretched PE {data['pe']}")

    return ts, bull, bear


# ====================== GANN (UPGRADED) ======================================
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_long_history(symbol):
    """Fetch max available history (10Y) for proper Gann anchor detection."""
    try:
        tk = yf.Ticker(f"{symbol}.NS")
        h = tk.history(period="10y")
        if h.empty:
            h = tk.history(period="5y")
        if not h.empty:
            h = _strip_timezone(h)
        return h if not h.empty else None
    except Exception:
        return None


def _find_significant_anchor(hist):
    """
    Find the most significant swing low from full history.
    Significance = lowest price with highest subsequent move.
    Returns (anchor_low_price, anchor_low_date, anchor_high_price, anchor_high_date).
    """
    if hist is None or len(hist) < 50:
        return None

    candidates = []
    win = 20
    for i in range(win, len(hist) - win):
        bar_low = float(hist["Low"].iloc[i])
        window_min = float(hist["Low"].iloc[i-win:i+win].min())
        if bar_low == window_min:
            vol = float(hist["Volume"].iloc[i])
            subsequent_high = float(hist["High"].iloc[i:].max())
            move_pct = (subsequent_high - bar_low) / max(bar_low, 1) * 100
            candidates.append((move_pct, vol, bar_low, hist.index[i]))

    if not candidates:
        idx = hist["Low"].idxmin()
        high_idx = hist["High"].idxmax()
        return (
            round(float(hist["Low"].min()), 2),
            idx.date() if hasattr(idx, "date") else idx,
            round(float(hist["High"].max()), 2),
            high_idx.date() if hasattr(high_idx, "date") else high_idx,
        )

    candidates.sort(key=lambda x: x[0], reverse=True)
    _, _, best_low, best_date = candidates[0]

    after = hist[hist.index >= best_date]
    anchor_high = round(float(after["High"].max()), 2)
    anchor_high_date = after["High"].idxmax()

    return (
        round(best_low, 2),
        best_date.date() if hasattr(best_date, "date") else best_date,
        anchor_high,
        anchor_high_date.date() if hasattr(anchor_high_date, "date") else anchor_high_date,
    )


def _sq9_levels(price):
    """
    Full 8-spoke Square of Nine levels around current price.
    Cardinals: 0°/90°/180°/270° → integer rings
    Diagonals: 45°/135°/225°/315° → half-step rings
    Returns sorted list of (label, price, spoke_type)
    """
    if price <= 0:
        return []
    root = math.sqrt(price)
    levels = []
    for offset in [-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 2.5, 3]:
        new_root = root + offset
        if new_root <= 0:
            continue
        lv_price = round(new_root ** 2, 2)
        spoke = "Cardinal" if offset == round(offset) else "Diagonal"
        direction = "Support" if offset < 0 else "Resistance"
        step_label = f"{'+' if offset > 0 else ''}{offset}"
        levels.append((f"{direction} ({step_label} {spoke})", lv_price, spoke))
    return sorted(levels, key=lambda x: x[1])


def _time_cycle_confluence(anchor_low_date, today):
    """
    Four independent time tools with same-window confluence check.

    Tool 1: Natural squares (days from anchor)
    Tool 2: Gann natural divisions (45, 90, 135, 144, 180, 225, 270, 315, 360, 450, 504, 720)
    Tool 3: Actual yearly anniversaries (calendar date matching)
    Tool 4: Seasonal / equinox-solstice cycle dates
    """
    days_from_low = (today - anchor_low_date).days
    if days_from_low < 0:
        days_from_low = 0
    window = 5

    # ── Tool 1: Natural squares ──────────────────────────────────────────────
    n = int(math.sqrt(days_from_low))
    sq_prev = n * n
    sq_next = (n + 1) * (n + 1)
    days_to_sq = sq_next - days_from_low
    t1_next_date = anchor_low_date + timedelta(days=sq_next)
    t1_prev_date = anchor_low_date + timedelta(days=sq_prev)
    t1_upcoming  = t1_next_date if days_to_sq > 0 else t1_prev_date
    tool1_active = abs((today - t1_upcoming).days) <= window

    # ── Tool 2: Gann natural divisions ──────────────────────────────────────
    gann_divs = [45, 90, 135, 144, 180, 225, 270, 315, 360, 450, 504, 720]
    t2_upcoming_dates = []
    for base in gann_divs:
        mult = 1
        while True:
            d = base * mult
            dt = anchor_low_date + timedelta(days=d)
            if dt >= today - timedelta(days=window):
                t2_upcoming_dates.append(dt)
                break
            mult += 1
            # Safety: don't loop forever
            if d > days_from_low + 720:
                break

    # Find the nearest upcoming division date
    if t2_upcoming_dates:
        t2_next_date = min(t2_upcoming_dates, key=lambda dt: abs((dt - today).days))
    else:
        t2_next_date = today + timedelta(days=90)

    tool2_active = any(abs((today - dt).days) <= window for dt in t2_upcoming_dates)

    # Track days_to_div for display
    nearest_div = min(gann_divs, key=lambda d: abs(days_from_low % d) if d > 0 else 9999)
    days_to_div = nearest_div - (days_from_low % nearest_div) if nearest_div > 0 else 9999

    # ── Tool 3: Actual yearly anniversaries ──────────────────────────────────
    t3_upcoming_date = None
    tool3_active     = False
    for yr in range(1, 15):
        try:
            anniv = anchor_low_date.replace(year=anchor_low_date.year + yr)
            days_away = (anniv - today).days
            if -window <= days_away <= window:
                tool3_active     = True
                t3_upcoming_date = anniv
                break
            if 0 < days_away <= 365:
                if t3_upcoming_date is None or days_away < (t3_upcoming_date - today).days:
                    t3_upcoming_date = anniv
        except Exception:
            pass
    if t3_upcoming_date is None:
        try:
            t3_upcoming_date = anchor_low_date.replace(year=today.year + 1)
        except Exception:
            t3_upcoming_date = today + timedelta(days=365)

    # ── Tool 4: Seasonal / equinox-solstice cycle dates ─────────────────────
    seasonal_dates_this_year = [
        date(today.year, 3, 20), date(today.year, 6, 21),
        date(today.year, 9, 22), date(today.year, 12, 21),
        date(today.year + 1, 3, 20), date(today.year + 1, 6, 21),
    ]
    tool4_active = any(abs((today - sd).days) <= window for sd in seasonal_dates_this_year)
    valid_seasonal = [sd for sd in seasonal_dates_this_year if sd >= today - timedelta(days=window)]
    if valid_seasonal:
        t4_upcoming = min(valid_seasonal, key=lambda d: abs((d - today).days))
    else:
        t4_upcoming = seasonal_dates_this_year[-1]

    # ── Same-window confluence check ────────────────────────────────────────
    upcoming = {
        "sq":       t1_upcoming,
        "div":      t2_next_date,
        "anniv":    t3_upcoming_date,
        "seasonal": t4_upcoming,
    }
    active_flags = {
        "sq":       tool1_active,
        "div":      tool2_active,
        "anniv":    tool3_active,
        "seasonal": tool4_active,
    }

    same_window_pairs = 0
    pair_labels = []
    keys = list(upcoming.keys())
    for i in range(len(keys)):
        for j in range(i+1, len(keys)):
            k1, k2 = keys[i], keys[j]
            if active_flags[k1] and active_flags[k2]:
                delta = abs((upcoming[k1] - upcoming[k2]).days)
                if delta <= window * 2:
                    same_window_pairs += 1
                    pair_labels.append(f"{k1}+{k2} within {delta}d")

    total_active = sum(active_flags.values())
    if same_window_pairs >= 3 or (same_window_pairs >= 2 and total_active >= 3):
        active_tools = 3
    elif same_window_pairs >= 1 and total_active >= 2:
        active_tools = 2
    elif total_active >= 2:
        active_tools = 1
    else:
        active_tools = 0

    details = {
        "tool1_active":    tool1_active,
        "tool2_active":    tool2_active,
        "tool3_active":    tool3_active,
        "tool4_active":    tool4_active,
        "active_tools":    active_tools,
        "same_window_pairs": same_window_pairs,
        "pair_labels":     pair_labels,
        "days_to_sq":      days_to_sq,
        "sq_prev":         sq_prev,
        "sq_next":         sq_next,
        "nearest_div":     nearest_div,
        "days_to_div":     days_to_div,
        "next_sq_date":    t1_upcoming,
        "next_div_date":   t2_next_date,
        "next_anniv_date": t3_upcoming_date,
        "next_seasonal_date": t4_upcoming,
        "days_from_low":   days_from_low,
    }
    return active_tools, details


def _build_gann_chart(hist, anchor_low, anchor_low_date, anchor_high,
                      scale, angle_1x1, angle_2x1, angle_1x2, angle_1x4,
                      sq9_levels, price, today):
    """
    Scaled Plotly chart where price and time are on the same scale.
    X-axis = days from anchor. Y-axis = price.
    Gann angles drawn as lines from anchor point.
    """
    if hist is None or len(hist) < 10:
        return None

    anchor_dt = pd.Timestamp(anchor_low_date)
    hist_after = hist[hist.index >= anchor_dt].copy()
    if hist_after.empty:
        return None

    days_arr  = [(idx - anchor_dt).days for idx in hist_after.index]
    close_arr = hist_after["Close"].tolist()
    high_arr  = hist_after["High"].tolist()
    low_arr   = hist_after["Low"].tolist()

    if not days_arr:
        return None

    max_days  = max(days_arr)
    proj_days = int(max_days * 1.20) + 1

    angle_x = list(range(0, proj_days, 1))
    def angle_y(rate):
        return [anchor_low + d * rate for d in angle_x]

    fig = go.Figure()

    # Candlestick
    fig.add_trace(go.Candlestick(
        x=days_arr,
        open=hist_after["Open"].tolist(),
        high=high_arr,
        low=low_arr,
        close=close_arr,
        name="Price",
        increasing_line_color="#10b981",
        decreasing_line_color="#ef4444",
        showlegend=False,
    ))

    # Gann angle lines
    angle_specs = [
        (scale * 4,    "4×1", "#ef4444", "dash"),
        (scale * 2,    "2×1", "#f59e0b", "dash"),
        (scale * 1,    "1×1", "#10b981", "solid"),
        (scale * 0.5,  "1×2", "#f59e0b", "dot"),
        (scale * 0.25, "1×4", "#ef4444", "dot"),
    ]
    for rate, label, color, dash in angle_specs:
        fig.add_trace(go.Scatter(
            x=angle_x,
            y=angle_y(rate),
            mode="lines",
            name=label,
            line=dict(color=color, width=1.5 if label == "1×1" else 1, dash=dash),
            opacity=0.8,
        ))

    # Sq9 horizontal levels
    for lv in sq9_levels:
        lbl, lv_price, spoke = lv
        if not isinstance(lv_price, (int, float)):
            continue
        col = "#3b82f6" if "Resistance" in lbl else "#8b5cf6" if "Support" in lbl else "#ffffff"
        fig.add_hline(
            y=lv_price,
            line_color=col,
            line_width=0.7,
            line_dash="dot",
            opacity=0.5,
            annotation_text=f"₹{lv_price:,.0f}",
            annotation_font_size=9,
            annotation_font_color=col,
        )

    # Current price line
    fig.add_hline(
        y=price,
        line_color="#ffffff",
        line_width=1,
        line_dash="solid",
        opacity=0.9,
        annotation_text=f"₹{price:,.2f}",
        annotation_font_size=10,
        annotation_font_color="#ffffff",
    )

    # Anchor point marker
    fig.add_trace(go.Scatter(
        x=[0], y=[anchor_low],
        mode="markers+text",
        marker=dict(color="#f59e0b", size=10, symbol="triangle-up"),
        text=["Anchor"], textposition="bottom center",
        textfont=dict(color="#f59e0b", size=10),
        name="Anchor Low", showlegend=False,
    ))

    fig.update_layout(
        height=520,
        paper_bgcolor="#060810",
        plot_bgcolor="#0d1117",
        font=dict(family="Space Grotesk", color="#94a3b8", size=11),
        title=dict(
            text=f"Gann Scaled Chart — 1 unit time = {scale:.4f} pts price",
            font=dict(color="#f59e0b", size=13),
        ),
        xaxis=dict(
            title="Days from Anchor Low",
            gridcolor="rgba(255,255,255,0.05)",
            zerolinecolor="rgba(255,255,255,0.1)",
            color="#64748b",
        ),
        yaxis=dict(
            title="Price (₹)",
            gridcolor="rgba(255,255,255,0.05)",
            zerolinecolor="rgba(255,255,255,0.1)",
            color="#64748b",
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", size=10),
        ),
        xaxis_rangeslider_visible=False,
        margin=dict(l=60, r=40, t=60, b=40),
    )
    return fig


def compute_gann_confluence(data, symbol=None):
    price = data["price"]
    today = datetime.now().date()

    # ── Use long history for proper anchor ──────────────────────────────────
    long_hist = None
    if symbol:
        long_hist = fetch_long_history(symbol)

    hist = long_hist if (long_hist is not None and not long_hist.empty) else data.get("hist")

    if hist is not None and len(hist) >= 50:
        anchor_result = _find_significant_anchor(hist)
        if anchor_result:
            anchor_low, anchor_low_date, anchor_high, anchor_high_date = anchor_result
        else:
            anchor_low  = round(float(hist["Low"].min()), 2)
            anchor_high = round(float(hist["High"].max()), 2)
            low_idx  = hist["Low"].idxmin()
            high_idx = hist["High"].idxmax()
            anchor_low_date  = low_idx.date()  if hasattr(low_idx, "date") else low_idx
            anchor_high_date = high_idx.date() if hasattr(high_idx, "date") else high_idx
        hl_range = round(anchor_high - anchor_low, 2)
    else:
        anchor_low       = round(price * 0.72, 2)
        anchor_high      = round(price * 1.22, 2)
        anchor_low_date  = today - timedelta(days=500)
        anchor_high_date = today - timedelta(days=90)
        hl_range         = round(anchor_high - anchor_low, 2)

    # Ensure anchor_low_date is a date object
    if isinstance(anchor_low_date, datetime):
        anchor_low_date = anchor_low_date.date()
    if isinstance(anchor_high_date, datetime):
        anchor_high_date = anchor_high_date.date()

    days_from_low  = (today - anchor_low_date).days
    days_from_high = (today - anchor_high_date).days
    days_from_low  = max(days_from_low, 1)
    days_from_high = max(days_from_high, 0)

    # ── Stock-specific scaling factor ───────────────────────────────────────
    price_range = max(anchor_high - anchor_low, 1.0)
    time_range  = max(days_from_low, 1)
    scale       = round(price_range / time_range, 4)

    # ── Calibrated Gann Angles ──────────────────────────────────────────────
    angle_4x1 = round(anchor_low + days_from_low * scale * 4,    2)
    angle_2x1 = round(anchor_low + days_from_low * scale * 2,    2)
    angle_1x1 = round(anchor_low + days_from_low * scale * 1,    2)
    angle_1x2 = round(anchor_low + days_from_low * scale * 0.5,  2)
    angle_1x4 = round(anchor_low + days_from_low * scale * 0.25, 2)

    angles = {"4×1": angle_4x1, "2×1": angle_2x1, "1×1": angle_1x1,
              "1×2": angle_1x2, "1×4": angle_1x4}
    closest_angle = min(angles, key=lambda k: abs(angles[k] - price))
    price_vs_1x1  = (price - angle_1x1) / max(angle_1x1, 1) * 100

    if price >= angle_2x1:
        angle_label = "Above 2×1 (Very Strong Bull)"; angle_color = "#10b981"
    elif price >= angle_1x1:
        angle_label = "1×1–2×1 (Bull Zone)";          angle_color = "#10b981"
    elif price >= angle_1x2:
        angle_label = "1×2–1×1 (Weak / Caution)";     angle_color = "#f59e0b"
    else:
        angle_label = "Below 1×2 (Bear)";              angle_color = "#ef4444"

    # ── Full 8-spoke Square of Nine levels ──────────────────────────────────
    sq9_all = _sq9_levels(price)
    sq9_supports    = [(l, p2, s) for l, p2, s in sq9_all if p2 < price]
    sq9_resistances = [(l, p2, s) for l, p2, s in sq9_all if p2 > price]
    sq9_s1  = sq9_supports[-1]    if sq9_supports    else ("—", price, "—")
    sq9_s2  = sq9_supports[-2]    if len(sq9_supports) >= 2    else sq9_s1
    sq9_r1  = sq9_resistances[0]  if sq9_resistances  else ("—", price, "—")
    sq9_r2  = sq9_resistances[1]  if len(sq9_resistances) >= 2 else sq9_r1

    gann_t1 = sq9_r1[1]
    gann_t2 = sq9_r2[1]
    gann_sl = sq9_s2[1]

    # Build display table
    sq_levels_display = [["⚪ Current", price, "—"]]
    for l, p2, s in sq9_supports[-3:]:
        sq_levels_display.append([f"🔴 {l}", p2, s])
    for l, p2, s in sq9_resistances[:3]:
        sq_levels_display.append([f"🟢 {l}", p2, s])
    sq_levels_display = sorted(sq_levels_display, key=lambda x: x[1])

    # ── Time cycle confluence ───────────────────────────────────────────────
    active_tools, cycle_details = _time_cycle_confluence(anchor_low_date, today)
    sqrt_days    = round(math.sqrt(days_from_low), 4)
    n_low        = int(sqrt_days)
    nearest_sq   = n_low * n_low
    next_sq      = (n_low + 1) * (n_low + 1)
    days_to_next = next_sq - days_from_low

    # ── Strict confluence scoring ───────────────────────────────────────────
    sq9_prices = [p2 for _, p2, _ in sq9_all]
    if sq9_prices:
        nearest_sq9_price = min(sq9_prices, key=lambda x: abs(x - price))
    else:
        nearest_sq9_price = price
    price_sq9_dev = abs(nearest_sq9_price - price) / max(price, 0.01) * 100
    at_sq9_tight    = price_sq9_dev <= 0.5
    at_sq9_moderate = price_sq9_dev <= 1.5

    at_1x1 = abs(price - angle_1x1) / max(price, 0.01) * 100 <= 1.0

    time_strong   = active_tools >= 3
    time_moderate = active_tools >= 2

    confluence = 0
    reasons    = []

    if at_sq9_tight and at_1x1 and time_strong:
        confluence = 5
        reasons.append("🔥 TIER 1: Sq9 tight (±0.5%) + 1×1 angle + 3/3 time tools")
    elif (at_sq9_tight or at_sq9_moderate) and time_strong:
        confluence = 4
        reasons.append("✅ TIER 2: Sq9 level + strong time cycle (3 tools)")
    elif at_sq9_tight and (at_1x1 or time_moderate):
        confluence = 4
        reasons.append("✅ TIER 2: Sq9 tight + angle/time confluence")
    elif at_sq9_moderate and time_moderate:
        confluence = 3
        reasons.append("✅ TIER 3: Sq9 moderate (±1.5%) + 2/3 time tools")
    elif at_sq9_moderate or time_moderate or at_1x1:
        confluence = 2
        reasons.append("⚡ TIER 4: Single confluence — wait for more alignment")
    else:
        confluence = 1
        reasons.append("⚪ No meaningful confluence — price between levels, time between cycles")

    reasons.append(f"   Sq9 nearest ₹{nearest_sq9_price:,.2f} · deviation {price_sq9_dev:.2f}%")
    reasons.append(f"   1×1 angle ₹{angle_1x1:,.2f} · price deviation {abs(price_vs_1x1):.1f}%")
    sw = cycle_details["same_window_pairs"]
    pair_info = " · ".join(cycle_details["pair_labels"]) if cycle_details["pair_labels"] else "no pairs in same window"
    reasons.append(f"   Time tools active: {active_tools}/3 · Same-window pairs: {sw} ({pair_info})")

    # Upcoming dates
    gann_time_units = [45, 90, 135, 144, 180, 225, 270, 315, 360, 450, 504, 720]
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
    for yr in [1, 2, 3, 5, 7, 10]:
        try:
            ad = anchor_low_date.replace(year=anchor_low_date.year + yr)
            if ad >= today:
                anniv_dates.append((yr, ad, (ad - today).days))
        except Exception:
            pass

    # Price-time squaring
    scaled_time  = days_from_low * scale
    squaring_pct = round(abs(price - scaled_time) / max(price, 0.01) * 100, 1)
    is_squared   = squaring_pct < 3.0

    anchor_sq9_root = round(math.sqrt(max(anchor_low, 0.01)), 4)
    range_sqrt      = round(math.sqrt(max(hl_range, 0.01)), 4)
    range_sq_target = round((math.ceil(range_sqrt) + 1) ** 2, 2)
    active_cycle    = next((t for t in gann_time_units if days_from_low <= t), 720)

    # BUG FIX 3: Complete the truncated return statement
    return (
        confluence, angle_label, angle_color, is_squared, squaring_pct,
        dict(
            # Anchor
            anchor_low=anchor_low, anchor_high=anchor_high,
            anchor_low_date=anchor_low_date, anchor_high_date=anchor_high_date,
            days_from_low=days_from_low, days_from_high=days_from_high,
            hl_range=hl_range,
            # Scale
            scale=scale,
            # Angles (calibrated)
            angle_4x1=angle_4x1, angle_2x1=angle_2x1, angle_1x1=angle_1x1,
            angle_1x2=angle_1x2, angle_1x4=angle_1x4,
            closest_angle=closest_angle, price_vs_1x1=round(price_vs_1x1, 1),
            # Sq9
            sq9_root=round(math.sqrt(max(price, 0.01)), 4),
            sq9_s1=sq9_s1, sq9_s2=sq9_s2, sq9_r1=sq9_r1, sq9_r2=sq9_r2,
            nearest_sq9_price=nearest_sq9_price, price_sq9_dev=price_sq9_dev,
            sq_levels=sq_levels_display,
            # Targets / SL
            gann_t1=gann_t1, gann_t2=gann_t2, gann_sl=gann_sl,
            # Time
            sqrt_days=sqrt_days, n_low=n_low,
            nearest_sq=nearest_sq, next_sq=next_sq, days_to_next=days_to_next,
            cycle_details=cycle_details, active_tools=active_tools,
            # Upcoming dates
            gann_future=gann_future, sq_dates=sq_dates, anniv_dates=anniv_dates,
            # Price-time squaring
            scaled_time=round(scaled_time, 2),
            anchor_sq9_root=anchor_sq9_root,
            range_sqrt=range_sqrt, range_sq_target=range_sq_target,
            active_cycle=active_cycle,
            # Confluence reasons
            reasons=reasons,
        ),
    )


# ====================== COMPOSITE VERDICT ====================================
def compute_verdict(tech_score, gann_confluence, data, tech, gann_info):
    """
    Combine technical score and Gann confluence into a final verdict.
    Returns (verdict_text, verdict_class, composite_score)
    """
    # Normalize tech_score to 0-100 range
    # tech_score typically ranges from -6 to +8
    tech_norm = max(0, min(100, (tech_score + 6) / 14 * 100))

    # Gann confluence is 1-5, normalize to 0-100
    gann_norm = max(0, min(100, (gann_confluence - 1) / 4 * 100))

    # Weighted composite: 55% technical + 45% Gann
    composite = round(tech_norm * 0.55 + gann_norm * 0.45, 1)

    # RSI modifier
    rsi = data["rsi"]
    if rsi > 75:
        composite = max(0, composite - 10)
    elif rsi < 25:
        composite = min(100, composite + 5)

    # Verdict
    if composite >= 70:
        return "STRONG BUY — Multi-factor alignment", "vb-buy", composite
    elif composite >= 55:
        return "BUY — Favorable setup", "vb-buy", composite
    elif composite >= 40:
        return "CAUTION — Mixed signals, wait for clarity", "vb-caution", composite
    elif composite >= 25:
        return "AVOID — Unfavorable risk-reward", "vb-avoid", composite
    else:
        return "STRONG AVOID — Bearish confluence", "vb-avoid", composite


# ====================== MAIN UI ==============================================
def render_analysis(symbol, data, tech, tech_score, bull, bear,
                    gann_conf, angle_label, angle_color, is_squared,
                    squaring_pct, gann_info, gann_chart):
    """Render the full analysis dashboard for a single stock."""
    price = data["price"]

    # ── KPI Row ────────────────────────────────────────────────────────────
    kpi_cols = st.columns(7)
    with kpi_cols[0]:
        st.markdown(kpi("Price", f"₹{price:,.2f}", "#e8edf5", data["name"]), unsafe_allow_html=True)
    with kpi_cols[1]:
        chg_color = "#10b981" if data["change_pct"] >= 0 else "#ef4444"
        st.markdown(kpi("Change", f"{data['change_pct']:+.2f}%", chg_color), unsafe_allow_html=True)
    with kpi_cols[2]:
        rsi_color = "#10b981" if 40 <= data["rsi"] <= 70 else "#f59e0b" if data["rsi"] > 70 else "#8b5cf6"
        st.markdown(kpi("RSI", f"{data['rsi']}", rsi_color), unsafe_allow_html=True)
    with kpi_cols[3]:
        st.markdown(kpi("ATR%", f"{data['atr_pct']}%", "#06b6d4"), unsafe_allow_html=True)
    with kpi_cols[4]:
        st.markdown(kpi("Beta", f"{data['beta']:.2f}", "#8b5cf6"), unsafe_allow_html=True)
    with kpi_cols[5]:
        st.markdown(kpi("PE", f"{data['pe']}", "#3b82f6"), unsafe_allow_html=True)
    with kpi_cols[6]:
        st.markdown(kpi("Vol Ratio", f"{tech['volr']}x", "#10b981" if tech["volr"] > 1 else "#64748b"), unsafe_allow_html=True)

    # ── Verdict Banner ─────────────────────────────────────────────────────
    verdict_text, verdict_class, composite = compute_verdict(
        tech_score, gann_conf, data, tech, gann_info
    )
    st.markdown(
        f'<div class="verdict-banner {verdict_class}">'
        f'  <span class="score-ring" style="color:inherit">{composite:.0f}</span>/100 &nbsp; {safe_html(verdict_text)}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Tabs ───────────────────────────────────────────────────────────────
    tab_tech, tab_gann, tab_pivot, tab_sr = st.tabs([
        "📊 Technicals", "🔷 Gann Analysis", "📐 Pivots", "🎯 S/R Map"
    ])

    # ── TECHNICALS TAB ─────────────────────────────────────────────────────
    with tab_tech:
        st.markdown('<div class="sec-title">Technical Score</div>', unsafe_allow_html=True)
        score_color = "#10b981" if tech_score > 0 else "#ef4444" if tech_score < 0 else "#f59e0b"
        st.markdown(
            f'<div class="gc gc-{"green" if tech_score > 0 else "red" if tech_score < 0 else "gold"}">'
            f'  <div class="score-ring" style="color:{score_color}">{tech_score:+d}</div>'
            f'  {pb(max(tech_score, 0), 8, score_color)}'
            f'</div>',
            unsafe_allow_html=True,
        )

        if bull:
            st.markdown('<div class="sec-title">Bullish Signals</div>', unsafe_allow_html=True)
            for b in bull:
                st.markdown(f'<div class="lc lc-green">{safe_html(b)}</div>', unsafe_allow_html=True)

        if bear:
            st.markdown('<div class="sec-title">Bearish Signals</div>', unsafe_allow_html=True)
            for b in bear:
                st.markdown(f'<div class="lc lc-red">{safe_html(b)}</div>', unsafe_allow_html=True)

        # EMA table
        st.markdown('<div class="sec-title">Moving Averages</div>', unsafe_allow_html=True)
        ema_data = {
            "EMA": ["9", "21", "55", "200"],
            "Value": [tech["ema9"], tech["ema21"], tech["ema55"], tech["ema200"]],
            "vs Price": [
                "Above ✅" if price > tech["ema9"] else "Below ❌",
                "Above ✅" if price > tech["ema21"] else "Below ❌",
                "Above ✅" if price > tech["ema55"] else "Below ❌",
                "Above ✅" if price > tech["ema200"] else "Below ❌",
            ],
        }
        st.dataframe(pd.DataFrame(ema_data), use_container_width=True, hide_index=True)

        # Oscillators
        st.markdown('<div class="sec-title">Oscillators</div>', unsafe_allow_html=True)
        osc_cols = st.columns(3)
        with osc_cols[0]:
            macd_color = "#10b981" if tech["macd_hist"] > 0 else "#ef4444"
            st.markdown(kpi("MACD", f"{tech['macd_val']:.2f}", macd_color, f"Hist {tech['macd_hist']:.2f}"), unsafe_allow_html=True)
        with osc_cols[1]:
            st.markdown(kpi("Stoch %K", f"{tech['stoch_k']}", "#f59e0b", f"%D {tech['stoch_d']}"), unsafe_allow_html=True)
        with osc_cols[2]:
            st.markdown(kpi("ADX", f"{tech['adx']}", "#8b5cf6", f"+DI {tech['di_pos']} / -DI {tech['di_neg']}"), unsafe_allow_html=True)

    # ── GANN TAB ───────────────────────────────────────────────────────────
    with tab_gann:
        # Confluence score
        conf_color = {5: "#10b981", 4: "#10b981", 3: "#f59e0b", 2: "#f59e0b", 1: "#64748b"}.get(gann_conf, "#64748b")
        conf_border = {5: "green", 4: "green", 3: "gold", 2: "gold", 1: "blue"}.get(gann_conf, "blue")
        st.markdown(
            f'<div class="gc gc-{conf_border}">'
            f'  <div class="kpi-label">GANN CONFLUENCE</div>'
            f'  <div class="score-ring" style="color:{conf_color}">{gann_conf}</div>/5'
            f'  {pb(gann_conf, 5, conf_color)}'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Confluence reasons
        for reason in gann_info.get("reasons", []):
            rc = "lc-green" if "🔥" in reason or "✅" in reason else "lc-gold" if "⚡" in reason else "lc-blue"
            st.markdown(f'<div class="lc {rc}">{safe_html(reason)}</div>', unsafe_allow_html=True)

        # Angle zone
        st.markdown('<div class="sec-title">Gann Angle Zone</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="gc gc-{"green" if "Bull" in angle_label else "red" if "Bear" in angle_label else "gold"}">'
            f'  <div style="font-size:18px;font-weight:700;color:{angle_color}">{safe_html(angle_label)}</div>'
            f'  <div style="font-size:13px;color:#64748b;margin-top:6px">'
            f'    1×1: ₹{gann_info["angle_1x1"]:,.2f} &nbsp;|&nbsp; '
            f'    2×1: ₹{gann_info["angle_2x1"]:,.2f} &nbsp;|&nbsp; '
            f'    1×2: ₹{gann_info["angle_1x2"]:,.2f}'
            f'  </div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Price-time squaring
        sq_color = "#10b981" if is_squared else "#64748b"
        sq_label = "SQUARED ⬢" if is_squared else "Not Squared"
        st.markdown(
            f'<div class="lc lc-{"green" if is_squared else "blue"}">'
            f'  <strong>Price-Time {sq_label}</strong> — deviation {squaring_pct}%'
            f'  (scaled time = ₹{gann_info.get("scaled_time", 0):,.2f})'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Sq9 levels
        st.markdown('<div class="sec-title">Square of Nine Levels</div>', unsafe_allow_html=True)
        if gann_info.get("sq_levels"):
            sq_df = pd.DataFrame(gann_info["sq_levels"], columns=["Level", "Price (₹)", "Type"])
            st.dataframe(sq_df, use_container_width=True, hide_index=True)

        # Targets
        st.markdown('<div class="sec-title">Gann Targets & Stop</div>', unsafe_allow_html=True)
        tgt_cols = st.columns(3)
        with tgt_cols[0]:
            st.markdown(kpi("Target 1", f"₹{gann_info['gann_t1']:,.2f}", "#10b981"), unsafe_allow_html=True)
        with tgt_cols[1]:
            st.markdown(kpi("Target 2", f"₹{gann_info['gann_t2']:,.2f}", "#10b981"), unsafe_allow_html=True)
        with tgt_cols[2]:
            st.markdown(kpi("Stop Loss", f"₹{gann_info['gann_sl']:,.2f}", "#ef4444"), unsafe_allow_html=True)

        # Anchor info
        st.markdown('<div class="sec-title">Anchor & Scale</div>', unsafe_allow_html=True)
        anchor_cols = st.columns(4)
        with anchor_cols[0]:
            st.markdown(kpi("Anchor Low", f"₹{gann_info['anchor_low']:,.2f}", "#f59e0b"), unsafe_allow_html=True)
        with anchor_cols[1]:
            st.markdown(kpi("Anchor High", f"₹{gann_info['anchor_high']:,.2f}", "#f59e0b"), unsafe_allow_html=True)
        with anchor_cols[2]:
            st.markdown(kpi("Days from Low", f"{gann_info['days_from_low']}", "#06b6d4"), unsafe_allow_html=True)
        with anchor_cols[3]:
            st.markdown(kpi("Scale (pts/day)", f"{gann_info['scale']:.4f}", "#8b5cf6"), unsafe_allow_html=True)

        # Time cycles
        st.markdown('<div class="sec-title">Upcoming Time Cycles</div>', unsafe_allow_html=True)
        tc_cols = st.columns(3)

        with tc_cols[0]:
            st.markdown('<div style="font-size:12px;font-weight:700;color:#f59e0b;margin-bottom:8px">Gann Divisions</div>', unsafe_allow_html=True)
            for t, fd, days_away in gann_info.get("gann_future", [])[:4]:
                st.markdown(f'<div class="lc lc-gold" style="font-size:12px">{t}d → {fd} ({days_away}d away)</div>', unsafe_allow_html=True)

        with tc_cols[1]:
            st.markdown('<div style="font-size:12px;font-weight:700;color:#3b82f6;margin-bottom:8px">Square Dates</div>', unsafe_allow_html=True)
            for d, sd, days_away, n in gann_info.get("sq_dates", [])[:4]:
                st.markdown(f'<div class="lc lc-blue" style="font-size:12px">{n}²={d}d → {sd} ({days_away}d)</div>', unsafe_allow_html=True)

        with tc_cols[2]:
            st.markdown('<div style="font-size:12px;font-weight:700;color:#8b5cf6;margin-bottom:8px">Anniversaries</div>', unsafe_allow_html=True)
            for yr, ad, days_away in gann_info.get("anniv_dates", [])[:4]:
                st.markdown(f'<div class="lc lc-purple" style="font-size:12px">{yr}yr → {ad} ({days_away}d)</div>', unsafe_allow_html=True)

        # Gann chart
        if gann_chart:
            st.markdown('<div class="sec-title">Gann Scaled Chart</div>', unsafe_allow_html=True)
            st.plotly_chart(gann_chart, use_container_width=True)

    # ── PIVOTS TAB ─────────────────────────────────────────────────────────
    with tab_pivot:
        piv_cols = st.columns(2)

        with piv_cols[0]:
            st.markdown('<div class="sec-title">Weekly Pivots</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="gc gc-gold">'
                f'  <div style="font-size:14px"><strong>R2</strong> ₹{tech["w_r2"]:,.2f}</div>'
                f'  <div style="font-size:14px;color:#ef4444"><strong>R1</strong> ₹{tech["w_r1"]:,.2f}</div>'
                f'  <div style="font-size:16px;font-weight:700;color:#f59e0b"><strong>Pivot</strong> ₹{tech["w_pivot"]:,.2f}</div>'
                f'  <div style="font-size:14px;color:#10b981"><strong>S1</strong> ₹{tech["w_s1"]:,.2f}</div>'
                f'  <div style="font-size:14px"><strong>S2</strong> ₹{tech["w_s2"]:,.2f}</div>'
                f'  <div style="font-size:11px;color:#64748b;margin-top:8px">CPR width: {tech["w_cpr_pct"]}%</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with piv_cols[1]:
            st.markdown('<div class="sec-title">Monthly Pivots</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="gc gc-purple">'
                f'  <div style="font-size:14px"><strong>R2</strong> ₹{tech["m_r2"]:,.2f}</div>'
                f'  <div style="font-size:14px;color:#ef4444"><strong>R1</strong> ₹{tech["m_r1"]:,.2f}</div>'
                f'  <div style="font-size:16px;font-weight:700;color:#8b5cf6"><strong>Pivot</strong> ₹{tech["m_pivot"]:,.2f}</div>'
                f'  <div style="font-size:14px;color:#10b981"><strong>S1</strong> ₹{tech["m_s1"]:,.2f}</div>'
                f'  <div style="font-size:14px"><strong>S2</strong> ₹{tech["m_s2"]:,.2f}</div>'
                f'  <div style="font-size:11px;color:#64748b;margin-top:8px">CPR width: {tech["m_cpr_pct"]}%</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── S/R MAP TAB ────────────────────────────────────────────────────────
    with tab_sr:
        st.markdown('<div class="sec-title">Key Resistance Levels</div>', unsafe_allow_html=True)
        for r in tech["key_res"]:
            dist_pct = round((r - price) / max(price, 0.01) * 100, 1)
            st.markdown(f'<div class="lc lc-red">₹{r:,.2f} <span style="color:#64748b">({dist_pct:+.1f}%)</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="sec-title">Key Support Levels</div>', unsafe_allow_html=True)
        for s in tech["key_sup"]:
            dist_pct = round((price - s) / max(price, 0.01) * 100, 1)
            st.markdown(f'<div class="lc lc-green">₹{s:,.2f} <span style="color:#64748b">({dist_pct:+.1f}%)</span></div>', unsafe_allow_html=True)

        if tech["rounds"]:
            st.markdown('<div class="sec-title">Round Number Levels</div>', unsafe_allow_html=True)
            for rn in tech["rounds"]:
                marker = "above" if rn > price else "below"
                col = "lc-red" if rn > price else "lc-green"
                st.markdown(f'<div class="lc {col}" style="font-size:12px">₹{rn:,.2f} ({marker} price)</div>', unsafe_allow_html=True)

        # 52-week context
        st.markdown('<div class="sec-title">52-Week Range</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="gc gc-cyan">'
            f'  <div style="font-size:14px"><strong>High</strong> ₹{tech["w52h"]:,.2f} <span style="color:#64748b">({tech["w52h_prox"]:+.1f}% away)</span></div>'
            f'  <div style="font-size:14px"><strong>Low</strong> ₹{tech["w52l"]:,.2f} <span style="color:#64748b">({tech["w52l_prox"]:+.1f}% away)</span></div>'
            f'  <div style="font-size:11px;color:#64748b;margin-top:8px">Position in range: {round((price - tech["w52l"]) / max(tech["w52h"] - tech["w52l"], 0.01) * 100, 1)}%</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ====================== MAIN APP =============================================
def main():
    all_symbols = fetch_nifty500_symbols()

    # ── Search / Input ─────────────────────────────────────────────────────
    input_cols = st.columns([3, 1])
    with input_cols[0]:
        query = st.text_input("symbol", placeholder="Search NSE symbol — e.g. RELIANCE, TCS, HDFCBANK …")
    with input_cols[1]:
        analyze_btn = st.button("⚡ Analyze", use_container_width=True)

    # Match symbols
    matched = []
    if query and len(query.strip()) >= 1:
        q = query.strip().upper()
        matched = [s for s in all_symbols if q in s]
        matched = matched[:20]  # cap for display

    # ── Symbol Selection ───────────────────────────────────────────────────
    selected = None
    if analyze_btn and matched:
        selected = matched[0]
        st.session_state.selected_symbol = selected
        st.session_state.analyze_triggered = True
    elif st.session_state.get("analyze_triggered") and st.session_state.get("selected_symbol"):
        selected = st.session_state.selected_symbol

    if matched and not selected:
        st.markdown('<div class="sec-title">Matching Symbols</div>', unsafe_allow_html=True)
        sym_cols = st.columns(min(len(matched), 5))
        for idx, sym in enumerate(matched[:10]):
            with sym_cols[idx % len(sym_cols)]:
                if st.button(sym, key=f"sym_{sym}"):
                    st.session_state.selected_symbol = sym
                    st.session_state.analyze_triggered = True
                    st.rerun()

    # ── Run Analysis ───────────────────────────────────────────────────────
    if selected:
        with st.spinner(f"Analyzing {selected} …"):
            data = fetch_stock_data(selected)
            tech = compute_technicals(data)
            tech_score, bull, bear = compute_tech_score(data, tech)

            gann_conf, angle_label, angle_color, is_squared, squaring_pct, gann_info = \
                compute_gann_confluence(data, symbol=selected)

            gann_chart = _build_gann_chart(
                data.get("hist"),
                gann_info["anchor_low"], gann_info["anchor_low_date"],
                gann_info["anchor_high"],
                gann_info["scale"],
                gann_info["angle_1x1"], gann_info["angle_2x1"],
                gann_info["angle_1x2"], gann_info["angle_1x4"],
                _sq9_levels(data["price"]),
                data["price"],
                datetime.now().date(),
            )

        render_analysis(
            selected, data, tech, tech_score, bull, bear,
            gann_conf, angle_label, angle_color, is_squared,
            squaring_pct, gann_info, gann_chart,
        )
    else:
        # Landing state
        st.markdown(
            """
<div class="gc gc-gold" style="text-align:center;padding:40px">
    <div style="font-size:1.8rem;font-weight:800;background:linear-gradient(135deg,#f59e0b,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:12px">
        Search an NSE stock to begin
    </div>
    <div style="font-size:14px;color:#64748b">
        VedicEdge combines Western technicals with Gann price-time theory and the<br>
        Sarvatobhadra confluence principle — when multiple independent systems align,<br>
        the signal is reliable from all directions.
    </div>
</div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()

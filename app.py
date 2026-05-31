import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
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

        # ── WEEKLY PIVOT (last completed week) ──────────────────────────────
        h_copy = h.copy()
        h_copy.index = pd.to_datetime(h_copy.index)
        weekly = h_copy.resample("W").agg({"High": "max", "Low": "min", "Close": "last"})
        weekly = weekly.dropna()
        # Use second-to-last row = last fully completed week
        if len(weekly) >= 2:
            wph = round(float(weekly["High"].iloc[-2]), 2)
            wpl = round(float(weekly["Low"].iloc[-2]),  2)
            wpc = round(float(weekly["Close"].iloc[-2]), 2)
        else:
            wph, wpl, wpc = round(float(h["High"].iloc[-2]),2), round(float(h["Low"].iloc[-2]),2), round(float(h["Close"].iloc[-2]),2)
        w_pivot = round((wph + wpl + wpc) / 3, 2)
        w_r1    = round(2*w_pivot - wpl, 2)
        w_s1    = round(2*w_pivot - wph, 2)
        w_r2    = round(w_pivot + (wph - wpl), 2)
        w_s2    = round(w_pivot - (wph - wpl), 2)
        # CPR width as % of price (meaningful threshold: <0.5% = narrow, >2% = wide)
        w_cpr_pct = round((w_r1 - w_s1) / p * 100, 2)

        # ── MONTHLY PIVOT (last completed month) ────────────────────────────
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
        m_cpr_pct = round((m_r1 - m_s1) / p * 100, 2)

        # ── KEY S/R: swing highs/lows + round numbers + 52W ─────────────────
        # Swing highs: local maxima over rolling 10-bar window
        swing_highs = []
        swing_lows  = []
        roll_win = 10
        for i in range(roll_win, len(h) - roll_win):
            if h["High"].iloc[i] == h["High"].iloc[i-roll_win:i+roll_win].max():
                swing_highs.append(round(float(h["High"].iloc[i]), 2))
            if h["Low"].iloc[i] == h["Low"].iloc[i-roll_win:i+roll_win].min():
                swing_lows.append(round(float(h["Low"].iloc[i]), 2))
        # Keep 3 closest above and below price
        key_res = sorted([x for x in swing_highs if x > p])[:3]
        key_sup = sorted([x for x in swing_lows  if x < p], reverse=True)[:3]
        # Round number levels within ±15% of price
        mag = 10 ** max(0, int(math.log10(p)) - 1)  # e.g. ₹334 → mag=10, ₹1200 → mag=100
        rounds = []
        base = round(p * 0.85 / mag) * mag
        while base <= p * 1.15:
            rounds.append(round(base, 2))
            base += mag
        # 52W proximity
        w52h = data["w52h"]
        w52l = data["w52l"]
        w52h_prox = round((w52h - p) / p * 100, 1)
        w52l_prox = round((p - w52l) / p * 100, 1)

    else:
        ema9 = ema21 = ema55 = ema200 = p
        macd_val = 0.5; macd_sig = 0.2; macd_hist = 0.3
        bb_upper = round(p*1.04, 2); bb_lower = round(p*0.96, 2); bb_mid = p
        stoch_k = 55.0; stoch_d = 52.0
        vol20 = data["volume"]; volr = 1.0
        di_pos = 22.0; di_neg = 18.0; adx = 24.0
        w_pivot = p; w_r1 = round(p*1.02,2); w_s1 = round(p*0.98,2)
        w_r2 = round(p*1.04,2); w_s2 = round(p*0.96,2); w_cpr_pct = 2.0
        m_pivot = p; m_r1 = round(p*1.04,2); m_s1 = round(p*0.96,2)
        m_r2 = round(p*1.08,2); m_s2 = round(p*0.92,2); m_cpr_pct = 4.0
        key_res = [round(p*1.03,2), round(p*1.06,2), round(p*1.10,2)]
        key_sup = [round(p*0.97,2), round(p*0.94,2), round(p*0.90,2)]
        rounds  = []
        w52h = data["w52h"]; w52l = data["w52l"]
        w52h_prox = round((w52h - p) / p * 100, 1)
        w52l_prox = round((p - w52l) / p * 100, 1)

    return dict(
        ema9=ema9, ema21=ema21, ema55=ema55, ema200=ema200,
        macd_val=macd_val, macd_sig=macd_sig, macd_hist=macd_hist,
        bb_upper=bb_upper, bb_lower=bb_lower, bb_mid=bb_mid,
        stoch_k=stoch_k, stoch_d=stoch_d,
        vol20=vol20, volr=volr,
        di_pos=di_pos, di_neg=di_neg, adx=adx,
        # Weekly pivot
        w_pivot=w_pivot, w_r1=w_r1, w_s1=w_s1, w_r2=w_r2, w_s2=w_s2, w_cpr_pct=w_cpr_pct,
        # Monthly pivot
        m_pivot=m_pivot, m_r1=m_r1, m_s1=m_s1, m_r2=m_r2, m_s2=m_s2, m_cpr_pct=m_cpr_pct,
        # S/R context
        key_res=key_res, key_sup=key_sup, rounds=rounds,
        w52h=w52h, w52l=w52l, w52h_prox=w52h_prox, w52l_prox=w52l_prox,
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
            h.index = h.index.tz_localize(None) if h.index.tzinfo is None else h.index.tz_convert(None)
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

    # Rolling 20-bar local minima
    candidates = []
    win = 20
    for i in range(win, len(hist) - win):
        bar_low = float(hist["Low"].iloc[i])
        window_min = float(hist["Low"].iloc[i-win:i+win].min())
        if bar_low == window_min:
            # Volume on that bar — higher vol = more significant
            vol = float(hist["Volume"].iloc[i])
            # Subsequent move from this low to the highest close afterward
            subsequent_high = float(hist["High"].iloc[i:].max())
            move_pct = (subsequent_high - bar_low) / max(bar_low, 1) * 100
            candidates.append((move_pct, vol, bar_low, hist.index[i]))

    if not candidates:
        # Fallback: absolute low of full history
        idx = hist["Low"].idxmin()
        return (
            round(float(hist["Low"].min()), 2),
            idx.date(),
            round(float(hist["High"].max()), 2),
            hist["High"].idxmax().date(),
        )

    # Sort by subsequent move % descending — the low that led to the biggest rally
    candidates.sort(key=lambda x: x[0], reverse=True)
    _, _, best_low, best_date = candidates[0]

    # Anchor high = highest point AFTER the anchor low
    after = hist[hist.index >= best_date]
    anchor_high = round(float(after["High"].max()), 2)
    anchor_high_date = after["High"].idxmax().date()

    return (
        round(best_low, 2),
        best_date.date() if hasattr(best_date, "date") else best_date,
        anchor_high,
        anchor_high_date,
    )


def _sq9_levels(price):
    """
    Full 8-spoke Square of Nine levels around current price.
    Cardinals: 0°/90°/180°/270° → integer rings
    Diagonals: 45°/135°/225°/315° → half-step rings
    Returns sorted list of (label, price, spoke_type)
    """
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
    Three independent time tools. Returns (confluence_count, details).
    All three must independently point to the same ±5-day window for HIGH.
    Any two = MODERATE.
    """
    days_from_low = (today - anchor_low_date).days

    # Tool 1: Natural squares — days that are perfect squares
    n = int(math.sqrt(days_from_low))
    sq_prev = n * n
    sq_next = (n + 1) * (n + 1)
    days_to_sq = sq_next - days_from_low
    tool1_active = days_to_sq <= 5 or (days_from_low - sq_prev) <= 5

    # Tool 2: Gann natural divisions (multiples of 90, 144, 180, 360)
    gann_divs = [45, 90, 135, 144, 180, 225, 270, 315, 360, 450, 504, 720]
    tool2_active = any(abs(days_from_low - d) <= 5 for d in gann_divs)
    nearest_div = min(gann_divs, key=lambda d: abs(days_from_low - d))
    days_to_div = nearest_div - days_from_low

    # Tool 3: Anniversary dates (yearly + Fibonacci years)
    fib_days = [days_from_low % 365]  # distance within current year cycle
    tool3_active = any(abs(r) <= 5 for r in fib_days)

    # Next upcoming events for each tool
    next_sq_date   = anchor_low_date + timedelta(days=sq_next)
    next_div_date  = anchor_low_date + timedelta(days=nearest_div) if days_to_div > 0 else anchor_low_date + timedelta(days=nearest_div + 90)

    active_tools = sum([tool1_active, tool2_active, tool3_active])

    details = {
        "tool1_active": tool1_active,
        "tool2_active": tool2_active,
        "tool3_active": tool3_active,
        "active_tools": active_tools,
        "days_to_sq": days_to_sq,
        "sq_prev": sq_prev, "sq_next": sq_next,
        "nearest_div": nearest_div, "days_to_div": days_to_div,
        "next_sq_date": next_sq_date,
        "next_div_date": next_div_date,
        "days_from_low": days_from_low,
    }
    return active_tools, details


def compute_gann_confluence(data, symbol=None):
    price = data["price"]
    today = datetime.now().date()

    # ── UPGRADE 1: Use long history for proper anchor ──────────────────────
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
            anchor_low_date  = low_idx.date()  if hasattr(low_idx,  "date") else low_idx.to_pydatetime().date()
            anchor_high_date = high_idx.date() if hasattr(high_idx, "date") else high_idx.to_pydatetime().date()
        hl_range = round(anchor_high - anchor_low, 2)
    else:
        anchor_low       = round(price * 0.72, 2)
        anchor_high      = round(price * 1.22, 2)
        anchor_low_date  = today - timedelta(days=500)
        anchor_high_date = today - timedelta(days=90)
        hl_range         = round(anchor_high - anchor_low, 2)

    days_from_low  = (today - anchor_low_date).days
    days_from_high = (today - anchor_high_date).days

    # ── UPGRADE 2: Stock-specific scaling factor ───────────────────────────
    # scale = price_range / time_range of the major move
    # This makes angles meaningful — 1 unit price = 1 unit time on scaled chart
    price_range = max(anchor_high - anchor_low, 1.0)
    time_range  = max(days_from_low, 1)
    scale       = price_range / time_range   # pts per day at 1×1 on THIS stock
    scale       = round(scale, 4)

    # ── UPGRADE 3: Calibrated Gann Angles using scale factor ───────────────
    # angle_NxM = anchor_low + (days * scale * N/M)
    angle_4x1 = round(anchor_low + days_from_low * scale * 4,   2)
    angle_2x1 = round(anchor_low + days_from_low * scale * 2,   2)
    angle_1x1 = round(anchor_low + days_from_low * scale * 1,   2)
    angle_1x2 = round(anchor_low + days_from_low * scale * 0.5, 2)
    angle_1x4 = round(anchor_low + days_from_low * scale * 0.25,2)

    # Current angle — which scaled angle is price closest to?
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

    # ── UPGRADE 4: Full 8-spoke Square of Nine levels ─────────────────────
    sq9_all = _sq9_levels(price)
    # Nearest support and resistance from the 8-spoke wheel
    sq9_supports    = [(l, p2, s) for l, p2, s in sq9_all if p2 < price]
    sq9_resistances = [(l, p2, s) for l, p2, s in sq9_all if p2 > price]
    sq9_s1  = sq9_supports[-1]    if sq9_supports    else ("—", price, "—")
    sq9_s2  = sq9_supports[-2]    if len(sq9_supports) >= 2    else sq9_s1
    sq9_r1  = sq9_resistances[0]  if sq9_resistances  else ("—", price, "—")
    sq9_r2  = sq9_resistances[1]  if len(sq9_resistances) >= 2 else sq9_r1

    # Targets and stop using scaled sq9
    gann_t1 = sq9_r1[1]
    gann_t2 = sq9_r2[1]
    gann_sl = sq9_s2[1]

    # Build display table from 8-spoke levels
    sq_levels = []
    for lbl, lv, spoke in sq9_all:
        marker = "⚪ Current" if lv == price else ("🔴" if "Support" in lbl else "🟢")
        sq_levels.append([f"{marker} {lbl}", lv, spoke])
    # Always insert current price row
    sq_levels_display = [["⚪ Current", price, "—"]] + \
                        [[f"🔴 {l}", p2, s] for l, p2, s in sq9_supports[-3:]] + \
                        [[f"🟢 {l}", p2, s] for l, p2, s in sq9_resistances[:3]]
    sq_levels_display = sorted(sq_levels_display, key=lambda x: x[1])

    # ── UPGRADE 5: Three-tool time cycle confluence ────────────────────────
    active_tools, cycle_details = _time_cycle_confluence(anchor_low_date, today)
    sqrt_days    = round(math.sqrt(days_from_low), 4)
    n_low        = int(sqrt_days)
    nearest_sq   = n_low * n_low
    next_sq      = (n_low + 1) * (n_low + 1)
    days_to_next = next_sq - days_from_low

    # ── UPGRADE 6: Strict confluence scoring ──────────────────────────────
    # Price confluence: how close is price to a Sq9 level? (±0.5% = tight)
    nearest_sq9_price = min([p2 for _, p2, _ in sq9_all], key=lambda x: abs(x - price))
    price_sq9_dev     = abs(nearest_sq9_price - price) / price * 100
    at_sq9_tight      = price_sq9_dev <= 0.5
    at_sq9_moderate   = price_sq9_dev <= 1.5

    # Angle confluence: is price within 1% of 1×1 angle?
    at_1x1 = abs(price - angle_1x1) / max(price, 1) * 100 <= 1.0

    # Time confluence: 2 of 3 tools active = moderate, all 3 = strong
    time_strong   = active_tools >= 3
    time_moderate = active_tools >= 2

    # Final confluence — strict hierarchy
    confluence = 0
    reasons    = []

    # Tier 1 — strongest: all three align (price at sq9 tight + angle + time strong)
    if at_sq9_tight and at_1x1 and time_strong:
        confluence = 5
        reasons.append("🔥 TIER 1: Sq9 tight (±0.5%) + 1×1 angle + 3/3 time tools")
    # Tier 2 — two of three
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

    # Add detail lines
    reasons.append(f"   Sq9 nearest ₹{nearest_sq9_price:,.2f} · deviation {price_sq9_dev:.2f}%")
    reasons.append(f"   1×1 angle ₹{angle_1x1:,.2f} · price deviation {abs(price_vs_1x1):.1f}%")
    reasons.append(f"   Time tools active: {active_tools}/3 "
                   f"(Sq {cycle_details['days_to_sq']}d · Div {cycle_details['days_to_div']}d)")

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

    # Price-time squaring using scale factor
    scaled_time     = days_from_low * scale
    squaring_pct    = round(abs(price - scaled_time) / max(price, 1) * 100, 1)
    is_squared      = squaring_pct < 3.0   # tighter threshold with proper scaling

    anchor_sq9_root = round(math.sqrt(anchor_low), 4)
    range_sqrt      = round(math.sqrt(hl_range), 4)
    range_sq_target = round((math.ceil(range_sqrt) + 1) ** 2, 2)
    active_cycle    = next((t for t in gann_time_units if days_from_low <= t), 720)

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
            sq9_root=round(math.sqrt(price), 4),
            sq9_s1=sq9_s1, sq9_s2=sq9_s2, sq9_r1=sq9_r1, sq9_r2=sq9_r2,
            nearest_sq9_price=nearest_sq9_price, price_sq9_dev=price_sq9_dev,
            sq_levels=sq_levels_display,
            # Targets / SL
            gann_t1=gann_t1, gann_t2=gann_t2, gann_sl=gann_sl,
            # Time
            sqrt_days=sqrt_days, n_low=n_low,
            nearest_sq=nearest_sq, next_sq=next_sq, days_to_next=days_to_next,
            cycle_details=cycle_details, active_tools=active_tools,
            gann_future=gann_future, sq_dates=sq_dates, anniv_dates=anniv_dates,
            active_cycle=active_cycle,
            # Squaring
            scaled_time=round(scaled_time, 2),
            is_squared=is_squared, squaring_pct=squaring_pct,
            # Range
            anchor_sq9_root=anchor_sq9_root,
            range_sqrt=range_sqrt, range_sq_target=range_sq_target,
            # Confluence
            confluence=confluence, reasons=reasons,
            today=today,
        ),
    )


# SBC removed — not classically valid (stock nakshatra requires IPO date, not hash)

# ====================== COMBINED VERDICT (Technical 70% + Gann 30%) =========
def combined_verdict(tech_score, gann_confluence):
    tech_norm = max(0, min(100, int((tech_score + 8) / 18 * 100)))
    gann_norm = max(0, min(100, int(gann_confluence / 5 * 100)))
    final = round(tech_norm * 0.70 + gann_norm * 0.30)
    if final >= 72:   lbl, cls, icon = "STRONG BUY",        "vb-buy",     "🟢"
    elif final >= 58: lbl, cls, icon = "BUY / ACCUMULATE",  "vb-buy",     "🟢"
    elif final >= 45: lbl, cls, icon = "CAUTIOUS — WAIT",   "vb-caution", "🟡"
    elif final >= 35: lbl, cls, icon = "NEUTRAL",           "vb-caution", "🟡"
    elif final >= 25: lbl, cls, icon = "AVOID / REDUCE",    "vb-avoid",   "🔴"
    else:             lbl, cls, icon = "STRONG AVOID",      "vb-avoid",   "🔴"
    return final, lbl, cls, icon, tech_norm, gann_norm


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

    with st.expander("⚙️  Scanner Settings", expanded=True):
        st.markdown(
            '<div style="font-size:12px;color:#64748b;margin-bottom:12px">'
            '🚦 <b>Sequential gates</b> — stock must pass ALL active gates. Fail one = out.'
            '</div>', unsafe_allow_html=True
        )
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            st.markdown("**Gate 1 — Liquidity (always on)**")
            min_vol_l = st.number_input("Min avg volume (lakhs/day)", value=5.0, step=0.5)
            min_price = st.number_input("Min price ₹", value=50)
            max_price = st.number_input("Max price ₹", value=5000)
        with fc2:
            st.markdown("**Gate 2 — Trend (always on)**")
            st.caption("Price > 200 EMA · 50 EMA > 200 EMA · Price > 20 EMA")
            st.markdown("**Gate 3 — Momentum**")
            min_rsi = st.slider("RSI min", 20, 55, 45)
            max_rsi = st.slider("RSI max", 55, 80, 65)
            f_macd_fresh = st.checkbox("MACD hist turned positive (fresh crossover)", value=True)
        with fc3:
            st.markdown("**Gate 4 — Entry Zone**")
            f_pullback   = st.checkbox("Near EMA21 or EMA50 pullback (within 3%)", value=True)
            f_vol_expand = st.checkbox("Volume expanding on bounce day", value=True)
            st.markdown("**Gate 5 — R:R**")
            min_rr = st.slider("Minimum R:R", 1.5, 4.0, 2.5, 0.5)
            max_pe = st.slider("Max PE", 10, 100, 60)

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
                    p = d["price"]
                    reasons  = []
                    fail_at  = None

                    # ── GATE 1: LIQUIDITY ────────────────────────────────────
                    # avg volume in lakhs
                    avg_vol_l = 0
                    if d.get("hist") is not None:
                        avg_vol_l = float(d["hist"]["Volume"].rolling(20).mean().iloc[-1]) / 1e5
                    if avg_vol_l < min_vol_l:
                        fail_at = f"G1: Vol {avg_vol_l:.1f}L < {min_vol_l}L"
                    elif not (min_price <= p <= max_price):
                        fail_at = f"G1: Price ₹{p} out of range"
                    elif d["pe"] <= 0 or d["pe"] > max_pe:
                        fail_at = f"G1: PE {d['pe']} invalid/high"
                    if fail_at:
                        continue

                    # ── GATE 2: TREND (hard — no checkbox, always required) ──
                    t = compute_technicals(d)
                    ema50 = round(float(d["hist"]["Close"].ewm(span=50, adjust=False).mean().iloc[-1]), 2) if d.get("hist") is not None else p
                    if p < t["ema200"]:
                        fail_at = "G2: Price below 200 EMA"
                    elif ema50 < t["ema200"]:
                        fail_at = "G2: 50 EMA below 200 EMA — not in bull trend"
                    elif p < t["ema21"]:
                        fail_at = "G2: Price below 20 EMA"
                    if fail_at:
                        continue
                    reasons.append(f"✅ Trend: P>{round(t['ema200'],0)} EMA200, EMA50>{round(t['ema200'],0)}")

                    # ── GATE 3: MOMENTUM ─────────────────────────────────────
                    if not (min_rsi <= d["rsi"] <= max_rsi):
                        continue
                    reasons.append(f"✅ RSI {d['rsi']} in {min_rsi}–{max_rsi} zone")

                    if f_macd_fresh:
                        # Fresh = histogram positive AND was negative 2 bars ago
                        if d.get("hist") is not None:
                            c  = d["hist"]["Close"]
                            ml = c.ewm(span=12, adjust=False).mean() - c.ewm(span=26, adjust=False).mean()
                            ms = ml.ewm(span=9,  adjust=False).mean()
                            mh = ml - ms
                            if not (mh.iloc[-1] > 0 and mh.iloc[-3] < 0):
                                continue
                            reasons.append("✅ MACD fresh bullish crossover")
                        else:
                            if t["macd_hist"] <= 0:
                                continue

                    # ── GATE 4: ENTRY ZONE ───────────────────────────────────
                    if f_pullback:
                        near_ema21 = abs(p - t["ema21"]) / p * 100 <= 3.0
                        near_ema50 = abs(p - ema50)     / p * 100 <= 3.0
                        if not (near_ema21 or near_ema50):
                            continue
                        reasons.append(f"✅ At EMA pullback zone ({'EMA21' if near_ema21 else 'EMA50'})")

                    if f_vol_expand:
                        # Volume today > yesterday AND > 20-day avg
                        if d.get("hist") is not None and len(d["hist"]) >= 3:
                            v_today = float(d["hist"]["Volume"].iloc[-1])
                            v_yest  = float(d["hist"]["Volume"].iloc[-2])
                            v_avg   = float(d["hist"]["Volume"].rolling(20).mean().iloc[-1])
                            if not (v_today > v_yest and v_today > v_avg):
                                continue
                            reasons.append(f"✅ Volume expanding ({round(v_today/v_avg,1)}x avg)")

                    # ── GATE 5: R:R ──────────────────────────────────────────
                    sl  = round(p - d["atr"] * 1.5, 2)
                    tgt = round(p + d["atr"] * 3.0, 2)
                    rr  = round((tgt - p) / max(p - sl, 0.01), 1)
                    if rr < min_rr:
                        continue
                    reasons.append(f"✅ R:R 1:{rr}")

                    # ── QUALITY SCORE (for sorting, not filtering) ───────────
                    score = 0
                    if p > t["ema9"] > t["ema21"]:              score += 20
                    if t["adx"] > 25 and t["di_pos"] > t["di_neg"]: score += 20
                    if t["volr"] > 1.5:                          score += 15
                    if d["rsi"] < 60:                            score += 15
                    if t["macd_hist"] > 0:                       score += 15
                    if d["atr_pct"] > 1.5:                       score += 15

                    entry = dict(
                        sym=sym, name=d["name"], price=p,
                        change=d["change_pct"], score=min(score, 100),
                        reasons=reasons,
                        criteria={
                            "trend": True, "rsi": True,
                            "macd": t["macd_hist"] > 0,
                            "vol":  t["volr"] >= 1.2,
                            "rr":   rr >= min_rr,
                        },
                        rsi=d["rsi"], pe=d["pe"], pb=d["pb"],
                        atr_pct=d["atr_pct"], beta=d["beta"],
                        volr=t["volr"], macd_hist=t["macd_hist"],
                        ema21=t["ema21"], ema200=t["ema200"],
                        sector=d["sector"], w52h=d["w52h"], w52l=d["w52l"],
                        sl=sl, tgt=tgt, rr=rr,
                    )
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
                f'{dot(cr.get("trend"))} Trend &nbsp;'
                f'{dot(cr.get("rsi"))} RSI &nbsp;'
                f'{dot(cr.get("macd"))} MACD &nbsp;'
                f'{dot(cr.get("vol"))} Volume &nbsp;'
                f'{dot(cr.get("rr"))} R:R'
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
        gann_conf, angle_label, angle_color, is_squared, squaring_pct, gd = compute_gann_confluence(data, symbol)
        tech_score, bull_pts, bear_pts = compute_tech_score(data, tech)
        cv_final, cv_lbl, cv_cls, cv_icon, tech_norm, gann_norm = combined_verdict(tech_score, gann_conf)

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
        overview_tab, tech_tab, gann_tab = st.tabs(
            ["📊 Overview", "📈 In-Depth Technical", "🔶 In-Depth Gann"]
        )

        # ── OVERVIEW ─────────────────────────────────────────────────────────
        with overview_tab:
            st.markdown(
                f'<div class="verdict-banner {cv_cls}">{cv_icon} {cv_lbl} — Combined Score: {cv_final}/100 (Technical 70% · Gann 30%)</div>',
                unsafe_allow_html=True,
            )
            oc1, oc2 = st.columns(2)
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
                        <div style="padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05);display:flex;justify-content:space-between"><span style="color:#64748b">MACD Hist</span><span style="font-weight:700;color:{'#10b981' if tech['macd_hist']>0 else '#ef4444'}">{tech['macd_hist']:+.2f}</span></div>
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
                        <div style="padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05);display:flex;justify-content:space-between"><span style="color:#64748b">Angle</span><span style="font-weight:700;color:{angle_color}">{angle_label}</span></div>
                        <div style="padding:6px 0;display:flex;justify-content:space-between"><span style="color:#64748b">Price-Time</span><span style="font-weight:700;color:{'#10b981' if is_squared else '#f59e0b'}">{'✅ Squared' if is_squared else f'⚠️ {squaring_pct}% dev'}</span></div>
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
                ("2. Pivots & S/R (Weekly + Monthly)",
                 f"<b>Weekly</b>: Pivot ₹{tech['w_pivot']:,.2f} | R1 ₹{tech['w_r1']:,.2f} | R2 ₹{tech['w_r2']:,.2f} | S1 ₹{tech['w_s1']:,.2f} | S2 ₹{tech['w_s2']:,.2f} · CPR width {tech['w_cpr_pct']}% {'(narrow — breakout likely 🔥)' if tech['w_cpr_pct'] < 0.5 else '(wide — range/consolidation)' if tech['w_cpr_pct'] > 2.0 else '(moderate)'}. "
                 f"Price {'above weekly pivot — bullish bias ✅' if price_t > tech['w_pivot'] else 'below weekly pivot — bearish bias ⚠️'}.<br>"
                 f"<b>Monthly</b>: Pivot ₹{tech['m_pivot']:,.2f} | R1 ₹{tech['m_r1']:,.2f} | S1 ₹{tech['m_s1']:,.2f} · CPR {tech['m_cpr_pct']}%.<br>"
                 f"<b>Key Resistance</b>: {', '.join(f'₹{x:,.2f}' for x in tech['key_res']) if tech['key_res'] else 'None found'} · "
                 f"<b>Key Support</b>: {', '.join(f'₹{x:,.2f}' for x in tech['key_sup']) if tech['key_sup'] else 'None found'}.<br>"
                 f"<b>Round levels nearby</b>: {', '.join(f'₹{x:,.0f}' for x in tech['rounds']) if tech['rounds'] else '—'}. "
                 f"52W High ₹{tech['w52h']:,.2f} ({tech['w52h_prox']}% away) · 52W Low ₹{tech['w52l']:,.2f} ({tech['w52l_prox']}% below).",
                 "gc-cyan"),
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
            cd    = gd["cycle_details"]

            # KPIs
            gk1, gk2, gk3, gk4, gk5, gk6 = st.columns(6)
            for col, (lbl, val, clr) in zip(
                [gk1, gk2, gk3, gk4, gk5, gk6],
                [("Price",      f"₹{price:,.2f}",           "#f59e0b"),
                 ("Sq9 Root",   str(gd["sq9_root"]),         "#8b5cf6"),
                 ("Anchor Low", f"₹{gd['anchor_low']:,.2f}", "#3b82f6"),
                 ("Days",       str(gd["days_from_low"]),    "#f59e0b"),
                 ("Scale",      str(gd["scale"]),            "#10b981"),
                 ("Time Tools", f"{gd['active_tools']}/3",   "#10b981" if gd["active_tools"]>=2 else "#ef4444")],
            ):
                with col:
                    st.markdown(kpi(lbl, val, clr), unsafe_allow_html=True)

            # Step 1 — Anchor
            gs1, gs2 = st.columns(2)
            with gs1:
                st.markdown(
                    f"""<div class="gc gc-blue"><div style="color:#f59e0b;font-weight:700;margin-bottom:6px">📌 Step 1: Significant Anchor (Multi-Year)</div>
                    <div style="font-size:13px;color:#94a3b8;line-height:2">
                    🔽 Anchor Low: <b style="color:#3b82f6">₹{gd['anchor_low']:,.2f}</b> · {gd['anchor_low_date'].strftime('%d %b %Y')}<br>
                    🔼 Anchor High: <b style="color:#ef4444">₹{gd['anchor_high']:,.2f}</b> · {gd['anchor_high_date'].strftime('%d %b %Y')}<br>
                    HL Range: <b style="color:#e8edf5">₹{gd['hl_range']:,.2f}</b> · Days elapsed: <b style="color:#f59e0b">{gd['days_from_low']}</b><br>
                    <span style="color:#475569;font-size:11px">Anchor = highest-move swing low from max available history</span>
                    </div></div>""",
                    unsafe_allow_html=True,
                )
            with gs2:
                st.markdown(
                    f"""<div class="gc gc-gold"><div style="color:#f59e0b;font-weight:700;margin-bottom:6px">📐 Step 2: Scaling Factor</div>
                    <div style="font-size:13px;color:#94a3b8;line-height:2">
                    Price Range: <b style="color:#e8edf5">₹{gd['hl_range']:,.2f}</b><br>
                    Time Range: <b style="color:#e8edf5">{gd['days_from_low']} days</b><br>
                    Scale (pts/day): <b style="color:#10b981;font-size:16px">{gd['scale']}</b><br>
                    <span style="color:#475569;font-size:11px">All angles calculated using this stock-specific scale</span>
                    </div></div>""",
                    unsafe_allow_html=True,
                )

            # Step 3 — Calibrated Angles
            st.markdown('<div style="font-size:13px;font-weight:700;color:#f59e0b;margin:16px 0 8px">📐 Step 3: Calibrated Gann Angles (Scale-Adjusted)</div>', unsafe_allow_html=True)
            ga1, ga2 = st.columns([2, 1])
            with ga1:
                st.dataframe(
                    pd.DataFrame([
                        ["4×1", f"₹{gd['angle_4x1']:,.2f}", f"4× scale ({round(gd['scale']*4,3)} pts/day)", "Very strong bull" if price >= gd["angle_4x1"] else "Above price"],
                        ["2×1", f"₹{gd['angle_2x1']:,.2f}", f"2× scale ({round(gd['scale']*2,3)} pts/day)", "Strong bull" if price >= gd["angle_2x1"] else "Above price"],
                        ["1×1 ★", f"₹{gd['angle_1x1']:,.2f}", f"1× scale ({gd['scale']} pts/day) — Master", f"Price {gd['price_vs_1x1']:+.1f}% from 1×1"],
                        ["1×2", f"₹{gd['angle_1x2']:,.2f}", f"0.5× scale — Caution zone", "Bear" if price <= gd["angle_1x2"] else "Above bear line"],
                        ["1×4", f"₹{gd['angle_1x4']:,.2f}", f"0.25× scale — Bear", "Strong bear" if price <= gd["angle_1x4"] else "Above bear line"],
                    ], columns=["Angle", "Level (₹)", "Scale Rate", "Status"]),
                    use_container_width=True, hide_index=True,
                )
            with ga2:
                st.markdown(
                    f'<div class="gc gc-gold" style="text-align:center"><div class="kpi-label">Current Zone</div>'
                    f'<div style="font-size:13px;font-weight:800;color:{angle_color};margin:8px 0;line-height:1.4">{angle_label}</div>'
                    f'<div style="color:#475569;font-size:12px">Closest: {gd["closest_angle"]}<br>'
                    f'1×1 deviation: {gd["price_vs_1x1"]:+.1f}%</div></div>',
                    unsafe_allow_html=True,
                )

            # Step 4 — Full 8-Spoke Square of Nine
            st.markdown('<div style="font-size:13px;font-weight:700;color:#f59e0b;margin:16px 0 8px">🌀 Step 4: Square of Nine — Full 8-Spoke Wheel</div>', unsafe_allow_html=True)
            sq_col = "#10b981" if gd["price_sq9_dev"] <= 0.5 else "#f59e0b" if gd["price_sq9_dev"] <= 1.5 else "#64748b"
            st.markdown(
                f'<div style="font-size:12px;color:{sq_col};margin-bottom:8px">'
                f'Nearest Sq9 level: ₹{gd["nearest_sq9_price"]:,.2f} · Deviation: {gd["price_sq9_dev"]:.2f}% '
                f'{"✅ Tight (≤0.5%)" if gd["price_sq9_dev"]<=0.5 else "⚡ Moderate (≤1.5%)" if gd["price_sq9_dev"]<=1.5 else "⚪ Loose (>1.5%)"}'
                f'</div>', unsafe_allow_html=True
            )
            st.dataframe(
                pd.DataFrame(gd["sq_levels"], columns=["Level", "Price (₹)", "Spoke Type"]),
                use_container_width=True, hide_index=True,
            )

            # Step 5 — Three-Tool Time Cycle
            st.markdown('<div style="font-size:13px;font-weight:700;color:#f59e0b;margin:16px 0 8px">⏱️ Step 5: Three-Tool Time Cycle Confluence</div>', unsafe_allow_html=True)
            tc1, tc2, tc3 = st.columns(3)
            tool_colors = ["#10b981" if cd[f"tool{i}_active"] else "#ef4444" for i in [1,2,3]]
            with tc1:
                st.markdown(
                    f'<div class="gc {"gc-green" if cd["tool1_active"] else "gc-red"}"><div style="font-weight:700;font-size:13px;margin-bottom:6px">'
                    f'{"✅" if cd["tool1_active"] else "❌"} Tool 1: Perfect Square</div>'
                    f'<div style="font-size:12px;color:#94a3b8">Days: {cd["days_from_low"]}<br>'
                    f'Prev sq: {cd["sq_prev"]} · Next sq: {cd["sq_next"]}<br>'
                    f'Days to next: <b style="color:{tool_colors[0]}">{cd["days_to_sq"]}</b><br>'
                    f'Next sq date: {cd["next_sq_date"].strftime("%d %b %Y")}</div></div>',
                    unsafe_allow_html=True,
                )
            with tc2:
                st.markdown(
                    f'<div class="gc {"gc-green" if cd["tool2_active"] else "gc-red"}"><div style="font-weight:700;font-size:13px;margin-bottom:6px">'
                    f'{"✅" if cd["tool2_active"] else "❌"} Tool 2: Gann Divisions</div>'
                    f'<div style="font-size:12px;color:#94a3b8">Days: {cd["days_from_low"]}<br>'
                    f'Nearest div: {cd["nearest_div"]}d<br>'
                    f'Days away: <b style="color:{tool_colors[1]}">{abs(cd["days_to_div"])}</b><br>'
                    f'Date: {cd["next_div_date"].strftime("%d %b %Y")}</div></div>',
                    unsafe_allow_html=True,
                )
            with tc3:
                yr_rem = gd["days_from_low"] % 365
                st.markdown(
                    f'<div class="gc {"gc-green" if cd["tool3_active"] else "gc-red"}"><div style="font-weight:700;font-size:13px;margin-bottom:6px">'
                    f'{"✅" if cd["tool3_active"] else "❌"} Tool 3: Anniversary</div>'
                    f'<div style="font-size:12px;color:#94a3b8">Days in year: {yr_rem}<br>'
                    f'Days to anniversary: <b style="color:{tool_colors[2]}">{365-yr_rem}</b><br>'
                    f'Active if within ±5 days</div></div>',
                    unsafe_allow_html=True,
                )

            # Upcoming dates
            td1, td2 = st.columns(2)
            with td1:
                st.markdown("**Next Gann Cycle Dates**")
                for t, fd, da in gd["gann_future"]:
                    is_maj = t in [90, 144, 180, 360, 504, 720]
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

            # Step 6 — Price-Time Squaring (scale-corrected)
            sq_col = "#10b981" if is_squared else "#f59e0b"
            st.markdown(
                f"""<div class="gc {'gc-green' if is_squared else 'gc-gold'}">
                <div style="color:#f59e0b;font-weight:700;margin-bottom:6px">⚖️ Step 6: Price Squared with Time (Scale-Corrected)</div>
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px">
                <div style="font-size:13px;color:#94a3b8;line-height:2">
                Price ₹{price:,.2f} · Days {gd['days_from_low']} · Scale {gd['scale']}<br>
                Scaled time = {gd['days_from_low']} × {gd['scale']} = <b style="color:#f59e0b">₹{gd['scaled_time']:,.2f}</b><br>
                Deviation from price: <b style="color:{sq_col}">{squaring_pct}%</b> {"✅ Squared (<3%)" if is_squared else "⚠️ Not squared (>3%)"}
                </div>
                <div class="verdict-banner {'vb-buy' if is_squared else 'vb-caution'}" style="font-size:13px;padding:10px 16px;margin:0">
                {"🟢 PRICE = TIME" if is_squared else "🟡 NOT SQUARED"}
                </div>
                </div></div>""",
                unsafe_allow_html=True,
            )

            # Step 7 — Range Squaring
            hl_r   = gd["hl_range"]
            r_proj = (gd["anchor_low_date"] + timedelta(days=round(hl_r))).strftime("%d %b %Y")
            st.markdown(
                f"""<div class="gc gc-cyan"><div style="color:#f59e0b;font-weight:700;margin-bottom:6px">📏 Step 7: Range Squaring</div>
                <div style="font-size:13px;color:#94a3b8;line-height:2">
                HL Range ₹{hl_r:,.2f} · √Range {gd['range_sqrt']} · Time proj: {round(hl_r)}d → {r_proj}<br>
                Range Sq Target: <b style="color:#10b981;font-size:16px">₹{gd['range_sq_target']:,.2f}</b><br>
                Anchor √Price: {gd['anchor_sq9_root']} → +2 ring: <b style="color:#10b981">₹{round((gd['anchor_sq9_root']+2)**2,2):,.2f}</b>
                </div></div>""",
                unsafe_allow_html=True,
            )

            # Step 8 — Final Confluence Verdict
            cg1, cg2 = st.columns([1, 2])
            with cg1:
                conf_c = "#10b981" if gann_conf >= 4 else "#f59e0b" if gann_conf >= 3 else "#ef4444"
                tier_lbl = "🔥 TIER 1-2 HIGH" if gann_conf >= 4 else "⚡ TIER 3 MODERATE" if gann_conf >= 3 else "⏳ LOW / WAIT"
                st.markdown(
                    f'<div class="gc" style="text-align:center"><div class="kpi-label">🎯 Step 8: Confluence</div>'
                    f'<div style="font-size:64px;font-weight:900;font-family:JetBrains Mono,monospace;color:{conf_c}">{gann_conf}/5</div>'
                    f'{pb(gann_conf,5,conf_c)}'
                    f'<div style="color:{conf_c};font-weight:700">{tier_lbl}</div></div>',
                    unsafe_allow_html=True,
                )
            with cg2:
                r_html = "".join([
                    f'<div class="lc lc-{"green" if any(x in r for x in ["🔥","✅"]) else "gold" if "⚡" in r else "blue"}" '
                    f'style="font-size:12px;margin-bottom:5px">{r}</div>'
                    for r in gd["reasons"]
                ])
                st.markdown(
                    f'<div class="gc gc-gold"><div style="color:#f59e0b;font-weight:700;margin-bottom:8px">Confluence Breakdown:</div>{r_html}'
                    f'<div style="color:#475569;font-size:11px;margin-top:8px">'
                    f'Rule: Only trade Tier 1-2 (score ≥4) + technical confirmation. '
                    f'Tier 3 = watch only. Tier 4 = wait.</div></div>',
                    unsafe_allow_html=True,
                )

            # Final verdict
            gv_rr  = round((gd["gann_t1"] - price) / max(price - gd["gann_sl"], 0.01), 2)
            gv_cls = "vb-buy" if gann_conf >= 4 else "vb-caution" if gann_conf >= 3 else "vb-avoid"
            gv_txt = ("STRONG GANN SETUP" if gann_conf >= 4
                      else "WATCH — PARTIAL CONFLUENCE" if gann_conf >= 3
                      else "WAIT — CYCLES NOT ALIGNED")
            st.markdown(
                f"""<div class="gc gc-gold"><div class="verdict-banner {gv_cls}" style="margin-bottom:14px">🔶 {gv_txt}</div>
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:12px">
                    <div class="lc lc-blue" style="font-size:12px">📍 Anchor<br>₹{gd['anchor_low']:,.2f} · {gd['anchor_low_date'].strftime('%d %b %Y')}</div>
                    <div class="lc lc-gold" style="font-size:12px">📐 Angle Zone<br>{angle_label}</div>
                    <div class="lc {'lc-green' if is_squared else 'lc-gold'}" style="font-size:12px">⚖️ P=T<br>{"✅ Squared" if is_squared else f"⚠️ {squaring_pct}% off"}</div>
                    <div class="lc lc-green" style="font-size:12px">🎯 T1 (Sq9 R1)<br>₹{gd['gann_t1']:,.2f}</div>
                    <div class="lc lc-blue"  style="font-size:12px">🎯 T2 (Sq9 R2)<br>₹{gd['gann_t2']:,.2f}</div>
                    <div class="lc lc-red"   style="font-size:12px">🛑 SL (Sq9 S2)<br>₹{gd['gann_sl']:,.2f}</div>
                </div>
                <div style="font-size:12px;color:#64748b">
                R:R 1:{gv_rr} {"✅" if gv_rr>=2.5 else "⚠️"} · 
                Sq9 root {gd['sq9_root']} · 
                Scale {gd['scale']} pts/day · 
                Range target ₹{gd['range_sq_target']:,.2f}
                </div></div>""",
                unsafe_allow_html=True,
            )


    elif symbol and not should_analyze:
        st.info("Press **Search** to analyze this symbol.")
    else:
        st.markdown(
            '<div style="color:#475569;text-align:center;padding:40px 0">Enter an NSE symbol above and press Search</div>',
            unsafe_allow_html=True,
        )

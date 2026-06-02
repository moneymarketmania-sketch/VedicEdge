import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import math
import requests
import io
import plotly.graph_objects as go

# ── CONFIGURATION & STYLING ──────────────────────────────────────────────────
st.set_page_config(page_title="VedicEdge", page_icon="🔵", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght=300;400;500;600;700&family=JetBrains+Mono:wght=400;700&display=swap');

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

# ── SESSION STATE INITIALIZATION ─────────────────────────────────────────────
for k, v in [
    ("selected_symbol", "RELIANCE"),
    ("scan_results", []),
    ("scan_ran", False),
    ("analyze_triggered", True),
    ("last_symbol", ""),
]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── HELPER STYLING METHODS ────────────────────────────────────────────────────
def pb(val, max_val, color):
    pct = min(100, max(0, val / max_val * 100))
    return f'<div class="pb-wrap"><div class="pb-fill" style="width:{pct}%;background:{color}"></div></div>'

def kpi(label, val, color="#e8edf5", sub=None):
    sub_h = f'<div style="font-size:11px;color:#64748b;margin-top:3px">{sub}</div>' if sub else ""
    return f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-val" style="color:{color}">{val}</div>{sub_h}</div>'

def safe_html(text):
    return str(text).replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# ── DATA FETCH PIPELINES (WITH MULTI-ASSET INDEX MAPPING SUPPORT) ────────────
@st.cache_data(ttl=180, show_spinner=False)
def fetch_stock_data(symbol):
    try:
        # Resolve index symbols for structural calculation validation
        sym_upper = symbol.strip().upper()
        if sym_upper in ["NIFTY", "NIFTY50", "NIFTY 50", "^NSEI"]:
            ticker_symbol = "^NSEI"
        elif sym_upper in ["BANKNIFTY", "BANK NIFTY", "NIFTYBANK", "^NSEBANK"]:
            ticker_symbol = "^NSEBANK"
        elif symbol.startswith("^"):
            ticker_symbol = symbol
        else:
            ticker_symbol = f"{symbol}.NS"

        tk = yf.Ticker(ticker_symbol)
        hist = tk.history(period="1y", auto_adjust=True)
        if not hist.empty:
            hist.index = hist.index.tz_localize(None) if hist.index.tzinfo is None else hist.index.tz_convert(None)

        if hist.empty or len(hist) < 10:
            raise ValueError("Empty or invalid history context returned.")

        try:
            fi = tk.fast_info
            price = float(fi.last_price or fi.regular_market_price or hist["Close"].iloc[-1])
            prev  = float(fi.previous_close or hist["Close"].iloc[-2])
        except Exception:
            price = float(hist["Close"].iloc[-1])
            prev  = float(hist["Close"].iloc[-2])

        chg = round((price - prev) / prev * 100, 2)

        try:
            info   = tk.info
            beta   = float(info.get("beta") or 1.0)
            pe     = float(info.get("trailingPE") or 0)
            pb_val = float(info.get("priceToBook") or 3.5)
            sector = info.get("sector", "Index / Benchmark") if "NSE" in ticker_symbol else info.get("sector", "Unknown")
            name   = info.get("longName", symbol) or symbol
            volume = int(info.get("volume") or hist["Volume"].iloc[-1])
        except Exception:
            beta   = 1.0
            pe     = 0.0
            pb_val = 3.5
            sector = "Index / Benchmark" if "NSE" in ticker_symbol else "Unknown"
            name   = symbol
            volume = int(hist["Volume"].iloc[-1])

        pe = round(pe, 1) if pe and pe > 0 else 25.0
        pb_val = round(pb_val, 2)

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
        st.warning(f"⚠️ Live Data fetch fallback triggered for {symbol} — structural demo configuration applied.")
        return dict(
            price=24210.50 if "NIFTY" in symbol.upper() else 51430.20, change_pct=0.45, rsi=58.4, atr=150.0, atr_pct=0.65,
            beta=1.0, volume=25000000, pe=22.5, pb=4.1, hist=None, source="DEMO", sector="Index / Benchmark", name=symbol, w52h=26000.0, w52l=21000.0
        )

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_long_history(symbol):
    try:
        sym_upper = symbol.strip().upper()
        if sym_upper in ["NIFTY", "NIFTY50", "NIFTY 50", "^NSEI"]:
            ticker_symbol = "^NSEI"
        elif sym_upper in ["BANKNIFTY", "BANK NIFTY", "NIFTYBANK", "^NSEBANK"]:
            ticker_symbol = "^NSEBANK"
        elif symbol.startswith("^"):
            ticker_symbol = symbol
        else:
            ticker_symbol = f"{symbol}.NS"

        tk = yf.Ticker(ticker_symbol)
        h = tk.history(period="10y")
        if not h.empty:
            h.index = h.index.tz_localize(None) if h.index.tzinfo is None else h.index.tz_convert(None)
        return h
    except Exception:
        return None

# ── TECHNICAL ENGINE ANALYTICS ───────────────────────────────────────────────
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
        stoch_k = round(float(((c - lo14) / (hi14 - lo14).clip(lower=0.01) * 100).iloc[-1]), 1)
        stoch_d = round(float(((c - lo14) / (hi14 - lo14).clip(lower=0.01) * 100).rolling(3).mean().iloc[-1]), 1)
        vol20 = round(float(h["Volume"].rolling(20).mean().iloc[-1]))
        volr  = round(data["volume"] / max(vol20, 1), 2)
        tr_s = pd.concat([
            h["High"] - h["Low"],
            (h["High"] - h["Close"].shift()).abs(),
            (h["Low"]  - h["Close"].shift()).abs(),
        ], axis=1).max(axis=1)
        atr14 = tr_s.ewm(alpha=1/14, min_periods=14, adjust=False).mean()

        dmp_raw = h["High"].diff().clip(lower=0)
        dmn_raw = (-h["Low"].diff()).clip(lower=0)
        dmp = dmp_raw.where(dmp_raw > dmn_raw, 0)
        dmn = dmn_raw.where(dmn_raw > dmp_raw, 0)

        di_pos_s = dmp.ewm(alpha=1/14, min_periods=14, adjust=False).mean()
        di_neg_s = dmn.ewm(alpha=1/14, min_periods=14, adjust=False).mean()
        di_pos = round(float((di_pos_s / atr14.clip(lower=0.01) * 100).iloc[-1]), 1)
        di_neg = round(float((di_neg_s / atr14.clip(lower=0.01) * 100).iloc[-1]), 1)
        dx_series = ((di_pos_s - di_neg_s).abs() / (di_pos_s + di_neg_s).clip(lower=0.01)) * 100
        adx = round(float(dx_series.ewm(alpha=1/14, min_periods=14, adjust=False).mean().iloc[-1]), 1)

        h_copy = h.copy()
        h_copy.index = pd.to_datetime(h_copy.index)
        weekly = h_copy.resample("W").agg({"High": "max", "Low": "min", "Close": "last"}).dropna()
        if len(weekly) >= 2:
            wph, wpl, wpc = round(float(weekly["High"].iloc[-2]), 2), round(float(weekly["Low"].iloc[-2]), 2), round(float(weekly["Close"].iloc[-2]), 2)
        else:
            wph, wpl, wpc = round(float(h["High"].iloc[-2]), 2), round(float(h["Low"].iloc[-2]), 2), round(float(h["Close"].iloc[-2]), 2)
        w_pivot = round((wph + wpl + wpc) / 3, 2)
        w_r1, w_s1 = round(2*w_pivot - wpl, 2), round(2*w_pivot - wph, 2)
        w_r2, w_s2 = round(w_pivot + (wph - wpl), 2), round(w_pivot - (wph - wpl), 2)
        w_cpr_pct = round((w_r1 - w_s1) / p * 100, 2)

        monthly = h_copy.resample("ME").agg({"High": "max", "Low": "min", "Close": "last"}).dropna()
        if len(monthly) >= 2:
            mph, mpl, mpc = round(float(monthly["High"].iloc[-2]), 2), round(float(monthly["Low"].iloc[-2]), 2), round(float(monthly["Close"].iloc[-2]), 2)
        else:
            mph, mpl, mpc = wph, wpl, wpc
        m_pivot = round((mph + mpl + mpc) / 3, 2)
        m_r1, m_s1 = round(2*m_pivot - mpl, 2), round(2*m_pivot - mph, 2)
        m_r2, m_s2 = round(m_pivot + (mph - mpl), 2), round(m_pivot - (mph - mpl), 2)
        m_cpr_pct = round((m_r1 - m_s1) / p * 100, 2)

        swing_highs, swing_lows = [], []
        for i in range(10, len(h) - 10):
            if h["High"].iloc[i] == h["High"].iloc[i-10:i+10].max(): swing_highs.append(round(float(h["High"].iloc[i]), 2))
            if h["Low"].iloc[i] == h["Low"].iloc[i-10:i+10].min(): swing_lows.append(round(float(h["Low"].iloc[i]), 2))
        key_res = sorted([x for x in swing_highs if x > p])[:3]
        key_sup = sorted([x for x in swing_lows  if x < p], reverse=True)[:3]
        
        w52h, w52l = data["w52h"], data["w52l"]
        w52h_prox = round((w52h - p) / p * 100, 1)
        w52l_prox = round((p - w52l) / p * 100, 1)
    else:
        ema9 = ema21 = ema55 = ema200 = p
        macd_val = 0.5; macd_sig = 0.2; macd_hist = 0.3
        bb_upper = round(p*1.04, 2); bb_lower = round(p*0.96, 2); bb_mid = p
        stoch_k = 55.0; stoch_d = 52.0; vol20 = data["volume"]; volr = 1.0
        di_pos = 22.0; di_neg = 18.0; adx = 24.0
        w_pivot = w_r1 = w_s1 = w_r2 = w_s2 = p; w_cpr_pct = 1.5
        m_pivot = m_r1 = m_s1 = m_r2 = m_s2 = p; m_cpr_pct = 3.0
        key_res = [round(p*1.03,2)]; key_sup = [round(p*0.97,2)]
        w52h = w52l = p; w52h_prox = w52l_prox = 0.0

    return dict(
        ema9=ema9, ema21=ema21, ema55=ema55, ema200=ema200,
        macd_val=macd_val, macd_sig=macd_sig, macd_hist=macd_hist,
        bb_upper=bb_upper, bb_lower=bb_lower, bb_mid=bb_mid, stoch_k=stoch_k, stoch_d=stoch_d,
        vol20=vol20, volr=volr, di_pos=di_pos, di_neg=di_neg, adx=adx,
        w_pivot=w_pivot, w_r1=w_r1, w_s1=w_s1, w_r2=w_r2, w_s2=w_s2, w_cpr_pct=w_cpr_pct,
        m_pivot=m_pivot, m_r1=m_r1, m_s1=m_s1, m_r2=m_r2, m_s2=m_s2, m_cpr_pct=m_cpr_pct,
        key_res=key_res, key_sup=key_sup, w52h=w52h, w52l=w52l, w52h_prox=w52h_prox, w52l_prox=w52l_prox
    )

def compute_tech_score(data, tech):
    p = data["price"]
    ts = 0
    bull, bear = [], []
    if p > tech["ema9"] and p > tech["ema21"] and p > tech["ema55"]:
        ts += 2; bull.append("Above EMA9/21/55 cluster alignment structure.")
    elif p > tech["ema9"]:
        ts += 1; bull.append("Holding short-term fast momentum threshold.")
    else:
        ts -= 1; bear.append("Below structural short-term EMAs.")
    if p > tech["ema200"]:
        ts += 1; bull.append("Trading safely above secular 200 EMA support.")
    else:
        ts -= 2; bear.append("Below major 200 EMA macro breakdown barrier.")
    if 40 < data["rsi"] < 70:
        ts += 1
    elif data["rsi"] >= 70:
        ts -= 1; bear.append(f"RSI overextended tracking at extreme overbought: {data['rsi']}")
    else:
        ts += 1; bull.append(f"RSI oversold baseline offering bounce margin: {data['rsi']}")
    if tech["macd_hist"] > 0:
        ts += 1; bull.append("MACD histogram printing positive acceleration bars.")
    else:
        ts -= 1; bear.append("MACD cross flashing downward distribution phase.")
    if tech["volr"] > 1.2:
        ts += 1; bull.append(f"Volume accumulation expanding at {tech['volr']}x normal avg.")
    if tech["adx"] > 22 and tech["di_pos"] > tech["di_neg"]:
        ts += 1; bull.append(f"ADX directional strength showing expansion wave ({tech['adx']})")
    
    normalized = int(min(100, max(0, ((ts + 5) / 12) * 100)))
    return normalized, bull, bear

# ── MATHEMATICAL GANN CHAKRA ALGORITHMS ──────────────────────────────────────
def _find_significant_anchor(hist):
    if hist is None or hist.empty:
        return None
    # Find ultimate standard cycle support floor over past lookback period
    low_idx = hist["Low"].idxmin()
    low_val = float(hist["Low"].min())
    idx_list = hist.index.tolist()
    try:
        offset = idx_list.index(low_idx)
    except ValueError:
        offset = 0
    return {"price": low_val, "offset": offset, "date": low_idx.date() if hasattr(low_idx, "date") else low_idx}

def _find_trailing_anchor(hist, lookback_bars=45):
    """Calculates dynamic intermediate structural lookback swings."""
    if hist is None or len(hist) < lookback_bars:
        return None
    recent_df = hist.tail(lookback_bars)
    trail_low = float(recent_df["Low"].min())
    trail_low_idx = recent_df["Low"].idxmin()
    full_idx_list = hist.index.tolist()
    try:
        day_offset = full_idx_list.index(trail_low_idx)
    except ValueError:
        day_offset = len(full_idx_list) - lookback_bars
    return {"price": trail_low, "offset": day_offset, "date": trail_low_idx.date() if hasattr(trail_low_idx, "date") else trail_low_idx}

def square_of_nine_levels(base_price):
    if base_price <= 0: return []
    base_root = math.sqrt(base_price)
    angles = [45, 90, 135, 180, 225, 270, 315, 360]
    colors = ["#ef4444", "#f59e0b", "#3b82f6", "#10b981", "#ef4444", "#f59e0b", "#3b82f6", "#8b5cf6"]
    levels = []
    # Structural calculation matrices across up/down wheels
    for ang, col in zip(angles, colors):
        factor = ang / 180.0
        up_val = (base_root + factor) ** 2
        levels.append((f"Sq9 Resistance (+{ang}°)", round(up_val, 2), col))
    for ang, col in zip(reversed(angles), reversed(colors)):
        factor = ang / 180.0
        dn_val = (base_root - factor) ** 2
        if dn_val > 0:
            levels.append((f"Sq9 Support (-{ang}°)", round(dn_val, 2), col))
    return levels

def compute_gann_data(data):
    if data.get("hist") is None:
        return dict(anchor_low=300.0, anchor_low_date=datetime.now(), scale=1.0, gann_t1=320.0, gann_t2=340.0, gann_sl=290.0, sq9_root=17.32, days_from_anchor=10)
    
    h = data["hist"]
    p = data["price"]
    anchor = _find_significant_anchor(h)
    anchor_low = anchor["price"]
    
    # Scale calculation framework
    raw_diff = float(h["High"].max() - h["Low"].min())
    raw_days = max(len(h), 1)
    scale = raw_diff / raw_days if raw_days > 0 else 1.0
    mag = 10 ** math.floor(math.log10(scale)) if scale > 0 else 1
    normalized_scale = round(scale / mag) * mag
    if normalized_scale <= 0: normalized_scale = 0.1
    
    sq9_all = square_of_nine_levels(anchor_low)
    res_l = [v for l, v, c in sq9_all if "Resistance" in l]
    sup_l = [v for l, v, c in sq9_all if "Support" in l]
    
    gann_t1 = res_l[0] if len(res_l) > 0 else p * 1.05
    gann_t2 = res_l[1] if len(res_l) > 1 else p * 1.10
    gann_sl = sup_l[1] if len(sup_l) > 1 else p * 0.95
    
    days_from_anchor = len(h) - anchor["offset"]
    sq9_root = round(math.sqrt(p), 2)
    
    return dict(
        anchor_low=anchor_low, anchor_low_date=anchor["date"], scale=normalized_scale,
        gann_t1=gann_t1, gann_t2=gann_t2, gann_sl=gann_sl, sq9_root=sq9_root,
        days_from_anchor=days_from_anchor, sq9_levels=sq9_all
    )

def evaluate_gann_squaring(data, gd):
    p = data["price"]
    days = gd["days_from_anchor"]
    scale = gd["scale"]
    
    calc_1x1_price = gd["anchor_low"] + (days * scale)
    diff_pct = round(abs(p - calc_1x1_price) / p * 100, 2)
    is_squared = diff_pct <= 2.5 # 2.5% proximity threshold criterion
    
    gs = 85 if is_squared else 45
    if p > gd["gann_t1"]: gs += 15
    elif p < gd["gann_sl"]: gs -= 20
    
    return int(min(100, max(0, gs))), is_squared, diff_pct

# ── ENHANCED ADVANCED CHART ENGINE ───────────────────────────────────────────
def _build_gann_chart(hist_after, anchor_low, scale, sq9_levels, days_arr, high_arr, low_arr, close_arr, proj_days, trail_anchor=None):
    angle_x = list(range(0, proj_days, 1))
    def angle_y(rate): return [anchor_low + d * rate for d in angle_x]
    
    sq9_prices = [lv[1] for lv in sq9_levels if isinstance(lv[1], (int, float))]
    fig = go.Figure()
    
    # 1. Candlestick Core Trace
    fig.add_trace(go.Candlestick(
        x=days_arr, open=hist_after["Open"].tolist(), high=high_arr, low=low_arr, close=close_arr,
        name="Price Data", increasing_line_color="#10b981", decreasing_line_color="#ef4444", showlegend=False,
    ))
    
    # 2. Anchored Structural Gann Angle Vectors
    angle_specs = [
        (scale * 4, "4×1", "#ef4444", "dash"),
        (scale * 2, "2×1", "#f59e0b", "dash"),
        (scale * 1, "1×1 Vector", "#10b981", "solid"),
        (scale * 0.5, "1×2", "#f59e0b", "dot"),
        (scale * 0.25,"1×4", "#ef4444", "dot"),
    ]
    for rate, label, color, dash in angle_specs:
        fig.add_trace(go.Scatter(
            x=angle_x, y=angle_y(rate), mode="lines", name=label,
            line=dict(color=color, width=1.5 if "1×1" in label else 1, dash=dash), opacity=0.4
        ))

    # 3. Dynamic Trailing Lookback Angle Systems
    if trail_anchor and trail_anchor["price"] > 0:
        t_start_x = trail_anchor["offset"]
        t_low = trail_anchor["price"]
        
        trail_specs = [
            (scale * 1, "Trailing 1×1", "#06b6d4", "dash"),
            (scale * 2, "Trailing 2×1", "#3b82f6", "dashdot")
        ]
        for t_rate, t_label, t_color, t_dash in trail_specs:
            t_x = [d for d in angle_x if d >= t_start_x]
            t_y = [t_low + ((d - t_start_x) * t_rate) for d in t_x]
            fig.add_trace(go.Scatter(
                x=t_x, y=t_y, mode="lines", name=t_label,
                line=dict(color=t_color, width=1.3, dash=t_dash), opacity=0.55
            ))

    # 4. Confluence Vector × Level Intersection Intersections
    conf_x, conf_y, conf_text = [], [], []
    current_day_idx = len(days_arr) - 1 
    
    for rate, label, _, _ in angle_specs:
        for d in angle_x:
            if abs(d - current_day_idx) <= 15: # Trading proximity matrix lookahead window
                calc_angle_p = anchor_low + (d * rate)
                for sq9_p in sq9_prices:
                    if abs(calc_angle_p - sq9_p) / sq9_p <= 0.004: # 0.4% mathematical convergence zone tolerance
                        conf_x.append(d)
                        conf_y.append(sq9_p)
                        conf_text.append(f"🎯 Confluence Zone: {label} × Sq9 Wheel Level (₹{sq9_p:,.2f}) at Day index {d}")

    if conf_x:
        fig.add_trace(go.Scatter(
            x=conf_x, y=conf_y, mode="markers", name="Confluence Nodes",
            marker=dict(color="#c084fc", size=10, symbol="hexagon-open", line=dict(color="#8b5cf6", width=2.5)),
            text=conf_text, hoverinfo="text"
        ))

    # 5. Square of 9 Radial Support/Resistance Grid Lines
    for label, val, col in sq9_levels:
        if isinstance(val, (int, float)):
            fig.add_hline(y=val, line_dash="dash", line_color=col, line_width=0.8, opacity=0.4,
                          annotation_text=f"{label} (₹{val:,.1f})", annotation_position="left")

    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.03)", title="Gann Axis Timeline (Days From Origin)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.03)", title="Price Matrix Axis (₹)", side="right"),
        margin=dict(l=10, r=10, t=20, b=20), height=580, showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

# ── APPLICATION CONTROL ENTRY UI LAYOUTS ─────────────────────────────────────
st.markdown('<div class="sec-title">🔍 Asset Analysis Core Scanner</div>', unsafe_allow_html=True)

col_search, col_indices = st.columns([2, 2])

with col_search:
    current_symbol = st.session_state.get("selected_symbol", "RELIANCE")
    symbol_input = st.text_input(
        "Stock Ticker Symbol Entry",
        value=current_symbol,
        placeholder="Enter asset identifier (e.g. RELIANCE, NIFTY)",
        key="symbol_text_entry_field"
    )
    if symbol_input.upper().strip() != current_symbol and symbol_input.strip() != "":
        st.session_state["selected_symbol"] = symbol_input.upper().strip()
        st.session_state["analyze_triggered"] = True

with col_indices:
    st.markdown('<div style="font-size:11px; text-transform:uppercase; color:var(--muted); margin-bottom:6px; letter-spacing:1px;">Quick Benchmark Asset Selectors</div>', unsafe_allow_html=True)
    idx_col1, idx_col2 = st.columns(2)
    with idx_col1:
        if st.button("📈 NIFTY 50", use_container_width=True):
            st.session_state["selected_symbol"] = "NIFTY"
            st.session_state["analyze_triggered"] = True
            st.rerun()
    with idx_col2:
        if st.button("🏦 BANK NIFTY", use_container_width=True):
            st.session_state["selected_symbol"] = "BANKNIFTY"
            st.session_state["analyze_triggered"] = True
            st.rerun()

# ── COMPUTATIONAL CORE DISPATCHER EXECUTION ──────────────────────────────────
if st.session_state["analyze_triggered"]:
    active_sym = st.session_state["selected_symbol"]
    
    with st.spinner(f"Processing mathematical metrics calculations for {active_sym}..."):
        data = fetch_stock_data(active_sym)
        tech = compute_technicals(data)
        gd = compute_gann_data(data)
        
        tech_score, bull_reasons, bear_reasons = compute_tech_score(data, tech)
        gann_score, is_squared, squaring_pct = evaluate_gann_squaring(data, gd)
        
        cv_final = int((tech_score * 0.7) + (gann_score * 0.3))
        
        if cv_final >= 70:
            cv_lbl, cv_cls, cv_icon = "BUY / ACCUMULATE", "vb-buy", "🟢"
        elif cv_final >= 50:
            cv_lbl, cv_cls, cv_icon = "CAUTIOUS CONFIRMATION", "vb-caution", "🟡"
        elif cv_final >= 35:
            cv_lbl, cv_cls, cv_icon = "NEUTRAL SIDEBAND", "vb-caution", "⚪"
        else:
            cv_lbl, cv_cls, cv_icon = "AVOID / LIQUIDATE", "vb-avoid", "🔴"

    # ── METRIC TOP ROW SUMMARY PRESENTATION CARD LAYOUT ──────────────────────
    st.markdown(f'<div class="sec-title">📊 {safe_html(data["name"])} (Sector: {safe_html(data["sector"])})</div>', unsafe_allow_html=True)
    
    ch_col = "var(--green)" if data["change_pct"] >= 0 else "var(--red)"
    ch_sgn = "+" if data["change_pct"] >= 0 else ""
    
    kpi_cols = st.columns(5)
    with kpi_cols[0]: st.markdown(kpi("Spot Trading Price", f"₹{data['price']:,.2f}", ch_col, f"{ch_sgn}{data['change_pct']}% Close Change"), unsafe_allow_html=True)
    with kpi_cols[1]: st.markdown(kpi("14-Bar RSI Oscillator", f"{data['rsi']}", "var(--gold)" if data['rsi']>65 else "var(--green)", "Momentum Tracker"), unsafe_allow_html=True)
    with kpi_cols[2]: st.markdown(kpi("Gann Scale Factor Floor", f"{gd['scale']:.2f}", "var(--cyan)", "Corrected Range Multiplier"), unsafe_allow_html=True)
    with kpi_cols[3]: st.markdown(kpi("Square of 9 Anchor", f"₹{gd['anchor_low']:,.2f}", "var(--purple)", f"Origin Date: {gd['anchor_low_date']}"), unsafe_allow_html=True)
    with kpi_cols[4]: st.markdown(kpi("Price-Time Space Matrix", "SQUARED ✅" if is_squared else "ASYMMETRIC", "var(--green)" if is_squared else "var(--muted)", f"{squaring_pct}% off axis deviation"), unsafe_allow_html=True)

    # ── TABBED IN-DEPTH DIAGNOSTIC BREAKDOWNS ────────────────────────────────
    overview_tab, tech_tab, gann_tab = st.tabs(["📊 Overview Analysis Dashboard", "📈 In-Depth Quantitative Technicals", "🔶 In-Depth Gann Chakra Mathematics"])
    
    with overview_tab:
        st.markdown(f'<div class="verdict-banner {cv_cls}">{cv_icon} Consensus Core Target: {cv_lbl} — Weighted Score Matrix: {cv_final}/100</div>', unsafe_allow_html=True)
        ov_col1, ov_col2 = st.columns(2)
        with ov_col1:
            st.markdown('<div class="gc gc-green"><h4 style="color:var(--green); margin-top:0;">Structural Bullish Accumulation Elements</h4>', unsafe_allow_html=True)
            for r in bull_reasons:
                st.markdown(f'<div class="lc lc-green">{r}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with ov_col2:
            st.markdown('<div class="gc gc-red"><h4 style="color:var(--red); margin-top:0;">Structural Bearish Distribution Flags</h4>', unsafe_allow_html=True)
            if not bear_reasons:
                st.markdown('<div class="lc lc-blue">No significant bearish structural deviations detected.</div>', unsafe_allow_html=True)
            for r in bear_reasons:
                st.markdown(f'<div class="lc lc-red">{r}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tech_tab:
        t_col1, t_col2 = st.columns([1, 1])
        with t_col1:
            st.markdown('<div class="gc">', unsafe_allow_html=True)
            st.markdown(f"**Exponential Moving Average Trackers:**<br>• EMA(9 Fast Trend Filter): ₹{tech['ema9']:,.2f}<br>• EMA(21 Swing Allocation): ₹{tech['ema21']:,.2f}<br>• EMA(55 Mid Baseline): ₹{tech['ema55']:,.2f}<br>• EMA(200 Secular Support): ₹{tech['ema200']:,.2f}", unsafe_allow_html=True)
            st.markdown(f"<br>**Trend Intensity Matrices:**<br>• ADX Trend Power Filter: {tech['adx']}<br>• Plus DI Acceleration Vector: {tech['di_pos']}<br>• Minus DI Distribution Vector: {tech['di_neg']}", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with t_col2:
            st.markdown('<div class="gc">', unsafe_allow_html=True)
            st.markdown(f"**Classical Weekly Floor Pivot System:**<br>• Resistance 2 Barrier: ₹{tech['w_r2']:,.2f}<br>• Resistance 1 Barrier: ₹{tech['w_r1']:,.2f}<br>• Central Base Pivot Line: ₹{tech['w_pivot']:,.2f}<br>• Support 1 Floor: ₹{tech['w_s1']:,.2f}<br>• Support 2 Floor: ₹{tech['w_s2']:,.2f}", unsafe_allow_html=True)
            st.markdown(f"<br>**Volatility Bandwidth Filters:**<br>• Bollinger Upper Band (2.0σ): ₹{tech['bb_upper']:,.2f}<br>• Bollinger Midline Core: ₹{tech['bb_mid']:,.2f}<br>• Bollinger Lower Band (2.0σ): ₹{tech['bb_lower']:,.2f}", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with gann_tab:
        g_col_txt, g_col_cht = st.columns([1, 2])
        with g_col_txt:
            st.markdown(f"""
            <div class="gc {'gc-green' if is_squared else 'gc-gold'}">
                <h4 style="color:var(--gold); margin-top:0;">🔶 Gann Space Matrix Quantifiers</h4>
                <div class="lc lc-gold"><b>Target Resistance 1 (+45°):</b> ₹{gd['gann_t1']:,.2f}</div>
                <div class="lc lc-blue"><b>Target Resistance 2 (+90°):</b> ₹{gd['gann_t2']:,.2f}</div>
                <div class="lc lc-red"><b>Invalidation Stop Loss (-90°):</b> ₹{gd['gann_sl']:,.2f}</div>
                <hr>
                <div style="font-size:13px; color:var(--muted); line-height:1.6">
                    • Square root calculation index: {gd['sq9_root']}<br>
                    • Linear days scalar offset from vector base: {gd['days_from_anchor']} intervals<br>
                    • Scale-corrected price alignment vector: ₹{gd['anchor_low'] + (gd['days_from_anchor'] * gd['scale']):,.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with g_col_cht:
            if data.get("hist") is not None:
                h_df = data["hist"]
                anchor_offset = _find_significant_anchor(h_df)["offset"]
                hist_after = h_df.iloc[anchor_offset:]
                
                days_arr = list(range(0, len(hist_after)))
                high_arr = hist_after["High"].tolist()
                low_arr = hist_after["Low"].tolist()
                close_arr = hist_after["Close"].tolist()
                
                proj_days = len(days_arr) + 30
                
                # Fetch Lookback Trailing Dynamic Low
                trailing_data = _find_trailing_anchor(h_df, lookback_bars=45)
                
                fig = _build_gann_chart(
                    hist_after, gd['anchor_low'], gd['scale'], gd['sq9_levels'],
                    days_arr, high_arr, low_arr, close_arr, proj_days,
                    trail_anchor=trailing_data
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 Charting framework unavailable under current mock dataset environments configuration.")

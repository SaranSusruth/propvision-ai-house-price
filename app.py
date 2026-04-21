import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG  (must be the very first Streamlit call)
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="PropVision AI — House Price Intelligence",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #080b12;
    color: #e2e8f0;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.2rem 2.5rem 3rem; max-width: 1440px; }

/* ══ SIDEBAR — Glass Control Panel ══ */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #08101f 0%, #0d1829 50%, #080f1c 100%);
    border-right: 1px solid rgba(59,130,246,0.15);
}
[data-testid="stSidebar"] .block-container { padding: 0.8rem 1rem 2rem; }

/* Sidebar brand strip */
.sb-brand {
    text-align: center;
    padding: 1.2rem 0 1rem;
    margin-bottom: 0.8rem;
    border-bottom: 1px solid rgba(59,130,246,0.12);
}
.sb-brand-icon {
    font-size: 2rem;
    display: block;
    margin-bottom: 0.2rem;
}
.sb-brand-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 700;
    background: linear-gradient(90deg, #93c5fd, #fbbf24);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.5px;
}
.sb-brand-sub {
    font-size: 0.65rem;
    color: #475569;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.15rem;
}

/* Sidebar step badge */
.step-badge {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.55rem 0.8rem;
    margin: 0.5rem 0 0.3rem;
    background: rgba(59,130,246,0.06);
    border-left: 3px solid #3b82f6;
    border-radius: 0 8px 8px 0;
}
.step-num {
    background: linear-gradient(135deg, #1d4ed8, #3b82f6);
    color: #fff;
    font-size: 0.62rem;
    font-weight: 700;
    width: 18px; height: 18px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    letter-spacing: 0;
}
.step-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    color: #93c5fd;
}

/* Glass input card */
.glass-card {
    background: rgba(17,24,39,0.7);
    border: 1px solid rgba(59,130,246,0.12);
    border-radius: 12px;
    padding: 0.9rem 1rem 1rem;
    margin-bottom: 0.7rem;
    backdrop-filter: blur(8px);
}
.glass-card-title {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 0.7rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

/* ── Predict Button ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 60%, #3b82f6 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.8px !important;
    width: 100% !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 18px rgba(59,130,246,0.4) !important;
    margin-top: 0.4rem !important;
}
div[data-testid="stButton"] > button:hover {
    box-shadow: 0 6px 28px rgba(59,130,246,0.65) !important;
    transform: translateY(-2px) !important;
}

/* Model info pill */
.model-pill {
    background: rgba(8,16,31,0.8);
    border: 1px solid rgba(59,130,246,0.15);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-top: 0.8rem;
}
.pill-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.72rem;
    color: #475569;
    padding: 0.18rem 0;
}
.pill-val { color: #94a3b8; font-weight: 500; }
.pill-val.green { color: #34d399; }
.pill-val.blue  { color: #93c5fd; }
.pill-val.gold  { color: #fbbf24; }

/* ══ HERO ══ */
.hero-banner {
    background: linear-gradient(135deg, #0a1628 0%, #0f2347 35%, #0d1b35 65%, #080b12 100%);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 18px;
    padding: 2.2rem 3rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute; top: -80px; right: -80px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute; bottom: -50px; left: 25%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(251,191,36,0.07) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(59,130,246,0.1);
    border: 1px solid rgba(59,130,246,0.3);
    color: #93c5fd;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 0.9rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    background: linear-gradient(100deg, #ffffff 0%, #93c5fd 45%, #fbbf24 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.6rem;
    line-height: 1.05;
}
.hero-sub {
    font-size: 1rem;
    color: #64748b;
    font-weight: 300;
    max-width: 620px;
    line-height: 1.65;
    margin: 0;
}

/* ══ SECTION LABEL ══ */
.section-label {
    font-size: 0.66rem;
    font-weight: 600;
    letter-spacing: 2.8px;
    text-transform: uppercase;
    color: #3b82f6;
    margin-bottom: 0.8rem;
}

/* ══ METRIC CARDS ══ */
.metric-card {
    background: linear-gradient(145deg, #0e1623, #111d2e);
    border: 1px solid rgba(30,45,64,0.8);
    border-radius: 14px;
    padding: 1.3rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, box-shadow 0.3s;
    height: 100%;
}
.metric-card:hover {
    border-color: rgba(59,130,246,0.4);
    box-shadow: 0 4px 24px rgba(59,130,246,0.1);
}
.metric-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 2px; border-radius: 14px 14px 0 0;
}
.metric-card.blue::before   { background: linear-gradient(90deg,#3b82f6,#60a5fa); }
.metric-card.gold::before   { background: linear-gradient(90deg,#f59e0b,#fbbf24); }
.metric-card.green::before  { background: linear-gradient(90deg,#10b981,#34d399); }
.metric-card.red::before    { background: linear-gradient(90deg,#ef4444,#f87171); }
.metric-card.purple::before { background: linear-gradient(90deg,#8b5cf6,#a78bfa); }
.metric-card.teal::before   { background: linear-gradient(90deg,#06b6d4,#22d3ee); }
.metric-label {
    font-size: 0.67rem;
    font-weight: 600;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.85rem;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.metric-value.highlight { color: #fbbf24; }
.metric-value.green-val { color: #34d399; }
.metric-delta { font-size: 0.75rem; color: #475569; }
.metric-delta.up   { color: #34d399; }
.metric-delta.down { color: #f87171; }

/* Demand bar */
.demand-bar-wrap {
    background: rgba(30,45,64,0.6);
    border-radius: 8px; height: 8px;
    overflow: hidden; margin: 0.35rem 0;
}
.demand-bar-fill { height: 100%; border-radius: 8px; transition: width 0.8s ease; }

/* ══ INSIGHT BOXES ══ */
.insight-box {
    background: linear-gradient(135deg, rgba(59,130,246,0.07), rgba(251,191,36,0.03));
    border: 1px solid rgba(59,130,246,0.18);
    border-left: 3px solid #3b82f6;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    font-size: 0.87rem;
    color: #94a3b8;
    line-height: 1.65;
}
.insight-box.warn {
    border-left-color: #f59e0b;
    background: linear-gradient(135deg, rgba(245,158,11,0.07), rgba(251,191,36,0.02));
    border-color: rgba(245,158,11,0.18);
}
.insight-box.success {
    border-left-color: #10b981;
    background: linear-gradient(135deg, rgba(16,185,129,0.07), rgba(52,211,153,0.02));
    border-color: rgba(16,185,129,0.18);
}
.insight-box strong { color: #e2e8f0; }

/* ══ RECOMMENDATION CARD ══ */
.rec-card {
    border-radius: 14px;
    padding: 1.5rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 1rem 0;
    border: 1px solid;
}
.rec-decision {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: -1px;
}
.rec-meta { text-align: right; }
.rec-conf { font-size: 0.8rem; color: #64748b; margin-bottom: 0.3rem; }
.conf-bar-wrap {
    background: rgba(30,45,64,0.6);
    border-radius: 8px; height: 6px;
    width: 140px; overflow: hidden;
}
.conf-bar-fill { height: 100%; border-radius: 8px; }

/* ══ DIVIDER ══ */
.fancy-divider {
    border: none; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(30,58,95,0.8), transparent);
    margin: 1.8rem 0;
}

/* ══ ANIMATIONS ══ */
@keyframes fadeSlideUp {
    from { opacity:0; transform:translateY(16px); }
    to   { opacity:1; transform:translateY(0); }
}
.animate-in { animation: fadeSlideUp 0.45s ease forwards; }
.delay-1 { animation-delay: 0.05s; }
.delay-2 { animation-delay: 0.10s; }
.delay-3 { animation-delay: 0.15s; }
.delay-4 { animation-delay: 0.20s; }

/* ══ TABS ══ */
[data-baseweb="tab-list"] { background: transparent !important; gap: 6px; }
[data-baseweb="tab"] {
    background: rgba(17,24,39,0.7) !important;
    border: 1px solid rgba(30,45,64,0.8) !important;
    border-radius: 8px !important;
    color: #475569 !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s !important;
}
[data-baseweb="tab"]:hover {
    border-color: rgba(59,130,246,0.3) !important;
    color: #64748b !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: rgba(59,130,246,0.12) !important;
    border-color: rgba(59,130,246,0.35) !important;
    color: #93c5fd !important;
}

/* ══ SLIDERS & SELECTS ══ */
[data-testid="stSlider"] > div > div > div > div { background: #3b82f6 !important; }
[data-testid="stSelectbox"] > div > div {
    background: rgba(17,24,39,0.8) !important;
    border: 1px solid rgba(30,45,64,0.8) !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}

/* Slider label */
[data-testid="stSlider"] label { font-size: 0.8rem !important; color: #64748b !important; }

/* Summary table */
.summary-table th {
    background: rgba(30,45,64,0.5) !important;
    color: #64748b !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
APP_CONFIG = {
    "currency_rate" : 83.5,
    "default_zone"  : "urban",
    "model_version" : "v4.0-propvision",
}

ZONE_DEMAND_BASE = {
    "luxury"  : 0.88,
    "urban"   : 0.75,
    "suburban": 0.58,
    "rural"   : 0.35,
}
ZONE_INFLATION_RATE = {
    "luxury"  : 0.085,
    "urban"   : 0.072,
    "suburban": 0.055,
    "rural"   : 0.032,
}


# ══════════════════════════════════════════════════════════════════════════════
#  LOAD MODEL BUNDLE
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource
def load_model():
    if not os.path.exists("model.pkl"):
        st.warning("⚠️ model.pkl not found — training now...")
        from train_model import train_model as _train
        return _train()
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

bundle = load_model()

if bundle is None:
    st.error("❌ Model failed to load. Run: python train_model.py")
    st.stop()   # only fires when bundle is actually None [B4]

model        = bundle["model"]
feat_cols    = bundle["feature_cols"]      # exact 10-column order
feat_imp     = bundle["feature_importance"]
model_r2     = bundle["r2_score"]
use_log      = bundle.get("log_transform", False)
area_max     = bundle.get("area_max", 4350.0)  # [B1] fallback to dataset max if old pkl

# Safe encoder setup [B8]
encoder      = bundle.get("encoder")
raw_classes  = list(getattr(encoder, "classes_", [])) if encoder is not None else []
zone_classes = (
    bundle.get("zone_classes")
    or (raw_classes if raw_classes else None)
    or ["luxury", "rural", "suburban", "urban"]
)
if encoder is not None and raw_classes:
    zone_enc_lookup = {z: int(encoder.transform([z])[0]) for z in raw_classes}
else:
    zone_enc_lookup = {z: i for i, z in enumerate(zone_classes)}


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def safe_encode(zone: str) -> int:
    """[B8] Fallback chain: zone → urban → first → 0"""
    return zone_enc_lookup.get(
        zone,
        zone_enc_lookup.get(APP_CONFIG["default_zone"],
        next(iter(zone_enc_lookup.values()), 0))
    )


def build_features(area, bedrooms, bathrooms, location_rating,
                   age, garage, pool, zone_enc) -> pd.DataFrame:
    """
    [B1][B2] Single function that builds the correct 10-column feature
    vector for the model. Used by BOTH main prediction and zone comparison.
    area_max comes from bundle — never hardcoded.
    """
    area_scaled    = area / area_max
    bed_bath_ratio = bedrooms / (bathrooms + 1)
    luxury_score   = location_rating * 0.4 + int(garage) * 0.2 + int(pool) * 0.4
    return pd.DataFrame(
        [[area_scaled, bedrooms, bathrooms, location_rating,
          age, int(garage), int(pool), zone_enc,
          bed_bath_ratio, luxury_score]],
        columns=feat_cols      # guaranteed column order matches training
    )


def safe_predict(features_df: pd.DataFrame) -> float:
    """[B3] Log-transform inverted exactly once."""
    raw = float(model.predict(features_df)[0])
    return max(float(np.expm1(raw)) if use_log else raw, 0.0)


def safe_pct(num: float, den: float) -> float:
    """[B5] Division-by-zero guard."""
    return (num / den * 100) if den > 0 else 0.0


def fmt(usd_val: float, show_inr: bool) -> str:
    """Format price with correct currency."""
    r = APP_CONFIG["currency_rate"]
    if show_inr:
        inr = usd_val * r
        if inr >= 1e7: return f"₹{inr/1e7:.2f} Cr"
        if inr >= 1e5: return f"₹{inr/1e5:.2f} L"
        return f"₹{inr:,.0f}"
    return f"${usd_val:,.0f}"


def compute_demand(zone: str, location_rating: int, area: int) -> float:
    base     = ZONE_DEMAND_BASE.get(zone, 0.5)
    loc_mod  = (location_rating - 1) / 9
    area_mod = min(area / 5000, 1.0)
    return round(min(0.55 * base + 0.30 * loc_mod + 0.15 * area_mod, 1.0), 4)


def demand_to_multiplier(score: float, sensitivity: float = 1.0) -> float:
    """[B7] Sensitivity wired in here."""
    return round(min(1.0 + score * 0.35 * sensitivity, 1.50), 4)


def demand_label(score: float):
    """[B10] Thresholds aligned with gauge steps."""
    if score >= 0.75: return "🔥 Extremely High", "red"
    if score >= 0.55: return "📈 High",            "gold"
    if score >= 0.35: return "⚖️ Moderate",         "blue"
    return "🧊 Low", "green"


def compute_inflation_price(base_price: float, zone: str, years: int = 10):
    rate, result, p = ZONE_INFLATION_RATE.get(zone, 0.05), [], base_price
    for yr in range(1, years + 1):
        p *= 1 + rate
        result.append({"Year": f"Yr {yr}", "Projected Price": round(p)})
    return result, rate


def investment_recommendation(demand_score, roi, inflation_rate):
    score, reasons = 0, []
    if demand_score >= 0.75:
        score += 40; reasons.append("Strong market demand")
    elif demand_score >= 0.55:
        score += 25; reasons.append("Moderate demand")
    else:
        score += 10; reasons.append("Weak demand")
    if roi >= 120:
        score += 40; reasons.append("High ROI potential")
    elif roi >= 60:
        score += 25; reasons.append("Decent ROI growth")
    else:
        score += 10; reasons.append("Limited ROI upside")
    if inflation_rate >= 0.07:
        score += 20; reasons.append("High appreciation zone")
    elif inflation_rate >= 0.05:
        score += 12; reasons.append("Stable appreciation")
    else:
        score += 6;  reasons.append("Slow appreciation")
    decision = "BUY" if score >= 80 else "HOLD" if score >= 55 else "AVOID"
    return decision, score, ", ".join(reasons)


def ai_insight(area, bedrooms, bathrooms, location_rating,
               age, garage, pool, zone, demand_score, base_price, final_price) -> str:
    parts = []
    if final_price > base_price:
        parts.append("Market demand is lifting the price above the model's base valuation.")
    if location_rating >= 8:
        parts.append("The premium location rating is a key value driver.")
    elif location_rating <= 4:
        parts.append("The lower location score is constraining price growth.")
    if area > 3000:
        parts.append("Large floor area contributes strongly to higher valuation.")
    elif area < 1000:
        parts.append("Compact size limits the overall valuation ceiling.")
    if age <= 5:
        parts.append("Recent construction boosts desirability and price.")
    elif age > 20:
        parts.append("Property age is applying a negative discount to value.")
    if pool:
        parts.append("Swimming pool adds luxury appeal and resale value.")
    if garage >= 2:
        parts.append("Multiple garage bays add functional and resale value.")
    zone_desc = {
        "luxury"  : "Luxury zones carry the highest appreciation and buyer competition.",
        "urban"   : "Urban zones benefit from infrastructure density and sustained demand.",
        "suburban": "Suburban zones offer balanced growth with good affordability.",
        "rural"   : "Rural zones typically see slower appreciation and softer demand.",
    }
    parts.append(zone_desc.get(zone, ""))
    if demand_score >= 0.75:
        parts.append("Current market conditions are highly competitive for this property type.")
    elif demand_score < 0.35:
        parts.append("Below-average demand may limit short-term price gains.")
    return " ".join(filter(None, parts))


# [B2] Zone comparison uses build_features → identical 10 columns as main prediction
@st.cache_data
def get_zone_comparison(_area, _bedrooms, _bathrooms, _location_rating,
                        _age, _garage, _pool):
    zones      = ["rural", "suburban", "urban", "luxury"]
    prices, demands, inflats = [], [], []
    for z in zones:
        z_enc = safe_encode(z)
        f_df  = build_features(_area, _bedrooms, _bathrooms, _location_rating,
                               _age, _garage, _pool, z_enc)
        bp    = safe_predict(f_df)
        ds    = compute_demand(z, _location_rating, _area)
        prices.append(round(bp * demand_to_multiplier(ds)))
        demands.append(round(ds * 100, 1))
        inflats.append(ZONE_INFLATION_RATE.get(z, 0.05) * 100)
    return zones, prices, demands, inflats


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — Premium Control Panel
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # Brand strip
    st.markdown("""
    <div class="sb-brand">
        <span class="sb-brand-icon">🏛️</span>
        <div class="sb-brand-name">PropVision AI</div>
        <div class="sb-brand-sub">Real Estate Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    # ── STEP 1: CURRENCY ─────────────────────────────────────────
    st.markdown("""
    <div class="step-badge">
        <div class="step-num">1</div>
        <div class="step-label">Currency</div>
    </div>""", unsafe_allow_html=True)

    with st.container():
        currency   = st.selectbox("Display in", ["INR (₹)", "USD ($)"],
                                  index=0, label_visibility="collapsed")
        show_inr   = currency == "INR (₹)"

    # ── STEP 2: PROPERTY SPECS ───────────────────────────────────
    st.markdown("""
    <div class="step-badge">
        <div class="step-num">2</div>
        <div class="step-label">Property Specs</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="glass-card-title">📐 Size</div>', unsafe_allow_html=True)
    area = st.slider("Area (sq ft)", 500, 5000, 1800, step=50)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="glass-card-title">🛏️ Rooms</div>', unsafe_allow_html=True)
    bedrooms  = st.slider("Bedrooms",  1, 8, 3)
    bathrooms = st.slider("Bathrooms", 1, 6, 2)
    garage    = st.slider("Garage Spaces", 0, 3, 1)
    pool      = st.checkbox("🏊 Swimming Pool", value=False)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── STEP 3: LOCATION ─────────────────────────────────────────
    st.markdown("""
    <div class="step-badge">
        <div class="step-num">3</div>
        <div class="step-label">Location</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    default_idx = (zone_classes.index(APP_CONFIG["default_zone"])
                   if APP_CONFIG["default_zone"] in zone_classes else 0)
    zone = st.selectbox(
        "Zone Type", options=zone_classes, index=default_idx,
        format_func=lambda z: {
            "luxury":"🏰 Luxury", "urban":"🏙️ Urban",
            "suburban":"🏘️ Suburban", "rural":"🌾 Rural"
        }.get(z, z.capitalize()),
        label_visibility="collapsed"
    )
    location_rating = st.slider("Location Quality", 1, 10, 7,
                                format="%d / 10")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── STEP 4: CONDITION ────────────────────────────────────────
    st.markdown("""
    <div class="step-badge">
        <div class="step-num">4</div>
        <div class="step-label">Condition</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    age = st.slider("Property Age (years)", 0, 35, 5)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── STEP 5: MARKET ───────────────────────────────────────────
    st.markdown("""
    <div class="step-badge">
        <div class="step-num">5</div>
        <div class="step-label">Market Controls</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    market_sensitivity = st.slider(
        "Market Sensitivity", 0.5, 1.5, 1.0, step=0.05,
        help="How strongly market demand inflates the final price (1.0 = neutral)"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── RUN BUTTON ───────────────────────────────────────────────
    predict_btn = st.button("⚡  Run AI Valuation", use_container_width=True)

    # ── MODEL INFO ───────────────────────────────────────────────
    mae_display = f"${bundle.get('mae_usd', 0):,.0f}" if bundle.get('mae_usd') else "N/A"
    st.markdown(f"""
    <div class="model-pill">
        <div style="font-size:0.65rem;font-weight:600;letter-spacing:1.5px;
                    text-transform:uppercase;color:#1e3a5f;margin-bottom:0.5rem;">
            Model Info
        </div>
        <div class="pill-row">
            <span>Algorithm</span>
            <span class="pill-val blue">{bundle.get("model_name","XGBoost")}</span>
        </div>
        <div class="pill-row">
            <span>R² Accuracy</span>
            <span class="pill-val green">{model_r2:.1%}</span>
        </div>
        <div class="pill-row">
            <span>Avg Error</span>
            <span class="pill-val">{mae_display}</span>
        </div>
        <div class="pill-row">
            <span>Training rows</span>
            <span class="pill-val">{bundle.get("training_rows","N/A")}</span>
        </div>
        <div class="pill-row">
            <span>Currency</span>
            <span class="pill-val gold">{"₹ INR" if show_inr else "$ USD"}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HERO BANNER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-banner">
    <div class="hero-eyebrow">🏛️ &nbsp; AI-Powered Real Estate Intelligence</div>
    <div class="hero-title">PropVision AI</div>
    <p class="hero-sub">
        Machine-learning valuation engine with dynamic demand scoring,
        zone-based market heat, and inflation-adjusted price projections
        — built for data-driven property decisions.
    </p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  LIVE MARKET SNAPSHOT  (always visible, no prediction needed)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">Live Market Snapshot</div>', unsafe_allow_html=True)

demand_score     = compute_demand(zone, location_rating, area)
d_label, d_color = demand_label(demand_score)
infl_rate        = ZONE_INFLATION_RATE.get(zone, 0.05)
live_mul         = demand_to_multiplier(demand_score, market_sensitivity)
proj_5yr_pct     = round((1 + infl_rate)**5 * 100 - 100, 1)
bar_color_map    = {"red":"#ef4444","gold":"#f59e0b","blue":"#3b82f6","green":"#10b981"}
bar_color        = bar_color_map[d_color]

m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.markdown(f"""
    <div class="metric-card blue">
        <div class="metric-label">Zone</div>
        <div class="metric-value" style="font-size:1.5rem">{zone.capitalize()}</div>
        <div class="metric-delta">Selected area type</div>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""
    <div class="metric-card {d_color}">
        <div class="metric-label">Market Demand</div>
        <div class="metric-value" style="font-size:1.7rem">{int(demand_score*100)}%</div>
        <div class="demand-bar-wrap">
            <div class="demand-bar-fill" style="width:{int(demand_score*100)}%;background:{bar_color};"></div>
        </div>
        <div class="metric-delta">{d_label}</div>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""
    <div class="metric-card gold">
        <div class="metric-label">Price Multiplier</div>
        <div class="metric-value highlight">×{live_mul:.2f}</div>
        <div class="metric-delta up">Sensitivity {market_sensitivity:.2f}×</div>
    </div>""", unsafe_allow_html=True)
with m4:
    st.markdown(f"""
    <div class="metric-card green">
        <div class="metric-label">Annual Appreciation</div>
        <div class="metric-value" style="font-size:1.7rem">{infl_rate*100:.1f}%</div>
        <div class="metric-delta up">Zone inflation rate</div>
    </div>""", unsafe_allow_html=True)
with m5:
    st.markdown(f"""
    <div class="metric-card purple">
        <div class="metric-label">5-Yr Growth Est.</div>
        <div class="metric-value" style="font-size:1.7rem">+{proj_5yr_pct}%</div>
        <div class="metric-delta up">Compounded inflation</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PREDICTION RESULTS
# ══════════════════════════════════════════════════════════════════════════════
if predict_btn:

    # [B6] Currency symbol derived once — flows into every chart
    csym = "₹" if show_inr else "$"

    # ── BUILD FEATURES & PREDICT ── [B1][B2][B3]
    zone_enc     = safe_encode(zone)
    features_df  = build_features(area, bedrooms, bathrooms, location_rating,
                                  age, garage, pool, zone_enc)
    base_price   = safe_predict(features_df)

    demand_score = compute_demand(zone, location_rating, area)
    multiplier   = demand_to_multiplier(demand_score, market_sensitivity)
    demand_price = base_price * multiplier
    yearly_proj, infl_rate = compute_inflation_price(demand_price, zone, 10)
    d_label, d_color = demand_label(demand_score)

    price_5yr  = yearly_proj[4]["Projected Price"]
    price_10yr = yearly_proj[9]["Projected Price"]
    roi        = round(safe_pct(price_10yr - demand_price, demand_price), 1)

    decision, confidence, reasoning = investment_recommendation(demand_score, roi, infl_rate)
    explanation = ai_insight(area, bedrooms, bathrooms, location_rating,
                             age, garage, pool, zone,
                             demand_score, base_price, demand_price)

    color_map = {"BUY":"#10b981","HOLD":"#f59e0b","AVOID":"#ef4444"}
    bg_map    = {"BUY":"rgba(16,185,129,0.07)",
                 "HOLD":"rgba(245,158,11,0.07)",
                 "AVOID":"rgba(239,68,68,0.07)"}

    # ── RESULT METRIC CARDS ──────────────────────────────────────
    st.markdown('<div class="section-label">Valuation Results</div>', unsafe_allow_html=True)

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown(f"""
        <div class="metric-card blue animate-in">
            <div class="metric-label">AI Base Price</div>
            <div class="metric-value">{fmt(base_price, show_inr)}</div>
            <div class="metric-delta">Pre-market model output</div>
        </div>""", unsafe_allow_html=True)
    with r2:
        diff      = demand_price - base_price
        diff_sign = "+" if diff >= 0 else "−"
        st.markdown(f"""
        <div class="metric-card gold animate-in delay-1">
            <div class="metric-label">Demand-Adjusted Price</div>
            <div class="metric-value highlight">{fmt(demand_price, show_inr)}</div>
            <div class="metric-delta up">{diff_sign}{fmt(abs(diff), show_inr)} from demand</div>
        </div>""", unsafe_allow_html=True)
    with r3:
        st.markdown(f"""
        <div class="metric-card green animate-in delay-2">
            <div class="metric-label">5-Year Projection</div>
            <div class="metric-value">{fmt(price_5yr, show_inr)}</div>
            <div class="metric-delta up">At {infl_rate*100:.1f}% p.a.</div>
        </div>""", unsafe_allow_html=True)
    with r4:
        st.markdown(f"""
        <div class="metric-card purple animate-in delay-3">
            <div class="metric-label">10-Year ROI</div>
            <div class="metric-value green-val">+{roi}%</div>
            <div class="metric-delta up">{fmt(price_10yr, show_inr)} projected</div>
        </div>""", unsafe_allow_html=True)

    # ── RECOMMENDATION ───────────────────────────────────────────
    dec_color = color_map[decision]
    dec_bg    = bg_map[decision]
    conf_pct  = confidence

    st.markdown(f"""
    <div class="rec-card animate-in delay-4"
         style="background:{dec_bg};border-color:rgba({
             '16,185,129' if decision=='BUY' else
             '245,158,11' if decision=='HOLD' else
             '239,68,68'
         },0.3);">
        <div>
            <div style="font-size:0.68rem;font-weight:600;letter-spacing:2px;
                        text-transform:uppercase;color:#475569;margin-bottom:0.4rem;">
                Investment Recommendation
            </div>
            <div class="rec-decision" style="color:{dec_color}">{decision}</div>
            <div style="font-size:0.8rem;color:#64748b;margin-top:0.3rem;">{reasoning}</div>
        </div>
        <div class="rec-meta">
            <div class="rec-conf">Confidence Score</div>
            <div style="font-family:'Playfair Display',serif;font-size:2rem;
                        color:{dec_color};line-height:1;">{conf_pct}<span style="font-size:1rem">/100</span></div>
            <div class="conf-bar-wrap" style="margin-left:auto;">
                <div class="conf-bar-fill"
                     style="width:{conf_pct}%;background:{dec_color};"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── INSIGHT BOXES ────────────────────────────────────────────
    insight_cls = "success" if demand_score >= 0.55 else ("warn" if demand_score >= 0.35 else "")
    st.markdown(f"""
    <div class="insight-box {insight_cls}">
        <strong>🧠 AI Market Insight:</strong>&nbsp;
        This <strong>{zone}</strong> zone property carries
        <strong>{d_label}</strong> demand ({int(demand_score*100)}%).
        The model valued it at <strong>{fmt(base_price, show_inr)}</strong>;
        after a demand multiplier of <strong>×{multiplier:.2f}</strong>
        (sensitivity {market_sensitivity:.2f}×), the market price is
        <strong>{fmt(demand_price, show_inr)}</strong>.
        At {infl_rate*100:.1f}% annual appreciation, the 10-year target is
        <strong>{fmt(price_10yr, show_inr)}</strong> — a
        <strong>+{roi}% ROI</strong>.
    </div>
    <div class="insight-box">
        <strong>🤖 AI Property Analysis:</strong>&nbsp;{explanation}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    #  ANALYTICS TABS
    # ══════════════════════════════════════════════════════════════
    tab_a, tab_b, tab_c, tab_d = st.tabs([
        "📈  Price Trajectory",
        "🔥  Demand Analysis",
        "🏘️  Zone Comparison",
        "🔬  Feature Importance",
    ])

    PLOT_BG  = "#0e1623"
    GRID_COL = "#1a2535"

    # ── TAB A: 10-YEAR TRAJECTORY ─────────────────────────────────
    with tab_a:
        years      = ["Now"] + [y["Year"] for y in yearly_proj]
        prices     = [demand_price] + [y["Projected Price"] for y in yearly_proj]
        benchmark  = [demand_price * (1.03**i) for i in range(11)]

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=years, y=prices, fill="tozeroy",
            fillcolor="rgba(59,130,246,0.06)",
            line=dict(width=0, color="rgba(0,0,0,0)"),
            showlegend=False, hoverinfo="skip"
        ))
        fig1.add_trace(go.Scatter(
            x=years, y=benchmark, mode="lines", name="3% Benchmark",
            line=dict(color="rgba(100,116,139,0.4)", width=1.5, dash="dot")
        ))
        fig1.add_trace(go.Scatter(
            x=years, y=prices, mode="lines+markers",
            name=f"{zone.capitalize()} ({infl_rate*100:.1f}% p.a.)",
            line=dict(color="#3b82f6", width=2.5),
            marker=dict(color="#fbbf24", size=7,
                        line=dict(color=PLOT_BG, width=2)),
            # [B6] dynamic currency symbol
            hovertemplate=f"<b>%{{x}}</b><br>{csym}%{{y:,.0f}}<extra></extra>"
        ))
        for idx, lbl in [(5,"5-Year"),(10,"10-Year")]:
            fig1.add_annotation(
                x=years[idx], y=prices[idx],
                text=f"<b>{lbl}<br>{fmt(prices[idx],show_inr)}</b>",
                showarrow=True, arrowhead=2,
                arrowcolor="#fbbf24", arrowwidth=1.5,
                ax=45, ay=-45,
                font=dict(color="#fbbf24", size=10),
                bgcolor="rgba(8,11,18,0.85)",
                bordercolor="#fbbf24", borderwidth=1, borderpad=5
            )
        fig1.update_layout(
            paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
            font=dict(family="DM Sans", color="#64748b"),
            xaxis=dict(gridcolor=GRID_COL, tickfont=dict(color="#475569")),
            # [B6] tickprefix instead of hardcoded '$'
            yaxis=dict(gridcolor=GRID_COL,
                       tickprefix=csym, tickformat=",.0f",
                       tickfont=dict(color="#475569")),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#64748b", size=11)),
            margin=dict(l=10, r=15, t=25, b=10), height=370,
            hovermode="x unified",
            hoverlabel=dict(bgcolor="#1a2535", font_color="#e2e8f0",
                            bordercolor="#3b82f6")
        )
        st.plotly_chart(fig1, use_container_width=True)

    # ── TAB B: DEMAND ANALYSIS ────────────────────────────────────
    with tab_b:
        base_d  = ZONE_DEMAND_BASE.get(zone, 0.5)
        loc_d   = (location_rating - 1) / 9
        area_d  = min(area / 5000, 1.0)
        contribs = {
            "Zone Base Demand": round(0.55 * base_d, 3),
            "Location Quality": round(0.30 * loc_d,  3),
            "Area Size Factor": round(0.15 * area_d,  3),
        }

        col_ba, col_bb = st.columns(2)
        with col_ba:
            # [B5] safe_pct guards against zero demand_score
            texts = [f"{v:.3f}  ({safe_pct(v,demand_score):.0f}%)"
                     for v in contribs.values()]
            fig2 = go.Figure(go.Bar(
                x=list(contribs.values()), y=list(contribs.keys()),
                orientation="h",
                marker=dict(color=["#3b82f6","#f59e0b","#10b981"],
                            line=dict(color=PLOT_BG, width=1)),
                text=texts, textposition="outside",
                textfont=dict(color="#64748b", size=11),
                hovertemplate="<b>%{y}</b><br>Score: %{x:.3f}<extra></extra>"
            ))
            fig2.update_layout(
                paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
                font=dict(family="DM Sans", color="#64748b"),
                xaxis=dict(gridcolor=GRID_COL, range=[0, 0.75]),
                yaxis=dict(gridcolor="rgba(0,0,0,0)"),
                margin=dict(l=5, r=80, t=15, b=5), height=320, showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col_bb:
            # [B10] Gauge steps aligned with demand_label thresholds
            gc = ("#ef4444" if demand_score >= 0.75 else
                  "#f59e0b" if demand_score >= 0.55 else
                  "#3b82f6" if demand_score >= 0.35 else "#10b981")
            fig3 = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=round(demand_score * 100, 1),
                title=dict(text="Demand Score", font=dict(color="#64748b", size=13)),
                number=dict(suffix="%", font=dict(color="#f1f5f9", size=34,
                                                   family="Playfair Display")),
                delta=dict(reference=50, valueformat=".1f", suffix="%",
                           increasing=dict(color="#34d399"),
                           decreasing=dict(color="#f87171")),
                gauge=dict(
                    axis=dict(range=[0,100], tickcolor=GRID_COL,
                              tickfont=dict(color="#475569")),
                    bar=dict(color=gc, thickness=0.22),
                    bgcolor=PLOT_BG, bordercolor=GRID_COL,
                    steps=[
                        dict(range=[0, 35],  color="rgba(16,185,129,0.08)"),
                        dict(range=[35, 55], color="rgba(59,130,246,0.08)"),
                        dict(range=[55, 75], color="rgba(245,158,11,0.08)"),
                        dict(range=[75,100], color="rgba(239,68,68,0.08)"),
                    ],
                    threshold=dict(line=dict(color="#fbbf24", width=2.5),
                                   thickness=0.65, value=demand_score*100)
                )
            ))
            fig3.update_layout(
                paper_bgcolor=PLOT_BG, font=dict(family="DM Sans"),
                margin=dict(l=15, r=15, t=25, b=5), height=320
            )
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown(f"""
        <div class="insight-box">
            <strong>💡 Demand Composition:</strong> Zone base =
            <strong>{safe_pct(contribs["Zone Base Demand"],demand_score):.0f}%</strong>,
            location quality =
            <strong>{safe_pct(contribs["Location Quality"],demand_score):.0f}%</strong>,
            area size =
            <strong>{safe_pct(contribs["Area Size Factor"],demand_score):.0f}%</strong>.
            Total demand score: <strong>{int(demand_score*100)}%</strong> →
            price premium of <strong>{fmt(demand_price-base_price,show_inr)}</strong>.
        </div>""", unsafe_allow_html=True)

    # ── TAB C: ZONE COMPARISON ────────────────────────────────────
    with tab_c:
        # [B2] uses build_features — all 10 columns built correctly
        zones_list, z_prices, z_demands, z_inflats = get_zone_comparison(
            area, bedrooms, bathrooms, location_rating, age, garage, pool
        )
        z_labels = ["Rural","Suburban","Urban","Luxury"]
        z_colors = ["#94a3b8","#34d399","#3b82f6","#fbbf24"]

        fig4 = make_subplots(
            rows=1, cols=2,
            subplot_titles=["Demand-Adjusted Price by Zone",
                            "Demand & Inflation by Zone"],
            specs=[[{"type":"bar"},{"type":"bar"}]]
        )
        fig4.add_trace(go.Bar(
            x=z_labels, y=z_prices,
            marker=dict(color=z_colors, line=dict(color=PLOT_BG, width=1)),
            text=[fmt(p,show_inr) for p in z_prices],
            textposition="outside", textfont=dict(color="#64748b", size=10),
            name="Price",
            hovertemplate="<b>%{x}</b><br>%{text}<extra></extra>"
        ), row=1, col=1)

        fig4.add_trace(go.Bar(
            x=z_labels, y=z_inflats,
            marker=dict(color=[f"rgba(251,191,36,{0.35+i*0.15})" for i in range(4)]),
            name="Inflation %",
            text=[f"{r:.1f}%" for r in z_inflats],
            textposition="outside", textfont=dict(color="#fbbf24", size=10)
        ), row=1, col=2)

        fig4.add_trace(go.Scatter(
            x=z_labels, y=z_demands, mode="lines+markers",
            name="Demand %",
            line=dict(color="#3b82f6", width=2),
            marker=dict(color="#60a5fa", size=8)
        ), row=1, col=2)

        sel_idx = zones_list.index(zone) if zone in zones_list else 0
        if z_prices:
            fig4.add_shape(
                type="rect", row=1, col=1,
                x0=sel_idx-0.42, x1=sel_idx+0.42,
                y0=0, y1=max(z_prices)*1.14,
                line=dict(color="#fbbf24", width=1.5, dash="dot"),
                fillcolor="rgba(251,191,36,0.03)"
            )
        fig4.update_layout(
            paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
            font=dict(family="DM Sans", color="#64748b"),
            xaxis=dict(gridcolor=GRID_COL),
            xaxis2=dict(gridcolor=GRID_COL),
            # [B6] currency prefix on zone price axis
            yaxis=dict(gridcolor=GRID_COL, tickprefix=csym, tickformat=",.0f"),
            yaxis2=dict(gridcolor=GRID_COL),
            margin=dict(l=10, r=10, t=45, b=10), height=370, showlegend=False,
        )
        st.plotly_chart(fig4, use_container_width=True)

    # ── TAB D: FEATURE IMPORTANCE ─────────────────────────────────
    with tab_d:
        # [B9] Exhaustive name map — covers all training column variants
        feat_name_map = {
            "area_scaled"     : "Property Area",
            "area"            : "Property Area",
            "bedrooms"        : "Bedrooms",
            "bathrooms"       : "Bathrooms",
            "location_rating" : "Location Rating",
            "age"             : "Property Age",
            "garage"          : "Garage Spaces",
            "pool"            : "Swimming Pool",
            "zone_encoded"    : "Zone Type",
            "zone_enc"        : "Zone Type",
            "zone"            : "Zone Type",
            "bed_bath_ratio"  : "Bed/Bath Ratio",
            "luxury_score"    : "Luxury Score",
        }
        sorted_fi = sorted(feat_imp.items(), key=lambda x: -x[1])
        fi_names  = [feat_name_map.get(k, k.replace("_"," ").title())
                     for k, _ in sorted_fi]
        fi_vals   = [v * 100 for _, v in sorted_fi]

        if fi_vals:
            fig5 = go.Figure(go.Bar(
                x=fi_vals, y=fi_names, orientation="h",
                marker=dict(
                    color=fi_vals,
                    colorscale=[[0,"#1a2d45"],[0.5,"#1d4ed8"],[1,"#60a5fa"]],
                    line=dict(color=PLOT_BG, width=0.5)
                ),
                text=[f"{v:.1f}%" for v in fi_vals],
                textposition="outside",
                textfont=dict(color="#64748b", size=11),
                hovertemplate="<b>%{y}</b><br>Importance: %{x:.1f}%<extra></extra>"
            ))
            fig5.update_layout(
                paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
                font=dict(family="DM Sans", color="#64748b"),
                xaxis=dict(gridcolor=GRID_COL, ticksuffix="%",
                           range=[0, max(fi_vals)*1.28]),
                yaxis=dict(gridcolor="rgba(0,0,0,0)", autorange="reversed"),
                margin=dict(l=10, r=80, t=15, b=10), height=340, showlegend=False
            )
            st.plotly_chart(fig5, use_container_width=True)

            fi1, fi2 = st.columns(2)
            with fi1:
                st.markdown(f"""
                <div class="insight-box success">
                    <strong>🏆 Top Driver:</strong> <strong>{fi_names[0]}</strong>
                    accounts for <strong>{fi_vals[0]:.1f}%</strong> of the model's
                    pricing decisions.
                </div>""", unsafe_allow_html=True)
            with fi2:
                st.markdown(f"""
                <div class="insight-box">
                    <strong>ℹ️ Least Influential:</strong>
                    <strong>{fi_names[-1]}</strong> has the smallest direct impact
                    at <strong>{fi_vals[-1]:.1f}%</strong>.
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Feature importance data not available.")

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    # ── PROPERTY SUMMARY TABLE ────────────────────────────────────
    st.markdown('<div class="section-label">Full Property Summary</div>',
                unsafe_allow_html=True)
    summary = pd.DataFrame({
        "Attribute": [
            "Area (sq ft)","Bedrooms","Bathrooms","Garage","Pool",
            "Location Rating","Zone","Property Age",
            "─── Valuation ───",
            "AI Base Price","Demand Score","Multiplier",
            "Market Sensitivity","Final Market Price",
            "5-Year Projection","10-Year Projection","10-Year ROI",
            "─── Decision ───",
            "Recommendation","Confidence"
        ],
        "Value": [
            f"{area} sq ft", str(bedrooms), str(bathrooms), str(garage),
            "Yes ✓" if pool else "No",
            f"{location_rating} / 10",
            zone.capitalize(), f"{age} yrs",
            "",
            fmt(base_price, show_inr),
            f"{int(demand_score*100)}%  —  {d_label}",
            f"×{multiplier:.2f}",
            f"{market_sensitivity:.2f}×",
            fmt(demand_price, show_inr),
            fmt(price_5yr, show_inr),
            fmt(price_10yr, show_inr),
            f"+{roi}%",
            "",
            decision,
            f"{confidence} / 100"
        ]
    })
    st.dataframe(
        summary.style.apply(
            lambda x: ["background-color:rgba(59,130,246,0.08)" if i >= 9 else
                       "background-color:rgba(30,45,64,0.3)" if x.iloc[i] == "" else ""
                       for i in range(len(x))], axis=0
        ).set_properties(**{"color":"#e2e8f0","border-color":"#1a2535"}),
        use_container_width=True, hide_index=True, height=680
    )

else:
    # ── PLACEHOLDER ───────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem;">
        <div style="font-size:4rem;margin-bottom:1.2rem;opacity:0.3">🏛️</div>
        <div style="font-family:'Playfair Display',serif;font-size:1.8rem;
                    color:#1e3a5f;margin-bottom:0.6rem;">
            Ready to analyse your property
        </div>
        <div style="font-size:0.95rem;color:#1e2d40;max-width:380px;margin:0 auto;">
            Configure the property details in the left panel, then click
            <strong style="color:#1d4ed8">Run AI Valuation</strong>
            to get your complete analysis.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center;color:#1e2d40;font-size:0.75rem;padding-bottom:1rem;">
    <span style="color:#1e3a5f">◆</span>&nbsp;
    PropVision AI — House Price Intelligence Platform &nbsp;|&nbsp;
    XGBoost ML Engine &nbsp;|&nbsp;
    {APP_CONFIG["model_version"]}
    &nbsp;<span style="color:#1e3a5f">◆</span>
</div>
""", unsafe_allow_html=True)
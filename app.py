import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
import os



# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG — must be first Streamlit call
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="PropVision AI — House Price Intelligence",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS — Luxury Dark Theme
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0d14;
    color: #e8e6e0;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2.5rem 3rem 2.5rem; max-width: 1400px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1120 0%, #111827 100%);
    border-right: 1px solid #1e2a3a;
}
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1.2rem; }

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #0d1b2a 0%, #1a2744 40%, #0f2342 70%, #0a0d14 100%);
    border: 1px solid #1e3a5f;
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(251,191,36,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    background: linear-gradient(90deg, #ffffff 0%, #93c5fd 50%, #fbbf24 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.5rem 0;
    line-height: 1.1;
}
.hero-sub {
    font-size: 1.05rem;
    color: #94a3b8;
    font-weight: 300;
    letter-spacing: 0.3px;
    margin: 0;
}
.hero-badge {
    display: inline-block;
    background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.4);
    color: #93c5fd;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 1rem;
}

/* ── Section Headers ── */
.section-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #3b82f6;
    margin-bottom: 0.8rem;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.45rem;
    font-weight: 600;
    color: #f1f5f9;
    margin: 0 0 1.5rem 0;
}

/* ── Metric Cards ── */
.metric-card {
    background: linear-gradient(145deg, #111827, #1a2233);
    border: 1px solid #1e2d40;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease;
}
.metric-card:hover { border-color: #3b82f6; }
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
}
.metric-card.blue::before  { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
.metric-card.gold::before  { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.metric-card.green::before { background: linear-gradient(90deg, #10b981, #34d399); }
.metric-card.red::before   { background: linear-gradient(90deg, #ef4444, #f87171); }
.metric-card.purple::before{ background: linear-gradient(90deg, #8b5cf6, #a78bfa); }

.metric-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #f8fafc;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.metric-value.highlight { color: #fbbf24; }
.metric-delta {
    font-size: 0.78rem;
    color: #94a3b8;
}
.metric-delta.up   { color: #34d399; }
.metric-delta.down { color: #f87171; }

/* ── Input Card ── */
.input-card {
    background: #111827;
    border: 1px solid #1e2d40;
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
}
.input-card-title {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #3b82f6;
    margin-bottom: 1.2rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid #1e2d40;
}

/* ── Predict Button ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #3b82f6 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(59, 130, 246, 0.35) !important;
}
div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%) !important;
    box-shadow: 0 6px 28px rgba(59, 130, 246, 0.55) !important;
    transform: translateY(-1px) !important;
}

/* ── Sliders ── */
[data-testid="stSlider"] > div > div > div > div {
    background: #3b82f6 !important;
}

/* ── Demand Bar ── */
.demand-bar-wrap {
    background: #1a2233;
    border-radius: 10px;
    height: 12px;
    overflow: hidden;
    margin: 0.4rem 0;
}
.demand-bar-fill {
    height: 100%;
    border-radius: 10px;
    transition: width 0.8s ease;
}

/* ── Insight Box ── */
.insight-box {
    background: linear-gradient(135deg, rgba(59,130,246,0.08), rgba(251,191,36,0.05));
    border: 1px solid rgba(59,130,246,0.2);
    border-left: 4px solid #3b82f6;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    font-size: 0.88rem;
    color: #cbd5e1;
    line-height: 1.6;
}
.insight-box.warn {
    border-left-color: #f59e0b;
    background: linear-gradient(135deg, rgba(245,158,11,0.08), rgba(251,191,36,0.03));
}
.insight-box.success {
    border-left-color: #10b981;
    background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(52,211,153,0.03));
}

/* ── Zone Badge ── */
.zone-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.zone-luxury   { background: rgba(251,191,36,0.15);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.zone-urban    { background: rgba(59,130,246,0.15);  color: #93c5fd; border: 1px solid rgba(59,130,246,0.3); }
.zone-suburban { background: rgba(16,185,129,0.15);  color: #6ee7b7; border: 1px solid rgba(16,185,129,0.3); }
.zone-rural    { background: rgba(148,163,184,0.12); color: #94a3b8; border: 1px solid rgba(148,163,184,0.2); }

/* ── Divider ── */
.fancy-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e3a5f, transparent);
    margin: 2rem 0;
}

/* ── Stagger animation ── */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
.animate-in { animation: fadeSlideUp 0.5s ease forwards; }

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: #111827 !important;
    border: 1px solid #1e2d40 !important;
    color: #e8e6e0 !important;
    border-radius: 8px !important;
}

/* ── Charts background ── */
.js-plotly-plot .plotly { border-radius: 12px !important; }

/* ── Tab styling ── */
[data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 4px;
}
[data-baseweb="tab"] {
    background: #111827 !important;
    border: 1px solid #1e2d40 !important;
    border-radius: 8px !important;
    color: #64748b !important;
    font-weight: 500 !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: rgba(59,130,246,0.15) !important;
    border-color: rgba(59,130,246,0.4) !important;
    color: #93c5fd !important;
}

</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  LOAD MODEL
# ══════════════════════════════════════════════════════════════════════════════


@st.cache_resource
def load_model():
    if not os.path.exists("model.pkl"):
        from train_model import train_model
        return train_model()
    else:
        with open("model.pkl", "rb") as f:
            return pickle.load(f)
bundle = load_model()

model = bundle['model']
encoder = bundle['encoder']
feat_cols = bundle['feature_cols']
feat_imp = bundle['feature_importance']
zone_classes = bundle['zone_classes']
model_r2 = bundle['r2_score']
# ══════════════════════════════════════════════════════════════════════════════
#  DEMAND ENGINE
# ══════════════════════════════════════════════════════════════════════════════
# Demand multipliers per zone (simulates market heat per area type)
ZONE_DEMAND_BASE = {
    'luxury'  : 0.88,
    'urban'   : 0.75,
    'suburban': 0.58,
    'rural'   : 0.35,
}

# Annual inflation rates per zone (simulates area-specific appreciation)
ZONE_INFLATION_RATE = {
    'luxury'  : 0.085,  # 8.5% per year
    'urban'   : 0.072,
    'suburban': 0.055,
    'rural'   : 0.032,
}

def compute_demand(zone, location_rating, area):
    """Dynamic demand score: blends zone base, location quality, and area size."""
    base     = ZONE_DEMAND_BASE.get(zone, 0.5)
    loc_mod  = (location_rating - 1) / 9      # normalise 1-10 → 0-1
    area_mod = min(area / 5000, 1.0)           # larger area → more interest
    demand   = 0.55 * base + 0.30 * loc_mod + 0.15 * area_mod
    return round(min(demand, 1.0), 4)

def compute_inflation_price(base_price, zone, years_to_project=5):
    """Project price appreciation year-by-year using zone-specific inflation."""
    rate = ZONE_INFLATION_RATE.get(zone, 0.05)
    yearly = []
    p = base_price
    for yr in range(1, years_to_project + 1):
        p = p * (1 + rate)
        yearly.append({'Year': f'Year {yr}', 'Projected Price': round(p), 'Rate': rate})
    return yearly, rate

def demand_to_multiplier(demand_score):
    """Convert demand score to a price inflation multiplier (1.0 – 1.35)."""
    return round(1.0 + demand_score * 0.35, 4)

def demand_label(score):
    if score >= 0.80: return "🔥 Extremely High", "red"
    if score >= 0.65: return "📈 High",           "gold"
    if score >= 0.45: return "⚖️ Moderate",        "blue"
    return "🧊 Low", "green"

def fmt(usd_val, show_inr, usd_to_inr=83.5):
    """Format a USD value into the selected currency with Indian number formatting."""
    if show_inr:
        inr = usd_val * usd_to_inr
        if inr >= 1e7:
            return f"₹{inr/1e7:.2f} Cr"
        elif inr >= 1e5:
            return f"₹{inr/1e5:.2f} L"
        else:
            return f"₹{inr:,.0f}"
    else:
        return f"${usd_val:,.0f}"

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — PREMIUM TABBED CONTROL PANEL (UI UPGRADE ONLY)
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    st.markdown('<div class="section-label">Control Panel</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Configure Property</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏠 Property", "📊 Market", "⚙️ Settings"])

    # ─────────────────────────────
    # 🏠 PROPERTY TAB
    # ─────────────────────────────
    with tab1:

        # Currency (kept same logic)
        st.markdown('<div class="input-card"><div class="input-card-title">💱 Currency</div>', unsafe_allow_html=True)
        currency = st.selectbox("Display Currency", options=["INR (₹)", "USD ($)"], index=0)
        usd_to_inr = 83.5
        show_inr = currency == "INR (₹)"
        st.markdown('</div>', unsafe_allow_html=True)

        # Size & Layout
        st.markdown('<div class="input-card"><div class="input-card-title">📐 Size & Layout</div>', unsafe_allow_html=True)

        col_s, col_n = st.columns([2, 1])
        with col_s:
            area = st.slider("Area (sq ft)", 500, 10000, 1800, step=50)
        with col_n:
            area = st.number_input("sq ft", min_value=500, max_value=10000, value=area, step=50)

        col_s2, col_n2 = st.columns([2, 1])
        with col_s2:
            bedrooms = st.slider("Bedrooms", 1, 10, 3)
        with col_n2:
            bedrooms = st.number_input("beds", min_value=1, max_value=10, value=bedrooms, step=1)

        col_s3, col_n3 = st.columns([2, 1])
        with col_s3:
            bathrooms = st.slider("Bathrooms", 1, 8, 2)
        with col_n3:
            bathrooms = st.number_input("baths", min_value=1, max_value=8, value=bathrooms, step=1)

        col_s4, col_n4 = st.columns([2, 1])
        with col_s4:
            garage = st.slider("Garage Spaces", 0, 5, 1)
        with col_n4:
            garage = st.number_input("spaces", min_value=0, max_value=5, value=garage, step=1)

        st.markdown('</div>', unsafe_allow_html=True)

        # Location
        st.markdown('<div class="input-card"><div class="input-card-title">📍 Location</div>', unsafe_allow_html=True)

        zone = st.selectbox(
            "Area Zone",
            options=zone_classes,
            format_func=lambda z: {
                "luxury":"🏰 Luxury",
                "urban":"🏙️ Urban",
                "suburban":"🏘️ Suburban",
                "rural":"🌾 Rural"
            }.get(z, z)
        )

        col_s5, col_n5 = st.columns([2, 1])
        with col_s5:
            location_rating = st.slider("Location Quality (1-10)", 1, 10, 7)
        with col_n5:
            location_rating = st.number_input("rating", min_value=1, max_value=10, value=location_rating, step=1)

        st.markdown('</div>', unsafe_allow_html=True)

        # Condition
        st.markdown('<div class="input-card"><div class="input-card-title">🏗️ Property Condition</div>', unsafe_allow_html=True)

        col_s6, col_n6 = st.columns([2, 1])
        with col_s6:
            age = st.slider("Property Age (Years)", 0, 50, 5)
        with col_n6:
            age = st.number_input("years", min_value=0, max_value=50, value=age, step=1)

        pool = st.checkbox("Swimming Pool 🏊", value=False)

        st.markdown('</div>', unsafe_allow_html=True)

    # ─────────────────────────────
    # 📊 MARKET TAB (UI ONLY — no logic interference)
    # ─────────────────────────────
    with tab2:

        st.markdown('<div class="input-card"><div class="input-card-title">🔥 Market Controls</div>', unsafe_allow_html=True)

        st.slider("Market Sensitivity", 0.5, 1.5, 1.0)
        st.slider("Investment Horizon (Years)", 1, 15, 5)

        st.markdown('</div>', unsafe_allow_html=True)

    # ─────────────────────────────
    # ⚙️ SETTINGS TAB
    # ─────────────────────────────
    with tab3:

        st.markdown('<div class="input-card"><div class="input-card-title">⚙️ Preferences</div>', unsafe_allow_html=True)

        st.checkbox("Enable Advanced Insights", True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    predict_btn = st.button("⚡ Run AI Valuation", use_container_width=True)

    # Model info (UNCHANGED)
    st.markdown(f"""
    <div style='margin-top:1.5rem; padding: 0.9rem 1rem; background:#0d1120;
                border:1px solid #1e2d40; border-radius:10px; font-size:0.78rem; color:#64748b;'>
        <div style='color:#3b82f6; font-weight:600; letter-spacing:1px; margin-bottom:0.5rem;'>MODEL INFO</div>
        <div>Algorithm: <span style='color:#93c5fd'>{bundle['model_name']}</span></div>
        <div>Accuracy (R²): <span style='color:#34d399'>{model_r2:.1%}</span></div>
        <div>Training rows: <span style='color:#e2e8f0'>{bundle['training_rows']}</span></div>
        <div style='margin-top:0.4rem;'>Currency: <span style='color:#fbbf24'>{"₹ INR" if show_inr else "$ USD"}</span></div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  HERO BANNER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">AI-Powered Real Estate Intelligence</div>
    <div class="hero-title">PropVision AI</div>
    <p class="hero-sub">
        Machine-learning valuation engine with dynamic demand scoring, zone-based market heat,
        and inflation-adjusted price projections — built for data-driven property decisions.
    </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  LIVE MARKET SNAPSHOT  (always visible, updates with inputs)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">Live Market Snapshot</div>', unsafe_allow_html=True)

demand_score = compute_demand(zone, location_rating, area)
d_label, d_color = demand_label(demand_score)
infl_rate = ZONE_INFLATION_RATE.get(zone, 0.05)

m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.markdown(f"""
    <div class="metric-card blue">
        <div class="metric-label">Zone Type</div>
        <div class="metric-value" style="font-size:1.3rem">{zone.capitalize()}</div>
        <div class="metric-delta">Selected area zone</div>
    </div>""", unsafe_allow_html=True)
with m2:
    bar_color = {"red":"#ef4444","gold":"#f59e0b","blue":"#3b82f6","green":"#10b981"}[d_color]
    st.markdown(f"""
    <div class="metric-card {d_color}">
        <div class="metric-label">Market Demand</div>
        <div class="metric-value" style="font-size:1.5rem">{int(demand_score*100)}%</div>
        <div class="demand-bar-wrap"><div class="demand-bar-fill"
            style="width:{int(demand_score*100)}%; background:{bar_color};"></div></div>
        <div class="metric-delta">{d_label}</div>
    </div>""", unsafe_allow_html=True)
with m3:
    mul = demand_to_multiplier(demand_score)
    st.markdown(f"""
    <div class="metric-card gold">
        <div class="metric-label">Demand Multiplier</div>
        <div class="metric-value highlight">×{mul:.2f}</div>
        <div class="metric-delta up">Applied to base price</div>
    </div>""", unsafe_allow_html=True)
with m4:
    st.markdown(f"""
    <div class="metric-card green">
        <div class="metric-label">Annual Appreciation</div>
        <div class="metric-value" style="font-size:1.6rem">{infl_rate*100:.1f}%</div>
        <div class="metric-delta up">Zone inflation rate</div>
    </div>""", unsafe_allow_html=True)
with m5:
    proj_5yr = round((1 + infl_rate) ** 5 * 100 - 100, 1)
    st.markdown(f"""
    <div class="metric-card purple">
        <div class="metric-label">5-Year Growth Est.</div>
        <div class="metric-value" style="font-size:1.6rem">+{proj_5yr}%</div>
        <div class="metric-delta up">Inflation compounded</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PREDICTION + RESULTS
# ══════════════════════════════════════════════════════════════════════════════
if predict_btn:
    with st.spinner("Running AI valuation model…"):
        time.sleep(0.6)  # micro-pause for dramatic effect

    # ── Core prediction
    zone_enc   = encoder.transform([zone])[0]
    features   = pd.DataFrame([[area, bedrooms, bathrooms, location_rating,
                                 age, int(garage), int(pool), zone_enc]],
                               columns=feat_cols)
    base_price = max(model.predict(features)[0], 0)

    demand_score  = compute_demand(zone, location_rating, area)
    multiplier    = demand_to_multiplier(demand_score)
    demand_price  = base_price * multiplier
    yearly_proj, infl_rate = compute_inflation_price(demand_price, zone, years_to_project=10)

    d_label, d_color = demand_label(demand_score)

    # ── RESULT HERO
    st.markdown('<div class="section-label">Valuation Results</div>', unsafe_allow_html=True)

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown(f"""
        <div class="metric-card blue animate-in" style="animation-delay:0s">
            <div class="metric-label">AI Base Price</div>
            <div class="metric-value">{fmt(base_price, show_inr, usd_to_inr)}</div>
            <div class="metric-delta">Model prediction (pre-market)</div>
        </div>""", unsafe_allow_html=True)
    with r2:
        st.markdown(f"""
        <div class="metric-card gold animate-in" style="animation-delay:0.1s">
            <div class="metric-label">Demand-Adjusted Price</div>
            <div class="metric-value highlight">{fmt(demand_price, show_inr, usd_to_inr)}</div>
            <div class="metric-delta up">+{fmt(demand_price - base_price, show_inr, usd_to_inr)} from demand</div>
        </div>""", unsafe_allow_html=True)
    with r3:
        price_5yr = yearly_proj[4]['Projected Price']
        st.markdown(f"""
        <div class="metric-card green animate-in" style="animation-delay:0.2s">
            <div class="metric-label">5-Year Projected Value</div>
            <div class="metric-value">{fmt(price_5yr, show_inr, usd_to_inr)}</div>
            <div class="metric-delta up">At {infl_rate*100:.1f}% annual appreciation</div>
        </div>""", unsafe_allow_html=True)
    with r4:
        price_10yr = yearly_proj[9]['Projected Price']
        roi = round((price_10yr - demand_price) / demand_price * 100, 1)
        st.markdown(f"""
        <div class="metric-card purple animate-in" style="animation-delay:0.3s">
            <div class="metric-label">10-Year ROI Estimate</div>
            <div class="metric-value">+{roi}%</div>
            <div class="metric-delta up">{fmt(price_10yr, show_inr, usd_to_inr)} projected</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    # ── INSIGHT BOX
    insight_color = "success" if demand_score >= 0.65 else ("warn" if demand_score >= 0.45 else "")
    st.markdown(f"""
    <div class="insight-box {insight_color}">
        <strong>🧠 AI Insight:</strong> This <strong>{zone}</strong> zone property shows
        <strong>{d_label}</strong> demand ({int(demand_score*100)}% demand score).
        The base AI model valued it at <strong>{fmt(base_price, show_inr, usd_to_inr)}</strong>, and after applying
        the demand multiplier of <strong>×{multiplier:.2f}</strong>, the market-adjusted
        valuation is <strong>{fmt(demand_price, show_inr, usd_to_inr)}</strong>. With the zone's annual appreciation
        rate of <strong>{infl_rate*100:.1f}%</strong>, this property is projected to reach
        <strong>{fmt(price_10yr, show_inr, usd_to_inr)}</strong> in 10 years — a <strong>+{roi}% ROI</strong>.
    </div>
    """, unsafe_allow_html=True)

    # ── TABS FOR CHARTS
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Inflation Projection",
        "🔥 Demand Analysis",
        "🏘️ Zone Comparison",
        "🔬 Feature Importance"
    ])

    # ── TAB 1: INFLATION PROJECTION CHART
    with tab1:
        st.markdown('<div class="section-label" style="margin-top:1rem">10-Year Price Trajectory</div>', unsafe_allow_html=True)

        years   = [f"Now"] + [y['Year'] for y in yearly_proj]
        prices  = [demand_price] + [y['Projected Price'] for y in yearly_proj]
        base_line = [demand_price * (1 + 0.03) ** i for i in range(11)]  # flat 3% benchmark

        fig1 = go.Figure()

        # Shaded area under projection
        fig1.add_trace(go.Scatter(
            x=years, y=prices,
            fill='tozeroy',
            fillcolor='rgba(59,130,246,0.07)',
            line=dict(color='rgba(59,130,246,0)', width=0),
            showlegend=False, hoverinfo='skip'
        ))

        # Benchmark line
        fig1.add_trace(go.Scatter(
            x=years, y=base_line,
            mode='lines',
            name='3% Benchmark',
            line=dict(color='rgba(148,163,184,0.5)', width=1.5, dash='dot'),
        ))

        # Main projection line
        fig1.add_trace(go.Scatter(
            x=years, y=prices,
            mode='lines+markers',
            name=f'{zone.capitalize()} Zone ({infl_rate*100:.1f}% p.a.)',
            line=dict(color='#3b82f6', width=3),
            marker=dict(color='#fbbf24', size=8, line=dict(color='#0a0d14', width=2)),
            hovertemplate="<b>%{x}</b><br>Projected: " + ("₹" if show_inr else "$") + "%{y:,.0f}<extra></extra>"
        ))

        # Highlight 5yr and 10yr
        for idx, label in [(5, "5-Year"), (10, "10-Year")]:
            fig1.add_annotation(
                x=years[idx], y=prices[idx],
                text=f"<b>{label}<br>{fmt(prices[idx], show_inr, usd_to_inr)}</b>",
                showarrow=True, arrowhead=2, arrowcolor='#fbbf24',
                arrowwidth=1.5, ax=40, ay=-40,
                font=dict(color='#fbbf24', size=11),
                bgcolor='rgba(10,13,20,0.8)', bordercolor='#fbbf24',
                borderwidth=1, borderpad=6
            )

        fig1.update_layout(
            paper_bgcolor='#111827', plot_bgcolor='#111827',
            font=dict(family='DM Sans', color='#94a3b8'),
            xaxis=dict(gridcolor='#1e2d40', tickfont=dict(color='#64748b')),
            yaxis=dict(gridcolor='#1e2d40', tickformat='$,.0f', tickfont=dict(color='#64748b')),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#94a3b8')),
            margin=dict(l=10, r=10, t=20, b=10),
            height=380,
            hovermode='x unified',
            hoverlabel=dict(bgcolor='#1a2233', font_color='#e2e8f0', bordercolor='#3b82f6')
        )
        st.plotly_chart(fig1, use_container_width=True)

    # ── TAB 2: DEMAND BREAKDOWN
    with tab2:
        st.markdown('<div class="section-label" style="margin-top:1rem">Demand Score Composition</div>', unsafe_allow_html=True)

        base_d   = ZONE_DEMAND_BASE.get(zone, 0.5)
        loc_d    = (location_rating - 1) / 9
        area_d   = min(area / 5000, 1.0)
        contributions = {
            'Zone Base Demand': round(0.55 * base_d, 3),
            'Location Quality': round(0.30 * loc_d, 3),
            'Area Size Factor': round(0.15 * area_d, 3),
        }

        col_a, col_b = st.columns([1, 1])

        with col_a:
            # Horizontal bar chart
            fig2 = go.Figure(go.Bar(
                x=list(contributions.values()),
                y=list(contributions.keys()),
                orientation='h',
                marker=dict(
                    color=['#3b82f6', '#f59e0b', '#10b981'],
                    line=dict(color='#0a0d14', width=1)
                ),
                text=[f'{v:.3f} ({v/demand_score*100:.0f}%)' for v in contributions.values()],
                textposition='outside',
                textfont=dict(color='#94a3b8', size=12),
                hovertemplate="<b>%{y}</b><br>Score: %{x:.3f}<extra></extra>"
            ))
            fig2.update_layout(
                paper_bgcolor='#111827', plot_bgcolor='#111827',
                font=dict(family='DM Sans', color='#94a3b8'),
                xaxis=dict(gridcolor='#1e2d40', range=[0, 0.8]),
                yaxis=dict(gridcolor='rgba(0,0,0,0)'),
                margin=dict(l=10, r=80, t=20, b=10),
                height=260,
                showlegend=False,
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col_b:
            # Gauge chart
            gauge_color = '#ef4444' if demand_score >= 0.80 else ('#f59e0b' if demand_score >= 0.65 else ('#3b82f6' if demand_score >= 0.45 else '#10b981'))
            fig3 = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=round(demand_score * 100, 1),
                title=dict(text="Demand Score", font=dict(color='#94a3b8', size=14)),
                number=dict(suffix="%", font=dict(color='#f8fafc', size=36, family='Playfair Display')),
                delta=dict(reference=50, valueformat=".1f", suffix="%",
                           increasing=dict(color='#34d399'), decreasing=dict(color='#f87171')),
                gauge=dict(
                    axis=dict(range=[0, 100], tickcolor='#1e2d40', tickfont=dict(color='#64748b')),
                    bar=dict(color=gauge_color, thickness=0.25),
                    bgcolor='#1a2233',
                    bordercolor='#1e2d40',
                    steps=[
                        dict(range=[0,35],  color='rgba(16,185,129,0.1)'),
                        dict(range=[35,65], color='rgba(59,130,246,0.1)'),
                        dict(range=[65,80], color='rgba(245,158,11,0.1)'),
                        dict(range=[80,100],color='rgba(239,68,68,0.1)'),
                    ],
                    threshold=dict(line=dict(color='#fbbf24', width=3), thickness=0.7, value=demand_score*100)
                )
            ))
            fig3.update_layout(
                paper_bgcolor='#111827',
                font=dict(family='DM Sans'),
                margin=dict(l=20, r=20, t=30, b=10),
                height=260,
            )
            st.plotly_chart(fig3, use_container_width=True)

        # Price impact breakdown
        st.markdown(f"""
        <div class="insight-box">
            <strong>💡 Demand Breakdown:</strong> Zone base contributes
            <strong>{contributions['Zone Base Demand']/demand_score*100:.0f}%</strong>,
            location quality <strong>{contributions['Location Quality']/demand_score*100:.0f}%</strong>,
            and area size <strong>{contributions['Area Size Factor']/demand_score*100:.0f}%</strong>
            to the overall demand score of <strong>{int(demand_score*100)}%</strong>.
            This inflates the base price by <strong>{fmt(demand_price-base_price, show_inr, usd_to_inr)}</strong>.
        </div>
        """, unsafe_allow_html=True)

    # ── TAB 3: ZONE COMPARISON
    with tab3:
        st.markdown('<div class="section-label" style="margin-top:1rem">Zone Market Comparison</div>', unsafe_allow_html=True)

        zones_list   = ['rural', 'suburban', 'urban', 'luxury']
        zone_enc_map = {z: encoder.transform([z])[0] for z in zones_list}
        zone_prices  = []
        zone_demands = []
        zone_inflats = []

        for z in zones_list:
            f_df = pd.DataFrame([[area, bedrooms, bathrooms, location_rating,
                                  age, int(garage), int(pool), zone_enc_map[z]]],
                                columns=feat_cols)
            bp  = max(model.predict(f_df)[0], 0)
            ds  = compute_demand(z, location_rating, area)
            mul = demand_to_multiplier(ds)
            zone_prices.append(round(bp * mul))
            zone_demands.append(round(ds * 100, 1))
            zone_inflats.append(ZONE_INFLATION_RATE[z] * 100)

        colors_z = ['#94a3b8', '#34d399', '#3b82f6', '#fbbf24']
        zone_labels = ['Rural', 'Suburban', 'Urban', 'Luxury']

        fig4 = make_subplots(
            rows=1, cols=2,
            subplot_titles=["Demand-Adjusted Price by Zone", "Demand Score & Inflation Rate"],
            specs=[[{"type": "bar"}, {"type": "scatter"}]]
        )

        fig4.add_trace(go.Bar(
            x=zone_labels, y=zone_prices,
            marker=dict(color=colors_z, line=dict(color='#0a0d14', width=1)),
            text=[fmt(p, show_inr, usd_to_inr) for p in zone_prices],
            textposition='outside', textfont=dict(color='#94a3b8', size=11),
            name='Price', hovertemplate="<b>%{x}</b><br>" + ("%{text}" ) + "<extra></extra>",
        ), row=1, col=1)

        fig4.add_trace(go.Scatter(
            x=zone_labels, y=zone_demands,
            mode='lines+markers',
            name='Demand %',
            line=dict(color='#3b82f6', width=2.5),
            marker=dict(color='#60a5fa', size=9),
            yaxis='y2',
        ), row=1, col=2)

        fig4.add_trace(go.Bar(
            x=zone_labels, y=zone_inflats,
            marker=dict(color=[f'rgba(251,191,36,{0.3+i*0.15})' for i in range(4)]),
            name='Inflation %',
            text=[f'{r:.1f}%' for r in zone_inflats],
            textposition='outside', textfont=dict(color='#fbbf24', size=11),
        ), row=1, col=2)

        fig4.update_layout(
            paper_bgcolor='#111827', plot_bgcolor='#111827',
            font=dict(family='DM Sans', color='#94a3b8'),
            xaxis=dict(gridcolor='#1e2d40'),
            xaxis2=dict(gridcolor='#1e2d40'),
            yaxis=dict(gridcolor='#1e2d40', tickformat='$,.0f'),
            yaxis2=dict(gridcolor='#1e2d40'),
            yaxis3=dict(overlaying='y2', side='right'),
            margin=dict(l=10, r=10, t=50, b=10),
            height=380,
            showlegend=False,
            annotations=[dict(text=a, font=dict(color='#64748b', size=12))
                         for a in ["Demand-Adjusted Price by Zone", "Demand Score & Inflation Rate"]]
        )
        # Highlight selected zone
        fig4.add_shape(
            type='rect', row=1, col=1,
            x0=zones_list.index(zone)-0.4, x1=zones_list.index(zone)+0.4,
            y0=0, y1=max(zone_prices)*1.12,
            line=dict(color='#fbbf24', width=1.5, dash='dot'),
            fillcolor='rgba(251,191,36,0.04)'
        )
        st.plotly_chart(fig4, use_container_width=True)

    # ── TAB 4: FEATURE IMPORTANCE
    with tab4:
        st.markdown('<div class="section-label" style="margin-top:1rem">What Drives the Price?</div>', unsafe_allow_html=True)

        feat_names = {
            'area': 'Property Area',
            'bedrooms': 'Bedrooms',
            'bathrooms': 'Bathrooms',
            'location_rating': 'Location Rating',
            'age': 'Property Age',
            'garage': 'Garage Spaces',
            'pool': 'Swimming Pool',
            'zone_encoded': 'Zone Type'
        }
        sorted_fi = sorted(feat_imp.items(), key=lambda x: x[1], reverse=True)
        names  = [feat_names.get(k, k) for k, _ in sorted_fi]
        values = [v * 100 for _, v in sorted_fi]

        fig5 = go.Figure(go.Bar(
            x=values, y=names,
            orientation='h',
            marker=dict(
                color=values,
                colorscale=[[0, '#1e3a5f'], [0.5, '#3b82f6'], [1, '#93c5fd']],
                line=dict(color='#0a0d14', width=0.5)
            ),
            text=[f'{v:.1f}%' for v in values],
            textposition='outside',
            textfont=dict(color='#94a3b8', size=12),
            hovertemplate="<b>%{y}</b><br>Importance: %{x:.1f}%<extra></extra>"
        ))
        fig5.update_layout(
            paper_bgcolor='#111827', plot_bgcolor='#111827',
            font=dict(family='DM Sans', color='#94a3b8'),
            xaxis=dict(gridcolor='#1e2d40', ticksuffix='%',
                       range=[0, max(values) * 1.25]),
            yaxis=dict(gridcolor='rgba(0,0,0,0)', autorange='reversed'),
            margin=dict(l=10, r=80, t=20, b=10),
            height=350,
            showlegend=False,
        )
        st.plotly_chart(fig5, use_container_width=True)

        col_fi1, col_fi2 = st.columns(2)
        top_feat = names[0]
        top_val  = values[0]
        with col_fi1:
            st.markdown(f"""
            <div class="insight-box success">
                <strong>🏆 Top Driver:</strong> <strong>{top_feat}</strong> accounts for
                <strong>{top_val:.1f}%</strong> of the model's decisions — making it the
                single most important feature in this dataset.
            </div>""", unsafe_allow_html=True)
        with col_fi2:
            bottom_feat = names[-1]
            st.markdown(f"""
            <div class="insight-box">
                <strong>ℹ️ Least Influential:</strong> <strong>{bottom_feat}</strong> has the
                smallest impact (<strong>{values[-1]:.1f}%</strong>), though it still contributes
                to the overall valuation.
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    # ── PROPERTY SUMMARY TABLE
    st.markdown('<div class="section-label">Property Summary</div>', unsafe_allow_html=True)
    summary_data = {
        "Attribute": ["Area (sq ft)", "Bedrooms", "Bathrooms", "Garage", "Pool",
                      "Location Rating", "Zone", "Property Age",
                      "AI Base Price", "Demand Score", "Demand Multiplier",
                      "Final Market Price", "5-Year Projection", "10-Year Projection"],
        "Value": [f"{area} sq ft", str(bedrooms), str(bathrooms), str(garage),
                  "Yes" if pool else "No", f"{location_rating}/10",
                  f"{zone.capitalize()}", f"{age} years",
                  fmt(base_price, show_inr, usd_to_inr),
                  f"{int(demand_score*100)}% ({d_label})",
                  f"×{multiplier:.2f}",
                  fmt(demand_price, show_inr, usd_to_inr),
                  fmt(yearly_proj[4]['Projected Price'], show_inr, usd_to_inr),
                  fmt(yearly_proj[9]['Projected Price'], show_inr, usd_to_inr)]
    }
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(
        summary_df.style.set_properties(**{
            'background-color': '#111827',
            'color': '#e2e8f0',
            'border-color': '#1e2d40'
        }).apply(lambda x: ['background-color: rgba(59,130,246,0.1)' if i >= 8
                            else '' for i in range(len(x))], axis=0),
        use_container_width=True,
        hide_index=True,
        height=530
    )

else:
    # ── PLACEHOLDER when no prediction yet
    st.markdown("""
    <div style="text-align:center; padding: 5rem 2rem; color:#334155;">
        <div style="font-size:4rem; margin-bottom:1rem;">🏛️</div>
        <div style="font-family:'Playfair Display',serif; font-size:1.6rem; color:#475569; margin-bottom:0.5rem;">
            Configure your property on the left
        </div>
        <div style="font-size:0.95rem; color:#334155;">
            Adjust the sliders and click <strong style="color:#3b82f6">Run AI Valuation</strong> to get your full analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#334155; font-size:0.78rem; padding-bottom:1rem;">
    <span style="color:#1e3a5f">●</span>&nbsp;
    PropVision AI — House Price Intelligence Platform &nbsp;|&nbsp;
    Powered by Random Forest ML &nbsp;|&nbsp;
    Dynamic Demand Engine v2.0
    &nbsp;<span style="color:#1e3a5f">●</span>
</div>
""", unsafe_allow_html=True)

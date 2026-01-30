"""
PORTFOLIO OPTIMIZER — PALANTIR GOTHAM EDITION
===============================================
Defense Intelligence Interface for Portfolio Analysis
Markowitz Modern Portfolio Theory Implementation

CLASSIFICATION: UNCLASSIFIED // FOR AUTHORIZED USERS ONLY
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Import des modules locaux
from data_fetcher import (
    validate_tickers,
    fetch_price_data,
    calculate_returns,
    calculate_annual_metrics
)
from optimizer import optimize_portfolio
from visualizations import (
    create_efficient_frontier,
    create_allocation_chart,
    create_correlation_heatmap,
    create_individual_returns_chart
)


# ============================================
# Configuration Streamlit
# ============================================
st.set_page_config(
    page_title="GOTHAM // Portfolio Optimizer",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================
# CSS GOTHAM - Defense Intelligence Interface
# ============================================
st.markdown("""
<style>
    /* ===== GOTHAM FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* ===== ROOT VARIABLES ===== */
    :root {
        --bg-primary: #0A0B10;
        --bg-secondary: #141722;
        --bg-tertiary: #1a1f2e;
        --border: #23283D;
        --accent-blue: #00A3FF;
        --accent-cyan: #00D4FF;
        --alert-red: #FF4B4B;
        --success-green: #00FF88;
        --text-primary: #E0E0E0;
        --text-secondary: #8892A0;
        --gold: #FFD700;
    }
    
    /* ===== GLOBAL STYLES ===== */
    .stApp {
        background: var(--bg-primary);
        font-family: 'Inter', sans-serif;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-blue);
    }
    
    /* ===== TERMINAL HEADER ===== */
    .terminal-header {
        background: linear-gradient(90deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 0.6rem 1.2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .terminal-status {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    .status-dot.active { background: var(--success-green); box-shadow: 0 0 8px var(--success-green); }
    .status-dot.secure { background: var(--accent-cyan); box-shadow: 0 0 8px var(--accent-cyan); }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .terminal-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: 2px;
    }
    
    .terminal-time {
        font-size: 0.7rem;
        color: var(--text-secondary);
    }
    
    /* ===== MAIN HEADER ===== */
    .main-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-primary);
        text-align: center;
        letter-spacing: 4px;
        margin: 0.5rem 0;
    }
    
    .sub-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--text-secondary);
        text-align: center;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }
    
    /* ===== SIDEBAR / CONFIG CONSOLE ===== */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: var(--text-primary);
    }
    
    .console-header {
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 0.8rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .console-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: var(--accent-cyan);
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* ===== WIDGET CONTAINERS ===== */
    .widget-container {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .widget-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--text-secondary);
        letter-spacing: 2px;
        text-transform: uppercase;
        border-bottom: 1px solid var(--border);
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* ===== GLOWING KPI CARDS ===== */
    .kpi-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 1rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent-blue), transparent);
    }
    
    .kpi-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--accent-cyan);
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
    }
    
    .kpi-value.gold {
        color: var(--gold);
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
    }
    
    .kpi-value.green {
        color: var(--success-green);
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.4);
    }
    
    .kpi-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    /* ===== SECTION HEADERS ===== */
    .section-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: 2px;
        text-transform: uppercase;
        border-left: 3px solid var(--accent-blue);
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
    }
    
    /* ===== ALERTS ===== */
    .alert-box {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-left: 3px solid var(--alert-red);
        border-radius: 4px;
        padding: 0.8rem 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: var(--alert-red);
    }
    
    .success-box {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-left: 3px solid var(--success-green);
        border-radius: 4px;
        padding: 0.8rem 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: var(--success-green);
    }
    
    .info-box {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-left: 3px solid var(--accent-blue);
        border-radius: 4px;
        padding: 1rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: var(--text-secondary);
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(180deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
        border: 1px solid var(--accent-blue);
        border-radius: 4px;
        color: var(--accent-blue);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 0.6rem 1.5rem;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: var(--accent-blue);
        color: var(--bg-primary);
        box-shadow: 0 0 15px rgba(0, 163, 255, 0.4);
    }
    
    /* ===== INPUTS ===== */
    .stTextInput > div > div > input {
        background: var(--bg-primary);
        border: 1px solid var(--border);
        color: var(--text-primary);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        border-radius: 4px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-blue);
        box-shadow: 0 0 5px rgba(0, 163, 255, 0.3);
    }
    
    .stSelectbox > div > div {
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 4px;
    }
    
    /* ===== SLIDER ===== */
    .stSlider > div > div > div > div {
        background: var(--accent-blue);
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 4px 4px 0 0;
        color: var(--text-secondary);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 8px 16px;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--bg-tertiary);
        border-bottom-color: var(--bg-tertiary);
        color: var(--accent-cyan);
    }
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 4px;
        color: var(--text-primary);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 1px;
    }
    
    .streamlit-expanderContent {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-top: none;
    }
    
    /* ===== DATAFRAME ===== */
    .dataframe {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
    }
    
    /* ===== HIDE STREAMLIT BRANDING ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ============================================
# Fonctions UI Gotham
# ============================================
def render_terminal_header():
    """Render the GOTHAM terminal header."""
    now = datetime.now()
    st.markdown(f"""
        <div class="terminal-header">
            <div class="terminal-status">
                <div class="status-indicator">
                    <div class="status-dot active"></div>
                    <span style="color: #00FF88;">SYSTEM ACTIVE</span>
                </div>
                <div class="status-indicator">
                    <div class="status-dot secure"></div>
                    <span style="color: #00D4FF;">TERMINAL LINK: SECURE</span>
                </div>
            </div>
            <div class="terminal-title">◆ YOUN GOGER-LE GOUX</div>
            <div class="terminal-time">{now.strftime('%Y-%m-%d')} // {now.strftime('%H:%M:%S')} UTC</div>
        </div>
    """, unsafe_allow_html=True)


def render_kpi_card(value: str, label: str, style: str = ""):
    """Render a glowing KPI card."""
    return f"""
        <div class="kpi-card">
            <div class="kpi-value {style}">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>
    """


def display_portfolio_metrics(portfolio: dict, title: str):
    """Display portfolio metrics in GOTHAM style."""
    st.markdown(f'<div class="section-header">◆ {title}</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(render_kpi_card(
            f"{portfolio['return']*100:.2f}%",
            "Expected Return",
            "green"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(render_kpi_card(
            f"{portfolio['volatility']*100:.2f}%",
            "Annual Volatility",
            ""
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(render_kpi_card(
            f"{portfolio['sharpe']:.3f}",
            "Sharpe Ratio",
            "gold"
        ), unsafe_allow_html=True)


# ============================================
# SIDEBAR - Configuration Console
# ============================================
with st.sidebar:
    st.markdown("""
        <div class="console-header">
            <div class="console-title">◆ Configuration Console</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="widget-header">ASSET SELECTION</div>', unsafe_allow_html=True)
    default_tickers = "AAPL, MSFT, GOOGL, TSLA, NVDA"
    tickers_input = st.text_input(
        "TARGET ASSETS",
        value=default_tickers,
        help="Enter ticker symbols separated by commas"
    )
    
    st.markdown('<div class="widget-header">ANALYSIS PARAMETERS</div>', unsafe_allow_html=True)
    years = st.slider(
        "HISTORICAL PERIOD (YEARS)",
        min_value=1,
        max_value=10,
        value=5
    )
    
    with st.expander("ADVANCED CONFIG"):
        n_simulations = st.number_input(
            "MONTE CARLO ITERATIONS",
            min_value=1000,
            max_value=20000,
            value=5000,
            step=1000
        )
        risk_free_rate = st.number_input(
            "RISK-FREE RATE (%)",
            min_value=0.0,
            max_value=10.0,
            value=2.0,
            step=0.5
        ) / 100
    
    st.markdown("<br>", unsafe_allow_html=True)
    run_optimization = st.button("◆ EXECUTE ANALYSIS", use_container_width=True)


# ============================================
# MAIN CONTENT
# ============================================
render_terminal_header()

st.markdown('<h1 class="main-header">PORTFOLIO OPTIMIZER</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Modern Portfolio Theory // Markowitz Optimization Engine</p>', unsafe_allow_html=True)


# ============================================
# Logique principale
# ============================================
if run_optimization:
    tickers = [t.strip().upper() for t in tickers_input.split(',') if t.strip()]
    
    if len(tickers) < 2:
        st.markdown("""
            <div class="alert-box">
                ⚠ ERROR: Minimum 2 assets required for optimization
            </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("◆ VALIDATING ASSETS..."):
            valid_tickers, invalid_tickers = validate_tickers(tickers)
        
        if invalid_tickers:
            st.markdown(f"""
                <div class="alert-box">
                    ⚠ INVALID TICKERS EXCLUDED: {', '.join(invalid_tickers)}
                </div>
            """, unsafe_allow_html=True)
        
        if len(valid_tickers) < 2:
            st.markdown("""
                <div class="alert-box">
                    ⚠ ERROR: Insufficient valid assets. Minimum: 2
                </div>
            """, unsafe_allow_html=True)
        else:
            try:
                with st.spinner("◆ ACQUIRING MARKET DATA..."):
                    prices = fetch_price_data(valid_tickers, years)
                    returns = calculate_returns(prices)
                    annual_returns, cov_matrix, corr_matrix = calculate_annual_metrics(returns)
                
                with st.spinner(f"◆ EXECUTING {n_simulations:,} SIMULATIONS..."):
                    simulation_results, optimal_portfolios = optimize_portfolio(
                        annual_returns,
                        cov_matrix,
                        valid_tickers,
                        n_simulations,
                        risk_free_rate
                    )
                
                st.markdown("""
                    <div class="success-box">
                        ✓ ANALYSIS COMPLETE — OPTIMIZATION SUCCESSFUL
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Optimal Portfolio
                display_portfolio_metrics(optimal_portfolios['max_sharpe'], "OPTIMAL PORTFOLIO [MAX SHARPE]")
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Defensive Portfolio
                display_portfolio_metrics(optimal_portfolios['min_volatility'], "DEFENSIVE PORTFOLIO [MIN VARIANCE]")
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Visualizations
                tab1, tab2, tab3, tab4 = st.tabs([
                    "EFFICIENT FRONTIER",
                    "ASSET ALLOCATION",
                    "CORRELATION MATRIX",
                    "INDIVIDUAL RETURNS"
                ])
                
                with tab1:
                    fig_frontier = create_efficient_frontier(
                        simulation_results,
                        optimal_portfolios,
                        valid_tickers
                    )
                    st.plotly_chart(fig_frontier, use_container_width=True)
                
                with tab2:
                    col1, col2 = st.columns(2)
                    with col1:
                        fig_alloc_sharpe = create_allocation_chart(
                            optimal_portfolios['max_sharpe']['weights'],
                            "Max Sharpe"
                        )
                        st.plotly_chart(fig_alloc_sharpe, use_container_width=True)
                    
                    with col2:
                        fig_alloc_minvol = create_allocation_chart(
                            optimal_portfolios['min_volatility']['weights'],
                            "Min Variance"
                        )
                        st.plotly_chart(fig_alloc_minvol, use_container_width=True)
                
                with tab3:
                    fig_corr = create_correlation_heatmap(corr_matrix)
                    st.plotly_chart(fig_corr, use_container_width=True)
                
                with tab4:
                    fig_returns = create_individual_returns_chart(annual_returns)
                    st.plotly_chart(fig_returns, use_container_width=True)
                
                # Weights Table
                st.markdown('<div class="section-header">◆ ALLOCATION MATRIX</div>', unsafe_allow_html=True)
                
                weights_df = pd.DataFrame({
                    'ASSET': valid_tickers,
                    'OPTIMAL %': [optimal_portfolios['max_sharpe']['weights'][t] * 100 for t in valid_tickers],
                    'DEFENSIVE %': [optimal_portfolios['min_volatility']['weights'][t] * 100 for t in valid_tickers]
                })
                
                st.dataframe(
                    weights_df.style.format({
                        'OPTIMAL %': '{:.2f}',
                        'DEFENSIVE %': '{:.2f}'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
                
            except Exception as e:
                st.markdown(f"""
                    <div class="alert-box">
                        ⚠ SYSTEM ERROR: {str(e)}
                    </div>
                """, unsafe_allow_html=True)

else:
    st.markdown("""
        <div class="info-box">
            <strong>◆ AWAITING INPUT</strong><br><br>
            Configure analysis parameters in the <b>Configuration Console</b> (sidebar) 
            and execute <b>◆ EXECUTE ANALYSIS</b> to initialize portfolio optimization.
        </div>
    """, unsafe_allow_html=True)


# ============================================
# Educational Section
# ============================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">◆ METHODOLOGY REFERENCE</div>', unsafe_allow_html=True)

with st.expander("MODERN PORTFOLIO THEORY — DOCUMENTATION"):
    st.markdown("""
    ### THEORETICAL FRAMEWORK
    
    The **Modern Portfolio Theory (MPT)**, developed by Harry Markowitz (1952), 
    provides the mathematical framework for constructing portfolios that maximize 
    expected return for a given level of risk.
    
    ---
    
    ### KEY METRICS
    
    | Metric | Formula | Description |
    |--------|---------|-------------|
    | **Expected Return (μ)** | `Σ(wᵢ × rᵢ)` | Weighted average of asset returns |
    | **Volatility (σ)** | `√(w'Σw)` | Portfolio standard deviation |
    | **Sharpe Ratio** | `(μ - rf) / σ` | Risk-adjusted return measure |
    
    ---
    
    ### OPTIMIZATION TARGETS
    
    - **Maximum Sharpe**: Optimal risk/reward trade-off
    - **Minimum Variance**: Lowest risk portfolio on the frontier
    
    ---
    
    ### LIMITATIONS
    
    - Historical data may not predict future performance
    - Assumes normally distributed returns
    - Correlation structures may change in crisis periods
    """)

# Footer
st.markdown("""
<div style="text-align: center; font-family: 'JetBrains Mono', monospace; 
            font-size: 0.65rem; color: #4a5568; padding: 2rem 0; letter-spacing: 1px;">
    YOUN GOGER-LE GOUX // PORTFOLIO OPTIMIZATION ENGINE // MARKOWITZ MPT v1.0
</div>
""", unsafe_allow_html=True)

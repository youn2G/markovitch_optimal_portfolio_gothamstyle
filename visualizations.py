"""
Visualizations Module - PALANTIR GOTHAM EDITION
=================================================
Graphiques interactifs Plotly pour l'optimisation de portefeuille.
Style "Defense Intelligence Interface" - Palantir Gotham.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict


# Palette GOTHAM - Defense Intelligence
GOTHAM = {
    'bg_primary': '#0A0B10',      # Deep obsidian
    'bg_secondary': '#141722',    # Container dark
    'border': '#23283D',          # Subtle borders
    'accent_blue': '#00A3FF',     # Primary accent
    'accent_cyan': '#00D4FF',     # Secondary accent
    'alert_red': '#FF4B4B',       # Alert/Warning
    'success_green': '#00FF88',   # Success/Positive
    'text_primary': '#E0E0E0',    # Main text
    'text_secondary': '#8892A0',  # Muted text
    'grid_faint': '#1E2330',      # Very faint grid
    'gold': '#FFD700',            # Highlight
}


def _get_gotham_layout():
    """Base layout configuration for Gotham theme."""
    return dict(
        plot_bgcolor=GOTHAM['bg_primary'],
        paper_bgcolor=GOTHAM['bg_secondary'],
        font=dict(
            family="JetBrains Mono, Roboto Mono, monospace",
            color=GOTHAM['text_primary'],
            size=11
        ),
        margin=dict(l=50, r=30, t=60, b=50),
    )


def create_efficient_frontier(
    simulation_results,
    optimal_portfolios: Dict,
    tickers: list
) -> go.Figure:
    """
    Crée le graphique de la Frontière Efficiente - Style Gotham.
    """
    fig = go.Figure()
    
    # Nuage de points des simulations
    fig.add_trace(go.Scatter(
        x=simulation_results.volatilities * 100,
        y=simulation_results.returns * 100,
        mode='markers',
        marker=dict(
            size=3,
            color=simulation_results.sharpe_ratios,
            colorscale=[
                [0, '#1a1f2e'],
                [0.5, '#00A3FF'],
                [1, '#00FF88']
            ],
            colorbar=dict(
                title=dict(
                    text='SHARPE',
                    font=dict(color=GOTHAM['text_secondary'], size=10)
                ),
                tickfont=dict(color=GOTHAM['text_secondary'], size=9),
                thickness=10,
                len=0.6,
                bgcolor=GOTHAM['bg_secondary'],
                bordercolor=GOTHAM['border'],
                borderwidth=1
            ),
            opacity=0.6,
            line=dict(width=0)
        ),
        hovertemplate=(
            '<b>σ:</b> %{x:.2f}%<br>'
            '<b>μ:</b> %{y:.2f}%<extra></extra>'
        ),
        name='SIMULATIONS'
    ))
    
    # Portefeuille Max Sharpe
    max_sharpe = optimal_portfolios['max_sharpe']
    fig.add_trace(go.Scatter(
        x=[max_sharpe['volatility'] * 100],
        y=[max_sharpe['return'] * 100],
        mode='markers+text',
        marker=dict(
            size=14,
            color=GOTHAM['gold'],
            symbol='diamond',
            line=dict(width=2, color=GOTHAM['bg_primary'])
        ),
        text=['MAX SHARPE'],
        textposition='top center',
        textfont=dict(color=GOTHAM['gold'], size=9, family='JetBrains Mono'),
        name=f"OPTIMAL [SR: {max_sharpe['sharpe']:.3f}]",
        hovertemplate=(
            '<b>█ OPTIMAL PORTFOLIO</b><br>'
            f'μ: {max_sharpe["return"]*100:.2f}%<br>'
            f'σ: {max_sharpe["volatility"]*100:.2f}%<br>'
            f'SR: {max_sharpe["sharpe"]:.3f}<extra></extra>'
        )
    ))
    
    # Portefeuille Min Volatilité
    min_vol = optimal_portfolios['min_volatility']
    fig.add_trace(go.Scatter(
        x=[min_vol['volatility'] * 100],
        y=[min_vol['return'] * 100],
        mode='markers+text',
        marker=dict(
            size=12,
            color=GOTHAM['accent_cyan'],
            symbol='square',
            line=dict(width=2, color=GOTHAM['bg_primary'])
        ),
        text=['MIN VAR'],
        textposition='top center',
        textfont=dict(color=GOTHAM['accent_cyan'], size=9, family='JetBrains Mono'),
        name=f"DEFENSIVE [σ: {min_vol['volatility']*100:.1f}%]",
        hovertemplate=(
            '<b>█ MINIMUM VARIANCE</b><br>'
            f'μ: {min_vol["return"]*100:.2f}%<br>'
            f'σ: {min_vol["volatility"]*100:.2f}%<br>'
            f'SR: {min_vol["sharpe"]:.3f}<extra></extra>'
        )
    ))
    
    # Layout Gotham
    fig.update_layout(
        **_get_gotham_layout(),
        title=dict(
            text='<b>EFFICIENT FRONTIER</b>',
            font=dict(size=14, color=GOTHAM['text_primary']),
            x=0.5
        ),
        xaxis=dict(
            title=dict(text='VOLATILITY (σ %)', font=dict(color=GOTHAM['text_secondary'], size=10)),
            tickfont=dict(color=GOTHAM['text_secondary'], size=9),
            gridcolor=GOTHAM['grid_faint'],
            gridwidth=1,
            griddash='dot',
            zerolinecolor=GOTHAM['border'],
            showline=True,
            linewidth=1,
            linecolor=GOTHAM['border']
        ),
        yaxis=dict(
            title=dict(text='RETURN (μ %)', font=dict(color=GOTHAM['text_secondary'], size=10)),
            tickfont=dict(color=GOTHAM['text_secondary'], size=9),
            gridcolor=GOTHAM['grid_faint'],
            gridwidth=1,
            griddash='dot',
            zerolinecolor=GOTHAM['border'],
            showline=True,
            linewidth=1,
            linecolor=GOTHAM['border']
        ),
        legend=dict(
            font=dict(color=GOTHAM['text_secondary'], size=9),
            bgcolor='rgba(20,23,34,0.9)',
            bordercolor=GOTHAM['border'],
            borderwidth=1,
            x=0.02,
            y=0.98
        ),
        height=480,
    )
    
    return fig


def create_allocation_chart(weights: Dict, portfolio_name: str) -> go.Figure:
    """
    Graphique en barres de l'allocation - Style Gotham.
    """
    tickers = list(weights.keys())
    values = [w * 100 for w in weights.values()]
    
    # Couleurs basées sur la valeur
    colors = [GOTHAM['accent_blue'] if v > 15 else GOTHAM['accent_cyan'] for v in values]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=tickers,
        y=values,
        marker=dict(
            color=colors,
            line=dict(width=1, color=GOTHAM['border'])
        ),
        text=[f'{v:.1f}%' for v in values],
        textposition='outside',
        textfont=dict(color=GOTHAM['accent_blue'], size=10, family='JetBrains Mono'),
        hovertemplate='<b>%{x}</b><br>WEIGHT: %{y:.2f}%<extra></extra>'
    ))
    
    fig.update_layout(
        **_get_gotham_layout(),
        title=dict(
            text=f'<b>ALLOCATION — {portfolio_name.upper()}</b>',
            font=dict(size=12, color=GOTHAM['text_primary']),
            x=0.5
        ),
        xaxis=dict(
            title=None,
            tickfont=dict(color=GOTHAM['text_primary'], size=10, family='JetBrains Mono'),
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor=GOTHAM['border']
        ),
        yaxis=dict(
            title=dict(text='WEIGHT %', font=dict(color=GOTHAM['text_secondary'], size=9)),
            tickfont=dict(color=GOTHAM['text_secondary'], size=9),
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor=GOTHAM['border'],
            range=[0, max(values) * 1.25]
        ),
        height=340,
        showlegend=False,
        bargap=0.3
    )
    
    return fig


def create_correlation_heatmap(corr_matrix: pd.DataFrame) -> go.Figure:
    """
    Heatmap de corrélation - Style Gotham.
    """
    # Annotations
    annotations = []
    for i, row in enumerate(corr_matrix.index):
        for j, col in enumerate(corr_matrix.columns):
            val = corr_matrix.iloc[i, j]
            annotations.append(dict(
                x=col,
                y=row,
                text=f'{val:.2f}',
                font=dict(
                    color=GOTHAM['text_primary'] if abs(val) > 0.5 else GOTHAM['text_secondary'],
                    size=10,
                    family='JetBrains Mono'
                ),
                showarrow=False
            ))
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale=[
            [0, GOTHAM['alert_red']],
            [0.5, GOTHAM['bg_primary']],
            [1, GOTHAM['success_green']]
        ],
        zmin=-1,
        zmax=1,
        colorbar=dict(
            title=dict(text='ρ', font=dict(color=GOTHAM['text_secondary'], size=10)),
            tickfont=dict(color=GOTHAM['text_secondary'], size=9),
            thickness=8,
            len=0.7,
            bgcolor=GOTHAM['bg_secondary'],
            bordercolor=GOTHAM['border'],
            borderwidth=1
        ),
        hovertemplate='<b>%{x}</b> × <b>%{y}</b><br>ρ = %{z:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        **_get_gotham_layout(),
        title=dict(
            text='<b>CORRELATION MATRIX</b>',
            font=dict(size=12, color=GOTHAM['text_primary']),
            x=0.5
        ),
        xaxis=dict(
            tickfont=dict(color=GOTHAM['text_primary'], size=10, family='JetBrains Mono'),
            side='bottom',
            showline=True,
            linewidth=1,
            linecolor=GOTHAM['border']
        ),
        yaxis=dict(
            tickfont=dict(color=GOTHAM['text_primary'], size=10, family='JetBrains Mono'),
            autorange='reversed',
            showline=True,
            linewidth=1,
            linecolor=GOTHAM['border']
        ),
        height=400,
        annotations=annotations
    )
    
    return fig


def create_individual_returns_chart(annual_returns: pd.Series) -> go.Figure:
    """
    Graphique des rendements individuels - Style Gotham.
    """
    tickers = annual_returns.index.tolist()
    values = [r * 100 for r in annual_returns.values]
    
    colors = [GOTHAM['success_green'] if v >= 0 else GOTHAM['alert_red'] for v in values]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=tickers,
        y=values,
        marker=dict(
            color=colors,
            line=dict(width=1, color=GOTHAM['border'])
        ),
        text=[f'{v:+.1f}%' for v in values],
        textposition='outside',
        textfont=dict(color=GOTHAM['text_secondary'], size=9, family='JetBrains Mono'),
        hovertemplate='<b>%{x}</b><br>RETURN: %{y:.2f}%<extra></extra>'
    ))
    
    # Zero line
    fig.add_hline(
        y=0,
        line=dict(color=GOTHAM['border'], width=1)
    )
    
    fig.update_layout(
        **_get_gotham_layout(),
        title=dict(
            text='<b>ANNUALIZED RETURNS</b>',
            font=dict(size=12, color=GOTHAM['text_primary']),
            x=0.5
        ),
        xaxis=dict(
            title=None,
            tickfont=dict(color=GOTHAM['text_primary'], size=10, family='JetBrains Mono'),
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor=GOTHAM['border']
        ),
        yaxis=dict(
            title=dict(text='RETURN %', font=dict(color=GOTHAM['text_secondary'], size=9)),
            tickfont=dict(color=GOTHAM['text_secondary'], size=9),
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor=GOTHAM['border']
        ),
        height=300,
        showlegend=False,
        bargap=0.3
    )
    
    return fig

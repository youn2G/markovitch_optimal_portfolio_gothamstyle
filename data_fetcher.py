"""
Data Fetcher Module
====================
Module pour télécharger les données de marché via yfinance
et effectuer les calculs de rendements.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from typing import Tuple, List
from datetime import datetime, timedelta


def validate_tickers(tickers: List[str]) -> Tuple[List[str], List[str]]:
    """
    Valide une liste de tickers en vérifiant leur existence.
    
    Parameters
    ----------
    tickers : List[str]
        Liste des symboles boursiers à valider
        
    Returns
    -------
    Tuple[List[str], List[str]]
        (tickers_valides, tickers_invalides)
    """
    valid_tickers = []
    invalid_tickers = []
    
    for ticker in tickers:
        ticker = ticker.strip().upper()
        if not ticker:
            continue
            
        try:
            stock = yf.Ticker(ticker)
            # Vérifier si des données existent
            hist = stock.history(period="5d")
            if hist.empty:
                invalid_tickers.append(ticker)
            else:
                valid_tickers.append(ticker)
        except Exception:
            invalid_tickers.append(ticker)
    
    return valid_tickers, invalid_tickers


def fetch_price_data(
    tickers: List[str], 
    years: int = 5
) -> pd.DataFrame:
    """
    Télécharge les prix de clôture ajustés pour une liste de tickers.
    
    Parameters
    ----------
    tickers : List[str]
        Liste des symboles boursiers
    years : int
        Nombre d'années d'historique
        
    Returns
    -------
    pd.DataFrame
        DataFrame avec les prix de clôture ajustés (colonnes = tickers)
        
    Raises
    ------
    ValueError
        Si aucune donnée n'est disponible
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)
    
    # Télécharger les données
    data = yf.download(
        tickers,
        start=start_date.strftime('%Y-%m-%d'),
        end=end_date.strftime('%Y-%m-%d'),
        progress=False,
        auto_adjust=True
    )
    
    if data.empty:
        raise ValueError("Aucune donnée disponible pour les tickers spécifiés.")
    
    # Extraire les prix de clôture
    if len(tickers) == 1:
        prices = data[['Close']].copy()
        prices.columns = tickers
    else:
        prices = data['Close'].copy()
    
    # Supprimer les lignes avec des valeurs manquantes
    prices = prices.dropna()
    
    if prices.empty:
        raise ValueError("Données insuffisantes après nettoyage.")
    
    return prices


def calculate_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les rendements logarithmiques quotidiens.
    
    Parameters
    ----------
    prices : pd.DataFrame
        Prix de clôture ajustés
        
    Returns
    -------
    pd.DataFrame
        Rendements logarithmiques quotidiens
    """
    returns = np.log(prices / prices.shift(1)).dropna()
    return returns


def calculate_annual_metrics(
    returns: pd.DataFrame, 
    trading_days: int = 252
) -> Tuple[pd.Series, pd.DataFrame, pd.DataFrame]:
    """
    Calcule les métriques annualisées.
    
    Parameters
    ----------
    returns : pd.DataFrame
        Rendements logarithmiques quotidiens
    trading_days : int
        Nombre de jours de trading par an
        
    Returns
    -------
    Tuple[pd.Series, pd.DataFrame, pd.DataFrame]
        (rendements_annuels, matrice_covariance, matrice_correlation)
    """
    # Rendements annuels moyens
    annual_returns = returns.mean() * trading_days
    
    # Matrice de covariance annualisée
    cov_matrix = returns.cov() * trading_days
    
    # Matrice de corrélation
    corr_matrix = returns.corr()
    
    return annual_returns, cov_matrix, corr_matrix

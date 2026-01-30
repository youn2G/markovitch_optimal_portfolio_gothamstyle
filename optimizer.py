"""
Portfolio Optimizer Module
===========================
Module d'optimisation de portefeuille basé sur la Théorie Moderne de Markowitz.
Génère des simulations Monte Carlo et identifie les portefeuilles optimaux.
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, NamedTuple
from dataclasses import dataclass


@dataclass
class PortfolioResult:
    """Résultat d'un portefeuille optimisé."""
    weights: np.ndarray
    expected_return: float
    volatility: float
    sharpe_ratio: float


class SimulationResults(NamedTuple):
    """Résultats des simulations Monte Carlo."""
    returns: np.ndarray
    volatilities: np.ndarray
    sharpe_ratios: np.ndarray
    all_weights: np.ndarray


def generate_random_weights(n_assets: int) -> np.ndarray:
    """
    Génère des poids aléatoires normalisés pour un portefeuille.
    
    Parameters
    ----------
    n_assets : int
        Nombre d'actifs dans le portefeuille
        
    Returns
    -------
    np.ndarray
        Poids normalisés (somme = 1)
    """
    weights = np.random.random(n_assets)
    weights /= weights.sum()
    return weights


def calculate_portfolio_metrics(
    weights: np.ndarray,
    annual_returns: pd.Series,
    cov_matrix: pd.DataFrame,
    risk_free_rate: float = 0.02
) -> Tuple[float, float, float]:
    """
    Calcule les métriques d'un portefeuille.
    
    Parameters
    ----------
    weights : np.ndarray
        Poids des actifs
    annual_returns : pd.Series
        Rendements annuels attendus
    cov_matrix : pd.DataFrame
        Matrice de covariance annualisée
    risk_free_rate : float
        Taux sans risque (défaut: 2%)
        
    Returns
    -------
    Tuple[float, float, float]
        (rendement_attendu, volatilité, ratio_sharpe)
    """
    # Rendement attendu du portefeuille
    portfolio_return = np.dot(weights, annual_returns)
    
    # Volatilité du portefeuille (écart-type)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    # Ratio de Sharpe
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
    
    return portfolio_return, portfolio_volatility, sharpe_ratio


def run_monte_carlo_simulation(
    annual_returns: pd.Series,
    cov_matrix: pd.DataFrame,
    n_simulations: int = 5000,
    risk_free_rate: float = 0.02
) -> SimulationResults:
    """
    Exécute une simulation Monte Carlo pour générer des portefeuilles aléatoires.
    
    Parameters
    ----------
    annual_returns : pd.Series
        Rendements annuels attendus par actif
    cov_matrix : pd.DataFrame
        Matrice de covariance annualisée
    n_simulations : int
        Nombre de simulations à exécuter
    risk_free_rate : float
        Taux sans risque
        
    Returns
    -------
    SimulationResults
        Résultats de toutes les simulations
    """
    n_assets = len(annual_returns)
    
    # Arrays pour stocker les résultats
    all_returns = np.zeros(n_simulations)
    all_volatilities = np.zeros(n_simulations)
    all_sharpe = np.zeros(n_simulations)
    all_weights = np.zeros((n_simulations, n_assets))
    
    # Exécuter les simulations
    for i in range(n_simulations):
        weights = generate_random_weights(n_assets)
        ret, vol, sharpe = calculate_portfolio_metrics(
            weights, annual_returns, cov_matrix, risk_free_rate
        )
        
        all_returns[i] = ret
        all_volatilities[i] = vol
        all_sharpe[i] = sharpe
        all_weights[i] = weights
    
    return SimulationResults(
        returns=all_returns,
        volatilities=all_volatilities,
        sharpe_ratios=all_sharpe,
        all_weights=all_weights
    )


def find_optimal_portfolios(
    simulation_results: SimulationResults,
    annual_returns: pd.Series,
    cov_matrix: pd.DataFrame,
    tickers: list,
    risk_free_rate: float = 0.02
) -> Dict[str, Dict]:
    """
    Identifie les portefeuilles optimaux à partir des simulations.
    
    Parameters
    ----------
    simulation_results : SimulationResults
        Résultats des simulations Monte Carlo
    annual_returns : pd.Series
        Rendements annuels attendus
    cov_matrix : pd.DataFrame
        Matrice de covariance
    tickers : list
        Liste des symboles
    risk_free_rate : float
        Taux sans risque
        
    Returns
    -------
    Dict[str, Dict]
        Dictionnaire contenant les portefeuilles 'max_sharpe' et 'min_volatility'
    """
    results = {}
    
    # Portefeuille à Ratio de Sharpe Maximum
    max_sharpe_idx = np.argmax(simulation_results.sharpe_ratios)
    max_sharpe_weights = simulation_results.all_weights[max_sharpe_idx]
    
    results['max_sharpe'] = {
        'weights': dict(zip(tickers, max_sharpe_weights)),
        'return': simulation_results.returns[max_sharpe_idx],
        'volatility': simulation_results.volatilities[max_sharpe_idx],
        'sharpe': simulation_results.sharpe_ratios[max_sharpe_idx]
    }
    
    # Portefeuille à Variance Minimale
    min_vol_idx = np.argmin(simulation_results.volatilities)
    min_vol_weights = simulation_results.all_weights[min_vol_idx]
    
    results['min_volatility'] = {
        'weights': dict(zip(tickers, min_vol_weights)),
        'return': simulation_results.returns[min_vol_idx],
        'volatility': simulation_results.volatilities[min_vol_idx],
        'sharpe': simulation_results.sharpe_ratios[min_vol_idx]
    }
    
    return results


def optimize_portfolio(
    annual_returns: pd.Series,
    cov_matrix: pd.DataFrame,
    tickers: list,
    n_simulations: int = 5000,
    risk_free_rate: float = 0.02
) -> Tuple[SimulationResults, Dict[str, Dict]]:
    """
    Fonction principale d'optimisation de portefeuille.
    
    Parameters
    ----------
    annual_returns : pd.Series
        Rendements annuels attendus
    cov_matrix : pd.DataFrame
        Matrice de covariance annualisée
    tickers : list
        Liste des symboles boursiers
    n_simulations : int
        Nombre de simulations Monte Carlo
    risk_free_rate : float
        Taux sans risque
        
    Returns
    -------
    Tuple[SimulationResults, Dict[str, Dict]]
        (résultats_simulations, portefeuilles_optimaux)
    """
    # Lancer les simulations
    simulation_results = run_monte_carlo_simulation(
        annual_returns, 
        cov_matrix, 
        n_simulations, 
        risk_free_rate
    )
    
    # Trouver les portefeuilles optimaux
    optimal_portfolios = find_optimal_portfolios(
        simulation_results,
        annual_returns,
        cov_matrix,
        tickers,
        risk_free_rate
    )
    
    return simulation_results, optimal_portfolios

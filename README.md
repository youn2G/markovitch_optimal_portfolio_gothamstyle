# 🚀 Modern Portfolio Optimizer (Markowitz MPT)
<img width="1490" height="763" alt="Capture d’écran 2026-01-30 à 16 11 05" src="https://github.com/user-attachments/assets/47746afb-66a1-4ae3-baf4-eb99f220322f" />
<img width="1474" height="778" alt="Capture d’écran 2026-01-30 à 16 11 19" src="https://github.com/user-attachments/assets/ce23ae38-1b95-41ba-9f54-ad3ba37e373f" />
<img width="1494" height="811" alt="Capture d’écran 2026-01-30 à 16 11 39" src="https://github.com/user-attachments/assets/662fcd1d-16d7-4784-920b-97a5f381b039" />
<img width="1492" height="815" alt="Capture d’écran 2026-01-30 à 16 12 00" src="https://github.com/user-attachments/assets/e3f53e9a-c0d4-4dd6-acf0-fbf8df02d15f" />


This interactive Streamlit application empowers investors to build and visualize optimal asset allocations using the **Modern Portfolio Theory (MPT)** developed by Harry Markowitz. By simulating thousands of portfolios, the tool identifies the most efficient risk-reward trade-offs based on historical market data.

## 🛠 Features

* **Real-time Data Fetching:** Seamless integration with `yfinance` to pull adjusted closing prices for any list of global tickers.
* **Monte Carlo Simulation:** Generates 5,000+ random portfolio weight combinations to map the risk-return spectrum.
* **Optimization Engines:**
    * **Maximum Sharpe Ratio:** Finds the portfolio with the best risk-adjusted return.
    * **Minimum Variance:** Identifies the lowest-risk allocation for conservative investors.
* **Interactive Visualizations:**
    * **Efficient Frontier:** A Plotly-powered scatter plot of volatility vs. expected return.
    * **Portfolio Weights:** Dynamic bar charts showing the exact asset distribution.
    * **Correlation Heatmap:** Visualizes asset relationships to understand diversification benefits.
* **Professional UI:** A clean, "Finance-Pro" interface with real-time error handling and educational insights.

## 📊 Core Mathematical Concepts

The app calculates the expected return $E(R_p)$ and the portfolio variance $\sigma_p^2$ using the following logic:

$$E(R_p) = \sum_{i=1}^{n} w_i E(R_i)$$

$$\sigma_p^2 = w^T \Sigma w$$

Where $w$ represents the vector of weights and $\Sigma$ is the covariance matrix of asset returns.

---

## 💻 Tech Stack

* **Frontend/App:** [Streamlit](https://streamlit.io/)
* **Data Analysis:** `Pandas`, `NumPy`
* **Financial Data:** `yfinance`
* **Visualization:** `Plotly`

## 🚀 Getting Started

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/modern-portfolio-optimizer.git](https://github.com/your-username/modern-portfolio-optimizer.git)
    cd modern-portfolio-optimizer
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app:**
    ```bash
    streamlit run app.py
    ```

## 📖 How to Use

1.  Enter your desired tickers (e.g

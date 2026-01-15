# 🚀 AI-Powered Quantitative Trading System (XGBoost)

A professional-grade, modular backtesting framework that utilizes Machine Learning to generate signals and dynamic risk management to optimize portfolio performance.



## 📊 Performance Architecture
- **Model:** XGBoost Classifier (Gradient Boosted Decision Trees)
- **Validation:** Walk-Forward Analysis (Rolling Window) to eliminate Data Leakage.
- **Risk Management:** Volatility-Targeting Position Sizing (Risk Parity).
- **Infrastucture:** Fully Dockerized for seamless deployment.

## 📈 Key Results (Out-of-Sample)
- **Total Return:** 100.97%
- **Sharpe Ratio:** 0.80
- **Max Drawdown:** -22.65%

## 🛠️ Project Structure
- `/src`: Core logic (Data fetching, ML Models, Backtest Engine).
- `/research`: Strategy optimization and final reporting scripts.
- `/tests`: Unit tests for financial logic validation.
- `Dockerfile`: Containerization for production-ready environments.

## 🚦 Getting Started
1. **Clone:** `git clone https://github.com/YOUR_USERNAME/quant-trading-system.git`
2. **Build Container:** `docker build -t quant-system .`
3. **Run Backtest:** `docker run quant-system`

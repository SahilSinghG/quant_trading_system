import pandas as pd
import numpy as np

class BacktestEngine:
    def __init__(self, initial_capital=10000.0, risk_target=0.15):
        self.initial_capital = initial_capital
        self.risk_target = risk_target # Target 15% annualized volatility

    def run(self, df):
        df = df.copy()
        
        # 1. Calculate Rolling Volatility (20-day realized vol)
        df['volatility'] = df['returns'].rolling(window=20).std() * np.sqrt(252)
        
        # 2. Risk-Adjusted Position Sizing
        # We target a specific risk level. If Vol is high, position is small.
        df['position_size'] = (self.risk_target / df['volatility']).fillna(0)
        df['position_size'] = df['position_size'].clip(0, 1.5) # Max 1.5x leverage
        
        # 3. Strategy Returns (Signal * Position Size * Market Returns)
        df['strat_ret'] = df['signal'].shift(1) * df['position_size'].shift(1) * df['returns']
        
        # 4. Cumulative Results
        df['cum_strategy_return'] = (1 + df['strat_ret'].fillna(0)).cumprod()
        df['portfolio_value'] = self.initial_capital * df['cum_strategy_return']
        
        # 5. Professional Stats
        if df['strat_ret'].std() != 0:
            sharpe = (df['strat_ret'].mean() / df['strat_ret'].std()) * np.sqrt(252)
        else:
            sharpe = 0
            
        rolling_max = df['portfolio_value'].cummax()
        df['drawdown'] = (df['portfolio_value'] / rolling_max) - 1
        
        return df, {
            "final_value": df['portfolio_value'].iloc[-1],
            "total_return_pct": (df['cum_strategy_return'].iloc[-1] - 1) * 100,
            "sharpe_ratio": sharpe,
            "max_drawdown_pct": df['drawdown'].min() * 100
        }
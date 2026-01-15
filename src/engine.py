class BacktestEngine:
    def __init__(self, initial_capital=10000.0, risk_target=0.15, commission=0.001, slippage=0.0005):
        self.initial_capital = initial_capital
        self.risk_target = risk_target
        self.commission = commission  # 0.1% per trade
        self.slippage = slippage      # 0.05% price impact

    def _calculate_stats(self, df):
        # Calculate daily returns
        daily_ret = df['strat_ret'].fillna(0)
        
        # 1. Annualized Return
        total_ret = (df['cum_strategy_return'].iloc[-1] - 1)
        annual_ret = daily_ret.mean() * 252
        
        # 2. Sharpe Ratio
        sharpe = (daily_ret.mean() / daily_ret.std()) * (252**0.5) if daily_ret.std() != 0 else 0
        
        # 3. Sortino Ratio (The Professional Metric)
        downside_rets = daily_ret[daily_ret < 0]
        downside_std = downside_rets.std() * (252**0.5)
        sortino = annual_ret / downside_std if downside_std != 0 else 0
        
        # 4. Max Drawdown
        rolling_max = df['portfolio_value'].cummax()
        drawdown = (df['portfolio_value'] / rolling_max) - 1
        
        return {
            "final_value": df['portfolio_value'].iloc[-1],
            "total_return_pct": total_ret * 100,
            "sharpe_ratio": sharpe,
            "sortino_ratio": sortino,
            "max_drawdown_pct": drawdown.min() * 100
        }
        
        # Add 'sortino_ratio': sortino to your stats dictionary
    def run(self, df):
        df = df.copy()
        
        # 1. Standard Vol-Adjusted Position Sizing
        df['volatility'] = df['returns'].rolling(window=20).std() * (252**0.5)
        df['position_size'] = (self.risk_target / df['volatility']).fillna(0).clip(0, 1.5)
        
        # 2. Raw Strategy Returns (Theoretical)
        raw_strat_ret = df['signal'].shift(1) * df['position_size'].shift(1) * df['returns']
        
        # 3. YOUR NEW CODE: Transaction Costs & Slippage
        commission_pct = 0.001 # 0.1% fee
        slippage_pct = 0.0005  # 0.05% price impact
        
        # Detect every time we flip from 0 to 1 or 1 to 0
        df['trade_count'] = df['signal'].diff().abs().fillna(0)
        
        # Apply the friction
        # We multiply by position_size because trading more shares costs more in fees
        costs = df['trade_count'] * (commission_pct + slippage_pct) * df['position_size']
        df['strat_ret'] = raw_strat_ret - costs
        
        # 4. Cumulative Results
        df['cum_strategy_return'] = (1 + df['strat_ret'].fillna(0)).cumprod()
        df['portfolio_value'] = self.initial_capital * df['cum_strategy_return']
        
        stats = self._calculate_stats(df)
        return df, stats  # <--- THIS IS THE MISSING PIECE# ... rest of the code (stats, etc.)
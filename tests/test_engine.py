import pandas as pd
import numpy as np
import pytest
from src.engine import BacktestEngine

def test_sharpe_ratio_is_calculated():
    # Use 30 days to satisfy the 20-day rolling window requirement
    df = pd.DataFrame({
        'returns': [0.01] * 30,
        'signal': [1] * 30
    })
    
    engine = BacktestEngine(initial_capital=10000)
    _, stats = engine.run(df)
    
    assert stats['sharpe_ratio'] > 0
    assert 'final_value' in stats

def test_drawdown_calculation():
    # Provide 25 days of data so the rolling(20) window can actually compute
    # 24 days of zeros, then a big 50% drop
    returns = [0.0] * 24 + [-0.50]
    df = pd.DataFrame({
        'returns': returns,
        'signal': [1] * 25
    })

    # Set risk_target high so it doesn't shrink our position to zero
    engine = BacktestEngine(initial_capital=10000, risk_target=1.0)
    _, stats = engine.run(df)

    # Max drawdown should now be properly detected as negative
    assert stats['max_drawdown_pct'] < 0
    print(f"Detected Drawdown: {stats['max_drawdown_pct']}%")
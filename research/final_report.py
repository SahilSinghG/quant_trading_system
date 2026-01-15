from src.data_fetcher import MarketDataFetcher
from src.models import QuantModel
from src.engine import BacktestEngine
import pandas as pd

def generate_final_report():
    print("Generating Institutional Grade Report...")
    
    # 1. Setup
    fetcher = MarketDataFetcher()
    data = fetcher.get_data('AAPL', '2018-01-01')
    ai = QuantModel()
    
    # 2. Use our best threshold (0.52)
    results = ai.walk_forward_predict(data)
    results['signal'] = (results['ai_confidence'] > 0.52).astype(int)
    
    # 3. Run Engine with Risk Management
    engine = BacktestEngine(initial_capital=10000, risk_target=0.15)
    final_df, stats = engine.run(results)
    
    # 4. Save to CSV for Excel Analysis (Managers love this)
    final_df.to_csv('aapl_backtest_results.csv')
    
    print("\n" + "="*40)
    print("      QUANT TRADING SYSTEM v1.0")
    print("="*40)
    print(f"Asset:           AAPL (Apple Inc.)")
    print(f"Model:           XGBoost Classifier")
    print(f"Validation:      Walk-Forward (252/21)")
    print("-" * 40)
    print(f"Total Return:    {stats['total_return_pct']:.2f}%")
    print(f"Sharpe Ratio:    {stats['sharpe_ratio']:.2f}")
    print(f"Max Drawdown:    {stats['max_drawdown_pct']:.2f}%")
    print(f"Final Equity:    ${stats['final_value']:.2f}")
    print("="*40)
    print("Report saved to: aapl_backtest_results.csv")

if __name__ == "__main__":
    generate_final_report()
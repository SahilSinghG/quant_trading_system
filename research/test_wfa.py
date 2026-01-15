from src.data_fetcher import MarketDataFetcher
from src.models import QuantModel
from src.engine import BacktestEngine

def run_rigorous_backtest():
    # 1. Fetch deep history (5+ years)
    fetcher = MarketDataFetcher()
    data = fetcher.get_data('AAPL', '2018-01-01')
    
    # 2. Run Walk-Forward Validation
    ai = QuantModel()
    print("Starting Walk-Forward Validation (this may take a minute)...")
    results = ai.walk_forward_predict(data)
    
    # 3. Backtest the Walk-Forward Results
    engine = BacktestEngine(initial_capital=10000)
    final_df, stats = engine.run(results)
    
    print("\n" + "🛡️" * 10)
    print("WALK-FORWARD RESULTS (ROBUST)")
    print(f"Final Value: ${stats['final_value']:.2f}")
    print(f"Total Return: {stats['total_return_pct']:.2f}%")
    print(f"Sharpe Ratio: {stats['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {stats['max_drawdown_pct']:.2f}%")
    print("🛡️" * 10)

if __name__ == "__main__":
    run_rigorous_backtest()
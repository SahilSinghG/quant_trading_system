from src.data_fetcher import MarketDataFetcher
from src.models import QuantModel
from src.engine import BacktestEngine

def run_ai_backtest():
    fetcher = MarketDataFetcher()
    # We fetch a larger range so the AI has enough data to learn
    data = fetcher.get_data('AAPL', '2018-01-01') 
    
    ai = QuantModel()
    ai.train(data)
    
    results_with_ai = ai.predict_signals(data)
    
    engine = BacktestEngine(initial_capital=10000)
    # UNPACKING TWO VALUES HERE:
    final_df, stats = engine.run(results_with_ai)
    
    print("\n" + "🚀" * 10)
    print("AI-POWERED BACKTEST RESULTS")
    print(f"Final Value: ${stats['final_value']:.2f}")
    print(f"Total Return: {stats['total_return_pct']:.2f}%")
    print(f"Sharpe Ratio: {stats['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {stats['max_drawdown_pct']:.2f}%")
    print("🚀" * 10)

if __name__ == "__main__":
    run_ai_backtest()
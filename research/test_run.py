from src.data_fetcher import MarketDataFetcher
from src.strategies import RSIStrategy
from src.engine import BacktestEngine

def main():
    # 1. Fetch Data
    fetcher = MarketDataFetcher()
    data = fetcher.get_data('AAPL', '2023-01-01')
    
    # 2. Apply Strategy
    strategy = RSIStrategy()
    signals_df = strategy.generate_signals(data)
    
    # 3. Run Backtest
    engine = BacktestEngine(initial_capital=10000)
    results, final_val, ret_pct = engine.run(signals_df)
    
    # 4. Final Report
    print("\n" + "="*30)
    print("FINAL BACKTEST REPORT")
    print("="*30)
    print(f"Initial Investment: $10,000")
    print(f"Final Portfolio Value: ${final_val:.2f}")
    print(f"Total Return: {ret_pct:.2f}%")
    
    # Compare with simply holding the stock (Market Return)
    market_ret = (results['cum_market_return'].iloc[-1] - 1) * 100
    print(f"Buy & Hold Return: {market_ret:.2f}%")
    print("="*30)

if __name__ == "__main__":
    main()
from src.data_fetcher import MarketDataFetcher
from src.models import QuantModel
from src.engine import BacktestEngine

def optimize():
    fetcher = MarketDataFetcher()
    data = fetcher.get_data('AAPL', '2018-01-01')
    
    ai = QuantModel()
    results = ai.walk_forward_predict(data)
    
    print("\nOPTIMIZING CONFIDENCE THRESHOLDS...")
    for threshold in [0.52, 0.55, 0.58, 0.60]:
        test_df = results.copy()
        test_df['signal'] = (test_df['ai_confidence'] > threshold).astype(int)
        
        engine = BacktestEngine()
        _, stats = engine.run(test_df)
        
        print(f"Threshold: {threshold} | Return: {stats['total_return_pct']:.1f}% | Sharpe: {stats['sharpe_ratio']:.2f} | DD: {stats['max_drawdown_pct']:.1f}%")

if __name__ == "__main__":
    optimize()
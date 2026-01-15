from src.data_fetcher import MarketDataFetcher
from src.models import QuantModel
from src.engine import BacktestEngine
import pandas as pd

def run_portfolio_backtest():
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'NVDA']
    fetcher = MarketDataFetcher()
    ai = QuantModel()
    engine = BacktestEngine(risk_target=0.10) # Target 10% risk
    
    portfolio_rets = []

    for symbol in symbols:
        data = fetcher.get_data(symbol, '2019-01-01')
        # Use our Walk-Forward logic
        results = ai.walk_forward_predict(data)
        results['signal'] = (results['ai_confidence'] > 0.52).astype(int)
        
        # Get individual strategy returns
        final_df, _ = engine.run(results)
        portfolio_rets.append(final_df['strat_ret'])

    # Aggregate: Equal weight the strategies
    total_strat_ret = pd.concat(portfolio_rets, axis=1).mean(axis=1)
    
    # Calculate Portfolio Performance
    cum_ret = (1 + total_strat_ret.fillna(0)).cumprod()
    print(f"Portfolio Final Return: {(cum_ret.iloc[-1]-1)*100:.2f}%")

if __name__ == "__main__":
    run_portfolio_backtest()
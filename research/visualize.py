import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.data_fetcher import MarketDataFetcher
from src.strategies import RSIStrategy
from src.engine import BacktestEngine

def create_dashboard():
    # 1. Get Data and Run Backtest
    fetcher = MarketDataFetcher()
    data = fetcher.get_data('AAPL', '2023-01-01')
    
    strategy = RSIStrategy()
    signals_df = strategy.generate_signals(data)
    
    engine = BacktestEngine()
    results, _, _ = engine.run(signals_df)
    
    # 2. Create Plotly Subplots
    fig = make_subplots(rows=2, cols=1, 
                        shared_xaxes=True, 
                        vertical_spacing=0.1,
                        subplot_titles=('Equity Curve: Strategy vs Market', 'Portfolio Drawdown (%)'))

    # Top Plot: Equity Curve
    fig.add_trace(go.Scatter(x=results.index, y=results['cum_strategy_return'], name='RSI Strategy'), row=1, col=1)
    fig.add_trace(go.Scatter(x=results.index, y=results['cum_market_return'], name='Market (AAPL)'), row=1, col=1)

    # Bottom Plot: Drawdown
    fig.add_trace(go.Scatter(x=results.index, y=results['drawdown'] * 100, 
                             fill='tozeroy', name='Drawdown', line=dict(color='red')), row=2, col=1)

    fig.update_layout(height=800, title_text="Quant Trading Performance Report")
    fig.show()

if __name__ == "__main__":
    create_dashboard()
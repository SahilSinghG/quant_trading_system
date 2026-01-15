import yfinance as yf
import pandas as pd

class MarketDataFetcher:
    def __init__(self):
        pass

    def get_data(self, symbol, start_date):
        print(f"--- Fetching & Engineering data for {symbol} ---")
        df = yf.download(symbol, start=start_date)
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.columns = [col.lower() for col in df.columns]
        
        # 1. Basic Indicators
        df['returns'] = df['close'].pct_change()
        df['rsi'] = self._add_rsi(df['close'])
        
        # 2. ADDED: Moving Averages (Trend)
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        
        # 3. ADDED: Volatility (Bollinger Bands)
        df['std_20'] = df['close'].rolling(window=20).std()
        df['upper_band'] = df['sma_20'] + (df['std_20'] * 2)
        df['lower_band'] = df['sma_20'] - (df['std_20'] * 2)
        
        # 4. TARGET: What the AI tries to predict 
        # (1 if price goes UP tomorrow, 0 if DOWN)
        df['target'] = (df['close'].shift(-1) > df['close']).astype(int)
        
        return df.dropna()

    def _add_rsi(self, series, period=14):
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
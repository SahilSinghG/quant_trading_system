import pandas as pd
import numpy as np

class RSIStrategy:
    def __init__(self, low_threshold=30, high_threshold=70):
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold

    def generate_signals(self, df):
        """
        Adds a 'signal' column: 
        1 = Buy, -1 = Sell, 0 = Hold
        """
        df = df.copy()
        df['signal'] = 0
        
        # Buy Signal: RSI crosses below 30
        df.loc[df['rsi'] < self.low_threshold, 'signal'] = 1
        
        # Sell Signal: RSI crosses above 70
        df.loc[df['rsi'] > self.high_threshold, 'signal'] = -1
        
        # Calculate daily strategy returns
        # If signal is 1, we get the next day's return
        df['strategy_returns'] = df['signal'].shift(1) * df['returns']
        
        return df
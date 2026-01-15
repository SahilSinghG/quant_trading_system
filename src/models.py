import xgboost as xgb
import pandas as pd
import numpy as np

class QuantModel:
    def __init__(self):
        self.model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=3,
            learning_rate=0.05,
            subsample=0.8,
            random_state=42
        )
        self.features = ['rsi', 'sma_20', 'sma_50', 'std_20', 'upper_band', 'lower_band']

    def walk_forward_predict(self, df, train_window=252, test_window=21):
        """
        train_window: ~1 year of trading days
        test_window: ~1 month (21 days)
        """
        df = df.copy()
        df['signal'] = 0
        df['ai_confidence'] = 0.5 # Neutral start
        
        # We start at the end of the first training window
        for i in range(train_window, len(df) - test_window, test_window):
            # 1. Define the Train and Test segments for this "step"
            train_df = df.iloc[i-train_window : i]
            test_df = df.iloc[i : i+test_window]
            
            # 2. Train on historical window
            X_train = train_df[self.features]
            y_train = train_df['target']
            self.model.fit(X_train, y_train)
            
            # 3. Predict on the "Future" month
            X_test = test_df[self.features]
            probs = self.model.predict_proba(X_test)[:, 1]
            
            # 4. Save results back to the main dataframe
            df.iloc[i : i+test_window, df.columns.get_loc('ai_confidence')] = probs
            
        # Generate final signals based on AI confidence
        df.loc[df['ai_confidence'] > 0.55, 'signal'] = 1
        return df
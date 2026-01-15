import shap
import matplotlib.pyplot as plt
import pandas as pd
from src.data_fetcher import MarketDataFetcher
from src.models import QuantModel

def explain_model():
    print("--- Fetching data for SHAP Analysis ---")
    fetcher = MarketDataFetcher()
    data = fetcher.get_data('AAPL', '2020-01-01')
    
    ai = QuantModel()
    
    # 1. Prepare features and target just like in the model logic
    df = data.copy().dropna()
    X = df[ai.features]
    y = (df['returns'].shift(-1) > 0).astype(int) # Predict if next day is UP
    
    # 2. Manually fit the internal model for explanation
    print("Training internal model for interpretability...")
    ai.model.fit(X, y)
    
    # 3. Use SHAP to explain the model's logic
    explainer = shap.TreeExplainer(ai.model)
    shap_values = explainer.shap_values(X)
    
    # 4. Generate the Plot
    print("Generating SHAP Summary Plot...")
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X, show=False)
    
    # Save it so you can add it to your GitHub README
    plt.savefig('shap_feature_importance.png', bbox_inches='tight')
    print("✅ Success! Plot saved as 'shap_feature_importance.png'")
    plt.show()

if __name__ == "__main__":
    explain_model()
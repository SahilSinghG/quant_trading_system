import shap
import matplotlib.pyplot as plt
from src.data_fetcher import MarketDataFetcher
from src.models import QuantModel

def explain_ai_decisions():
    # 1. Get Data
    fetcher = MarketDataFetcher()
    data = fetcher.get_data('AAPL', '2020-01-01')
    
    # 2. Train Model
    ai = QuantModel()
    ai.train(data) # This trains the internal XGBoost model
    
    # 3. Use SHAP to explain the model
    # We take the trained model inside the QuantModel class
    explainer = shap.TreeExplainer(ai.model)
    X = data[ai.features]
    shap_values = explainer.shap_values(X)
    
    # 4. Plot Feature Importance
    print("Generating SHAP Feature Importance Plot...")
    shap.summary_plot(shap_values, X, plot_type="bar")
    plt.show()

if __name__ == "__main__":
    explain_ai_decisions()
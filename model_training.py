import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
import mlflow
import mlflow.sklearn

# Load the processed dataset
data_path = 'processed_data.csv'  # Update with the actual path
df = pd.read_csv(data_path)

# Split the data into training and testing sets
X = df.drop(columns=['fee_rate'])
y = df['fee_rate']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Calculate evaluation metrics
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Log parameters and metrics with MLflow
mlflow.set_experiment("Fee Rate Prediction")
with mlflow.start_run():
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("random_state", 42)
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("r2", r2)
    mlflow.sklearn.log_model(model, "model")

# Additional Metric: Mean Absolute Percentage Error (MAPE)
mape = mean_absolute_percentage_error(y_test, y_pred)

# Residual Plot
sns.residplot(x=y_test, y=y_pred, lowess=True, line_kws={'color': 'red'})
plt.xlabel("Actual Feerate")
plt.ylabel("Predicted Feerate")
plt.title("Residual Plot")
plt.show()

# Log the new metric
with mlflow.start_run():
    mlflow.log_metric("mape", mape)
    mlflow.log_artifact("residual_plot.png")

print(f"Model training completed with MAE: {mae}, MSE: {mse}, R2: {r2}, MAPE: {mape}")

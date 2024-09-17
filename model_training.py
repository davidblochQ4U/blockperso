"""
MLFlow experiment: https://ccb-data-lightningml-icg-msst-ccb-data-processing-147872.apps.namigitad26d.ecs.dyn.nsroot.net/ccbml/#/experiments/1435
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mlflow.sklearn
from mlflow_config import set_mlflow_env
from mlflow.models.signature import infer_signature
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error

# Load the processed dataset
data_path = 'processed_data.csv'
df = pd.read_csv(data_path)
print(df.shape)

# Split the data into training and testing sets
X = df.drop(columns=['fee_rate'])
y = df['fee_rate']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Set MLflow
os.environ['MLFLOW_TRACKING_USERNAME'] = os.getenv('MLFLOW_TRACKING_USERNAME')
os.environ['MLFLOW_TRACKING_PASSWORD'] = os.getenv('MLFLOW_TRACKING_PASSWORD')
set_mlflow_env()
mlflow.end_run()
mlflow.autolog()

# Initialize and train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Calculate evaluation metrics
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred)

print(f"Model training completed with MAE: {mae}, MSE: {mse}, R2: {r2}, MAPE: {mape}")

# Residual Plot
residual_plot = sns.residplot(x=y_test, y=y_pred, lowess=True, line_kws={'color': 'red'})
fig = residual_plot.get_figure()
fig.savefig("residual_plot.png")
plt.xlabel("Actual Fee rate")
plt.ylabel("Predicted Fee rate")
plt.title("Residual Plot")
plt.show()

# Log parameters and metrics with MLflow
signature = infer_signature(X_train, model.predict(X_train))
input_example = X_train.head(5)
mlflow.set_experiment("coinxpert")

with mlflow.start_run():
    mlflow.log_param(key="n_estimators", value=100)
    mlflow.log_param(key="random_state", value=42)
    mlflow.log_metric(key="mae", value=mae)
    mlflow.log_metric(key="mse", value=mse)
    mlflow.log_metric(key="r2", value=r2)
    mlflow.sklearn.log_model(model, "model", signature=signature, input_example=input_example)
    mlflow.log_metric(key="mape", value=mape)
    mlflow.log_artifact("residual_plot.png")


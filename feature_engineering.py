import pandas as pd
import numpy as np
import os

# Load the dataset
file_path = 'transactions_500k.csv'  # Update with your actual path
df = pd.read_csv(file_path)

# Feature Engineering

# Calculate fee rate (fee per vbyte)
df['fee_rate'] = df['fee'] / df['virtual_size']

# Convert block timestamp to datetime
df['block_timestamp'] = pd.to_datetime(df['block_timestamp'])

# Extract relevant time-based features
df['year'] = df['block_timestamp'].dt.year
df['month'] = df['block_timestamp'].dt.month
df['day'] = df['block_timestamp'].dt.day
df['hour'] = df['block_timestamp'].dt.hour

# Handle missing values (if any)
df.fillna(0, inplace=True)

# Select relevant columns for the model
features = [
    'size', 'virtual_size', 'input_count', 'output_count',
    'input_value', 'output_value', 'year', 'month', 'day', 'hour'
]

# Target variable
target = 'fee_rate'

# Prepare data for modeling
X = df[features]
y = df[target]

# Save the processed dataset
processed_file_path = 'processed_data.csv'  # Update with your desired path
columns = features + [target]
df[columns].to_csv(processed_file_path, index=False)

print("Feature engineering completed. Processed data saved at:", processed_file_path)

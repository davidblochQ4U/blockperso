from google.cloud import bigquery
import pandas as pd

# Initialize BigQuery client
client = bigquery.Client()

# Query
query = """
SELECT *
FROM `bigquery-public-data.crypto_bitcoin.transactions`
LIMIT 10000000
"""

# Execute query and convert to dataframe
query_job = client.query(query)
df = query_job.to_dataframe()

# Save to CSV
df.to_csv('transactions_50M.csv', index=False)
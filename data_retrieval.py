import pandas as pd
from google.cloud import bigquery


def retrieve_data (query: str, output_csv: str):
    client = bigquery.Client()
    query_job = client.query(query)
    results = query_job.result()

    # Convert results to DataFrame and save as CSV
    df = results.to_dataframe()
    df.to_csv(output_csv, index=False)
    print(f"Data saved to {output_csv}")


if __name__ == "__main__":
    query = """
    SELECT *
    FROM `bigquery-public-data.crypto_bitcoin.transactions`
    LIMIT 500000
    """
    output_csv = "transactions.csv"
    retrieve_data(query, output_csv)

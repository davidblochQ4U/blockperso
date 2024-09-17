"""
Confluence page: https://cedt-confluence.nam.nsroot.net/confluence/display/C147873A/Lightning+ML%3A+MLflow+Docs+for+python+3.7+version
"""

import requests, os, mlflow
from dotenv import load_dotenv

load_dotenv()

os.environ['MLFLOW_TRACKING_USERNAME'] = os.getenv('MLFLOW_TRACKING_USERNAME')
os.environ['MLFLOW_TRACKING_PASSWORD'] = os.getenv('MLFLOW_TRACKING_PASSWORD')

# Function to set MLflow environment
def set_mlflow_env():
    url = f'https://ccb-mlopservice-icg-msst-ccb-data-processing-147873.apps.namigcgtad50d.ecs.dyn.nsroot.net/mlconfig'
    cert_path = 'cert.pem'
    res = requests.get(url, verify=cert_path)
    print(res)

    if res.ok and res.status_code == 200:
        response = res.json()

        os.environ['MLFLOW_S3_ENDPOINT_URL'] = response['MLFLOW_S3_ENDPOINT_URL']
        os.environ['AWS_ACCESS_KEY_ID'] = response['AWS_ACCESS_KEY_ID']
        os.environ['AWS_SECRET_ACCESS_KEY'] = response['AWS_SECRET_ACCESS_KEY']
        os.environ['MLFLOW_S3_IGNORE_TLS'] = "False"
        os.environ['MLFLOW_TRACKING_INSECURE_TLS'] = "False"
        os.environ['AWS_CA_BUNDLE'] = cert_path
        os.environ['MLFLOW_TRACKING_SERVER_CERT_PATH'] = cert_path
        uri = 'https://ccb-data-lightningml-icg-msst-ccb-data-processing-147873.apps.namigcgtad26d.ecs.dyn.nsroot.net'
        mlflow.set_tracking_uri(uri)
        print("MLFlow env set successfully")
        return uri

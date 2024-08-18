# CoinXpert: AI/ML Dynamic Fee Prediction

## Overview

This branch focuses on developing a machine learning model for dynamic fee prediction within the CoinXpert API. The goal is to optimize transaction fees based on current network conditions, leveraging historical data and advanced algorithms to provide real-time fee estimates.

## Features

- **Data Retrieval**: Integration with data sources such as blockchain-etl/bitcoin-etl using Google Cloud BigQuery to build a robust dataset for model training.
- **Feature Engineering**: Extract and preprocess features relevant to transaction fees.
- **Model Training**: Implement and train machine learning models for fee prediction.
- **Hyperparameter Tuning**: Optimize model performance through systematic tuning.
- **Monitoring**: Continuous monitoring and evaluation of model performance using tools like MLflow and Prometheus.
- **API Integration**: Seamless integration of the ML model with the existing CoinXpert API.

## Getting Started

### Prerequisites

- Python 3.8+
- Sklearn (for ML models)
- FastAPI
- MLflow
- Prometheus/Grafana

### Installation

Clone the repository and switch to the `ml-fee-prediction` branch:

```bash
git clone https://cedt-icg-bitbucket.nam.nsroot.net/bitbucket/projects/E4-COINXPERT-175873/repos/coinxpert/browse
cd coinxpert
git checkout ai-ml-fee-prediction
```
Install the required dependencies:
```bash
pip install -r requirements.txt
```
## Running the Project

- Data Retrieval: Fetch the required data using the provided scripts in the data directory.
- Model Training: Execute the train_model.py script to train the model on the retrieved dataset.
- API Integration: Use the main.py script to run the CoinXpert API with the integrated ML model.

## Contributing
We welcome contributions to improve the fee prediction model or integrate new features.

## Contact
For any inquiries or issues, please contact the maintainer.

Maintainer: David Bloch (db48046)



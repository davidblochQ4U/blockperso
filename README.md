# CoinXpert - Transaction Fees Optimizer

CoinXpert is an API designed to optimize transaction fees for UTXOs based systems like Bitcoin through advanced Coin Selection. It leverages various coin selection algorithms to minimize transaction fees while ensuring transactions are processed efficiently.

## Features

- **UTXO Selection Algorithms**: Implements multiple strategies for UTXO selection to optimize transaction fees.
- **FastAPI Backend**: Utilizes FastAPI for efficient backend processing and API management.
- **Dynamic Frontend**: Offers a dynamic and interactive web interface for simulating transactions and visualizing the impact of different coin selection algorithms on transaction fees.
- **Transaction Simulation**: Enables users to input custom UTXOs and target transaction amounts for simulation.
- **Fee Calculation**: Calculates transaction fees based on selected UTXOs and provides comparisons between different selection algorithms.

## Installation

To set up CoinXpert on your local machine, follow these steps:

1. Ensure you have Python 3.9+ installed on your system.
2. Clone this repository to your local machine.
   ```sh
   git clone ssh://git@cedt-icg-bitbucketcli.nam.nsroot.net:7999/e4-coinxpert-175873/coinxpert.git
   cd coinxpert
   ```
3. Install the required Python packages by running:
   ```sh
   pip install -r requirements.txt
   ```

## Requirements

Refer to `requirements.txt` for a complete list of dependencies.

## Usage

1. Start the FastAPI server by executing:
   ```sh
   uvicorn app.main:app --reload
   ```
2. Open a web browser and navigate to `http://127.0.0.1:8000` to access the CoinXpert interface.
3. Follow the on-screen instructions to simulate transactions and view the results of different coin selection algorithms.

## Project Structure

```plaintext
coinxpert/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── demo.py
│   │   ├── ml_model.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── db.py
│   │   ├── logging.py
│   │   ├── monitoring.py
│   │   ├── security.py
│   ├── data/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── ml_models.py
│   │   ├── utxo_models.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── coin_selection_algorithms.py
│   │   ├── fee_calculator.py
│   │   ├── ml_model_service.py
│   │   ├── transaction_simulation.py
├── helm/
│   ├── Chart.yaml
│   ├── dev-values.yaml
│   ├── templates/
│   │   ├── deploymentconfig.yaml
│   │   ├── route.yaml
│   │   ├── service.yaml
│   ├── values.yaml
├── tests/
│   ├── __init__.py
│   ├── test_coin_selection_algorithms.py
│   ├── test_fee_calculator.py
│   ├── test_main.py
│   ├── test_ml_model_service.py
│   ├── test_transaction_simulation.py
│   ├── test_utxo_models.py
├── webapp_demo/
│   ├── app.py
│   ├── requirements.txt
│   ├── static/
│   │   ├── Dockerfile
│   │   ├── script.js
│   │   ├── style.css
│   │   ├── images/
│   │       ├── btc_wallet.png
│   │       ├── coinxpert_logo.png
│   ├── templates/
│       ├── demo.html
├── .dockerignore
├── .gitignore
├── Dockerfile
├── pipeline.yaml
├── README.md
├── requirement.txt
├── requirements_tests.txt
```

## Contributing

Contributions to CoinXpert are welcome.

## Contact

For any inquiries or issues, please contact the maintainer.

Maintainer: David Bloch (db48046)
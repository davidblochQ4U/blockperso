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
3. Install the required Python packages by running `pip install -r requirements.txt` in your terminal.

## Requirements

Refer to `requirements.txt` for a complete list of dependencies.

## Usage

1. Start the FastAPI server by executing `uvicorn main:app --reload` in your terminal.
2. Open a web browser and navigate to `http://127.0.0.1:8000` to access the CoinXpert interface.
3. Follow the on-screen instructions to simulate transactions and view the results of different coin selection algorithms.

## Contributing

Contributions to CoinXpert are welcome.
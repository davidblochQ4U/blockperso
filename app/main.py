"""
Main module for CoinXpert FastAPI application.

This module initializes the FastAPI app, configures routing for static files and endpoints, 
and defines the core business logic for selecting UTXOs based on various coin selection algorithms.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers import demo, ml_model
import os

from app.services.coin_selection_algorithms import (
    bitcoin_core_coin_selection,
    greedy_coin_selection,
    genetic_coin_selection,
)
from app.models.utxo_models import UTXO, TransactionRequest
from app.services.fee_calculator import calculate_transaction_fee


app = FastAPI()

# Mount static files directory
static_files_path = os.path.join(os.path.dirname(__file__), "../webapp_demo/static")
app.mount("/static", StaticFiles(directory=static_files_path), name="static")

# Configure template directory for HTML responses
templates_path = os.path.join(os.path.dirname(__file__), "../webapp_demo/templates")
templates = Jinja2Templates(directory=templates_path)

app.include_router(demo.router, prefix="/demo", tags=["demo"])
app.include_router(ml_model.router, prefix="/ml_model", tags=["ml_model"])

@app.post("/select_utxos/")
async def select_utxos(request: TransactionRequest) -> dict:
    """
    Endpoint for selecting UTXOs based on the given request.

    Parameters:
    - request (TransactionRequest): The request object containing UTXOs and target amount.

    Returns:
    - dict: A dictionary containing selected UTXOs, change UTXO, and calculated fees.
    """
    utxos = [UTXO(utxo.value) for utxo in request.utxos]

    try:
        selected_utxos_core, change_utxo_core = bitcoin_core_coin_selection(utxos, request.target)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        selected_utxos_coinxpert, change_utxo_coinxpert = genetic_coin_selection(utxos, request.target)
    except Exception as e:
        print(e)
        selected_utxos_coinxpert, change_utxo_coinxpert = greedy_coin_selection(utxos, request.target)

    # Assuming one output for the recipient and one for change
    nb_output = lambda x: 2 if x else 1
    nb_output_core, nb_output_coinxpert = nb_output(change_utxo_core), nb_output(change_utxo_coinxpert)
    fee_btc_core = calculate_transaction_fee(len(selected_utxos_core), nb_output_core)
    fee_coinxpert = calculate_transaction_fee(len(selected_utxos_coinxpert), nb_output_coinxpert)

    # Convert selected UTXOs and change to a serializable format
    response = {
        "selected_utxos_core": [{'value': utxo.value} for utxo in selected_utxos_core],
        "change_utxo_core": {'value': change_utxo_core.value} if change_utxo_core else None,
        "selected_utxos_coinxpert": [{'value': utxo.value} for utxo in selected_utxos_coinxpert],
        "change_utxo_coinxpert": {'value': change_utxo_coinxpert.value} if change_utxo_coinxpert else None,
        "fee_btc_core": fee_btc_core,
        "fee_coinxpert": fee_coinxpert
    }

    print('response:', response)
    return response


@app.get("/", response_class=HTMLResponse)
async def show_demo(request: Request):
    """
   Endpoint to serve the main HTML demo page.

   Parameters:
   - request (Request): The request object.

   Returns:
   - HTMLResponse: The main demo HTML page response.
   """
    context = {"request": request}
    return templates.TemplateResponse("demo.html", context)
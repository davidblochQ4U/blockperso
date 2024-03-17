from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from coin_selection_algorithms import bitcoin_core_coin_selection, greedy_coin_selection, genetic_coin_selection
from utxo_models import UTXO, TransactionRequest
from fee_calculator import calculate_transaction_fee

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.post("/select_utxos/")
async def select_utxos(request: TransactionRequest):
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
    context = {"request": request}
    return templates.TemplateResponse("demo.html", context)
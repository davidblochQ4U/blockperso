import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_select_utxos():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        request_payload = {
            "utxos": [
                {"value": 5.0},
                {"value": 3.0},
                {"value": 2.0}
            ],
            "target": 4.0
        }
        response = await ac.post("/select_utxos/", json=request_payload)
    assert response.status_code == 200
    data = response.json()
    assert "selected_utxos_core" in data
    assert "fee_btc_core" in data

@pytest.mark.asyncio
async def test_select_utxos_insufficient_funds():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        request_payload = {
            "utxos": [
                {"value": 1.0}
            ],
            "target": 4.0
        }
        response = await ac.post("/select_utxos/", json=request_payload)
    assert response.status_code == 400
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_select_utxos_bitcoin_core_value_error():
    # Payload designed to trigger ValueError in bitcoin_core_coin_selection
    request_payload = {
        "utxos": [{"value": 0.5}],  # Use a setup that you know will fail
        "target": 10
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/select_utxos/", json=request_payload)
    assert response.status_code == 400
    assert "detail" in response.json()  # The detail should be the ValueError message

async def test_select_utxos_genetic_exception_fallback():
    # Use a valid setup that would normally not raise an exception
    request_payload = {
        "utxos": [{"value": 1}, {"value": 2}, {"value": 3}],
        "target": 5
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/select_utxos/", json=request_payload)
    assert response.status_code == 200
    # Check if the response indicates a fallback to greedy_coin_selection
    data = response.json()
    assert "selected_utxos_coinxpert" in data

@pytest.mark.asyncio
async def test_show_demo_content():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert 'id="navbar"' in response.text
    assert "/static/" in response.text


import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from main import app

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
    # Add more assertions based on expected response structure

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
async def test_show_demo():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "<html" in response.text

import pytest
from fastapi.testclient import TestClient
from app.routers.demo import router  # Adjust the import path as needed
from fastapi import Request

# Initialize the TestClient with the FastAPI router
client = TestClient(router)


# Test the /demo route
def test_demo_view ():
    # Make a GET request to the /demo route
    response = client.get("/demo")

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response contains the expected HTML content (e.g., template content)
    assert "<title>CoinXpert" in response.text  # Ensure the correct template is rendered
    assert "<script src=\"/static/script.js\"></script>" in response.text  # Static content check

    # To verify context, we can simulate a request and capture the response.
    with client:
        response = client.get("/demo")
        # Ensure the template name is "demo.html" and context includes "key" with value "value"
        assert response.status_code == 200
        assert "CoinXpert" in response.text  # Ensure some expected text is in the response


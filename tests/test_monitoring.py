import pytest
from unittest.mock import patch, MagicMock
from app.utils.monitoring import start_monitoring_server, track_request_duration, process_request,REQUEST_COUNT, REQUEST_LATENCY
from prometheus_client import Counter, Histogram

# Test that the Prometheus server starts correctly
@patch("app.utils.monitoring.start_http_server")
def test_start_monitoring_server(mock_start_http_server):
    # Call the function
    start_monitoring_server(port=8080)

    # Check that start_http_server was called with the correct port
    mock_start_http_server.assert_called_once_with(8080)

# Test the track_request_duration decorator
def test_track_request_duration():
    # Mock a function to simulate request processing
    mock_func = MagicMock()
    mock_func.__name__ = "mock_func"  # Required for decorators

    # Apply the track_request_duration decorator
    decorated_func = track_request_duration(mock_func)

    # Call the decorated function
    decorated_func()

    # Assert that the original function was called
    mock_func.assert_called_once()

    # Check if the metrics were updated
    assert REQUEST_COUNT._value.get() == 1
    assert len(REQUEST_LATENCY.collect()) > 0

# Test the process_request function using the decorator
@patch("app.utils.monitoring.time.sleep", return_value=None)
def test_process_request(mock_sleep):
    # Call the process_request function
    process_request()

    # Check that time.sleep was called with the correct duration
    mock_sleep.assert_called_once_with(2)

    # Check that the metrics were updated
    assert REQUEST_COUNT._value.get() == 2.0
    assert len(REQUEST_LATENCY.collect()) > 0

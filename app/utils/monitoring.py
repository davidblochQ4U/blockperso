from prometheus_client import Counter, Histogram, start_http_server
import time

# Metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total number of requests')
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Histogram for the duration in seconds', buckets=(0.1, 0.5, 1, 2, 5, 10))

def start_monitoring_server(port=8001):
    """Start a Prometheus metrics server."""
    start_http_server(port)
    print(f"Monitoring server started at http://localhost:{port}")

def track_request_duration(func):
    """Decorator to track request duration."""
    def wrapper(*args, **kwargs):
        with REQUEST_LATENCY.time():
            result = func(*args, **kwargs)
        REQUEST_COUNT.inc()
        return result
    return wrapper

# Example usage
@track_request_duration
def process_request():
    """A dummy function to simulate request processing."""
    time.sleep(2)

if __name__ == "__main__":
    start_monitoring_server()
    while True:
        process_request()


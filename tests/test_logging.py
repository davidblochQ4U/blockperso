import logging
import os
import pytest
from app.utils.logging import setup_logger

# Test if the logger writes a log file correctly
def test_logger_writes_file():
    log_file = 'test_app.log'

    # Ensure log file doesn't exist before the test
    if os.path.exists(log_file):
        os.remove(log_file)

    # Create logger and write a log message
    logger = setup_logger('test_logger', log_file)
    logger.info('Test log message')

    # Check if the log file is created and contains the log message
    assert os.path.exists(log_file)
    with open(log_file, 'r') as f:
        log_content = f.read()
        assert 'Test log message' in log_content

    # Close the logger handlers to release the file
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)

    # Clean up by removing the log file after the test
    os.remove(log_file)

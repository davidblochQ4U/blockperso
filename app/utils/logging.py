import logging

def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup a logger"""
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# Usage:
app_logger = setup_logger('app_logger', 'app.log')
app_logger.info('Logger is set up.')
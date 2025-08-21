#Creating a logging system 

import os
import sys
import logging
from datetime import datetime
import traceback

def setup_logger():
    # Ensure artifacts/logs directory exists
    log_dir = os.path.join("artifacts", "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Log file name with current date
    log_filename = datetime.now().strftime("%Y-%m-%d") + "_log.txt"
    log_filepath = os.path.join(log_dir, log_filename)

    # Logging format
    log_format = (
        "%(asctime)s | [%(levelname)s] | "
        "%(filename)s:%(funcName)s:%(lineno)d | "
        "%(message)s"
    )

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_filepath, mode="a"),  # logs to file
            logging.StreamHandler(sys.stdout)             # logs to console
        ]
    )

    logger = logging.getLogger()

    # Custom exception hook for errors (prints function, line, file)
    def exception_hook(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.error(
            "Uncaught exception",
            exc_info=(exc_type, exc_value, exc_traceback)
        )
        traceback.print_exception(exc_type, exc_value, exc_traceback)

    sys.excepthook = exception_hook

    return logger

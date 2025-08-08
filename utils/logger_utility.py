import logging
import os
from datetime import datetime

class LoggerUtility:
    def __init__(self, log_dir="logs", log_level=logging.INFO):
        """
        Initialize the LoggerUtility.
        Creates a log directory if it doesn't exist and sets up file and stream handlers.
        Each log file is named with a timestamp to ensure uniqueness per execution.
        """
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"test_log_{timestamp}.log")
        self.logger = logging.getLogger(f"Logger_{timestamp}")
        self.logger.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s  | %(funcName)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def info(self, message):
        """
        Log an info level message.
        Returns self for method chaining.
        """
        self.logger.info(message)
        return self

    def warning(self, message):
        """
        Log a warning level message.
        Returns self for method chaining.
        """
        self.logger.warning(message)
        return self

    def error(self, message):
        """
        Log an error level message.
        Returns self for method chaining.
        """
        self.logger.error(message)
        return self

    def debug(self, message):
        """
        Log a debug level message.
        Returns self for method chaining.
        """
        self.logger.debug(message)
        return self

    def critical(self, message):
        """
        Log a critical level message.
        Returns self for method chaining.
        """
        self.logger.critical(message)
        return self

# Mechanism to invoke logger at the start and end of execution
logger = LoggerUtility()

def pytest_sessionstart(session):
    """
    Pytest hook: Called after the Session object has been created and before performing collection and entering the run test loop.
    Logs the start of the test execution.
    """
    logger.info("Test execution started.")

def pytest_sessionfinish(session, exitstatus):
    """
    Pytest hook: Called after whole test run finished, right before returning the exit status to the system.
    Logs the end of the test execution.
    """
    logger.info("Test execution finished.")
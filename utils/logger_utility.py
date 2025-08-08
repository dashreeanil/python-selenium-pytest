import logging
import os
import inspect
from datetime import datetime

class LoggerUtility:
    def __init__(self, log_dir="logs", log_level=logging.INFO):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"test_log_{timestamp}.log")
        self.logger = logging.getLogger(f"Logger_{timestamp}")
        self.logger.setLevel(log_level)

        # Use 'caller' instead of 'funcName'
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(caller)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def _log(self, level, message):
        # Safely extract caller function name
        caller_name = inspect.stack()[2].function
        self.logger.log(level, message, extra={'caller': caller_name})

    def info(self, message):
        self._log(logging.INFO, message)
        return self

    def warning(self, message):
        self._log(logging.WARNING, message)
        return self

    def error(self, message):
        self._log(logging.ERROR, message)
        return self

    def debug(self, message):
        self._log(logging.DEBUG, message)
        return self

    def critical(self, message):
        self._log(logging.CRITICAL, message)
        return self
    
logger = LoggerUtility()
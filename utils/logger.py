# utils/logger.py
import logging
import sys
from pathlib import Path

# Create logs directory
Path("logs").mkdir(exist_ok=True)


def setup_logger(name: str = "baro_api") -> logging.Logger:
    """
    Setup structured logger with file and console output
    
    WHY: Professional apps need proper logging for debugging
    HOW: Python's logging module with custom formatting
    WHEN: Called once at app startup
    """
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate logs if called multiple times
    if logger.handlers:
        return logger
    
    # Console handler (terminal output)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # File handler (save to file)
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setLevel(logging.INFO)
    
    # Custom format: timestamp | level | message
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


# Create global logger instance
logger = setup_logger()

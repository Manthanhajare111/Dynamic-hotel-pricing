import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Log file name with current date
log_filename = datetime.now().strftime("hotel_pricing_%Y-%m-%d.log")
log_filepath = os.path.join(LOG_DIR, log_filename)

# Configure logging to overwrite the log file each run (mode='w')
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(log_filepath, mode='w', encoding='utf-8'),  # mode='w' overwrites file
        logging.StreamHandler()
    ]
)

def get_logger(name):
    """
    Returns a logger with the specified name.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger


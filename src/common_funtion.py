import os
import pandas as pd
from src.logger import get_logger 
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"YAML file {file_path} read successfully.")
            return config
    except Exception as e:
        logger.error(f"Error reading YAML file {file_path}: {e}")
        raise CustomException(f"Error reading YAML file: {e}")
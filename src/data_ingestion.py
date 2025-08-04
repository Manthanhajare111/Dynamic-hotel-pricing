import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
import sys

from common_funtion import read_yaml


logger = get_logger(__name__)

class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["file_path"]
        self.train_test_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info("DataIngestion class initialized with configuration: %s", self.config)

    def download_csv_from_gcs(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)

            # Check if file exists locally
            if not os.path.exists(RAW_FILE_PATH):
                if not blob.exists():
                    logger.error(f"File {self.file_name} does not exist in bucket {self.bucket_name}.")
                    raise CustomException(f"File {self.file_name} does not exist in bucket {self.bucket_name}.")
                blob.download_to_filename(RAW_FILE_PATH)
                logger.info(f"File {self.file_name} downloaded from GCS bucket {self.bucket_name} to {RAW_FILE_PATH}.")
            else:
                logger.info(f"File {RAW_FILE_PATH} already exists locally. Skipping download.")

            return RAW_FILE_PATH
        except Exception as e:
            logger.error(f"Error downloading file from GCS: {e}")
            raise CustomException(f"Error downloading file from GCS: {e}") 
        
    def split_data(self):
        try:
            df = pd.read_csv(RAW_FILE_PATH)
            logger.info(f"Data loaded from {RAW_FILE_PATH} with shape {df.shape}.")

            train_df, test_df = train_test_split(df, test_size=1-self.train_test_ratio, random_state=42)
            logger.info(f"Data split into train and test sets with shapes {train_df.shape} and {test_df.shape} respectively.")

            train_df.to_csv(TRAIN_FILE_PATH, index=False)
            test_df.to_csv(TEST_FILE_PATH, index=False)

            logger.info(f"Train data saved to {TRAIN_FILE_PATH} and test data saved to {TEST_FILE_PATH}.")
        except Exception as e:
            logger.error(f"Error during data splitting: {e}")
            raise CustomException(f"Error during data splitting: {e}")
        
    def run(self):
        try:
            self.download_csv_from_gcs()
            self.split_data()
            logger.info("Data ingestion and splitting completed successfully.")
        except CustomException as e:
            logger.error(f"Data ingestion failed: {e}")
            raise e
        finally:
            logger.info("DataIngestion run method completed.")

if __name__ == "__main__":
    config = read_yaml(CONFIG_PATH)
    data_ingestion = DataIngestion(config)
    data_ingestion.run()
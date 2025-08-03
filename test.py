from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

def divide_numbers(a, b):
    try:
        result =  a / b
        logger.info(f"Division result: {result}")
        return result
    except ZeroDivisionError as e:
        logger.error("Attempted to divide by zero.")
        raise CustomException("Division by zero is not allowed.", sys) from e
    except Exception as e:
        raise CustomException("An unexpected error occurred during division.", sys) from e
    
if __name__ == "__main__":
    try:
        logger.info("Starting division operation.")
        divide_numbers(10, 0)
    except CustomException as ce:
        logger.error(str(ce))
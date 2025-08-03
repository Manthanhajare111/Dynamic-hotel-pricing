import sys

class CustomException(Exception):
    """
    Custom exception class for the hotel pricing project.
    Optionally accepts an error message and the original exception.
    """
    def __init__(self, error_message, errors=None):
        super().__init__(error_message)
        self.error_message = error_message  # Store error_message as an attribute
        self.errors = self.get_details(error_message, errors) if errors else None

    @staticmethod
    def get_details(error_message, error_details: sys):
        _, _, exc_tb = error_details.exc_info()
        if exc_tb is not None:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
            function_name = exc_tb.tb_frame.f_code.co_name
            return f"Error occurred in file '{file_name}' at line {line_number} in function '{function_name}': {error_message}"
        else:
            return f"Error: {error_message}"

    def __str__(self):
        if self.errors:
            return self.errors
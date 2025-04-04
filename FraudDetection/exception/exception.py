import sys
from FraudDetection.logging import logger
class FraudDetectionException(Exception):
    def __init__(self, error_message: Exception, error_details: sys):
        super().__init__(error_message)
        self.error_message = FraudDetectionException.get_error_message(error_message=error_message,
                                                                        error_details=error_details)

    @staticmethod
    def get_error_message(error_message: Exception, error_details: sys) -> str:
        _, _, exec_tb = error_details.exc_info()
        line_number = exec_tb.tb_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename
        error_message = f"Error occurred in script: [{file_name}] at line number: [{line_number}] error message: [{error_message}]"
        return error_message

    def __str__(self):
        return self.error_message
    
if __name__ == "__main__":
    try:
        logger.logging.info("Entered the try block")
        a = 1 / 0
    except Exception as e:
        raise FraudDetectionException(e, sys)


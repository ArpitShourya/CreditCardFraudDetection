from FraudDetection.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_TRAINER_FILENAME
from FraudDetection.exception.exception import FraudDetectionException
from FraudDetection.logging.logger import logging
import mlflow.pyfunc
import os,sys,numpy as np

class FraudDetectionModel(mlflow.pyfunc.PythonModel):
    def __init__(self,model):
        try:
            self.model=model
        except Exception as e:
            raise FraudDetectionException(e,sys)
        
    def predict(self,context):
        try:
            xgb_model = self.model["xgb_model"]
            iso_forest = self.model["iso_forest"]
            y_pred_xgb = xgb_model.predict(context)  # XGBoost probability for fraud
            y_pred_iso = iso_forest.predict(context) # Isolation Forest predictions

            # Convert Isolation Forest output (-1 = fraud, 1 = normal) to (1 = fraud, 0 = normal)
            y_pred_iso = np.where(y_pred_iso == -1, 1, 0)

            # Compute final ensemble prediction
            final_pred = np.where((y_pred_xgb + y_pred_iso) > 0, 1, 0)
            return final_pred
        except Exception as e:
            raise FraudDetectionException(e,sys)
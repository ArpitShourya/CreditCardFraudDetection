import pandas as pd,sys
from FraudDetection.components.kafka_producer import KafkaProducerService
from FraudDetection.utils.main_utils.utils import load_object
from FraudDetection.utils.ml_utils.model.estimator import FraudDetectionModel
from FraudDetection.exception.exception import FraudDetectionException
from FraudDetection.logging.logger import logging

class BatchPredictionPipeline:
    def __init__(self,df:pd.DataFrame):
        self.df=df
    def start_batch_prediction(self):
        try:
            rows_to_scale=['Time','Amount']
            preprocessor=load_object("final_models/preprocessing.pkl")
            model=load_object("final_models/Model.pkl")
            fraud_detection_model=FraudDetectionModel(model=model)
            self.df[rows_to_scale]=preprocessor.transform(self.df[rows_to_scale])
            y_pred=fraud_detection_model.predict(self.df)
            self.df['predicted column']=y_pred
            self.df.to_csv("Prediction_Data/output.csv")
            kfpservice=KafkaProducerService()
            kfpservice.stream_dataframe(self.df)

        except Exception as e:
            raise FraudDetectionException(e,sys)
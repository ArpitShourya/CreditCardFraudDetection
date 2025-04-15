from kafka import KafkaConsumer
import json,pandas as pd
import numpy as np
import joblib,sys
from FraudDetection.exception.exception import FraudDetectionException
from FraudDetection.logging.logger import logging
from FraudDetection.utils.ml_utils.model.estimator import FraudDetectionModel
from FraudDetection.entity.config_entity import ModelTrainerConfig,TrainingPipelineConfig,DataTransformationConfig

class KafkaConsumerService:
    def __init__(self, bootstrap_servers="localhost:9092", topic="credit_card_transactions"):
        try:
            self.trainingpipelineconfig=TrainingPipelineConfig()
            self.columns = [
                "Time", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10",
                "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18", "V19", "V20",
                "V21", "V22", "V23", "V24", "V25", "V26", "V27", "V28", "Amount"
            ]
            self.model_trainer_config=ModelTrainerConfig(training_pipeline_config=self.trainingpipelineconfig)
            self.data_transformation_config=DataTransformationConfig(training_pipeline_config=self.trainingpipelineconfig)
            self.consumer = KafkaConsumer(
                topic,
                bootstrap_servers=bootstrap_servers,
                value_deserializer=lambda x: json.loads(x.decode("utf-8"))
            )
            self.model = joblib.load(self.model_trainer_config.trained_model_file_path)
            self.preprocessor=joblib.load(self.data_transformation_config.preprocess_model_file_path)
            self.fraud_detection_model=FraudDetectionModel(self.model)
        except Exception as e:
            raise FraudDetectionException(e,sys)
        

    def detect_fraud(self):
        print("Listening for transactions...")
        num_fraud=0
        num_not_fraud=0
        for message in self.consumer:
            transaction = message.value  # dictionary with "time", "amount", "features", etc.

            # Step 1: Create a dummy DataFrame to scale "time" and "amount"
            temp_df = pd.DataFrame([{"Time": transaction["Time"], "Amount": transaction["Amount"]}])

            # Step 2: Scale them using pre-fitted StandardScaler
            scaled = self.preprocessor.transform(temp_df[["Time", "Amount"]])
            scaled_time, scaled_amount = scaled[0]  # since it's just one row

            # Step 3: Build the full input feature list
            # Format: [Time (scaled), V1, V2, ..., V28, Amount (scaled)]
            full_features = [scaled_time] + transaction["features"] + [scaled_amount]

            # Step 4: Create a 1-row DataFrame with correct column names
            columns = [
                "Time", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10",
                "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18", "V19", "V20",
                "V21", "V22", "V23", "V24", "V25", "V26", "V27", "V28", "Amount"
            ]

            input_df = pd.DataFrame([full_features], columns=columns)


            # Predict fraud
            prediction = self.fraud_detection_model.predict(input_df)
            fraud = prediction[0] == 1

            if fraud:
                print(f"🚨 FRAUD DETECTED: {transaction}")
                num_fraud+=1
            else:
                print(f"✅ Legit Transaction: {transaction}")
                num_not_fraud+=1
        print("Number of Frauds: ",num_fraud)
        print("Number of non frauds: ",num_not_fraud)

if __name__ == "__main__":
    consumer = KafkaConsumerService()
    consumer.detect_fraud()

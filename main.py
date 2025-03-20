from FraudDetection.components.data_ingestion import DataIngestion
from FraudDetection.components.data_validation import DataValidation
from FraudDetection.exception.exception import FraudDetectionException
from FraudDetection.logging.logger import logging
from FraudDetection.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig
import sys

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        logging.info("Initiate data ingestion")
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed")
        logging.info("Initiate data validation")
        datavalidationconfig=DataValidationConfig(training_pipeline_config=trainingpipelineconfig)
        data_validation=DataValidation(data_ingestion_artifact=dataingestionartifact,data_validation_config=datavalidationconfig)
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        print(data_validation_artifact)
    except Exception as e:
        raise FraudDetectionException(e,sys)
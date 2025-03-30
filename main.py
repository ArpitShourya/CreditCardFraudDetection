from FraudDetection.components.data_ingestion import DataIngestion
from FraudDetection.components.data_validation import DataValidation
from FraudDetection.components.data_transformation import DataTransformation
from FraudDetection.components.model_trainer import ModelTrainer
from FraudDetection.exception.exception import FraudDetectionException
from FraudDetection.logging.logger import logging
from FraudDetection.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig

import sys

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()

        logging.info("Initiate data ingestion")
        dataingestionconfig=DataIngestionConfig(training_pipeline_config=trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed")

        logging.info("Initiate data validation")
        datavalidationconfig=DataValidationConfig(training_pipeline_config=trainingpipelineconfig)
        data_validation=DataValidation(data_ingestion_artifact=dataingestionartifact,data_validation_config=datavalidationconfig)
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("Data validation completed")

        logging.info("Initiate Data Transformation")
        datatransformationconfig=DataTransformationConfig(training_pipeline_config=trainingpipelineconfig)
        data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=datatransformationconfig)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        logging.info("Data Transsformation completed")

        logging.info("Initiated Model training")
        modeltrainerconfig=ModelTrainerConfig(training_pipeline_config=trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config=modeltrainerconfig,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_training()
        logging.info("Model Trianing Completed")

        print(model_trainer_artifact)
    except Exception as e:
        raise FraudDetectionException(e,sys)
from FraudDetection.exception.exception import FraudDetectionException
from FraudDetection.logging.logger import logging
from FraudDetection.components.data_ingestion import DataIngestion
from FraudDetection.components.data_validation import DataValidation
from FraudDetection.components.data_transformation import DataTransformation
from FraudDetection.components.model_trainer import ModelTrainer
from FraudDetection.constants.training_pipeline import TRAINING_BUCKET_NAME
from FraudDetection.cloud.s3_sync import S3Sync

from FraudDetection.entity.config_entity import (TrainingPipelineConfig,
                                                 DataIngestionConfig,
                                                 DataTransformationConfig,
                                                 DataValidationConfig,
                                                 ModelTrainerConfig)

from FraudDetection.entity.artifact_entity import (DataIngestionArtifact,
                                                   DataTransformationArtifact,
                                                   DataValidationArtifact,
                                                   ModelTrainerArtifact)
import sys


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
        self.s3=S3Sync()

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            trainingpipelineconfig=self.training_pipeline_config
            logging.info("Initiate data ingestion")
            dataingestionconfig=DataIngestionConfig(training_pipeline_config=trainingpipelineconfig)
            data_ingestion=DataIngestion(dataingestionconfig)
            dataingestionartifact=data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed")
            return dataingestionartifact
        except Exception as e:
            raise FraudDetectionException(e,sys)
        

    def start_data_validation(self,dataingestionartifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            trainingpipelineconfig=self.training_pipeline_config
            logging.info("Initiate data validation")
            datavalidationconfig=DataValidationConfig(training_pipeline_config=trainingpipelineconfig)
            data_validation=DataValidation(data_ingestion_artifact=dataingestionartifact,data_validation_config=datavalidationconfig)
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info("Data validation completed")
            return data_validation_artifact
        except Exception as e:
            raise FraudDetectionException(e,sys)
        

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            trainingpipelineconfig=self.training_pipeline_config
            logging.info("Initiate Data Transformation")
            datatransformationconfig=DataTransformationConfig(training_pipeline_config=trainingpipelineconfig)
            data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=datatransformationconfig)
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            logging.info("Data Transsformation completed")
            return data_transformation_artifact
        except Exception as e:
            raise FraudDetectionException(e,sys)
        

    def start_model_training(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            trainingpipelineconfig=self.training_pipeline_config
            logging.info("Initiated Model training")
            modeltrainerconfig=ModelTrainerConfig(training_pipeline_config=trainingpipelineconfig)
            model_trainer=ModelTrainer(model_trainer_config=modeltrainerconfig,data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact=model_trainer.initiate_model_training()
            logging.info("Model Trianing Completed")
            return model_trainer_artifact
        except Exception as e:
            raise FraudDetectionException(e,sys)
        
    ## local artifact is going to s3 bucket    
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3
            self.s3.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise FraudDetectionException(e,sys)
        
    ## local final model is going to s3 bucket 
        
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3.sync_folder_to_s3(folder = self.training_pipeline_config.model_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise FraudDetectionException(e,sys)
        
    def run_training_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(dataingestionartifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_training(data_transformation_artifact=data_transformation_artifact)

            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
            return model_trainer_artifact
        except Exception as e:
            raise(e,sys)
        
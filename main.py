from FraudDetection.components.data_ingestion import DataIngestion
from FraudDetection.components.data_validation import DataValidation
from FraudDetection.components.data_transformation import DataTransformation
from FraudDetection.components.model_trainer import ModelTrainer
from FraudDetection.components.kafka_producer import KafkaProducerService
from FraudDetection.components.kafka_consumer import KafkaConsumerService
from FraudDetection.utils.ml_utils.model.estimator import FraudDetectionModel
from FraudDetection.exception.exception import FraudDetectionException
from FraudDetection.logging.logger import logging
from FraudDetection.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig

import sys,threading

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

        # Kafka Streaming (Run Producer & Consumer in Parallel)
        producer = KafkaProducerService()
        #consumer = KafkaConsumerService()

        # Run Kafka Producer & Consumer in Threads
        producer_thread = threading.Thread(target=producer.stream_data, args=("Data/creditcard.csv",))
        #consumer_thread = threading.Thread(target=consumer.detect_fraud)

        producer_thread.start()
        #consumer_thread.start()

        producer_thread.join()
        #consumer_thread.join()
    except Exception as e:
        raise FraudDetectionException(e,sys)
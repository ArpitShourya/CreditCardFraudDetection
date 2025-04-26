from datetime import datetime
from FraudDetection.constants import training_pipeline
import os

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_S")
        self.pipeline_name=training_pipeline.PIPELINE_NAME
        self.artifact_name=training_pipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact_name,timestamp)
        self.model_dir=os.path.join("final_models")
        self.timestamp=timestamp

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir:str=os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path:str=os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILE_NAME
        )
        '''
        self.X_train_data_file_path:str=os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_TRAIN_INGESTED_DIR,
            training_pipeline.X_TRAIN_FILE_NAME
        )
        self.X_test_data_file_path:str=os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_TEST_INGESTED_DIR,
            training_pipeline.X_TEST_FILE_NAME
        )
        self.y_train_data_file_path:str=os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_TRAIN_INGESTED_DIR,
            training_pipeline.Y_TRAIN_FILE_NAME
        )
        self.y_test_data_file_path:str=os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_TEST_INGESTED_DIR,
            training_pipeline.Y_TEST_FILE_NAME
        )
        '''
        self.training_data_file_path:str=os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
        )
        self.testing_data_file_path:str=os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
        )

        self.train_test_split_ratio:float=training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name:str=training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.target_column:str=training_pipeline.TARGET_COLUMN
        self.database_name:str=training_pipeline.DATA_INGESTION_DATABASE_NAME


class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir:str=os.path.join(training_pipeline_config.artifact_dir,
                                                      training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR)

        self.valid_train_file_path:str=os.path.join(self.valid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path:str=os.path.join(self.valid_data_dir,training_pipeline.TEST_FILE_NAME)
        
        self.invalid_train_file_path:str=os.path.join(self.invalid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path:str=os.path.join(self.invalid_data_dir,training_pipeline.TEST_FILE_NAME)
        
        self.drift_report_path:str=os.path.join(self.data_validation_dir,
                                                    training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
                                                    training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
                                                    )

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_train_file_path=os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMED_DIR,training_pipeline.TRAIN_FILE_NAME)
        self.transformed_test_file_path=os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMED_DIR,training_pipeline.TEST_FILE_NAME)
        self.preprocess_model_file_path=os.path.join(self.data_transformation_dir,
                                                     training_pipeline.DATA_TRANSFORMATION_MODEL_DIR,
                                                     training_pipeline.DATA_TRANSFORMATION_MODEL_NAME)


class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir=os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.MODEL_TRAINER_DIR_NAME
            )
        self.trained_model_file_path=os.path.join(self.model_trainer_dir,
                                                  training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
                                                  training_pipeline.MODEL_TRAINER_FILENAME)
        
        self.expected_G_Mean=training_pipeline.MODEL_TRAINER_EXPECTED_G_MEAN_SCORE
        self.overfitting_underfitting_threshold=training_pipeline.MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD

        
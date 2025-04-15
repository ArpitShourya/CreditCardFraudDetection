import sys,os,numpy as np,pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from FraudDetection.exception.exception import FraudDetectionException
from FraudDetection.logging.logger import logging
from FraudDetection.utils.main_utils.utils import save_object
from FraudDetection.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from FraudDetection.entity.config_entity import DataTransformationConfig
from FraudDetection.utils.main_utils.utils import save_numpy_array_data,save_object
from FraudDetection.constants.training_pipeline import DATA_TRANSFORMATION_COLUMN_TO_SCALE

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise FraudDetectionException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise FraudDetectionException(e,sys)
    
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")
            train_data=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_data=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)


            #removing duplicate columns
            train_data_unique=train_data.drop_duplicates()
            test_data_unique=test_data.drop_duplicates()

            #scaling data
            scaler=StandardScaler()
            
            # Ensure train_data_unique and test_data_unique are copies to avoid SettingWithCopyWarning
            train_data_unique = train_data_unique.copy()
            test_data_unique = test_data_unique.copy()

            # Apply scaling
            train_data_unique.loc[:, DATA_TRANSFORMATION_COLUMN_TO_SCALE] = scaler.fit_transform(train_data_unique[DATA_TRANSFORMATION_COLUMN_TO_SCALE])
            test_data_unique.loc[:, DATA_TRANSFORMATION_COLUMN_TO_SCALE] = scaler.transform(test_data_unique[DATA_TRANSFORMATION_COLUMN_TO_SCALE])

            save_object(self.data_transformation_config.preprocess_model_file_path,scaler)



            dir_path=os.path.dirname(self.data_transformation_config.transformed_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            
            train_data_unique.to_csv(
                self.data_transformation_config.transformed_train_file_path,index=False,header=True
            )
            test_data_unique.to_csv(
                self.data_transformation_config.transformed_test_file_path,index=False,header=True
            )

            
            data_transformation_artifact=DataTransformationArtifact(transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                                                                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path)
            return data_transformation_artifact
        except Exception as e:
            raise FraudDetectionException(e,sys)
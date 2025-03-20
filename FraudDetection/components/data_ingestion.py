from FraudDetection.entity.config_entity import DataIngestionConfig
from FraudDetection.entity.artifact_entity import DataIngestionArtifact
from FraudDetection.exception.exception import FraudDetectionException
from FraudDetection.logging.logger import logging
from sklearn.model_selection import train_test_split
from typing import List
from dotenv import load_dotenv
import os,sys,numpy,pymongo,pandas as pd
load_dotenv()

MONGO_DB_URI=os.getenv("MONGO_DB_URI")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config

        except Exception as e:
            raise FraudDetectionException(e,sys)
        
    def export_collection_as_df(self):
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URI)
            collection=self.mongo_client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            df.dropna(inplace=True)
            return df            
        except Exception as e:
            raise FraudDetectionException(e,sys)
        
    def export_data_to_feature_store(self,df:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            df.to_csv(feature_store_file_path,index=False,header=True)
            return df
        except Exception as e:
            raise FraudDetectionException(e,sys)
        

    def split_data_train_test(self,df:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(
                df,test_size=self.data_ingestion_config.train_test_split_ratio,stratify=df['Class'],random_state=42
            )
            logging.info("Performed train test split")

            logging.info("Exited train test split method")

            dir_path=os.path.dirname(self.data_ingestion_config.training_data_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info("Exporting train and test file path")
            
            train_set.to_csv(
                self.data_ingestion_config.training_data_file_path,
                index=False,
                header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_data_file_path,
                index=False,
                header=True
            )

            logging.info(f"Exported train and test file path")
        except Exception as e:
            raise FraudDetectionException(e,sys)
        
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_df()
            dataframe=self.export_data_to_feature_store(dataframe)
            self.split_data_train_test(dataframe)
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_data_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_data_file_path)
            return dataingestionartifact


        except Exception as e:
            raise FraudDetectionException(e,sys)
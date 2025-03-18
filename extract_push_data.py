import os, kaggle,sys,json,certifi,numpy as np,pandas as pd,pymongo
from FraudDetection.logging import logger
from FraudDetection.exception.exception import FraudDetectionException
from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URI=os.getenv("MONGO_DB_URI")
ca=certifi.where()

def download_data(dataset_identifier,save_path="Data"):
    try:
        os.makedirs(save_path,exist_ok=True)
        kaggle.api.dataset_download_files(dataset_identifier,path=save_path,unzip=True)
        print(f"Datset downloaded and saved in {save_path}")
    except Exception as e:
        raise FraudDetectionException(e,sys)

class DetectionDataExtract:
    def __init__(self):
        try:
            logger.logging.info("Downloaded Credit Card Fraud Dataset file")
            download_data("mlg-ulb/creditcardfraud")
        except Exception as e:
            raise FraudDetectionException(e,sys)

    def convert_csv_to_json(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise FraudDetectionException(e,sys)
        
    def insert_data_to_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URI)
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise FraudDetectionException(e,sys)

if __name__=="__main__":
    FILE_PATH="Data\creditcard.csv"
    DATABASE="CREDITCARDPROJECT"
    Collection="FraudDetectionData"
    detectionobj=DetectionDataExtract()
    records=detectionobj.convert_csv_to_json(FILE_PATH)
    #print(records)
    no_of_records=detectionobj.insert_data_to_mongodb(records=records,database=DATABASE,collection=Collection)
    print(no_of_records)
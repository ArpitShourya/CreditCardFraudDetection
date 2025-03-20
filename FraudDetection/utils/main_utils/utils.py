import yaml,os,sys
from FraudDetection.exception.exception import FraudDetectionException
from FraudDetection.logging.logger import logging

def create_yaml(path,*args):
    try:
        os.makedirs(os.path.dirname(path),exist_ok=True)
        with open(path,"w") as file:
            for i in range(len(args)):
                yaml.dump(args[i],file)
    except Exception as e:
        raise FraudDetectionException(e,sys)

def read_yaml(file_path):
    try:
        with open(file_path,"rb") as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise FraudDetectionException(e,sys)
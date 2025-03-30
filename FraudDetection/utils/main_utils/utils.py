import yaml,os,sys,numpy as np,pickle,pandas as pd
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
    
def save_numpy_array_data(file_path:str, array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise FraudDetectionException(e,sys)
    
def get_data(file_path:str):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise FraudDetectionException(e,sys)
    
def save_object(file_path:str,obj:object):
    try:
        logging.info("Entered the save_object Method")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method")
    except Exception as e:
        raise FraudDetectionException(e,sys)
    
def load_object(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The path {file_path} doesn't exist")
        with open(file_path,"rb") as obj:
            return pickle.load(obj)
    except Exception as e:
        raise FraudDetectionException(e,sys)
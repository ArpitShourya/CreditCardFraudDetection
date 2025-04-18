import yaml,os,sys,numpy as np,pickle,pandas as pd
from FraudDetection.exception.exception import FraudDetectionException
from FraudDetection.logging.logger import logging
from FraudDetection.constants.training_pipeline import EMAIL_ADDRESS,TO_EMAIL
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()

email_pass=os.getenv("GOOGLE_EMAIL_PASS")


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
    

EMAIL_ADDRESS = EMAIL_ADDRESS
EMAIL_PASSWORD = email_pass
TO_EMAIL = TO_EMAIL

def send_email_alert(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✅ Email alert sent successfully!")
    except Exception as e:
        print("❌ Failed to send email:", e)
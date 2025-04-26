import sys,os,certifi,pymongo,pandas as pd
from FraudDetection.exception.exception import FraudDetectionException
from FraudDetection.logging.logger import logging
from FraudDetection.utils.ml_utils.model.estimator import FraudDetectionModel
from FraudDetection.pipeline.training_pipeline import TrainingPipeline
from FraudDetection.components.kafka_producer import KafkaProducerService
from FraudDetection.constants.training_pipeline import (DATA_INGESTION_COLLECTION_NAME,
                                                        DATA_INGESTION_DATABASE_NAME)
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from FraudDetection.utils.main_utils.utils import load_object
ca=certifi.where()

from dotenv import load_dotenv

load_dotenv()

mongo_db_uri=os.getenv('MONGO_DB_URI')
client=pymongo.MongoClient(mongo_db_uri,tlsCAFile=ca)
database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]

app=FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="./templates")

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_training_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise FraudDetectionException(e,sys)
    
@app.get("/predict")
async def predict_route(file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        rows_to_scale=['Time','Amount']
        preprocessor=load_object("final_models/preprocessing.pkl")
        model=load_object("final_models/Model.pkl")
        fraud_detection_model=FraudDetectionModel(model=model)
        df[rows_to_scale]=preprocessor.transform(df[rows_to_scale])
        y_pred=fraud_detection_model.predict(df)
        df['predicted column']=y_pred
        df.to_csv("Prediction_Data/output.csv")
        kfpservice=KafkaProducerService()
        kfpservice.stream_dataframe(df)
        return Response("Output saved in folder Prediction Data")
    except Exception as e:
        raise FraudDetectionException(e,sys)
    
if __name__=="__main__":
    app_run(app=app,host="localhost",port=8000)

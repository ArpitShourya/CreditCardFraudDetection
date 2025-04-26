import sys,os,certifi,pymongo,pandas as pd
from FraudDetection.exception.exception import FraudDetectionException
from FraudDetection.logging.logger import logging
from FraudDetection.pipeline.training_pipeline import TrainingPipeline
from FraudDetection.constants.training_pipeline import (DATA_INGESTION_COLLECTION_NAME,
                                                        DATA_INGESTION_DATABASE_NAME)
from FraudDetection.pipeline.batch_prediction_pipeline import BatchPredictionPipeline
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
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


@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        logging.info("Training Stared")
        train_pipeline.run_training_pipeline()
        logging.info("Training complete")
        return Response("Training is successful")
    except Exception as e:
        logging.info("Some error occured in training")
        raise FraudDetectionException(e,sys)
    
@app.get("/predict")
async def predict_route(file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        logging.info("Prediction Started")
        prediction_pipeline=BatchPredictionPipeline(df)
        prediction_pipeline.start_batch_prediction()
        logging.info("Prediction Complete")
        return Response("Output saved in folder Prediction Data")
    except Exception as e:
        logging.info("Some error occured in Prediction")
        raise FraudDetectionException(e,sys)
    
if __name__=="__main__":
    app_run(app=app,host="0.0.0.0",port=8000)

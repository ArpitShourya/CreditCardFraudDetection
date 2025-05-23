import os
'''
Common constant variable for training pipeline
'''
TARGET_COLUMN="Class"
PIPELINE_NAME="FraudDetection"
ARTIFACT_DIR="Artifacts"
FILE_NAME="creditcard.csv"

EMAIL_ADDRESS = "arpitshourya2233@gmail.com"
TO_EMAIL = "arpitshourya2233@gmail.com"


TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"
#X_TRAIN_FILE_NAME="X_train.csv"
#X_TEST_FILE_NAME="x_test.csv"
#Y_TRAIN_FILE_NAME="y_train.csv"
#Y_TEST_FILE_NAME="y_test.csv"

SCHEMA_FILE_DIR="data_schema"
SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")

PREPROCESSING_OBJECT_FILE_NAME="preprocessing.pkl"
SAVED_MODEL_DIR=os.path.join("saved_models")

'''
Data Ingestion related constant start with DATA_INGESTION VAR NAME
'''
DATA_INGESTION_COLLECTION_NAME="FraudDetectionData"
DATA_INGESTION_DATABASE_NAME="CREDITCARDPROJECT"
DATA_INGESTION_DIR_NAME="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR="feature_store"
DATA_INGESTION_INGESTED_DIR="data_ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO=0.2

'''
Data validation related constant start with DATA_VALIDATION VAR NAME
'''
DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_VALID_DIR:str="validated"
DATA_VALIDATION_INVALID_DIR:str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str="drift_report.yaml"


"""
Data Transformation related constant
"""

DATA_TRANSFORMATION_DIR_NAME:str="data_transformation"
DATA_TRANSFORMED_DIR:str="transformed"
DATA_TRANSFORMATION_COLUMN_TO_SCALE=['Time','Amount']
DATA_TRANSFORMATION_MODEL_DIR="Preprocessing model"
DATA_TRANSFORMATION_MODEL_NAME="preprocessing.pkl"


"""
Model Trainer related constant starts with MODEL_TRAINER var name
"""

MODEL_TRAINER_DIR_NAME:str="Model Trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str="Trained Model"
MODEL_TRAINER_FILENAME:str="Model.pkl"
MODEL_TRAINER_EXPECTED_G_MEAN_SCORE:float=0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD=0.05


TRAINING_BUCKET_NAME = "frauddetection2209"
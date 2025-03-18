'''
Common constant variable for training pipeline
'''
TARGET_COLUMN="Class"
PIPELINE_NAME="FraudDetection"
ARTIFACT_DIR="Artifacts"
FILE_NAME="creditcard.csv"

#TRAIN_FILE_NAME="train.csv"
#TEST_FILE_NAME="test.csv"
X_TRAIN_FILE_NAME="X_train.csv"
X_TEST_FILE_NAME="x_test.csv"
Y_TRAIN_FILE_NAME="y_train.csv"
Y_TEST_FILE_NAME="y_test.csv"





'''
Data Ingestion related constant start with DATA_INGESTION VAR NAME
'''
DATA_INGESTION_COLLECTION_NAME="FraudDetectionData"
DATA_INGESTION_DATABASE_NAME="CREDITCARDPROJECT"
DATA_INGESTION_DIR_NAME="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR="feature_store"
DATA_INGESTION_TRAIN_INGESTED_DIR="train_data_ingested"
DATA_INGESTION_TEST_INGESTED_DIR="test_data_ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO=0.2
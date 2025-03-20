from FraudDetection.logging.logger import logging
from FraudDetection.exception.exception import FraudDetectionException
from FraudDetection.entity.config_entity import DataValidationConfig
from FraudDetection.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from FraudDetection.utils.main_utils.utils import create_yaml,read_yaml
from FraudDetection.constants.training_pipeline import SCHEMA_FILE_PATH,SCHEMA_FILE_DIR
from scipy.stats import ks_2samp
import pandas as pd,numpy as np,os,sys,yaml

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            # Create Yaml File
            df=pd.read_csv("Data\creditcard.csv")
            columns_dict=dict(columns=list(df.columns))
            num_col=[]
            for i in df.columns:
                if isinstance(df[i][0],np.float64) or isinstance(df[i][0],np.int64):
                    num_col.append(i)
            num_col_dict=dict(numerical_columns=num_col)
            #os.makedirs(TEST_SCHEMA_FILE_PATH,exist_ok=True)
            #os.makedirs(TRAIN_SCHEMA_FILE_PATH,exist_ok=True)
            #os.makedirs(SCHEMA_FILE_DIR,exist_ok=True)
            create_yaml(SCHEMA_FILE_PATH,columns_dict,num_col_dict)
            #with open(TEST_SCHEMA_FILE_PATH,"w") as file:
            #    yaml.dump(test_columns_dict,file)
            #    yaml.dump(test_num_col_dict,file)
            #with open(TRAIN_SCHEMA_FILE_PATH,"w") as file:
            #    yaml.dump(train_columns_dict,file)
            #    yaml.dump(train_num_col_dict,file)
            self._schema_config=read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise FraudDetectionException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise FraudDetectionException(e,sys)
        
    def validate_number_of_columns(self,df:pd.DataFrame):
        try:
            columns = self._schema_config.get("columns", [])
            logging.info(f"Required number of columns: {len(columns)}")
            logging.info(f"Dataframe has {len(df.columns)} columns")
            if(len(df.columns)==len(columns)):
                return True
            return False
        except Exception as e:
            raise FraudDetectionException(e,sys)
        
    def validate_numerical_columns(self,df:pd.DataFrame):
        try:
            invalid_columns = []
            self.integer_columns = self._schema_config.get("numerical_columns", [])

            for col in self.integer_columns:
                if col in df.columns:
                    if not pd.api.types.is_integer_dtype(df[col]):
                        invalid_columns.append(col)
                else:
                    logging.warning(f"Column {col} is missing in the DataFrame.")

            if invalid_columns:
                logging.error(f"Invalid integer columns: {invalid_columns}")
                return False

            logging.info("All specified integer columns are valid.")
            return True

        except Exception as e:
            raise Exception(f"Error validating integer columns: {e}")
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({
                    column:{
                        "p_value":float(is_same_dist.pvalue),
                        "drift_status":is_found
                    }
                })
            
            drift_report_file_path=self.data_validation_config.drift_report_path
        
            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            create_yaml(drift_report_file_path,report)
            return status
        except Exception as e:
            raise FraudDetectionException(e,sys)
    
    def initiate_data_validation(self)->DataValidationArtifact:
        train_file_path=self.data_ingestion_artifact.trained_file_path
        test_file_path=self.data_ingestion_artifact.test_file_path
        train_dataframe=DataValidation.read_data(train_file_path)
        test_dataframe=DataValidation.read_data(test_file_path)
        status=self.validate_number_of_columns(df=train_dataframe)
        if not status:
            error_msg=f"Train dataframe doesn't contain all columns"
            logging.error(error_msg)
        status=self.validate_number_of_columns(df=test_dataframe)
        if not status:
            error_msg=f"Test dataframe doesn't contain all columns"
            logging.error(error_msg)
        status=self.validate_numerical_columns(df=train_dataframe)
        if not status:
            error_msg=f"Train dataframe doesn't contain numerical column"
            logging.error(error_msg)
        status=self.validate_numerical_columns(df=test_dataframe)
        if not status:
            error_msg=f"Test dataframe doesn't contain numerical column"
            logging.error(error_msg)
        status=self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
        if not status:
            error_msg=f"Test dataframe has data drift"
            logging.error(error_msg)
        dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
        os.makedirs(dir_path,exist_ok=True)

        train_dataframe.to_csv(
            self.data_validation_config.valid_train_file_path,index=False,header=True
        )
        test_dataframe.to_csv(
            self.data_validation_config.valid_test_file_path,index=False,header=True
        )
        data_validation_artifact = DataValidationArtifact(
            validation_status=status,
            valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
            valid_test_file_path=self.data_ingestion_artifact.test_file_path,
            invalid_train_file_path=None,
            invalid_test_file_path=None,
            drift_report_path=self.data_validation_config.drift_report_path,
        )
        return data_validation_artifact
        
        

        
        
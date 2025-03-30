from FraudDetection.exception.exception import FraudDetectionException
from FraudDetection.logging.logger import logging
from FraudDetection.entity.config_entity import ModelTrainerConfig
from FraudDetection.entity.artifact_entity import DataTransformationArtifact,ClassificationMetricArtifact,ModelTrainerArtifact
from FraudDetection.utils.main_utils.utils import save_object,load_object,get_data
from FraudDetection.utils.ml_utils.metric.classification_metric import get_classification_score
from FraudDetection.utils.ml_utils.model.estimator import FraudDetectionModel
from FraudDetection.constants.training_pipeline import TARGET_COLUMN
from xgboost import XGBClassifier
from sklearn.ensemble import IsolationForest
import sys,numpy as np,os,mlflow


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise FraudDetectionException(e,sys)
        

    def track_mlflow(self,model,classification_artifact):
        with mlflow.start_run():
            f1_score=classification_artifact.f1_score
            recall_score=classification_artifact.recall_score
            g_mean=classification_artifact.g_mean_score

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.log_metric("g_mean",g_mean)

            mlflow_model = FraudDetectionModel(model)

            mlflow.pyfunc.log_model( artifact_path=self.model_trainer_config.trained_model_file_path,python_model=mlflow_model)


    def train_model(self,X_train,y_train):
        fraud_ratio = sum(y_train == 0) / sum(y_train == 1)  # Majority / Minority ratio

    # Train XGBoost
        xgb_model = XGBClassifier(n_estimators=200, learning_rate=0.05, max_depth=6, scale_pos_weight=fraud_ratio, random_state=42)
        xgb_model.fit(X_train, y_train)
        X_train_nonfraud = X_train[y_train == 0]
        iso_forest = IsolationForest(n_estimators=100, contamination=0.002, random_state=42)
        iso_forest.fit(X_train_nonfraud)

        ensemble_model = {
        "xgb_model": xgb_model,
        "iso_forest": iso_forest,
        }
        return ensemble_model

    def initiate_model_training(self):
        train_file_path=self.data_transformation_artifact.transformed_train_file_path
        test_file_path=self.data_transformation_artifact.transformed_test_file_path
        train_data=get_data(train_file_path)
        test_data=get_data(test_file_path)
        X_train,X_test,y_train,y_test=(
            train_data.drop(columns=TARGET_COLUMN),
            test_data.drop(columns=TARGET_COLUMN),
            train_data[TARGET_COLUMN],
            test_data[TARGET_COLUMN]
        )

        model=self.train_model(X_train,y_train)
        fraud_detection_model=FraudDetectionModel(model=model)

        final_pred_test = fraud_detection_model.predict(X_test)
        final_pred_train=fraud_detection_model.predict(X_train)
        
        test_classification_artifact=get_classification_score(y_true=y_test,y_pred=final_pred_test)
        train_classification_artifact=get_classification_score(y_true=y_train,y_pred=final_pred_train)

        #mlflow tracking
        self.track_mlflow(model,train_classification_artifact)
        self.track_mlflow(model,test_classification_artifact)
    
        
        

        save_object(self.model_trainer_config.trained_model_file_path,model)

        model_trainer_artifact=ModelTrainerArtifact(trained_model_path=self.model_trainer_config.trained_model_file_path,
                                                    train_metric_artifact=train_classification_artifact,
                                                    test_metric_artifact=test_classification_artifact)
        
        return model_trainer_artifact
    




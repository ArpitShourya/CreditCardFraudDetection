import joblib
from FraudDetection.entity.config_entity import ModelTrainerConfig,TrainingPipelineConfig
from FraudDetection.utils.ml_utils.model.estimator import FraudDetectionModel
trainingpipelineconfig=TrainingPipelineConfig()
model_trainer_config=ModelTrainerConfig(training_pipeline_config=trainingpipelineconfig)
model=joblib.load("Artifacts\\03_31_2025_14_36_S\Model Trainer\Trained Model\Model.pkl")
fraud_detection_model=FraudDetectionModel(model=model)
print(fraud_detection_model.predict([354.0, 11.38, -0.687099302570821, 0.790436270915636, 2.24242432271365, 2.40646163016605, 0.359711754795171, 0.279410289878938, 0.103677151511258, 0.399071184305469, -1.5187327616647, 0.601268282242301, 1.38977445144218, -0.1918927274936, -1.27907560001655, 0.680096415708661, 0.689691524612909, 0.276206191009753, -0.0890122108842315, -0.0657719433477332, 0.0798821723495131, 0.0568705740168107, -0.146194338775118, -0.702302599396075, 0.0880384486538265, 0.138006040839989, -0.129552530218793, -0.141250330639071, -0.0113855026567034, -0.006343762762011]))
#print(fraud_detection_model)
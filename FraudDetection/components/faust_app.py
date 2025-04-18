import faust
import joblib
import pandas as pd
from FraudDetection.entity.config_entity import TrainingPipelineConfig, ModelTrainerConfig, DataTransformationConfig
from FraudDetection.utils.ml_utils.model.estimator import FraudDetectionModel
from FraudDetection.utils.main_utils.utils import send_email_alert


# Load preprocessor and model
trainingpipelineconfig = TrainingPipelineConfig()
model_trainer_config = ModelTrainerConfig(training_pipeline_config=trainingpipelineconfig)
data_transformation_config = DataTransformationConfig(training_pipeline_config=trainingpipelineconfig)

model = joblib.load(r"E:\ETE FraudDetection Project\Artifacts\04_17_2025_08_36_S\Model Trainer\Trained Model\Model.pkl")
preprocessor = joblib.load(r"E:\ETE FraudDetection Project\Artifacts\04_17_2025_08_36_S\data_transformation\Preprocessing model\preprocessing.pkl")
fraud_model = FraudDetectionModel(model)

# Faust app
app = faust.App(
    'fraud-detector-app',
    broker='kafka://localhost:9092',
    value_serializer='json',
)

# Define the Kafka topic schema
class Transaction(faust.Record, serializer='json'):
    event_time: str
    Time: float
    features: list
    Amount: float

credit_card_topic = app.topic('credit_card_transactions', value_type=Transaction)

@app.agent(credit_card_topic)
async def detect_fraud(transactions):
    async for tx in transactions:
        try:
            # Scale Time & Amount
            scaled = preprocessor.transform([[tx.Time, tx.Amount]])
            scaled_time, scaled_amount = scaled[0]

            # Combine with V1-V28 features
            features = [scaled_time] + tx.features + [scaled_amount]
            columns = [
                "Time", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10",
                "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18", "V19", "V20",
                "V21", "V22", "V23", "V24", "V25", "V26", "V27", "V28", "Amount"
            ]
            df = pd.DataFrame([features], columns=columns)
            
            prediction = fraud_model.predict(df)[0]
            if prediction == 1:
                print(f"🚨 FRAUD DETECTED: {tx}")
                message = f"🚨 FRAUD ALERT!\nAmount: {tx.Amount} dollars \nTime : {tx.Time} seconds"
                send_email_alert("🚨 FRAUD DETECTED", message)
            else:
                print(f"✅ Legit Transaction: {tx}")
        except Exception as e:
            print(f"Error processing transaction: {e}")

if __name__ == '__main__':
    app.main()

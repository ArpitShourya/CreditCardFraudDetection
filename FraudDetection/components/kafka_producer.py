from kafka import KafkaProducer
import pandas as pd
import json
import time
from datetime import datetime, timedelta

class KafkaProducerService:
    def __init__(self, bootstrap_servers="localhost:9092", topic="credit_card_transactions"):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode("utf-8")
        )
        self.topic = topic

    def stream_data(self, data_path):
        df = pd.read_csv(data_path)
        base_time = datetime.now()

        for _, row in df.iterrows():
            # Convert relative Time to absolute datetime
            event_time = base_time + timedelta(seconds=row["Time"])

            transaction = {
                "event_time": event_time.isoformat(),  
                "Time": row["Time"],                   
                "features": row.iloc[1:29].tolist(),
                "Amount": row["Amount"]
            }

            self.producer.send(self.topic, value=transaction)
            print(f"Sent: {transaction}")

            
            time.sleep(1)  # simulate real-time

    def stream_dataframe(self, df):
    
        base_time = datetime.now()

        for _, row in df.iterrows():
            event_time = base_time + timedelta(seconds=row["Time"])

            transaction = {
                "event_time": event_time.isoformat(),
                "Time": row["Time"],
                "features": row.iloc[1:29].tolist(),
                "Amount": row["Amount"]
            }

            self.producer.send(self.topic, value=transaction)
            print(f"Sent: {transaction}")


if __name__ == "__main__":
    producer = KafkaProducerService()
    producer.stream_data(r"E:\ETE FraudDetection Project\Data\creditcard.csv")

# Real-Time Bank Transaction Fraud Detection 🚀

## 🏷️ Badges

![Dockerized](https://img.shields.io/badge/Dockerized-Yes-blue?logo=docker)
![Real-Time Streaming](https://img.shields.io/badge/Streaming-Kafka%20%2B%20Faust-orange?logo=apache-kafka)
![FastAPI](https://img.shields.io/badge/API-FastAPI-0E7C61?logo=fastapi)
![AWS Deployed](https://img.shields.io/badge/Deployed%20On-AWS-232F3E?logo=amazon-aws)
![CI/CD](https://img.shields.io/badge/CI/CD-GitHub%20Actions-blue?logo=github-actions)
![Machine Learning](https://img.shields.io/badge/Model-Isolation%20Forest%20%2B%20XGBoost-brightgreen?logo=scikit-learn)

## 📋 Project Overview

- Built an end-to-end Real-Time Bank Transaction Fraud Detection System using the Kaggle Credit Card Fraud Detection dataset.
- The system detects fraudulent transactions instantly, triggers email alerts, and is production-ready with containerization, real-time streaming, and cloud deployment.

## 🏗️ Architecture

- MongoDB Atlas for transaction data storage.

- Kafka Producer streams data to a Kafka Broker.

- Faust App listens to the Kafka stream, predicts frauds, and labels transactions.

- FastAPI backend for model training and prediction through Swagger UI.

- Email Alerts sent via Gmail SMTP for detected frauds.

- AWS S3 to store model artifacts.

- Docker and Docker-Compose for containerization.

- AWS ECR + EC2 for deployment via GitHub Actions CI/CD.

## ⚙️ Tech Stack

|      Category        |         Technologies        |
|----------------------|-----------------------------|
| Data Storage         | MongoDB Atlas               |
| Machine Learning     | Isolation Forest + XGBoost  |
| Backend              | FastAPI                     |
| Real-Time Streaming  | Apache Kafka + Faust        |
| Email Alerts         | Gmail SMTP                  |
| Containerization     | Docker + Docker-Compose     |
| Cloud Services       | AWS S3, ECR, EC2            |
| CI/CD                | GitHub Actions              |
| Deployment           | AWS CLI                     |

## 📈 Model Details

- Hybrid model combining Isolation Forest (unsupervised anomaly detection) and XGBoost (supervised classification).

- Achieved 92% combined accuracy on the Kaggle Credit Card Fraud Detection dataset.

- Pipeline-based architecture for clean training and prediction processes.

## 🔥 Real-Time Streaming Flow

- Kafka Producer sends transaction events.

- Faust App consumes events, makes predictions, and classifies transactions.

- If fraud is detected, an instant email alert is triggered via SMTP.

## 🚀 Deployment Steps

- Upload trained models and artifacts to AWS S3 using AWS CLI.

- Build Docker images for FastAPI, Faust, and supporting services.

- Use Docker-Compose to orchestrate services locally or on EC2.

- GitHub Actions (deploy.yml) automates:

- Docker image build.

- Push to AWS ECR.

- Deployment to AWS EC2.

## 🛡️ Key Features

- ✅ Real-time fraud detection and notification.

- ✅ Hybrid ML model with high accuracy.

- ✅ Fully containerized microservices.

- ✅ Automated cloud deployment using GitHub Actions.

- ✅ Modular and scalable architecture.

## 📚 Dataset

- Kaggle - Credit Card Fraud Detection Dataset

## 📩 Email Alert Example

- When fraud is detected, an automatic email alert is sent:

'''bash
Subject: ⚠️ Fraud Alert Detected
Body: Transaction ID [XYZ] flagged as FRAUD at [timestamp].
'''

## 🙌 Acknowledgements

- Inspired by real-world production needs for real-time ML systems.

- Thanks to open-source communities of Kafka, FastAPI, Faust, and AWS for their excellent tools.

## 📌 Let's Connect!
- Interested in real-time Machine Learning, MLOps, or Cloud Engineering?

- Let’s connect and innovate together! 🚀
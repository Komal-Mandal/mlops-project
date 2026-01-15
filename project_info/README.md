# 📌 MLOps Project Structure 

## 📖 Project Overview

This project follows a professional MLOps folder structure used in real-world Machine Learning applications.

It helps in building, training, evaluating, and deploying ML models in an organized and scalable way.

The main goal of this structure is to keep code clean, reusable, and easy to debug.

## 📂 Project Structure
```
project-root/
│
├── notebook/                     # Jupyter notebooks (EDA & experiments)
│   ├── *.ipynb
│
├── src/                          # Main source code
│   ├── components/               # ML pipeline steps
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   ├── model_evaluation.py
│   │   └── model_pusher.py
│   │
│   ├── configuration/            # Database & cloud connections
│   │   ├── mongo_db_connection.py
│   │   └── aws_connection.py
│   │
│   ├── cloud_storage/            # AWS S3 operations
│   │   └── aws_storage.py
│   │
│   ├── data_access/              # Data reading layer
│   │   └── proj1_data.py
│   │
│   ├── constants/                # Fixed values & paths
│   │   └── __init__.py
│   │
│   ├── entity/                   # Data containers
│   │   ├── config_entity.py
│   │   ├── artifact_entity.py
│   │   ├── metric_entity.py
│   │   ├── estimator.py
│   │   └── s3_estimator.py
│   │
│   ├── exception/                # Custom error handling
│   │   └── __init__.py
│   │
│   ├── logger/                   # Logging setup
│   │   └── __init__.py
│   │
│   ├── pipline/                  # Pipeline controller
│   │   ├── training_pipeline.py
│   │   └── prediction_pipeline.py
│   │
│   ├── utils/                    # Helper functions
│   │   └── main_utils.py
│
├── config/                       # YAML configuration files
│   ├── model.yaml
│   └── schema.yaml
│
├── app.py                        # API entry point
├── demo.py                       # Run training pipeline
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker setup
├── .dockerignore                 # Docker ignore file
├── setup.py                      # Package setup
└── pyproject.toml                # Build configuration
```

### 🔹 src/

- This folder contains all the main source code of the project

### 🔹 src/components/

- Each file here represents one step of the ML pipeline.

- data_ingestion.py → Fetches data from MongoDB / CSV

- data_validation.py → Checks data quality and schema

- data_transformation.py → Feature engineering and preprocessing

- model_trainer.py → Trains the ML model

- model_evaluation.py → Compares new and old models

- model_pusher.py → Pushes best model to cloud (AWS S3)

### 🔹 src/pipline/

- Controls the flow of the entire project.

- training_pipeline.py → Runs complete training process

- prediction_pipeline.py → Handles prediction logic

### 🔹 src/entity/

- Contains data classes used to pass structured data between steps.

- config_entity.py → Stores configuration values

- artifact_entity.py → Stores output of each pipeline step

- estimator.py → Model interface

- s3_estimator.py → Model stored in AWS S3

- metric_entity.py -> Stores model performance results like accuracy, precision, recall, etc.
It helps decide how good the model is.

### 🔹 src/configuration/

- Handles external connections.

- mongo_db_connection.py → MongoDB connection

- aws_connection.py → AWS connection

### 🔹 src/cloud_storage/

- Used for cloud operations.

- aws_storage.py → Upload/download files from AWS S3

### 🔹 src/data_access/

- Responsible for reading data from database or files.

- proj1_data.py → Fetches data and converts it to DataFrame

### 🔹 src/constants/

- Stores fixed values like file paths and collection names.

### 🔹 src/utils/

- Contains helper functions used across the project.

- main_utils.py → Read YAML, save/load models, etc.

### 🔹 src/logger/

- Manages logging for tracking execution and debugging.

### 🔹 src/exception/

Contains custom exception handling for clear error messages.

### ⚙️ Configuration Files (config/)

- model.yaml → Model parameters and settings

- schema.yaml → Dataset schema (columns and data types)

### 📄 Root Files Explanation

- app.py → API entry point (FastAPI / Flask)

- demo.py → Runs training pipeline

- requirements.txt → Required Python libraries

- Dockerfile → Docker configuration

- setup.py → Makes project installable

- pyproject.toml → Build and dependency management

### 📁 notebook/ Folder (Very Important)

- The notebook folder contains all Jupyter Notebook (.ipynb) files.

### 📌 Purpose of notebook/ folder

- This folder is mainly used for:

- Data exploration (EDA)

- Understanding the dataset

- Trying different models

- Feature engineering experiments

- 👉 These notebooks are for learning and experimentation, not for production.



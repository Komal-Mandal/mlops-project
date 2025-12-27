import sys
from typing import Tuple

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import load_numpy_array_data, load_object, save_object
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ClassificationMetricArtifact,
)
from src.entity.estimator import MyModel


class ModelTrainer:
    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_config: ModelTrainerConfig,
    ):
        """
        :param data_transformation_artifact: Output of data transformation stage
        :param model_trainer_config: Model trainer configuration
        """
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_model_object_and_report(
        self, train: np.ndarray, test: np.ndarray
    ) -> Tuple[object, ClassificationMetricArtifact]:
        """
        Trains the model and returns trained model and metric artifact
        """
        try:
            logging.info("Training RandomForestClassifier with specified parameters")

            # Split features and target
            x_train, y_train = train[:, :-1], train[:, -1]
            x_test, y_test = test[:, :-1], test[:, -1]
            logging.info("Train-test split completed")

            # Initialize model
            model = RandomForestClassifier(
                n_estimators=self.model_trainer_config._n_estimators,
                min_samples_split=self.model_trainer_config._min_samples_split,
                min_samples_leaf=self.model_trainer_config._min_samples_leaf,
                max_depth=self.model_trainer_config._max_depth,
                criterion=self.model_trainer_config._criterion,
                random_state=self.model_trainer_config._random_state,
            )

            # Train model
            logging.info("Model training started")
            model.fit(x_train, y_train)
            logging.info("Model training completed")

            # Predictions
            y_pred = model.predict(x_test)

            # Evaluation metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            logging.info(
                f"Model Metrics | Accuracy: {accuracy}, "
                f"Precision: {precision}, Recall: {recall}, F1-score: {f1}"
            )

            # Metric artifact
            metric_artifact = ClassificationMetricArtifact(
                accuracy=accuracy,
                precision_score=precision,
                recall_score=recall,
                f1_score=f1,
            )

            return model, metric_artifact

        except Exception as e:
            raise MyException(e, sys) from e

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        """
        Initiates model training pipeline
        """
        logging.info("Entered initiate_model_trainer method of ModelTrainer")

        try:
            print("------------------------------------------------------------")
            print("Starting Model Trainer Component")

            # Load transformed datasets
            train_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_train_file_path
            )
            test_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_test_file_path
            )
            logging.info("Train-test data loaded")

            # Train model and get metrics
            trained_model, metric_artifact = self.get_model_object_and_report(
                train=train_arr, test=test_arr
            )
            logging.info("Model and metric artifact generated")

            # Load preprocessing object
            preprocessing_obj = load_object(
                self.data_transformation_artifact.transformed_object_file_path
            )
            logging.info("Preprocessing object loaded")

            # Validate model performance on training data
            train_accuracy = accuracy_score(
                train_arr[:, -1],
                trained_model.predict(train_arr[:, :-1]),
            )

            if train_accuracy < self.model_trainer_config.expected_accuracy:
                raise Exception(
                    "Trained model accuracy is less than expected accuracy"
                )

            logging.info("Model meets expected accuracy threshold")

            # Save final model
            my_model = MyModel(
                preprocessing_object=preprocessing_obj,
                trained_model_object=trained_model,
            )

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=my_model,
            )
            logging.info("Final model saved successfully")

            # Model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact,
            )

            logging.info(f"ModelTrainerArtifact created: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise MyException(e, sys) from e

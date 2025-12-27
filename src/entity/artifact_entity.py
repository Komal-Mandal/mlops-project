
from dataclasses import dataclass
from src.entity.metric_entity import ClassificationMetricArtifact


@dataclass
class DataIngestionArtifact:
    trained_file_path:str 
    test_file_path:str

@dataclass
class DataValidationArtifact:
    validation_status:bool
    message: str
    validation_report_file_path: str


@dataclass
class DataTransformationArtifact:
    transformed_object_file_path:str 
    transformed_train_file_path:str
    transformed_test_file_path:str

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str 
    metric_artifact:ClassificationMetricArtifact

    class ClassificationMetricArtifact:
        def __init__(self, accuracy, precision_score, recall_score, f1_score):
         self.accuracy = accuracy
         self.precision_score = precision_score
         self.recall_score = recall_score
         self.f1_score = f1_score





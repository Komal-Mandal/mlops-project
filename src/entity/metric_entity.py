
from dataclasses import dataclass

@dataclass

class ClassificationMetricArtifact:
    accuracy: float
    precision_score: float
    recall_score: float
    f1_score: float

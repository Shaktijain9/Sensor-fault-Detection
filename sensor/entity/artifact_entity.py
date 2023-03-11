class DataIngestionArtifact: ...


from dataclasses import dataclass


@dataclass
class DataValidationArtifact:
    feature_store_file_path: str
    train_file_path: str
    test_file_path: str


class DataTransformationArtifact: ...


class ModelTrainerArtifact: ...


class ModelEvaluationArtifact: ...


class ModelPusherArtifact: ...

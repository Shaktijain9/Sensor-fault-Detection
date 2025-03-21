from sensor.component.data_ingestion import DataIngestion
from sensor.component.data_transformation import DataTransformation
from sensor.component.data_validation import DataValidation
from sensor.component.model_evaluation import ModelEvaluation
from sensor.component.model_pusher import ModelPusher
from sensor.component.model_trainer import ModelTrainer
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.config_entity import DataTransformationConfig
from sensor.entity.config_entity import DataValidationConfig
from sensor.entity.config_entity import ModelEvaluationConfig
from sensor.entity.config_entity import ModelPusherConfig
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.entity.config_entity import TrainingPipelineConfig


def start_training_pipeline():
    try:
        training_pipeline_config = TrainingPipelineConfig()

        # data ingestion
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        # data validation
        data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,
                                         data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_validation()

        # data transformation
        data_transformation_config = DataTransformationConfig(
            training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(
            data_transformation_config=data_transformation_config,
            data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()

        # model trainer
        model_trainer_config = ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,
                                     data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()

        # model evaluation
        model_eval_config = ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_eval = ModelEvaluation(model_eval_config=model_eval_config,
                                     data_ingestion_artifact=data_ingestion_artifact,
                                     data_transformation_artifact=data_transformation_artifact,
                                     model_trainer_artifact=model_trainer_artifact)
        model_eval_artifact = model_eval.initiate_model_evaluation()

        # model pusher
        model_pusher_config = ModelPusherConfig(training_pipeline_config)

        model_pusher = ModelPusher(model_pusher_config=model_pusher_config,
                                   data_transformation_artifact=data_transformation_artifact,
                                   model_trainer_artifact=model_trainer_artifact)

        model_pusher_artifact = model_pusher.initiate_model_pusher()


    except Exception as e:
        print(e)

from sensor.predictor import ModelResolver
from sensor.entity.config_entity import ModelPusherConfig
from sensor.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ModelPusherArtifact
from sensor.exception import SensorException
import os, sys
from sensor.utils import load_object, save_object
import logging


class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig,
                 data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_artifact: ModelTrainerArtifact):
        logging.info("-------Model Pusher -------")
        try:
            self.model_pusher_config = model_pusher_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_pusher(self, ) -> ModelPusherArtifact:
        try:
            # Load objects
            logging.info("Loading transformed model & target encoder")
            transformer = load_object(file_path=self.data_transformation_artifact.transformed_object_path)
            model = load_object(file_path=self.model_trainer_artifact.model_path)
            target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)

            # Model pusher dir
            logging.info("Saving Model to model-pusher dir")
            save_object(file_path=self.model_pusher_config.pusher_transformer_path, obj=transformer)
            save_object(file_path=self.model_pusher_config.pusher_model_path, obj=model)
            save_object(file_path=self.model_pusher_config.pusher_target_encoder_path, obj=target_encoder)

            # Saved model dir
            logging.info("Saving Model to saved-models dir")
            transformer_path = self.model_resolver.get_latest_save_transformer_path()
            model_path = self.model_resolver.get_latest_save_model_path()
            target_encoder_path = self.model_resolver.get_latest_save_encoder_path()

            save_object(file_path=transformer_path, obj=transformer)
            save_object(file_path=model_path, obj=model)
            save_object(file_path=target_encoder_path, obj=target_encoder)

            model_pusher_artifact = ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.pusher_model_dir,
                                                        saved_model_dir=self.model_pusher_config.saved_model_dir)
            logging.info(f"Model Pusher Artifact {model_pusher_artifact}")

            return model_pusher_artifact


        except Exception as e:
            raise SensorException(e, sys)

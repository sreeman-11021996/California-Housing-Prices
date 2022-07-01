from housing.entity.config_entity import DataIngestionConfig, \
DataValidationConfig,DataTransformationConfig,ModelTrainerConfig, \
ModelEvaluationConfig,ModelPusherConfig,TrainingPipelineConfig
#from housing.entity.config_entity import *
from housing.util.util import read_yaml_file
from housing.logger import logging
import os,sys
from housing.constant import *
from housing.exception import HousingException


class Configuration:
    
    def __init__ (self,config_file_path:str =CONFIG_FILE_PATH,
        current_time_stamp:str = CURRENT_TIME_STAMP) -> None:
        try:
            self.config_info  = read_yaml_file(file_path=config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
        
            artifact_dir = self.training_pipeline_config.artifact_dir
            
            data_ingestion_artifact_dir=os.path.join(
                artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                self.time_stamp
            )
            
            data_ingestion_info:dict = self.config_info[DATA_INGESTION_CONFIG_KEY]
            
            dataset_download_url = data_ingestion_info[
                DATA_INGESTION_DOWNLOAD_URL_KEY]
            
            tgz_download_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY]
            )
            
            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY]
            )

            ingested_data_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY]
            )
            
            ingested_train_dir = os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY]
            )
            ingested_test_dir =os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY]
            )


            data_ingestion_config = DataIngestionConfig(
                dataset_download_url=dataset_download_url, 
                tgz_download_dir=tgz_download_dir, 
                raw_data_dir=raw_data_dir, 
                ingested_train_dir=ingested_train_dir, 
                ingested_test_dir=ingested_test_dir
            )
            
            logging.info(f"Data Ingestion config: {data_ingestion_config}")
            return data_ingestion_config
        
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            
            data_validation_artifact_dir=os.path.join(
                artifact_dir,
                DATA_VALIDATION_ARTIFACT_DIR,
                self.time_stamp
            )
            
            data_validation_info:dict = self.config_info[
                DATA_VALIDATION_CONFIG_KEY]
            schema_file_name = data_validation_info[
                DATA_VALIDATION_SCHEMA_FILE_NAME_KEY]
            
            schema_file_path = os.path.join(
                data_validation_artifact_dir,
                schema_file_name
            )
            
            data_validation_config = DataValidationConfig(
                schema_file_path=schema_file_path
            )
            
            logging.info(f"Data Validation config: {data_validation_config}")
            return data_validation_config
        
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def get_data_tranformation_config(self)->DataTransformationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            
            data_transformation_artifact_dir=os.path.join(
                artifact_dir,
                DATA_TRANSFORMATION_ARTIFACT_DIR,
                self.time_stamp
            )
            
            data_transformation_info:dict = self.config_info[
                DATA_TRANSFORMATION_CONFIG_KEY]
            
            add_bedroom_per_room = data_transformation_info[
                DATA_TRANSFORMATION_ADD_BEDROOM_PER_ROOM_KEY]
            transformed_dir = os.path.join(data_transformation_artifact_dir,
                data_transformation_info[
                DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY])
            transformed_train_dir = os.path.join(transformed_dir,
                data_transformation_info[
                DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY])
            transformed_test_dir = os.path.join(transformed_dir,
                data_transformation_info[
                DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY])
            preprocessing_dir = os.path.join(data_transformation_artifact_dir,
                data_transformation_info[
                DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY])
            preprocessed_object_file_name = data_transformation_info[
                DATA_TRANSFORMATION_PREPROCESSING_OBJECT_FILE_NAME_KEY]
            preprocessed_object_file_path = os.path.join(preprocessing_dir,
                preprocessed_object_file_name)
            
            data_transformation_config = DataTransformationConfig(
                add_bedroom_per_room=add_bedroom_per_room,
                transformed_train_dir=transformed_train_dir,
                transformed_test_dir=transformed_test_dir,
                preprocessed_object_file_path=preprocessed_object_file_path
            )
            
            logging.info(f"Data Transformation config: {data_transformation_config}")
            return data_transformation_config

        except Exception as e:
            raise HousingException(e,sys) from e
        
    def get_model_trainer_config(self)->ModelTrainerConfig:
        try:
            
            artifact_dir = self.training_pipeline_config.artifact_dir
            
            model_trainer_artifact_dir=os.path.join(
                artifact_dir,
                MODEL_TRAINER_ARTIFACT_DIR,
                self.time_stamp
            )
            
            model_trainer_info:dict = self.config_info[
                MODEL_TRAINER_CONFIG_KEY]
            trained_model_dir = os.path.join(model_trainer_artifact_dir,
                model_trainer_info[MODEL_TRAINER_TRAINED_MODEL_DIR_KEY])
            model_file_name = model_trainer_info[MODEL_TRAINER_MODEL_FILE_NAME_KEY]
            trained_model_file_path = os.path.join(trained_model_dir,
                model_file_name)
            base_accuracy = model_trainer_info[MODEL_TRAINER_BASE_ACCURACY_KEY]
            
            model_trainer_config = ModelTrainerConfig(
                trained_model_file_path=trained_model_file_path,
                base_accuracy=base_accuracy
            )
            
            logging.info(f"Model Trainer config: {model_trainer_config}")
            return model_trainer_config
            
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def get_model_evaluation_config(self)->ModelEvaluationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            
            model_evaluation_artifact_dir=os.path.join(
                artifact_dir,
                MODEL_EVALUATION_ARTIFACT_DIR,
                self.time_stamp
            )
            
            model_evaluation_info:dict = self.config_info[
                MODEL_EVALUATION_CONFIG_KEY]
            
            model_evaluation_file_name = model_evaluation_info[
                MODEL_EVALUATION_MODEL_EVALUATION_FILE_NAME_KEY]
            
            model_evaluation_file_path = os.path.join(
                model_evaluation_artifact_dir,model_evaluation_file_name)
            
            model_evaluation_config = ModelEvaluationConfig(
                model_evaluation_file_path=model_evaluation_file_path,
                time_stamp=self.time_stamp
            )
            
            logging.info(f"Model Evaluation config: {model_evaluation_config}")
            return model_evaluation_config
            
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def get_model_pusher_config(self)->ModelPusherConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            
            model_pusher_artifact_dir=os.path.join(
                artifact_dir,
                MODEL_PUSHER_ARTIFACT_DIR,
                self.time_stamp
            )
            
            model_pusher_info:dict = self.config_info[
                MODEL_PUSHER_CONFIG_KEY]
            
            model_export_dir_path = os.path.join(model_pusher_artifact_dir,
                model_pusher_info[MODEL_PUSHER_MODEL_EXPORT_DIR_KEY]
                )
            
            model_pusher_config = ModelPusherConfig(
                model_export_dir_path=model_export_dir_path
                )
            
            logging.info(f"Model Pusher config: {model_pusher_config}")
            return model_pusher_config
            
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        
        try:
            training_pipeline_config_dict = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            
            artifact_dir = os.path.join(ROOT_DIR,
            training_pipeline_config_dict[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config_dict[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
            )

            training_pipeline_config = TrainingPipelineConfig(
                artifact_dir=artifact_dir)
            logging.info(f"Training Pipleine config: {training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise HousingException(e,sys) from e
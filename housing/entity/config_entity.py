from collections import namedtuple

# all the config info is provided through .yaml file

# ..............................................................................

DataIngestionConfig = namedtuple("DataIngestionConfig",
["dataet_download_url","tgz_download_dir","raw_data_dir","ingested_train_dir",
"ingested_testdir"])

# dataet_download_url ->  Download url for data
# tgz_download_dir -> Download folder (Compressed file)
# raw_data_dir -> Extract folder (Extracted file)
# ingested_train_dir -> Train Dataset Folder
# ingested_testdir -> Test Dataset Folder

# ..............................................................................

DataValidationConfig = namedtuple("DataValidationConfig",["schema_file_path"])

# ..............................................................................

DataTransformationConfig = namedtuple("DataTransformationConfig",
["add_bedroom_per_room","transformed_train_dir","transformed_test_dir",
"preprocessed_oject_file_path"])

# transformed_train_dir -> train_trf.csv
# transformed_test_dir  -> test_trf.csv
# preprocessed_oject_file_path -> trf.pkl

# ..............................................................................

ModelTrainingConfig = namedtuple("ModelTrainingConfig",
["trained_model_file_path","base_accuracy"])

# base_accuracy -> expectation
# trained_model_file_path -> model.pkl

# ..............................................................................

ModelEvaluationConfig = namedtuple("ModelEvaluationConfig",
["model_evaluation_file_path","time_stamp"])

# model_evaluation_file_path -> file path for model in production
# time_stamp -> at what time have we compared the model

# ..............................................................................

ModelPusherConfig = namedtuple("ModelPusherConfig",["export_dir_path"])
# export_dir_path -> where to export our new model

# ..............................................................................

from housing.constant import SCHEMA_COLUMNS_KEY, SCHEMA_DOMAIN_VALUE_KEY
from housing.entity.config_entity import DataValidationConfig
from housing.logger import logging
from housing.exception import HousingException
import os,sys
from housing.entity.artifact_entity import DataIngestionArtifact,\
    DataValidationArtifact
from housing.util.util import read_yaml_file
import pandas as pd


class DataValidation:
    
    def __intt__(self,data_validation_config: DataValidationConfig,
                 data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'='*20}Data Validation log started.{'='*20} ")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config

        except Exception as e:
            raise HousingException(e,sys) from e
        
    def get_train_and_test_dataset (self):
        try:
            # get the data sets
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)
            
            logging.info(f"Train & Test Dataset loaded")
            return train_df,test_df     
        
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def check_train_and_test_file_exists (self)->bool:
        try:
            data_exists = False
            
            # get the data file paths
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            # check if the file paths are valid
            if os.path.exists(train_file_path) and os.path.exists(test_file_path):
                data_exists = True
            else:
                message = f"Train path : [{train_file_path}] \n Test path : "
                "[{test_file_path}] \n Check : One or Both are Missing"
                raise Exception(message)
            
            logging.info(f"Train & Test data Check is Completed \n " 
            "Train path : [{train_file_path}] \n Test path : [{test_file_path}]")    
            return data_exists

        except Exception as e:
            raise HousingException(e,sys) from e
        
    def validate_num_columns(self):
        try:
            validate_num_columns = False
            no_col_schema = len(self.schema[SCHEMA_COLUMNS_KEY])
            no_col_train_df = len(self.train_df.columns)
            no_col_test_df = len(self.test_df.columns)
            if (no_col_schema==no_col_train_df) and (no_col_schema==no_col_test_df):
                validate_num_cols = True
            
            logging.info(f"Number of Columns Check: Passed")
            return validate_num_columns                
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def validate_column_names(self):
        try:
            validate_column_names = False
            for column in self.train_df.columns:
                if not column in self.schema[SCHEMA_COLUMNS_KEY]:
                    message = f"{column} not in schema file"
                    raise Exception(message)
            validate_column_names = True
            
            logging.info(f"Column Names Check: Passed")
            return validate_column_names
            
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def validate_domain_values (self):
        try:
            validate_domain_values = False
            for column,category_list in self.schema[SCHEMA_DOMAIN_VALUE_KEY]. \
                items():
                for category in self.train_df[column].unique():
                    if category not in category_list:
                        message = f"[{column}] column does not accept <{category}>"
                        "in schema"
                        raise Exception(message)
            validate_domain_values = True
            
            logging.info(f"Domain Values Check: Passed")    
            return validate_domain_values
        
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def validate_column_dtypes (self):
        try:
            pass
        except Exception as e:
            raise HousingException(e,sys) from e
        
        
    def validate_schema (self):
        try:

            schema_file_path = self.data_validation_config.schema_file_path
            # read the schema
            self.schema = read_yaml_file(file_path=schema_file_path)
            # get the train & test data
            self.train_df,self.test_df =self.get_train_and_test_dataset()            
            
            #1. Number of Column
            self.validate_num_columns()
            
            #2. Check column names
            self.validate_column_names()
            
            #3. Check the value of ocean proximity 
            self.validate_domain_values()
            
            #4. check dtypes of columns
            
             
            
        
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def initiate_validation(self) -> DataValidationArtifact:
        try:
            self.check_train_and_test_file_exists()
            
            schema_file_path = None
            report_file_path = None
            report_page_file_path = None
            message = None
            
            data_validation_artifact = DataValidationArtifact(
                schema_file_path=schema_file_path,
                report_file_path=report_file_path,
                report_page_file_path=report_page_file_path,
                is_validated=True,
                message=message
            )
            
            return data_validation_artifact
        
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def __del__(self):
        logging.info(f"{'='*20}Data Validation log completed.{'='*20} \n\n")
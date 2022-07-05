from housing.entity.config_entity import DataIngestionConfig
import sys,os
from housing.exception import HousingException
from housing.logger import logging
from housing.entity.artifact_entity import DataIngestionArtifact
import tarfile  # to download url
import numpy as np
#from six.moves import urllib    # to extract tdz file
from urllib import request # to extract tdz file
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit

class DataIngestion:
    
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'='*20}Data Ingestion log started.{'='*20} ")
            self.data_ingestion_config = data_ingestion_config
            
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def download_housing_data(self,) -> str:
        try:
            #extraction remote url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url

            #folder location to download file
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir
            
            # clear the folder if it already exists 
            # housing\\artifact\\data_ingestion\\<time_stamp>\\tgz_data -> folder
            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)
            
            # make a new folder if not exists
            os.makedirs(tgz_download_dir,exist_ok=True)

            # get the file name from url
            housing_file_name = os.path.basename(download_url)

            # make the file path
            tgz_file_path = os.path.join(tgz_download_dir, housing_file_name)
            
            # extract data into the file path
            logging.info(f"Downloading file from :[{download_url}] into "
                         ":[{tgz_file_path}]")
            
            request.urlretrieve(download_url, tgz_file_path)
            logging.info(f"File :[{tgz_file_path}] has been downloaded "
                         "successfully.")
            return tgz_file_path
        
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def extract_tgz_file(self,tgz_file_path:str):
        try:
            # folder location to extract the file
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            
            # clear the folder if it already exists 
            # housing\\artifact\\data_ingestion\\<time_stamp>\\raw_data -> folder
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
                
            # create the folder -> raw_data
            os.makedirs(raw_data_dir,exist_ok=True)
            
            # Extract the raw_data from tdz_data
            logging.info(f"Extracting tgz file: [{tgz_file_path}] into dir: "
                         "[{raw_data_dir}]")
            with tarfile.open(tgz_file_path) as housing_tgz_file_obj:
                housing_tgz_file_obj.extractall(path=raw_data_dir)
            logging.info(f"Extraction completed")
            
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            file_name = os.listdir(raw_data_dir)[0]
            # get the path to .csv file
            housing_file_path = os.path.join(raw_data_dir,file_name)

            logging.info(f"Reading csv file: [{housing_file_path}]")
            housing_data_frame = pd.read_csv(housing_file_path)

            # Stratify split by "median_income" column
            housing_data_frame["income_cat"] = pd.cut(
                housing_data_frame["median_income"],
                bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
                labels=[1,2,3,4,5]
            )
            
            logging.info(f"Splitting data into train and test")

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, 
                    random_state=42)

            for train_index,test_index in split.split(housing_data_frame, housing_data_frame["income_cat"]):
                strat_train_set = housing_data_frame.loc[train_index].drop([
                    "income_cat"],axis=1)
                strat_test_set = housing_data_frame.loc[test_index].drop([
                    "income_cat"],axis=1)
            
            # get the file_paths for train & test
            train_file_path = os.path.join(
                self.data_ingestion_config.ingested_train_dir,file_name)
            test_file_path = os.path.join(
                self.data_ingestion_config.ingested_test_dir,file_name)
            
            # Export train & test to their respective folders
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,
                    exist_ok=True)
                logging.info(f"Exporting training datset to file: ["
                    "{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, 
                    exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)
            

            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=train_file_path,
                test_file_path=test_file_path,
                is_ingested=True,
                message=f"Data ingestion completed successfully."
                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact
            
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            tgz_file_path = self.download_housing_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            data_ingestion_artifact = self.split_data_as_train_test()
            
            return data_ingestion_artifact
        
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def __del__(self):
        logging.info(f"{'='*20}Data Ingestion log completed.{'='*20} \n\n")
         
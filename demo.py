from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingException
from housing.logger import logging
from housing.config.configuration import Configuration
from housing.component.data_validation import DataValidation
from housing.component.data_ingestion import DataIngestion

def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()
        #data_validation_config = Configuration().get_data_validation_config()
        #data_ingestion_config=Configuration().get_data_ingestion_config()
        # print(data_validation_config)
        #data_ingestion = DataIngestion(data_ingestion_config)
        #data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        #data_validation = DataValidation(
            #data_validation_config=data_validation_config,
            #data_ingestion_artifact=data_ingestion_artifact)
        
        #data_validation.initiate_validation()

    except Exception as e:
        logging.error(f"{e}")
        print(e)
        
        
if __name__=="__main__":
    main()
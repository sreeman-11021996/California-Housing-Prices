from cgitb import html
import yaml
import json
from housing.exception import HousingException
import os,sys
from housing.logger import logging

def read_yaml_file (file_path:str) -> dict:
    """
    Reads a YAML file and returns the contents as a dictionary
    file_path: str
    """
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HousingException(e,sys) from e
    
def save_json_file(file_path:str,file:json):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        # Save the file in file_path
        with open(file_path, "w") as json_file:
            json.dump(file,json_file,indent=6)
        logging.info(f"{file} saved at {file_path}")
    except Exception as e:
        raise HousingException(e,sys) from e
    
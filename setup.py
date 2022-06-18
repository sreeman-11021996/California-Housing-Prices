from setuptools import setup,find_packages
from typing import List


# Declaring variables on setup functinos
PROJECT_NAME = "housing-predictor"
VERSION = "0.0.1"
AUTHOR = "Srinivaas"
DESCRIPTION = "This is the first FSDS Nov batch Machine Learning Project"
PACKAGES = ["housing"]
# PACKAGES = find_packages()
REQUIREMENT_FILE_NAME = "requirements.txt"

# def function()-><return_var.>:
# List(data_type) -> we can specify the dtype of elements 
def get_requirements_list()->List[str]:
    """
    Description: This function is going to return a list of 
    requirement mentioned in requirements.txt file

    Returns:
        List[str] : list of requirement mentioned in requirements.txt file
        ex.["numpy","pandas",...]
    """

    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        return requirement_file.readlines().remove("-e .")
    # we are removing  "-e ." because we are using PACKAGES in setup


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=PACKAGES,
    install_requires=get_requirements_list()
)

if __name__ == "__main__":
    print(get_requirements_list())
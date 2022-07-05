from collections import namedtuple


DataIngestionArtifact = namedtuple("DataIngestionArtifact",
[ "train_file_path", "test_file_path", "is_ingested", "message"])

DataValidationArtifact = namedtuple("DataValidationArtifact",
["schema_file_path", "report_file_path", "report_page_file_path", "is_validated", 
 "message"])
# we can have a report mentioning the results of all validation to be dropped or
# imputed in Transformation Phase
# Then we can have it detect duplicates,missing_values,outliers
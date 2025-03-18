from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    X_train_file_path:str
    X_test_file_path:str
    y_train_file_path:str
    y_test_file_path:str

    #trained_file_path:str
    #test_file_path:str
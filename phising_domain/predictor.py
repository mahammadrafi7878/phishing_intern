import os 
from phising_domain.exception import PhisingException 
from phising_domain.logger import logging 
from phising_domain.entity.config_entity import TRANSFER_OBJECT_FILE_NAME,MODEL_FILE_NAME
from glob import glob 
from typing import Optional 



class ModelResolver:
    def __init__(self,model_registery:str="saved_models",transformer_dir_name="transformer",model_dir_name='model'):
        try:
            self.model_registery=model_registery
            os.makedirs(self.model_registery,exist_ok=True)
            self.transformer_dir_name=transformer_dir_name
            self.model_dir_name=model_dir_name
        except Exception as e:
            raise PhisingException(e,sys)   

    def get_latest_dir_path(self):
        try:
            dir_names=os.listdir(self.model_registery)
            if len(dir_names)==0:
                return None
            dir_names=listr(map(int,dir_names))
            latest_dir_name=max(dir_names)
            return os.path.join(self.model_registery,f"{latest_dir_name}")
        except Exception as e:
            raise PhisingException(e, sys)


    def get_latest_model_path(self):
        try:
            latest_dir=self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception("there are no saved models")
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME) 
        except Exception as e:
            raise PhisingException(e,sys)


    def get_latest_transformer_path(self):
        try:
            latest_dir=self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception("there are no saved models")
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFER_OBJECT_FILE_NAME)
        except Exception as e:
            raise PhisingException(e,sys)

    
    def get_latest_save_dir_path(self):
        try:
            latest_dir=self.get_latest_dir_path()
            if latest_dir is None:
                return os.path.join(self.model_registery,f"{0}")
            latest_dir_num=int(os.path.basename(self.get_latest_dir_path()))
            return os.path.join(self.model_registery,f"{latest_dir_num+1}") 
        except Exception as e:
            raise PhisingException(e,sys) 

    def get_latest_save_model_path(self):
        try:
            latest_dir=self.get_latest_save_dir_path() 
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise PhisingException(e,sys) 

    def get_latest_save_transformer_path(self):
        try:
            latest_dir=self.get_latest_save_dir_path()
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFER_OBJECT_FILE_NAME) 
        except Exception as e:
            raise PhisingException(e, sys)
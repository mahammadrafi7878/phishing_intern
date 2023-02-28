from phising_domain.logger import logging 
from phising_domain.exception import PhisingException 
from phising_domain.entity import config_entity,artifact_entity
import os,sys 
import yaml
from scipy.stats import ks_2samp
from typing import Optional 
import pandas as pd 
import numpy as np 
from phising_domain import utils


class DataValidation:
    def __init__(self,data_validation_config:config_entity.DataValidationConfig,data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.validation_error=dict()
        except Exception as e:
            raise PhisingException(e,sys)


    def is_required_columns_exist(self,base_df,current_df,report_key_name):
        try:
            base_columns=base_df.columns 
            current_columns=current_df.columns 
            missing_columns=[]
            for base_column in base_columns:
                if base_column not in current_columns:
                    missing_columns.append(base_column)

                if len(missing_columns)>0:
                    self.validation_error[report_key_name]=missing_columns
                    return False 
                return True
        except Exception as e:
            raise PhisingException(e,sys)    


    

    def data_drift(self,base_df,current_df,report_key_name):
        try:
            drift_report=dict()
            base_columns=base_df.columns 
            current_columns=current_df.columns

            for base_column in base_columns:
                base_data,current_data=base_df[base_column],current_df[base_column]

                same_distribution=ks_2samp(base_data,current_data)

                if same_distribution.pvalue>0.05:
                    drift_report[base_column]={
                    "pvalues":float(same_distribution.pvalue),
                    "same_distribution":True}

                else:
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":False
                    }

            self.validation_error[report_key_name]=drift_report
        except Exception as e:
            raise PhisingException(e,sys) 


    
    def initiate_data_validation(self):
        try:
            base_df=pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na":np.NAN},inplace=True)
            base_df.drop_duplicates()

            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #exclude_columns=['phishing']
            #base_df=utils.convert_columns_float(df=base_df,exclude_columns=exclude_columns)
            #train_df=utils.convert_columns_float(df=train_df,exclude_columns=exclude_columns)
            #test_df=utils.convert_columns_float(df=test_df,exclude_columns=exclude_columns)


            train_df_column_status=self.is_required_columns_exist(base_df=base_df,current_df=train_df,report_key_name="missing_columns_within_trainset")
            test_df_column_status=self.is_required_columns_exist(base_df=base_df,current_df=test_df,report_key_name="missing_columns_within_test_dataset")


            if train_df_column_status:
                self.data_drift(base_df=base_df,current_df=train_df,report_key_name="data_drift_with_in_train")
            if test_df_column_status:
                self.data_drift(base_df=base_df,current_df=test_df,report_key_name="data_drift_with_in_test")


            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,data=self.validation_error)

            data_validation_artifact=artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path)

            return data_validation_artifact
        except Exception as e:
            raise PhisingException(e,sys)
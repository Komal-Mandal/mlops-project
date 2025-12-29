import os
import sys
import pickle
from io import StringIO
from typing import Union, List

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from pandas import DataFrame, read_csv
from mypy_boto3_s3.service_resource import Bucket

from src.logger import logging
from src.exception import MyException
from src.configuration.aws_connection import S3Client


class SimpleStorageService:
    """
    Production-safe AWS S3 Storage Service for MLOps pipelines.
    """

    def __init__(self):
        try:
            # Centralized AWS connection
            s3_client = S3Client()

            self.s3_resource = s3_client.s3_resource
            self.s3_client = s3_client.s3_client

            logging.info("Initialized SimpleStorageService")

        except Exception as e:
            raise MyException(e, sys)

    # ==========================================================
    # Bucket & Object Utilities
    # ==========================================================

    def get_bucket(self, bucket_name: str) -> Bucket:
        try:
            return self.s3_resource.Bucket(bucket_name)
        except Exception as e:
            raise MyException(e, sys)

    def s3_key_path_available(self, bucket_name: str, s3_key: str) -> bool:
        try:
            bucket = self.get_bucket(bucket_name)
            return any(bucket.objects.filter(Prefix=s3_key))
        except Exception as e:
            raise MyException(e, sys)

    def get_file_object(self, filename: str, bucket_name: str):
        """
        Used ONLY for CSV / small files
        """
        try:
            bucket = self.get_bucket(bucket_name)
            objects = list(bucket.objects.filter(Prefix=filename))

            if not objects:
                raise FileNotFoundError(f"{filename} not found in {bucket_name}")

            return objects[0] if len(objects) == 1 else objects

        except Exception as e:
            raise MyException(e, sys)

    # ==========================================================
    # READ OPERATIONS
    # ==========================================================

    @staticmethod
    def read_object(
        object_name,
        decode: bool = True,
        make_readable: bool = False
    ) -> Union[StringIO, str, bytes]:
        """
        Used ONLY for CSV / text files
        """
        try:
            content = object_name.get()["Body"].read()
            if decode:
                content = content.decode()
            return StringIO(content) if make_readable else content
        except Exception as e:
            raise MyException(e, sys)

    def read_binary_object(self, bucket_name: str, key: str) -> bytes:
        """
        SAFE method for reading ML models (.pkl)
        """
        try:
            response = self.s3_client.get_object(
                Bucket=bucket_name,
                Key=key
            )
            return response["Body"].read()
        except Exception as e:
            raise MyException(e, sys)

    # ==========================================================
    # MODEL OPERATIONS
    # ==========================================================

    def load_model(self, model_name: str, bucket_name: str, model_dir: str = None):
        """
        Loads ML model from S3 safely (NO TIMEOUTS)
        """
        try:
            model_key = f"{model_dir}/{model_name}" if model_dir else model_name

            logging.info(f"Loading model from S3: {bucket_name}/{model_key}")

            model_bytes = self.read_binary_object(
                bucket_name=bucket_name,
                key=model_key
            )

            model = pickle.loads(model_bytes)

            logging.info("Model loaded successfully from S3")
            return model

        except Exception as e:
            raise MyException(e, sys)

    # ==========================================================
    # WRITE OPERATIONS
    # ==========================================================

    def create_folder(self, folder_name: str, bucket_name: str):
        try:
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=f"{folder_name}/"
            )
        except Exception as e:
            raise MyException(e, sys)

    def upload_file(
        self,
        from_filename: str,
        to_filename: str,
        bucket_name: str,
        remove: bool = True
    ):
        try:
            logging.info(f"Uploading {from_filename} → s3://{bucket_name}/{to_filename}")

            self.s3_client.upload_file(
                Filename=from_filename,
                Bucket=bucket_name,
                Key=to_filename
            )

            if remove:
                os.remove(from_filename)

            logging.info("File upload successful")

        except Exception as e:
            raise MyException(e, sys)

    def upload_df_as_csv(
        self,
        data_frame: DataFrame,
        local_filename: str,
        bucket_filename: str,
        bucket_name: str
    ):
        try:
            data_frame.to_csv(local_filename, index=False)
            self.upload_file(local_filename, bucket_filename, bucket_name)
        except Exception as e:
            raise MyException(e, sys)

    # ==========================================================
    # CSV OPERATIONS
    # ==========================================================

    def get_df_from_object(self, object_) -> DataFrame:
        try:
            content = self.read_object(object_, make_readable=True)
            return read_csv(content)
        except Exception as e:
            raise MyException(e, sys)

    def read_csv(self, filename: str, bucket_name: str) -> DataFrame:
        try:
            csv_obj = self.get_file_object(filename, bucket_name)
            return self.get_df_from_object(csv_obj)
        except Exception as e:
            raise MyException(e, sys)

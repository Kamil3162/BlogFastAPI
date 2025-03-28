from datetime import datetime

import boto3
from botocore.exceptions import (
    ClientError,
    NoCredentialsError,
    ParamValidationError
)
import logging
import os

class S3Client:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        region: str,
        bucket_name: str
    ):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.bucket_name = bucket_name
        self.setup_logging()
        self.logger = logging.getLogger(__name__)

    def setup_logging(self):
        """
        Configure logging to write to both a file and console.
        The log file will be created in a 'logs' directory with the current date.
        """
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Create a formatter for our log messages
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Set up file handler to write logs to a file
        log_filename = f"logs/s3_client_{datetime.now().strftime('%Y_%m_%d')}.log"
        file_handler = logging.FileHandler(log_filename)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        # Set up console handler to write logs to console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)

        # Get the root logger and add our handlers
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)

        # Remove existing handlers to avoid duplicates
        root_logger.handlers = []

        # Add our handlers
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

    def initialise_client(self):
        try:
            # initialize the s3 client
            self.client = boto3.client(
                's3',
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region,
            )
            self.client.head_bucket(Bucket=self.bucket_name)
            self.logger.info("Successfully initialised S3 client")
        except Exception as e:
            print(e)
            print(type(e))

    def s3_list_objects(self):
        s3_objects = self.client.list_objects(Bucket=self.bucket_name)
        try:
            print(s3_objects.get('Contents'))
        except KeyError as e:
            print("Dict have a following key")


S3Instance = S3Client(

)

S3Instance.initialise_client()
S3Instance.s3_list_objects()
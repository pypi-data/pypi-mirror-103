# pylint: disable=logging-fstring-interpolation, too-many-nested-blocks, too-few-public-methods

import json
import logging
import os
from datetime import datetime

import boto3
import pandas as pd
import yaml

from data_tap.utils import _log_level


def write_to_s3(bucket, key, data, **kwargs):
    """
    A simple method to write data to s3.
    :bucket: str. name of the bucket.
    :key: str. key path of the object (excluding object name)
    :data: dict. data written to s3 as json

    :aws_access_key_id: AWS access key ID
    :aws_secret_access_key: AWS secret access key
    :aws_session_token: AWS temporary session token
    :region_name: Default region when creating new connections
    :botocore_session: Use this Botocore session instead of creating a new default one.
    :profile_name: The name of a profile to use. If not given, then the default profile is used.
    """

    logging.info('Writing data to S3')
    boto3_session = boto3.Session(**kwargs)
    s3_resource = boto3_session.resource('s3')

    now = datetime.now().strftime('%Y%m%d%H%M%S')
    key_path = f'{os.path.join(key, now)}.json'

    logging.info(f'Writing data to S3://{bucket}/{key}')
    s3_resource.Object(
        bucket, key_path
    ).put(Body=json.dumps(data))


class BaseTap:
    """
    Base Tap Class for the data tap module.
    """
    def __init__(self, **kwargs):
        self.creds_file = kwargs.get('creds_file')
        self.config_file = kwargs.get('config_file')

        self.creds = self._load_file(self.creds_file)
        self.config = self._load_file(self.config_file)

        logging.basicConfig(
            level=_log_level(kwargs.get('log_level', 'info')),
            format="[DATA-TAP] %(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(kwargs.get('log_file', 'debug.log')),
                logging.StreamHandler(),
            ]
        )

    @staticmethod
    def _load_file(file_name):
        try:
            extension = file_name.split('.')[-1]
            if extension in ['yaml', 'yml']:
                with open(file_name, 'r') as file_data:
                    return yaml.safe_load(file_data)
            if extension in ['json']:
                with open(file_name, 'r') as file_data:
                    return json.load(file_data)
            if extension in ['csv']:
                return pd.read_csv(file_name).to_dict(orient='records')[0]
            return file_name
        except AttributeError:
            return file_name

    def _return_creds(self):
        return self.creds

    def _return_config(self):
        return self.config

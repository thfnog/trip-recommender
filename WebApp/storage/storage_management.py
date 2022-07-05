import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError


class storage_management(object):
    load_dotenv()
    ACCESS_KEY = os.environ.get('ACCESS_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    REGION_NAME = os.environ.get('REGION_NAME')

    s3 = boto3.client('s3', region_name=REGION_NAME, aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    def upload_to_s3(local_file, bucket, s3_file):
        print(f'uploading file : {s3_file} to bucket {bucket}')
        try:
            storage_management.s3.upload_file(local_file, bucket, s3_file)
            print('Upload Successful')
            return True
        except FileNotFoundError:
            print('The file was not found')
            return False
        except NoCredentialsError:
            print('Credentials not available')
            return False

    def download_from_s3(local_file_name, bucket, key):
        print(f'download file : {key} from bucket {bucket}')
        try:
            storage_management.s3.download_file(bucket, key, local_file_name)
            print('Download Successful')
            return True
        except FileNotFoundError:
            print('The file was not found')
            return False
        except NoCredentialsError:
            return False
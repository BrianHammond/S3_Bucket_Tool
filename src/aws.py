import boto3
from botocore.exceptions import ClientError

# Define your AWS credentials and region
access_key_id = 'EXAMPLEKEYEXAMPLEKEY'
secret_access_key = 'TESTTESTTESTTESTTESTTESTTESTTESTTESTTEST'
region = 'ap-northeast-1'

# Initialize the S3 client with credentials and region
s3 = boto3.client(
    's3',
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    region_name=region
)

# Your bucket name from the ARN
bucket_name = '123456789012-brian'

# Function to upload a file to S3
def upload_file(local_file_path, s3_file_name):
    try:
        s3.upload_file(local_file_path, bucket_name, s3_file_name)
        print(f"Success: Uploaded {local_file_path} to s3://{bucket_name}/{s3_file_name}")
    except FileNotFoundError:
        print(f"Error: The file {local_file_path} was not found.")
    except ClientError as e:
        print(f"Error uploading file: {e}")

# Function to download a file from S3
def download_file(s3_file_name, local_file_path):
    try:
        s3.download_file(bucket_name, s3_file_name, local_file_path)
        print(f"Success: Downloaded s3://{bucket_name}/{s3_file_name} to {local_file_path}")
    except ClientError as e:
        print(f"Error downloading file: {e}")

# Example usage
if __name__ == "__main__":
    # Upload example
    upload_file('test.txt', 'test.txt')  # Local file 'test.txt' -> S3 'test.txt'

    # Download example
    download_file('test.txt', 'downloaded_test.txt')  # S3 'test.txt' -> Local 'downloaded_test.txt'
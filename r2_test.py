import boto3
import os
from dotenv import load_dotenv

load_dotenv()

session = boto3.session.Session()

s3 = session.client(
    service_name='s3',
    region_name='auto',
    endpoint_url=os.getenv("R2_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("R2_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("R2_SECRET_ACCESS_KEY")
)

bucket_name = os.getenv("R2_BUCKET_NAME")

# Upload test
file_path = "test.txt"
with open(file_path, "w") as f:
    f.write("R2 Upload Check")

s3.upload_file(file_path, bucket_name, "test.txt")
print("Uploaded test.txt to R2!")

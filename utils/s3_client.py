import boto3

from django.conf import settings


class PublicS3Client:
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=settings.S3_PUBLIC_BUCKET_ACCESS_KEY,
            aws_secret_access_key=settings.S3_PUBLIC_BUCKET_SECRET_KEY,
        )
        self.bucket_name = settings.S3_PUBLIC_BUCKET_NAME

    def upload(self, file, s3_key, content_type=None):
        extra_args = {
            'ACL': 'public-read',
        }
        if content_type:
            extra_args['ContentType'] = content_type

        self.client.upload_fileobj(
            file,
            self.bucket_name,
            s3_key,
            ExtraArgs=extra_args
        )
        return f'https://{self.bucket_name}.s3.ap-northeast-2.amazonaws.com/{s3_key}'

def test():
    file_name = 'test.txt'
    key = 'data/test.txt'
    client = PublicS3Client()
    client.upload(open(file_name, 'rb'), key)
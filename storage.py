import boto3
import os
import requests

from config import BaseConfig


settings = BaseConfig()


class Storage:

    def upload_image_bytes_to_s3(
            self,
            image_bytes: bytes,
            storage_bucket: str,
            object_name: str | None = None
    ):
        # s3_client = boto3.client('s3')

        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_DEFAULT_REGION,
        )

        try:
            # some models provide image url and not bytes
            if isinstance(image_bytes, str) and image_bytes.startswith("http"):
                # download the bytes
                response = requests.get(image_bytes)
                response.raise_for_status()  # Ensure download was successful
                image_bytes = response.content

            # upload the bytes
            response = s3_client.put_object(
                Bucket=storage_bucket,
                Key=object_name,
                Body=image_bytes,
                ContentType="image/jpeg"
            )
        except Exception as e:
            print(f"Error uploading image bytes: {e}")
            return False
        
        return True
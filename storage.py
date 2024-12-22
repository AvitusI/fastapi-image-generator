import boto3
import os


class Storage:

    def upload_image_bytes_to_s3(
            self,
            image_bytes: bytes,
            storage_bucket: str,
            object_name: str | None = None
    ):
        s3_client = boto3.client('s3')

        try:
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
from typing import Dict

from django.conf import settings

import boto3


class ImagesService:

    def __init__(self) -> None:
        self.session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )

    def create_presigned_url(self, item_id: int, image_id: int) -> Dict:
        client = self.session.client("s3")
        url = client.generate_presigned_post(
            settings.AWS_BUCKET_NAME, f"/{item_id}/{image_id}", ExpiresIn=3600
        )
        return url

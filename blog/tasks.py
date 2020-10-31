import os
from . import celery, session
from .s3client import upload_video
from .models import Video


@celery.tasks(name='pipeline.upload')
def upload(video_id, local_path, path, field):
    upload_video(local_path, path)
    try:
        video = Video.query.get(video_id)
        video.update(
            **{field: f''}
        )
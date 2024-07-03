from tubemonitor.celery import app
from .services import update_channel_toplist, update_video_toplist


@app.task
def update_toplists_task():
    update_channel_toplist()
    update_video_toplist()
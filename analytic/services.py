from googleapiclient.discovery import build
from urllib.parse import urlparse
import os



def get_channel_data(parsed_url_str):
    API_KEY = os.environ.get('API_KEY')
    parsed_url = urlparse(parsed_url_str)
    path = parsed_url.path.strip('/')
    my_request = build('youtube', 'v3', developerKey=API_KEY)
    if path.startswith('channel/'):
        channel_id = path.split('/')[-1]
        data_api = my_request.channels().list(
            part='snippet,statistics',
            id=channel_id
        )
    else:
        if path.startswith(('c/', 'user/')):
            username = path.split('/')[-1]
        else:
            username = path.split('@')[-1]
        data_api = my_request.channels().list(
            part='snippet,statistics',
            forUsername=username
        )
    response = data_api.execute()
    channel_data = response['items'][0] if 'items' in response else None
    return channel_data


def get_video_data(parsed_url_str):
    API_KEY = os.environ.get('API_KEY')
    parsed_url = urlparse(parsed_url_str)
    if parsed_url.netloc == "youtu.be":
        path = parsed_url.path.strip('/')
    elif parsed_url.path == "/watch":
        path = parsed_url.query.strip('/v=')
    video_id = path.split('/')[-1]
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request_yt = youtube.videos().list(
        part='snippet,statistics',
        id=video_id
    )
    response = request_yt.execute()
    video_data = response['items'][0] if 'items' in response else None
    return video_data


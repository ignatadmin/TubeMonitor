from googleapiclient.discovery import build
from urllib.parse import urlparse
import os
from .models import *


def get_channel_data(parsed_url_str):
    parsed_url = urlparse(parsed_url_str)
    path = parsed_url.path.strip('/')
    API_KEY = os.environ.get('API_KEY')
    my_request = build('youtube', 'v3', developerKey=API_KEY)
    if path.startswith('channel/'):
        channel_id = path.split('/')[-1]
        data_api = my_request.channels().list(
            part='snippet,statistics,status',
            id=channel_id
        )
    else:
        if path.startswith(('c/', 'user/')):
            username = path.split('/')[-1]
            data_api = my_request.channels().list(
                part='snippet,statistics,status',
                forUsername=username
            )
        else:
            username = path.split('@')[-1]
            data_api = my_request.channels().list(
                part='snippet,statistics,status',
                forHandle=username
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
        part='snippet,statistics,status',
        id=video_id
    )
    response = request_yt.execute()
    video_data = response['items'][0] if 'items' in response else None
    return video_data


def get_toplist_videos():
    api_key = os.environ.get('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    playlist_id = 'PL11E57E1166929B60'
    playlist_items = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=10
    ).execute()

    def formatting(value_str):
        value = float(value_str)
        arr = [(0, ''), (3, ' тыс'), (6, ' млн'), (9, ' млрд'), (12, ' трлн')]
        for n, s in arr[::-1]:
            n = 10 ** n
            if value >= n:
                return str(round(value / n)) + s
        return str(value)

    videos_info = []
    for item in playlist_items['items']:
        video_id = item['snippet']['resourceId']['videoId']
        video_info = youtube.videos().list(
            part='snippet,contentDetails,statistics,status',
            id=video_id
        ).execute()

        snippet = video_info['items'][0]['snippet']
        statistics = video_info['items'][0]['statistics']
        status = video_info['items'][0]['status']

        info = {
            'published_at': snippet['publishedAt'],
            'channel_id': snippet['channelId'],
            'title': snippet['title'],
            'description': snippet['description'],
            'thumbnail': snippet['thumbnails']['default']['url'],
            'channel_title': snippet['channelTitle'],
            'category_id': snippet['categoryId'],
            'default_language': snippet['defaultLanguage'],
            'made_for_kids': status['madeForKids'],
            'view_count_formatting': formatting(statistics['viewCount']),
            'like_count_formatting': formatting(statistics['likeCount']),
            'comment_count_formatting': formatting(statistics['commentCount'])
        }

        channel_info = youtube.channels().list(
            part='snippet',
            id=info['channel_id']
        ).execute()

        info['channel_icon'] = channel_info['items'][0]['snippet']['thumbnails']['default']['url']

        videos_info.append(info)

    context = {'videos_info': videos_info}
    return context



def get_toplist_channels():
    queryset = TopChannels.objects.all()
    channels_info = []

    for top_channel in queryset:
        API_KEY = os.environ.get('API_KEY')
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request_yt = youtube.channels().list(
            part='snippet,statistics,status',
            id=top_channel.channel_id
        )
        response = request_yt.execute()
        channel_data = response['items'][0] if 'items' in response else None
        if channel_data:
            channels_info.append(channel_data)
    return channels_info

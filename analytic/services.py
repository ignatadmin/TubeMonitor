from googleapiclient.discovery import build
from urllib.parse import urlparse
from django.conf import settings
from .models import *


def get_channel_data(parsed_url_str):
    parsed_url = urlparse(parsed_url_str)
    path = parsed_url.path.strip('/')
    key = settings.API_KEY
    api_request = build('youtube', 'v3', developerKey=key)
    if path.startswith('channel/'):
        channel_id = path.split('/')[-1]
        request_data = api_request.channels().list(
            part='snippet,statistics,status',
            id=channel_id
        )
    else:
        if path.startswith(('c/', 'user/')):
            username = path.split('/')[-1]
            request_data = api_request.channels().list(
                part='snippet,statistics,status',
                forUsername=username
            )
        else:
            username = path.split('@')[-1]
            request_data = api_request.channels().list(
                part='snippet,statistics,status',
                forHandle=username
            )
    response = request_data.execute()
    channel_data = response['items'][0] if 'items' in response else None
    return channel_data


def get_video_data(parsed_url_str):
    key = settings.API_KEY
    parsed_url = urlparse(parsed_url_str)
    if parsed_url.netloc == "youtu.be":
        path = parsed_url.path.strip('/')
    elif parsed_url.path == "/watch":
        path = parsed_url.query.strip('/v=')
    video_id = path.split('/')[-1]
    api_request = build('youtube', 'v3', developerKey=key)
    video_request = api_request.videos().list(
        part='snippet,statistics,status',
        id=video_id
    )
    video_request_data = video_request.execute()
    if video_request_data:
        channel_id = video_request_data['items'][0]['snippet']['channelId']
        channel_request_data = api_request.channels().list(
            part='snippet',
            id=channel_id
        ).execute()
        thumbnail = channel_request_data['items'][0]['snippet']['thumbnails']
        channel_title = channel_request_data['items'][0]['snippet']['title']
    video_data = video_request_data['items'][0] if 'items' in video_request_data else None
    channel_data = {'thumbnail': thumbnail, 'channel_title': channel_title}
    return video_data, channel_data


def update_video_toplist():
    key = settings.API_KEY
    api_request = build('youtube', 'v3', developerKey=key)
    playlist_id = 'PL11E57E1166929B60'
    next_page_token = None
    counter = 0
    ListTopVideos.objects.all().delete()
    while counter < 100:
        playlist_items = api_request.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=25,
            pageToken=next_page_token
        ).execute()

        for item in playlist_items['items']:
            video_id = item['snippet']['resourceId']['videoId']

            # Проверяем, существует ли видео с таким же video_id в базе данных
            if ListTopVideos.objects.filter(video_id=video_id).exists():
                continue

            video_request_data = api_request.videos().list(
                part='snippet,contentDetails,statistics,status',
                id=video_id
            ).execute()

            if not video_request_data['items']:
                continue

            channel_id = video_request_data['items'][0]['snippet']['channelId']
            title = video_request_data['items'][0]['snippet']['title']
            thumbnail = video_request_data['items'][0]['snippet']['thumbnails']['default']['url']
            channel_title = video_request_data['items'][0]['snippet']['channelTitle']
            made_for_kids = video_request_data['items'][0]['status']['madeForKids']
            view_count = video_request_data['items'][0]['statistics']['viewCount']

            channel_request_data = api_request.channels().list(
                part='snippet',
                id=channel_id
            ).execute()

            channel_icon = channel_request_data['items'][0]['snippet']['thumbnails']['default']['url']

            ListTopVideos.objects.create(
                video_id=video_id,
                title=title,
                thumbnail=thumbnail,
                view_count=view_count,
                channel_icon=channel_icon,
                channel_id=channel_id,
                channel_title=channel_title,
                made_for_kids=made_for_kids
            )

            if not made_for_kids:
                counter += 1

        next_page_token = playlist_items.get('nextPageToken')
        if not next_page_token:
            break


def update_channel_toplist():
    queryset = ListTopChannels.objects.all()

    for top_channel in queryset:
        key = settings.API_KEY
        api_request = build('youtube', 'v3', developerKey=key)
        request_data = api_request.channels().list(
            part='snippet,statistics,status',
            id=top_channel.channel_id
        ).execute()
        channel_data = request_data['items'][0] if 'items' in request_data else None
        if channel_data:
            top_channel.title = channel_data['snippet']['title']
            top_channel.channel_icon = channel_data['snippet']['thumbnails']['default']['url']
            top_channel.thumbnails = channel_data['snippet']['thumbnails']['default']['url']
            top_channel.view_count = int(channel_data['statistics']['viewCount'])
            top_channel.subscriber_count = int(channel_data['statistics']['subscriberCount'])
            top_channel.video_count = int(channel_data['statistics']['videoCount'])
            top_channel.country = channel_data['snippet'].get('country', '')
            if 'status' in channel_data and 'madeForKids' in channel_data['status']:
                top_channel.made_for_kids = channel_data['status']['madeForKids']
            else:
                top_channel.made_for_kids = True
            top_channel.save()
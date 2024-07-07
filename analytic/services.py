from googleapiclient.discovery import build
from urllib.parse import urlparse
from django.conf import settings
from .models import ListTopVideos, ListTopChannels


def fetch_channel_data_by_id(api_request, channel_id):
    return api_request.channels().list(
        part='snippet,statistics,status',
        id=channel_id
    ).execute()


def fetch_channel_data_by_username(api_request, username):
    return api_request.channels().list(
        part='snippet,statistics,status',
        forUsername=username
    ).execute()


def fetch_channel_data_by_handle(api_request, handle):
    return api_request.channels().list(
        part='snippet,statistics,status',
        forHandle=handle
    ).execute()


def get_channel_data(parsed_url_str):
    """ По URL канала запрашивает данные у YouTube API и возвращает информацию о канале"""
    try:
        parsed_url = urlparse(parsed_url_str)
        path = parsed_url.path.strip('/')
        key = settings.YOUTUBE_API_KEY
        api_request = build('youtube', 'v3', developerKey=key)

        if path.startswith('channel/'):
            channel_id = path.split('/')[-1]
            response = fetch_channel_data_by_id(api_request, channel_id)
        elif path.startswith(('c/', 'user/')):
            username = path.split('/')[-1]
            response = fetch_channel_data_by_username(api_request, username)
        else:
            handle = path.split('@')[-1]
            response = fetch_channel_data_by_handle(api_request, handle)

        channel_data = response['items'][0] if 'items' in response else None
    except Exception as e:
        raise RuntimeError(f"Error fetching channel data: {e}")

    return channel_data


def fetch_video_data(api_request, video_id):
    return api_request.videos().list(
        part='snippet,statistics,status',
        id=video_id
    ).execute()


def fetch_channel_info(api_request, channel_id):
    return api_request.channels().list(
        part='snippet',
        id=channel_id
    ).execute()


def extract_video_id(parsed_url):
    if parsed_url.netloc == "youtu.be":
        return parsed_url.path.strip('/')
    elif parsed_url.path == "/watch":
        return parsed_url.query.split('v=')[-1]
    else:
        raise ValueError("Invalid URL format")


def get_video_data(parsed_url_str):
    """ По URL видео запрашивает данные у YouTube API и возвращает информацию о видео"""
    try:
        parsed_url = urlparse(parsed_url_str)
        video_id = extract_video_id(parsed_url)
        key = settings.YOUTUBE_API_KEY
        api_request = build('youtube', 'v3', developerKey=key)

        video_response = fetch_video_data(api_request, video_id)

        if not video_response.get('items'):
            raise ValueError("No video data found")

        video_item = video_response['items'][0]
        channel_id = video_item['snippet']['channelId']
        channel_response = fetch_channel_info(api_request, channel_id)

        thumbnail = channel_response['items'][0]['snippet']['thumbnails']
        channel_title = channel_response['items'][0]['snippet']['title']

        video_data = video_item
        channel_data = {'thumbnail': thumbnail, 'channel_title': channel_title}
    except Exception as e:
        raise RuntimeError(f"Error fetching video data: {e}")

    return video_data, channel_data


def process_video_item(api_request, item):
    """ Запрашивает данные о видео из плейлиста у YouTube API и возвращает информацию о видео """
    video_id = item['snippet']['resourceId']['videoId']

    if ListTopVideos.objects.filter(video_id=video_id).exists():
        return None

    video_response = fetch_video_data(api_request, video_id)

    if not video_response.get('items'):
        return None

    video_item = video_response['items'][0]
    channel_id = video_item['snippet']['channelId']
    title = video_item['snippet']['title']
    thumbnail = video_item['snippet']['thumbnails']['default']['url']
    channel_title = video_item['snippet']['channelTitle']
    made_for_kids = video_item['status'].get('madeForKids', True)
    view_count = video_item['statistics']['viewCount']

    channel_response = fetch_channel_info(api_request, channel_id)
    channel_icon = channel_response['items'][0]['snippet']['thumbnails']['default']['url']

    return {
        'video_id': video_id,
        'title': title,
        'thumbnail': thumbnail,
        'view_count': view_count,
        'channel_icon': channel_icon,
        'channel_id': channel_id,
        'channel_title': channel_title,
        'made_for_kids': made_for_kids
    }


def update_video_toplist():
    """
    Обновляет список топовых видео, загружая данные о видео из плейлиста YouTube
    Запрашивает данные у YouTube API и сохраняет их в базу данных
    """
    try:
        key = settings.YOUTUBE_API_KEY
        api_request = build('youtube', 'v3', developerKey=key)
        video_playlist = settings.TOP_VIDEO_PLAYLIST
        next_page_token = None
        counter = 0
        ListTopVideos.objects.all().delete()

        while counter < 100:
            playlist_response = api_request.playlistItems().list(
                part='snippet',
                playlistId=video_playlist,
                maxResults=25,
                pageToken=next_page_token
            ).execute()

            for item in playlist_response['items']:
                video_data = process_video_item(api_request, item)

                if video_data:
                    ListTopVideos.objects.create(**video_data)
                    if not video_data['made_for_kids']:
                        counter += 1

            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break
    except Exception as e:
        raise RuntimeError(f"Error updating video toplist: {e}")


def update_channel_data(api_request, top_channel):
    """ Обновляет данные канала в базе данных, запрашивая их у YouTube API """
    request_data = fetch_channel_data_by_id(api_request, top_channel.channel_id)
    channel_data = request_data['items'][0] if 'items' in request_data else None

    if channel_data:
        top_channel.title = channel_data['snippet']['title']
        top_channel.channel_icon = channel_data['snippet']['thumbnails']['default']['url']
        top_channel.thumbnails = channel_data['snippet']['thumbnails']['default']['url']
        top_channel.view_count = int(channel_data['statistics']['viewCount'])
        top_channel.subscriber_count = int(channel_data['statistics']['subscriberCount'])
        top_channel.video_count = int(channel_data['statistics']['videoCount'])
        top_channel.country = channel_data['snippet'].get('country', '')

        status = channel_data.get('status', {})
        top_channel.made_for_kids = status.get('madeForKids', True)

        top_channel.save()


def update_channel_toplist():
    """ Обновляет список топовых каналов, запрашивая данные у YouTube API и сохраняет их в базу данных """
    try:
        key = settings.YOUTUBE_API_KEY
        api_request = build('youtube', 'v3', developerKey=key)
        queryset = ListTopChannels.objects.all()

        for top_channel in queryset:
            update_channel_data(api_request, top_channel)
    except Exception as e:
        raise RuntimeError(f"Error updating channel toplist: {e}")

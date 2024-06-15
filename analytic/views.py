from googleapiclient.discovery import build
from django.shortcuts import render, redirect
from urllib.parse import urlparse
import os
import requests


def index(request):
    if request.method == 'POST':
        channel_url = request.POST.get('channel_url')
        parsed_url = urlparse(channel_url)
        path = parsed_url.path.strip('/')

        if path.startswith('channel/'):
            channel_id = path.split('/')[-1]
        else:
            username = path.split('@')[-1]
            api_key = os.environ.get('API_KEY')
            url = f'https://www.googleapis.com/youtube/v3/channels?part=id&forHandle={username}&key={api_key}'
            response = requests.get(url)
            data = response.json()
            channel_id = data['items'][0]['id']

        return redirect('channel', id=channel_id)
    return render(request, 'index.html')


def channel(request, id):
    API_KEY = os.environ.get('API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    request_yt = youtube.channels().list(
        part='snippet,statistics',
        id=id
    )

    response = request_yt.execute()
    channel_data = response['items'][0] if 'items' in response else None
    return render(request, 'channel.html', {'channel_data': channel_data})


def toplist(request):
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
            part='snippet,statistics',
            id=video_id
        ).execute()

        title = video_info['items'][0]['snippet']['title']
        thumbnail = video_info['items'][0]['snippet']['thumbnails']['default']['url']
        view_count_formatting = formatting(video_info['items'][0]['statistics']['viewCount'])
        channel_title = video_info['items'][0]['snippet']['channelTitle']
        channel_id = video_info['items'][0]['snippet']['channelId']
        channel_info = youtube.channels().list(
            part='snippet',
            id=channel_id
        ).execute()

        channel_icon = channel_info['items'][0]['snippet']['thumbnails']['default']['url']
        videos_info.append({'title': title, 'thumbnail': thumbnail, 'view_count': view_count_formatting,
                            'channel_title': channel_title, 'channel_icon': channel_icon})

    context = {'videos_info': videos_info}

    return render(request, 'toplist.html', context)

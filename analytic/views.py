from django.shortcuts import render
from googleapiclient.discovery import build
import os

def index(request):
    return render(request, 'index.html')


def result(request):
    api_key = os.environ.get('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    playlist_id = 'PL11E57E1166929B60'

    playlist_items = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=20
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


        videos_info.append({'title': title, 'thumbnail': thumbnail, 'view_count': view_count_formatting, 'channel_title': channel_title, 'channel_icon': channel_icon})

    context = {'videos_info': videos_info}

    return render(request, 'result.html', context)

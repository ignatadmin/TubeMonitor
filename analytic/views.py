from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .services import *
from .models import *

import os


class Index(CreateView):
    def post(self, request, *args, **kwargs):
        url = request.POST.get('url')
        parsed_url = urlparse(url)
        request.session['parsed_url'] = parsed_url.geturl()
        if parsed_url.netloc == "youtu.be" or parsed_url.path.startswith("/watch"):
            return redirect('video')
        else:
            return redirect('channel')

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


def channel(request):
    parsed_url_str = request.session.get('parsed_url')
    channel_data = get_channel_data(parsed_url_str)
    return render(request, 'channel.html', {'channel_data': channel_data})


def video(request):
    parsed_url_str = request.session.get('parsed_url')
    video_data = get_video_data(parsed_url_str)
    return render(request, 'video.html', {'video_data': video_data})


def toplist_videos(request):
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

    return render(request, 'toplist-videos.html', context)


def toplist_channels(request):
    queryset = TopChannels.objects.all()
    channels_info = []

    for top_channel in queryset:
        API_KEY = os.environ.get('API_KEY')
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request_yt = youtube.channels().list(
            part='snippet,statistics',
            id=top_channel.channel_id
        )
        response = request_yt.execute()
        channel_data = response['items'][0] if 'items' in response else None
        if channel_data:
            channels_info.append(channel_data)
    return render(request, 'toplist-channels.html', {'channels_data': channels_info})

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
    request_data = api_request.videos().list(
        part='snippet,statistics,status',
        id=video_id
    )
    response = request_data.execute()
    video_data = response['items'][0] if 'items' in response else None
    return video_data


class UpdateVideosToplists:
    def __init__(self):
        self.api_key = settings.API_KEY
        self.api_service_name = 'youtube'
        self.api_version = 'v3'
        self.playlist_id = 'PL11E57E1166929B60'
        self.api_request = build(self.api_service_name, self.api_version, developerKey=self.api_key)

    def _fetch_playlist_items(self):
        return self.api_request.playlistItems().list(
            part='snippet',
            playlistId=self.playlist_id,
            maxResults=100
        ).execute()['items']

    def _fetch_video_details(self, video_id):
        video_response = self.api_request.videos().list(
            part='snippet,statistics,status',
            id=video_id
        ).execute()
        return video_response['items'][0] if video_response['items'] else None

    def _fetch_channel_details(self, channel_id):
        channel_response = self.api_request.channels().list(
            part='snippet',
            id=channel_id
        ).execute()
        return channel_response['items'][0] if channel_response['items'] else None

    def _update_videos(self, videos, model_class):
        model_class.objects.all().delete()

        for video in videos:
            video_id = video['snippet']['resourceId']['videoId']
            video_title = video['snippet']['title']
            video_thumbnail = video['snippet']['thumbnails']['maxres']['url']

            video_details = self._fetch_video_details(video_id)
            if video_details:
                stats = video_details['statistics']
                view_count = int(stats['viewCount'])
                channel_id = video['snippet']['channelId']

                channel_details = self._fetch_channel_details(channel_id)
                if channel_details:
                    channel_title = channel_details['snippet']['title']
                    channel_icon = channel_details['snippet']['thumbnails']['default']['url']

                    model_class.objects.create(
                        title=video_title,
                        thumbnail=video_thumbnail,
                        view_count=view_count,
                        channel_icon=channel_icon,
                        channel_id=channel_id,
                        channel_title=channel_title
                    )

    def update_data_toplist_videos_not_for_kids(self):
        playlist_items = self._fetch_playlist_items()

        filtered_videos = [
            video for video in playlist_items
            if video['status']['madeForKids'] == False
        ]

        self._update_videos(filtered_videos, VideosByViewsNotKids)

    def update_data_toplist_videos(self):
        playlist_items = self._fetch_playlist_items()

        self._update_videos(playlist_items, VideosByViews)

    def update_video_toplists(self):
        self.update_data_toplist_videos_not_for_kids()
        self.update_data_toplist_videos()


class UpdateChannelsToplists():
    def update_data_toplist_channels(self):
        """обноление общего списка топ каналов"""
        queryset = TopChannels.objects.all()

        for top_channel in queryset:
            key = settings.API_KEY
            api_request = build('youtube', 'v3', developerKey=key)
            request_data = api_request.channels().list(
                part='snippet,statistics,status',
                id=top_channel.channel_id
            )
            response = request_data.execute()
            channel_data = response['items'][0] if 'items' in response else None
            if channel_data:
                top_channel.title = channel_data['snippet']['title']
                top_channel.thumbnails = channel_data['snippet']['thumbnails']['default']['url']
                top_channel.viewCount = int(channel_data['statistics']['viewCount'])
                top_channel.subscriberCount = int(channel_data['statistics']['subscriberCount'])
                top_channel.videoCount = int(channel_data['statistics']['videoCount'])
                top_channel.country = channel_data['snippet'].get('country', '')
                top_channel.save()

    def update_channels_data(self, model_cls, country_filter=None):
        """обновление талблиц топ каналов по критериям"""
        top_channels = TopChannels.objects.all()
        if country_filter:
            top_channels = top_channels.filter(country=country_filter)

        top_channels = top_channels.order_by(
            '-subscriberCount' if model_cls == ChannelsBySubs else
            '-viewCount' if model_cls == ChannelsByViews else
            '-videoCount'
        )[:100]
        model_cls.objects.all().delete()

        for channel in top_channels:
            model_cls.objects.create(
                title=channel.title,
                channel_id=channel.channel_id,
                thumbnails=channel.thumbnails,
                viewCount=channel.viewCount,
                subscriberCount=channel.subscriberCount,
                videoCount=channel.videoCount,
                country=channel.country
            )

    def update_channel_toplists(self):
        models_to_update = [
            (ChannelsByVideos, None),
            (ChannelsByVideos, 'RU'),
            (ChannelsByViews, None),
            (ChannelsByViews, 'RU'),
            (ChannelsBySubs, None),
            (ChannelsBySubs, 'RU'),
        ]
        self.update_data_toplist_channels()
        for model_cls, country_filter in models_to_update:
            self.update_channels_data(model_cls, country_filter)

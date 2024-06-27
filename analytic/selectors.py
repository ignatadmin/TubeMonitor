from .models import ListTopVideos, ListTopChannels


class GetTopListVideos():
    def get_world_videos_data(self, for_kids=None):
        if for_kids is None:
            for_kids = True
        if for_kids:
            videos_data = ListTopVideos.objects.all().order_by('-view_count')[:100]
        else:
            videos_data = ListTopVideos.objects.filter(made_for_kids=False).order_by('-view_count')[:100]
        return videos_data


class GetTopListChannels():
    def get_channels_data_by_subscribers(self, for_kids=True, only_ru=False):
        if for_kids or not only_ru:
            channels_data = ListTopChannels.objects.all().order_by('-subscriber_count')[:100]
        if not for_kids:
            channels_data = ListTopChannels.objects.filter(made_for_kids=False).order_by('-subscriber_count')[:100]
        if only_ru:
            channels_data = ListTopChannels.objects.filter(country='RU').order_by('-subscriber_count')[:100]
        return channels_data

    def get_channels_data_by_views(self, for_kids=True, only_ru=False):
        if for_kids or not only_ru:
            channels_data = ListTopChannels.objects.all().order_by('-view_count')[:100]
        if not for_kids:
            channels_data = ListTopChannels.objects.filter(made_for_kids=False).order_by('-view_count')[:100]
        if only_ru:
            channels_data = ListTopChannels.objects.filter(country='RU').order_by('-view_count')[:100]
        return channels_data

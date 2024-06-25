from .models import ListTopVideos, ListTopChannels


class GetTopListVideos():
    def get_world_videos_data(self):
        videos_data = ListTopVideos.objects.all()
        return videos_data

    def get_ru_videos_data(self):
        pass


class GetTopListChannels():
    def get_world_channels_data_by_subscribers(self):
        channels_data = ListTopChannels.objects.all()
        return channels_data

    def get_ru_channels_data_by_subscribers(self):
        pass

    def get_world_channels_data_by_views(self):
        pass

    def get_ru_channels_data_by_views(self):
        pass

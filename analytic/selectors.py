from .models import ListTopVideos, ListTopChannels


class GetTopListVideos:
    def get_videos_data(self, length_list: int, for_kids: bool = True):
        """ Возвращает данные топовых видео, отфильтрованных по количеству просмотров """
        try:
            if for_kids:
                videos_data = ListTopVideos.objects.all().order_by('-view_count')[:length_list]
            else:
                videos_data = ListTopVideos.objects.filter(made_for_kids=False).order_by('-view_count')[:length_list]
        except Exception as e:
            raise RuntimeError(f"Error fetching videos data: {e}")
        return videos_data


class GetTopListChannels:
    def get_channels_data(self, length_list: int, sort_by: str, for_kids: bool = True, only_ru: bool = False):
        """ Возвращает данные топовых каналов, отфильтрованных и отсортированных по указанным параметрам """
        try:
            query = ListTopChannels.objects.all()

            if not for_kids:
                query = query.filter(made_for_kids=False)

            if only_ru:
                query = query.filter(country='RU')

            if sort_by == 'subscribers':
                query = query.order_by('-subscriber_count')
            elif sort_by == 'views':
                query = query.order_by('-view_count')

            channels_data = query[:length_list]
        except Exception as e:
            raise RuntimeError(f"Error fetching top channels data: {e}")
        return channels_data

    def get_channels_data_by_subscribers(self, length_list: int, for_kids: bool = True, only_ru: bool = False):
        return self.get_channels_data(length_list, sort_by='subscribers', for_kids=for_kids, only_ru=only_ru)

    def get_channels_data_by_views(self, length_list: int, for_kids: bool = True, only_ru: bool = False):
        return self.get_channels_data(length_list, sort_by='views', for_kids=for_kids, only_ru=only_ru)

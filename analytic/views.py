from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView
from urllib.parse import urlparse
from .services import get_channel_data, get_video_data
from .selectors import GetTopListVideos, GetTopListChannels


class Index(CreateView):
    def post(self, request, *args, **kwargs):
        url = request.POST.get('url')
        parsed_url = urlparse(url)
        response = HttpResponseRedirect('/')
        response.set_cookie('parsed_url', parsed_url.geturl())

        if parsed_url.netloc == "youtu.be" or parsed_url.path.startswith("/watch"):
            response['Location'] = 'video'
        else:
            response['Location'] = 'channel'

        return response

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


def channel_data(request):
    """ По URL получает данные канала из YouTube API, и отображает их"""
    parsed_url_str = request.COOKIES.get('parsed_url')
    channel_data = get_channel_data(parsed_url_str)
    return render(request, 'channel.html', {'channel_data': channel_data})


def video_data(request):
    """ По URL получает данные видео из YouTube API, и отображает их"""
    parsed_url_str = request.COOKIES.get('parsed_url')
    video_data, channel_data = get_video_data(parsed_url_str)
    return render(request,
                  'video.html',
                  {'video_data': video_data, 'channel_data': channel_data})


class TopListVideos(View):
    """ Представление для отображения списка топовых видео """

    def get_videos_data(self, request, for_kids: bool = True):
        length_list = 100 if request.user.is_active else 15
        try:
            videos_data = GetTopListVideos().get_videos_data(for_kids=for_kids, length_list=length_list)
        except Exception as e:
            return HttpResponse(f"Error getting top videos data: {e}", status=500)
        return render(request,
                      'toplist-videos.html',
                      {'videos_data': videos_data, 'for_kids': for_kids})

    def get(self, request):
        return self.get_videos_data(request)

    def post(self, request):
        for_kids = request.POST.get('for_kids')
        if for_kids:
            for_kids = True
        return self.get_videos_data(request, for_kids)


class TopListChannels(View):
    """ Представление для отображения списка топовых каналов """

    def get_channels_data(self, request, for_kids: bool, only_ru: bool, sort: str) -> HttpResponse:
        length_list = 100 if request.user.is_active else 15
        channels_data_func = {
            'subscribers': GetTopListChannels().get_channels_data_by_subscribers,
            'views': GetTopListChannels().get_channels_data_by_views
        }.get(sort, GetTopListChannels().get_channels_data_by_subscribers)

        try:
            channels_data = channels_data_func(length_list=length_list, for_kids=for_kids, only_ru=only_ru)
        except Exception as e:
            return HttpResponse(f"Error getting top channels data: {e}", status=500)
        return render(request,
                      'toplist-channels.html',
                      {'channels_data': channels_data, 'for_kids': for_kids, 'only_ru': only_ru})

    def get(self, request):
        sort = request.GET.get('sort', 'subscribers')
        return self.get_channels_data(request, for_kids=True, only_ru=False, sort=sort)

    def post(self, request):
        sort = request.GET.get('sort', 'subscribers')
        for_kids = request.POST.get('for_kids')
        only_ru = request.POST.get('only_ru')
        if for_kids:
            for_kids = True
        else:
            for_kids = False
        if only_ru:
            only_ru = True
            for_kids = True
        else:
            only_ru = False
        return self.get_channels_data(request, for_kids=for_kids, only_ru=only_ru, sort=sort)

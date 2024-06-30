from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from .services import *
from .selectors import *


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


def channel(request):
    parsed_url_str = request.COOKIES.get('parsed_url')
    if parsed_url_str:
        channel_data = get_channel_data(parsed_url_str)
        return render(request, 'channel.html', {'channel_data': channel_data})
    else:
        return redirect('/')


def video(request):
    parsed_url_str = request.COOKIES.get('parsed_url')
    if parsed_url_str:
        video_data, channel_data = get_video_data(parsed_url_str)
        return render(request, 'video.html', {'video_data': video_data, 'channel_data': channel_data})
    else:
        return redirect('/')


class TopListVideos(View):
    def get(self, request):
        if request.user.is_active:
            length_list = 100
        else:
            length_list = 15
        videos_data = GetTopListVideos().get_world_videos_data(length_list=length_list)
        return render(request, 'toplist-videos.html', {'videos_data': videos_data, 'for_kids': True})

    def post(self, request):
        for_kids = request.POST.get('for_kids')
        if request.user.is_active:
            length_list = 100
        else:
            length_list = 15
        if for_kids:
            for_kids = True
        else:
            for_kids = False
        videos_data = GetTopListVideos().get_world_videos_data(for_kids=for_kids,length_list=length_list)
        return render(request, 'toplist-videos.html', {'videos_data': videos_data, 'for_kids': for_kids})


class TopListChannels(View):
    def get(self, request):
        sort = request.GET.get('sort', 'subscribers')
        if sort == 'subscribers':
            channels_data = GetTopListChannels().get_channels_data_by_subscribers()
        elif sort == 'views':
            channels_data = GetTopListChannels().get_channels_data_by_views()
        return render(request, 'toplist-channels.html', {'channels_data': channels_data, 'for_kids': True})

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
        else:
            only_ru = False
        if sort == 'subscribers':
            channels_data = GetTopListChannels().get_channels_data_by_subscribers(for_kids=for_kids, only_ru=only_ru)
        elif sort == 'views':
            channels_data = GetTopListChannels().get_channels_data_by_views(for_kids=for_kids, only_ru=only_ru)
        return render(request, 'toplist-channels.html',
                      {'channels_data': channels_data, 'for_kids': for_kids, 'only_ru': only_ru, })
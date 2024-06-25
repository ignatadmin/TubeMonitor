from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from .services import *
from .selectors import *


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


class TopListVideos(View):
    def get(self, request):
        videos_data = GetTopListVideos().get_world_videos_data()
        return render(request, 'toplist-videos.html', {'videos_data': videos_data})


class TopListChannels(View):
    def get(self, request):
        sort = request.GET.get('sort', 'subscribers')
        if sort == 'subscribers':
            channels_data = GetTopListChannels().get_world_channels_data_by_subscribers()
        elif sort == 'views':
            channels_data = GetTopListChannels().get_world_channels_data_by_views()
        return render(request, 'toplist-channels.html', {'channels_data': channels_data})


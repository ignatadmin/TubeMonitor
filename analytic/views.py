from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .services import *


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
    context = get_toplist_videos()
    return render(request, 'toplist-videos.html', context)


def toplist_channels(request):
    channels_info = get_toplist_channels()
    return render(request, 'toplist-channels.html', {'channels_data': channels_info})

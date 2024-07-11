from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import ListTopVideos, ListTopChannels

@receiver([post_save, post_delete], sender=ListTopVideos)
@receiver([post_save, post_delete], sender=ListTopChannels)
def clear_cache(sender, **kwargs):
    cache.clear()
from django.db import models


class ListTopVideos(models.Model):
    title = models.CharField(default=None, null=True, verbose_name="название")
    thumbnail = models.CharField(default=None, null=True, verbose_name="миниатюра")
    view_count = models.BigIntegerField(default=None, null=True, verbose_name="число просмотров")
    channel_icon = models.CharField(default=None, null=True, verbose_name="иконка канала")
    channel_id = models.CharField(default=None, null=True, verbose_name="айди канала")
    channel_title = models.CharField(default=None, null=True, verbose_name="название канала")
    made_for_kids = models.BooleanField(default=False, null=True, verbose_name="контент для детей")

    def __str__(self):
        return f'{self.pk} - {self.title} - {self.view_count} - {self.made_for_kids}'

    class Meta:
        verbose_name = "топ видео по просмотрам"
        verbose_name_plural = "топ видео по просмотрам"


class ListTopChannels(models.Model):
    title = models.CharField(default=None, null=True, verbose_name="название")
    channel_id = models.CharField(max_length=24, default=None, null=True, verbose_name="айди канала")
    thumbnails = models.CharField(default=None, null=True, verbose_name="миниатюра")
    view_count = models.BigIntegerField(default=None, null=True, verbose_name="число просмотров")
    subscriber_count = models.BigIntegerField(default=None, null=True, verbose_name="число подписчиков")
    video_count = models.BigIntegerField(default=None, null=True, verbose_name="число видео")
    country = models.CharField(default=None, null=True, verbose_name="страна")

    def __str__(self):
        return f'{self.pk} - {self.title} - {self.channel_id}'

    class Meta:
        verbose_name = "список топ каналов"
        verbose_name_plural = "список топ каналов"

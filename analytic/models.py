from django.db import models


class VideosByViews(models.Model):
    title = models.CharField(default=None, null=True, verbose_name="123")
    thumbnail = models.CharField(default=None, null=True, verbose_name="123")
    view_count = models.IntegerField(default=None, null=True, verbose_name="123")
    channel_icon = models.CharField(default=None, null=True, verbose_name="123")
    channel_id = models.CharField(default=None, null=True, verbose_name="123")
    channel_title = models.CharField(default=None, null=True, verbose_name="123")

    def __str__(self):
        return f'{self.pk} - {self.title} - {self.view_count}'

    class Meta:
        verbose_name = "топ 100 видео по просмотрам"
        verbose_name_plural = "топ 100 видео по просмотрам"


class VideosByViewsNotKids(models.Model):
    title = models.CharField(default=None, null=True, verbose_name="123")
    thumbnail = models.CharField(default=None, null=True, verbose_name="123")
    view_count = models.IntegerField(default=None, null=True, verbose_name="123")
    channel_icon = models.CharField(default=None, null=True, verbose_name="123")
    channel_id = models.CharField(default=None, null=True, verbose_name="123")
    channel_title = models.CharField(default=None, null=True, verbose_name="123")

    def __str__(self):
        return f'{self.pk} - {self.title} - {self.view_count}'

    class Meta:
        verbose_name = "топ 100 видео по просмотрам кроме для детей"
        verbose_name_plural = "топ 100 видео по просмотрам кроме для детей"


class ChannelBaseModel(models.Model):
    title = models.CharField(default=None, null=True, verbose_name="название")
    channel_id = models.CharField(max_length=24, default=None, null=True, verbose_name="айди канала")
    thumbnails = models.CharField(default=None, null=True, verbose_name="миниатюра")
    view_count = models.IntegerField(default=None, null=True, verbose_name="число просмотров")
    subscriber_count = models.IntegerField(default=None, null=True, verbose_name="число подписчиков")
    video_count = models.IntegerField(default=None, null=True, verbose_name="число видео")
    country = models.CharField(default=None, null=True, verbose_name="страна")

    class Meta:
        abstract = True


class TopChannels(ChannelBaseModel):
    def __str__(self):
        return f'{self.pk} - {self.title} - {self.channel_id}'

    class Meta:
        verbose_name = "список топ каналов"
        verbose_name_plural = "список топ каналов"


class ChannelsBySubs(ChannelBaseModel):
    def __str__(self):
        return f'{self.pk} - {self.title} - {self.subscriber_count}'

    class Meta:
        verbose_name = "топ 100 каналов по подписчикам"
        verbose_name_plural = "топ 100 каналов по подписчикам"


class ChannelsBySubsRu(ChannelBaseModel):
    def __str__(self):
        return f'{self.pk} - {self.title} - {self.subscriber_count}'

    class Meta:
        verbose_name = "топ 100 RU каналов по подписчикам"
        verbose_name_plural = "топ 100 RU аналов по подписчикам"


class ChannelsByViews(ChannelBaseModel):
    def __str__(self):
        return f'{self.pk} - {self.title} - {self.view_count}'

    class Meta:
        verbose_name = "топ 100 каналов по просмотрам"
        verbose_name_plural = "топ 100 каналов по просмотрам"


class ChannelsByViewsRu(ChannelBaseModel):
    def __str__(self):
        return f'{self.pk} - {self.title} - {self.view_count}'

    class Meta:
        verbose_name = "топ 100 RU каналов по просмотрам"
        verbose_name_plural = "топ 100 RU каналов по просмотрам"


class ChannelsByVideos(ChannelBaseModel):
    def __str__(self):
        return f'{self.pk} - {self.title} - {self.video_count}'

    class Meta:
        verbose_name = "топ 100 каналов по количеству видео"
        verbose_name_plural = "топ 100 каналов по количеству видео"


class ChannelsByVideosRu(ChannelBaseModel):
    def __str__(self):
        return f'{self.pk} - {self.title} - {self.video_count}'

    class Meta:
        verbose_name = "топ 100 RU каналов по количеству видео"
        verbose_name_plural = "топ 100 RU каналов по количеству видео"

from django.db import models


class VideosByViews(models.Model):
    title = models.CharField()
    thumbnail = models.CharField()
    view_count = models.IntegerField()
    channel_icon = models.CharField()
    channel_id = models.CharField()
    channel_title = models.CharField()

    def __str__(self):
        return f'{self.pk} - {self.title} - {self.view_count}'

    class Meta:
        verbose_name = "топ 100 видео по просмотрам"
        verbose_name_plural = "топ 100 видео по просмотрам"


class VideosByViewsNotKids(models.Model):
    title = models.CharField()
    thumbnail = models.CharField()
    view_count = models.IntegerField()
    channel_icon = models.CharField()
    channel_id = models.CharField()
    channel_title = models.CharField()

    def __str__(self):
        return f'{self.pk} - {self.title} - {self.view_count}'

    class Meta:
        verbose_name = "топ 100 видео по просмотрам кроме для детей"
        verbose_name_plural = "топ 100 видео по просмотрам кроме для детей"


class ChannelBaseModel(models.Model):
    title = models.CharField()
    channel_id = models.CharField(max_length=24)
    thumbnails = models.CharField()
    view_count = models.IntegerField()
    subscriber_count = models.IntegerField()
    video_count = models.IntegerField()
    country = models.CharField()

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

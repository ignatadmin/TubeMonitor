from django.db import models


class TopChannels(models.Model):
    channel_id = models.TextField(max_length=24)

    def __str__(self):
        return f'{self.pk} - {self.channel_id}'

    class Meta:
        verbose_name = "топ каналов"
        verbose_name_plural = "топ каналов"

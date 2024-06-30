import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    telegram_username = models.CharField(max_length=255, verbose_name="телеграм username", null=True, blank=True)
    telegram_activation_code = models.CharField(max_length=36, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.telegram_username}'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователь"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

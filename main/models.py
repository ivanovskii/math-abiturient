from django.db import models
from django.contrib.auth.models import AbstractUser
from mdeditor.fields import MDTextField


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Пpoшeл активацию?')
    image = models.ImageField(upload_to='users/%Y/%m-%d/', blank=True, verbose_name='Фотография профиля')
    biography = models.TextField(blank=True, verbose_name='О себе')

    class Meta(AbstractUser.Meta):
        pass


class Task(models.Model):
    title = models.CharField(max_length=50)
    content = MDTextField()
    creator = models.ForeignKey(AdvUser, on_delete=models.CASCADE, null=True)

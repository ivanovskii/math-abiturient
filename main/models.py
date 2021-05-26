from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Пpoшeл активацию?')
    image = models.ImageField(upload_to='', blank=True)
    biography = models.TextField(blank=True)

    class Meta(AbstractUser.Meta):
        pass

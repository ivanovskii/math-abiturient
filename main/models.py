from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class AdvUser(AbstractUser):
    image = models.ImageField(upload_to='')
    biography = models.TextField(blank=True)

    class Meta(AbstractUser.Meta):
        pass
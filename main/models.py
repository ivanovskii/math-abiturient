from django.db import models
from django.contrib.auth.models import AbstractUser
from mdeditor.fields import MDTextField

import os
import re
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from math_abiturient.settings import MDEDITOR_IMAGE_FOLDER_PATH


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


# Signal that removes task images from server
# Bad decision: images remain when canceling task creation 
@receiver(pre_delete, sender=Task)
def task_images_delete(sender, instance, **kwargs):
    images = re.findall(
        r'(?<=!\[]\(/media/editor\\)\w+\.\w+(?=\))',
        instance.content
    )

    for image in images:
        try:
            os.remove(os.path.join(MDEDITOR_IMAGE_FOLDER_PATH, image))
        except:
            continue

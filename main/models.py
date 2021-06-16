from django.db import models
from django.contrib.auth.models import AbstractUser
from mdeditor.fields import MDTextField

import os
import re
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from math_abiturient.settings import MDEDITOR_IMAGE_FOLDER_PATH


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Пpoшeл активацию?')
    image = models.ImageField(upload_to='users/%Y/%m-%d/', blank=True,
                              verbose_name='Фотография профиля')
    biography = models.TextField(blank=True, verbose_name='О себе')
    
    @property
    def get_published_tasks(self):
        return Task.objects.filter(creator=self, is_published=True)

    @property
    def get_unpublished_tasks(self):
        return Task.objects.filter(creator=self, is_published=False)

    class Meta(AbstractUser.Meta):
        pass


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Task(TimeStampMixin):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    description = models.CharField(max_length=500, blank=True, verbose_name='Описание')
    content = MDTextField(verbose_name='Содержание')
    creator = models.ForeignKey(AdvUser, on_delete=models.CASCADE)
    published_at = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False, db_index=True,
                                       verbose_name='Опубликовано?')

    def __str__(self):
        return f"[{self.creator}]: {self.title}"

    def get_favorite_count(self):
        return self.favoritetask_set.all().count()

    class Meta:
        ordering = ['-published_at', ]
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


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


class FavoriteBase(models.Model):
    user = models.ForeignKey(AdvUser, verbose_name="Пользователь",
                                      on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

    class Meta:
        abstract = True


class FavoriteTask(FavoriteBase):
    obj = models.ForeignKey(Task, verbose_name="Закладка",
                                  on_delete=models.CASCADE)

    class Meta:
        db_table = "favorite_task"
        verbose_name = 'Избранная задача'
        verbose_name_plural = 'Избранные задачи'

from django.contrib import admin
from .models import AdvUser, Task, FavoriteTask

admin.site.register(AdvUser)
admin.site.register(Task)
admin.site.register(FavoriteTask)
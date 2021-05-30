from django.apps import AppConfig
from django.dispatch import Signal
from .utilities import send_activation_notification

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

user_joined = Signal(providing_args=['instance'])

def user_joined_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])

user_joined.connect(user_joined_dispatcher)
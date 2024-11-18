# chat/urls.py
from django.urls import path, re_path

from .consumers import *


websocket_urlpatterns = [
    re_path("ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
]
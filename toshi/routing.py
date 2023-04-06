from . import consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/toshi/$', consumers.FrontendConsumer().as_asgi()),
    re_path(r'ws/toshi-profile/$', consumers.FrontendProfileConsumer().as_asgi()),
    re_path(r'ws/toshi-history/$', consumers.HistoryConsumer().as_asgi()),
]

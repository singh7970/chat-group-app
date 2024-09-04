from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/ac/$', consumers.myAsyncConsumer.as_asgi()),
    
    re_path(r'ws/sc/$', consumers.mysyncCounsumer.as_asgi()),
]

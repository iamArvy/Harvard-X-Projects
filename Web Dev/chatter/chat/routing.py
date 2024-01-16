# yourapp/routing.py

from django.urls import path, re_path

from .consumers import ChatConsumer, ChatListConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<crid>\w+)/$', ChatConsumer.as_asgi()),
    path('ws/chat_list/', ChatListConsumer.as_asgi()),
    # Add more patterns as needed
]
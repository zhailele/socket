from django.urls import path
from chat.consumers import ChatConsumer, ChatConsumerTest, DeployResult

websocket_urlpatterns = [
    path('ws/chat/', ChatConsumer),
    path('ws/test/', ChatConsumerTest),
    path('ws/send/', DeployResult)
]
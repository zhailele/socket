import json

from channels.generic.websocket import WebsocketConsumer


class xChatConsumer(WebsocketConsumer):
    def connect(self):
        print('--->:' + str(self.channel_layer))

        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = '运维咖啡吧：' + text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))


from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class yChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'ops_coffee'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = '运维咖啡吧：' + event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'ops_coffee'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = '运维咖啡吧：' + event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


class ChatConsumerTest(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'ops_coffee'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)

        # Send message to room group
        await self.channel_layer.send(
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = '运维咖啡吧：' + event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import User

class DeployResult(AsyncWebsocketConsumer):
    async def connect(self):
        self.service_uid = self.scope["client"][1]
        self.chat_group_name = 'chat_%s' % self.service_uid
        # 收到连接时候处理，
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        print("get------>chat_group_name",self.chat_group_name)
        print("get------>channel_name",self.channel_name)
        user = User.objects.filter(id=3).update(name=self.chat_group_name)
        user2 = User.objects.filter(id=4).update(name=self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # 关闭channel时候处理
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    # 收到消息
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("收到消息--》",message)
        # 发送消息到组
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'client.message',
                'message': message
            }
        )

    # 处理客户端发来的消息
    async def client_message(self, event):
        message = event['message']
        print("发送消息。。。",message)
        # 发送消息到 WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def system_message(self, event):
        print('$' * 20,event)
        message = event['message']
        # Send message to WebSocket单发消息
        await self.send(text_data=json.dumps({
            'message': message
        }))

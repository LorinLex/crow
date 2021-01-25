from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from collections import defaultdict
import weakref
import json

from .services.websocket_services.controllers import get_session_controller


class GameConsumer(WebsocketConsumer):
    __refs__ = defaultdict(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__refs__[self.__class__].append(weakref.ref(self))

    @classmethod
    def get_instances(cls):
        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()
            if inst is not None:
                yield inst

    def connect(self):
        self.room_group_name = 'game'
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
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': text_data_json['type'],
                'message': message
            }
        )
    # Receive message from room group

    def sendall(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'message',
            'data': message
        }))

    def get_games(self, _):
        get_session_controller(self)


class GameDetailConsumer(WebsocketConsumer):
    __refs__ = defaultdict(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__refs__[self.__class__].append(weakref.ref(self))

    @classmethod
    def get_instances(cls):
        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()
            if inst is not None:
                yield inst

    def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'game_%s' % self.game_id

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
        message = text_data_json
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
        print(event)
        message = event['message']

        # Send message to WebSocket

        self.send(text_data=json.dumps({
            'message': message
        }))



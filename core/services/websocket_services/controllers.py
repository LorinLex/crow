import json

from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from ...models import Session, GameSetting
from .websocket_serializers import WSSessionSerializer


def websocket_send_message(message_type: str = None, message: str = None, socket_obj: object = None):
    channel_layer = get_channel_layer()
    if message_type:
        pass


def get_session_controller(obj: object):
    queryset = Session.objects.exclude(status='Filled').annotate(players_quantity=models.Count('player'))
    data = json.dumps(WSSessionSerializer(queryset, many=True).data)
    obj.send(
        text_data=json.dumps({
            'data': data
        }))


import json

from django.db import models

from ...models import Session, GameSetting
from .websocket_serializers import WSSessionSerializer


def get_game_controller(obj: object):
    queryset = Session.objects.exclude(status='Filled').annotate(players_quantity=models.Count('player'))
    data = json.dumps(WSSessionSerializer(queryset, many=True).data)
    obj.send(
        text_data=json.dumps({
            'type': 'games',
            'data': data
        }))

import json

from django.db import models

from ...models import Game, GameSetting
from .websocket_serializers import WSGameSerializer


def get_game_controller(obj: object):
    queryset = Game.objects.filter(game_status=True).annotate(players_quantity=models.Count('user'))
    data = json.dumps(WSGameSerializer(queryset, many=True).data)
    obj.send(
        text_data=json.dumps({
            'type': 'games',
            'data': data
        }))

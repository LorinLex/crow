import json

from django.db import models

from ...models import Game, GameSetting
from .websocket_serializers import WSGameSerializer


def get_game_controller():
    queryset = Game.objects.filter(game_status=True).annotate(players_quantity=models.Count('user'))
    return json.dumps(WSGameSerializer(queryset, many=True).data), 'send_me'
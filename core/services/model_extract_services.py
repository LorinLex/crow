import json

from ..models import Game
from ..serializers import GameSerializer


def get_all_games():
    queryset = Game.objects.all()
    return json.dumps(GameSerializer(queryset, many=True).data)

'''
from core.services.websocket_services.websocket_serializers import WSGameSerializer

from core.models import Game
game = Game.objects.all
game = Game.objects.all()
import json
json.dumps(WSGameSerializer(game, many=True).data)
'''
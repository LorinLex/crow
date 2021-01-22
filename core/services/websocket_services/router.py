import json

from .controllers import get_game_controller


def rout(data):
    router = json.loads(data)['type']
    if router == 'get_game':
        return get_game_controller()
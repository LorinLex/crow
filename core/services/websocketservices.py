from ..consumers import GameConsumer


def get_socket_obj(id):
    sockets = list(GameConsumer.get_instances())
    filter_sok = []
    for socket in sockets:
        if socket.scope['url_route']['kwargs']['room_name'] == id:
            filter_sok.append(socket)
    return filter_sok


def get_game_socket(game_id: str):
    """:return Объект сокета игры"""
    return get_socket_obj(game_id)

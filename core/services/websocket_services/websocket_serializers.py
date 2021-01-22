from rest_framework import serializers

from ...models import Game, GameSetting


class WSGameSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSetting
        fields = ('crow_balance', )


class WSGameSerializer(serializers.ModelSerializer):
    '''Сериализатор для игор'''
    settings = WSGameSettingSerializer()

    class Meta:
        model = Game
        fields = ("id", 'name', 'turn_count', 'settings', 'players_quantity')
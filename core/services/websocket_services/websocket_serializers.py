from rest_framework import serializers

from ...models import Session, GameSetting


class WSGameSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSetting
        fields = ('crow_balance', )


class WSSessionSerializer(serializers.ModelSerializer):
    '''Сериализатор для игор'''
    players_quantity = serializers.IntegerField()
    settings = WSGameSettingSerializer()

    class Meta:
        model = Session
        fields = ("id", 'name', 'turn_count', 'settings', 'players_quantity')
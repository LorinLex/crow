from rest_framework.serializers import ModelSerializer

from .models import  GameSetting, MainUser, Transaction


class MainUserListSerializer(ModelSerializer):
    class Meta:
        model = MainUser
        fields = ('id', 'username')


class MainUserDetailSerializer(ModelSerializer):
    class Meta:
        model = MainUser
        fields = ('username',)


class GameSettingSerializer(ModelSerializer):
    class Meta:
        model = GameSetting
        fields = "__all__"


class TransactionSerializer(ModelSerializer):

    class Meta:
        model = Transaction
        fields = "__all__"


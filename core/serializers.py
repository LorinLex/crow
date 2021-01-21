from rest_framework.serializers import ModelSerializer

from .models import Game, GameSetting, Step, Profile, MainUser, City, Transaction


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


class ProfileListSerializer(ModelSerializer):
    user = MainUserListSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"


class ProfileDetailSerializer(ModelSerializer):
    user = MainUserListSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'balance', 'city', 'role')


class CitySerializer(ModelSerializer):

    class Meta:
        model = City
        fields = "__all__"


class TransactionSerializer(ModelSerializer):

    class Meta:
        model = Transaction
        fields = "__all__"


class StepSerializer(ModelSerializer):
    transaction = TransactionSerializer(many=True)

    class Meta:
        model = Step
        fields = "__all__"


class GameSerializer(ModelSerializer):

    settings = GameSettingSerializer(read_only=True)
    step = StepSerializer(many=True, read_only=True)
    user = ProfileListSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = "__all__"
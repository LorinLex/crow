from rest_framework.viewsets import ModelViewSet

from .models import Game, Profile, GameSetting, MainUser, City, Transaction, Step
from .serializers import GameSerializer, GameSettingSerializer, \
    ProfileDetailSerializer, MainUserDetailSerializer, CitySerializer, TransactionSerializer, StepSerializer


class GameViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameSettingViewSet(ModelViewSet):
    queryset = GameSetting.objects.all()
    serializer_class = GameSettingSerializer


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer


class UserViewSet(ModelViewSet):
    queryset = MainUser.objects.all()
    serializer_class = MainUserDetailSerializer


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class StepViewSet(ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer

from rest_framework.viewsets import ModelViewSet

from .models import  GameSetting, MainUser,  Transaction
from .serializers import GameSettingSerializer, MainUserDetailSerializer, \
    TransactionSerializer


class GameSettingViewSet(ModelViewSet):
    queryset = GameSetting.objects.all()
    serializer_class = GameSettingSerializer


class UserViewSet(ModelViewSet):
    queryset = MainUser.objects.all()
    serializer_class = MainUserDetailSerializer


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer



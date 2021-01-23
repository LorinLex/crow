from rest_framework.viewsets import ModelViewSet

from .models import  GameSetting, MainUser,  Transaction, Session
from .serializers import GameSettingSerializer, MainUserDetailSerializer, \
    TransactionSerializer, SessionSerializer


class GameSettingViewSet(ModelViewSet):
    """Вывод настроек игры"""
    # FIXME посмотреть get serializer
    queryset = GameSetting.objects.all()
    serializer_class = GameSettingSerializer


class SessionViewSet(ModelViewSet):
    """Вывод игровых ссесий"""
    queryset = Session.objects.exclude(status='Filled')
    serializer_class = SessionSerializer


class UserViewSet(ModelViewSet):
    queryset = MainUser.objects.all()
    serializer_class = MainUserDetailSerializer


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer



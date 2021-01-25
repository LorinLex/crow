from django.contrib.auth.models import AbstractUser
from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_sok_get_games():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("game", {"type": "get_games"})


CITIES = (
    ('NF', "Неверфол"),
    ('TT', "Тортуга"),
    ('WS', "Вемшир"),
    ('AV', "Айво"),
    ('AD', "Алендор"),
    ('ET', "Этруа"),)

# FIXME Нужно проработать статусы лобби
SESSION_STATUS = (
    ('Created', "Сессия создана"),
    ('Awaiting', "Ожидание подключения игроков"),
    ('Filled', "Сессия заполнена"),
)

ROLES = (
    ('broker', 'Маклер'),
    ('manufacturer', 'Производитель'),
)


class MainUser(AbstractUser):
    """Модель пользователя платформы"""

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


# FIXME Значения настроек должны быть строгими и зависеть от количества игроков в лобби
# Скорее всего, мы их сделаем сами ручками и впоследствии трогать не будем
class GameSetting(models.Model):
    """Модель пресета настроек игры"""
    manufacturer_balance = models.IntegerField(verbose_name='Баланс производителя')
    broker_balance = models.IntegerField(verbose_name="Баланс маклера")
    crown_balance = models.IntegerField(verbose_name="Баланс короны")
    transaction_limit = models.IntegerField(verbose_name="Лимит сделки")

    def __str__(self):
        return f'Сет настроек {self.pk}'

    class Meta:
        verbose_name = 'Пресет настроек'
        verbose_name_plural = 'Пресеты настроек'


class Session(models.Model):
    """Модель игровой сессии"""
    name = models.CharField(max_length=255, verbose_name='Название сессии')
    turn_count = models.IntegerField(verbose_name='Количество игровых ходов')
    settings = models.ForeignKey(GameSetting, related_name='session', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=100, choices=SESSION_STATUS, verbose_name='Статус сессии')
    is_started = models.BooleanField()

    def __str__(self):
        return f'Сессия "{self.name}"'

    class Meta:
        verbose_name = 'Игровая сессия'
        verbose_name_plural = 'Игровые сессии'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        send_sok_get_games()


class State(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='state')
    turn = models.PositiveIntegerField()
    game_state = models.JSONField()


class Player(models.Model):
    """Модель игрока в игровой сессии"""

    nickname = models.CharField(max_length=255, verbose_name='Никнейм', default='')
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='player')
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, related_name='player', null=True)
    city = models.CharField(max_length=10, choices=CITIES, verbose_name='Город', null=True)
    role = models.CharField(max_length=20, choices=ROLES, verbose_name='Игровая роль', blank=True, default='')
    balance = models.IntegerField(default=0)
    is_bankrupt = models.BooleanField()

    def __str__(self):
        return f'{self.nickname} в городе {self.city}'

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    def save(self, *args, **kwargs):
        send = False
        if self.session.status == 'Created':
            if not self.role:
                send = True
            else:
                if self.role == 'broker':
                    self.balance = self.session.settings.broker_balance
                else:
                    self.balance = self.session.settings.manufacturer_balance
        super().save(*args, **kwargs)
        if send:
            send_sok_get_games()


class Production(models.Model):
    manufacturer = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, related_name='production')
    billets_produced = models.IntegerField()

    def __str__(self):
        return f'Запрос на производство игрока {self.manufacturer.nickname}'

    class Meta:
        verbose_name = 'Запрос на производство'
        verbose_name_plural = 'Запросы на производство'


class Warehouse(models.Model):
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, related_name='warehouse')
    billets = models.IntegerField()

    def __str__(self):
        return f'Склад игрока {self.player.nickname}'


class Turn(models.Model):
    # FIXME Димон ты заебал нахуй он нужен без связей
    """Модель хода"""
    turn_time = models.IntegerField(verbose_name='Время хода', blank=True, default='')

    def __str__(self):
        return f'Ход № {self.pk}'

    class Meta:
        verbose_name = 'Ход'
        verbose_name_plural = 'Ходы'


class Transaction(models.Model):
    """Модель транзакции"""
    manufacturer = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='transaction_m')
    broker = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='transaction_b')
    number_of_billets = models.IntegerField(verbose_name='Количество')
    billet_price = models.IntegerField(verbose_name="Цена за заготовку")
    costs_transporting_single = models.PositiveIntegerField(default=10)
    approved_by_broker = models.BooleanField(default=False)
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE, related_name='transaction', default='')

    def __str__(self):
        return f'Сделка между {self.manufacturer} и {self.broker} на {self.turn} ходу'

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'

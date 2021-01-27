from django.contrib.auth.models import AbstractUser
from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_sok_get_games():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("game", {"type": "send_game_data"})


def send_sok_change_session_id(session_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f"session_{session_id}", {"type": "send_detail_data", 'pk': f'{session_id}'})



CITIES = (
    ('NF', "Неверфол"),
    ('TT', "Тортуга"),
    ('WS', "Вемшир"),
    ('AV', "Айво"),
    ('AD', "Алендор"),
    ('ET', "Этруа"),)

SESSION_STATUS = (
    ('Created', "Сессия создана"),
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
    manufacturer_balance = models.PositiveIntegerField(verbose_name='Баланс производителя')
    broker_balance = models.PositiveIntegerField(verbose_name="Баланс маклера")
    crown_balance = models.PositiveIntegerField(verbose_name="Баланс короны")
    transaction_limit = models.PositiveIntegerField(verbose_name="Лимит сделки")

    def __str__(self):
        return f'Сет настроек {self.pk}'

    class Meta:
        verbose_name = 'Пресет настроек'
        verbose_name_plural = 'Пресеты настроек'


class Session(models.Model):
    """Модель игровой сессии"""

    name = models.CharField(max_length=255, verbose_name='Название сессии')
    turn_count = models.PositiveIntegerField(verbose_name='Количество игровых ходов')
    settings = models.ForeignKey(GameSetting, related_name='session', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=100, choices=SESSION_STATUS, verbose_name='Статус сессии', default='Created')
    crown_balance = models.PositiveIntegerField(default=12000, verbose_name='Баланс Короны')
    is_started = models.BooleanField(default=False)


    def __str__(self):
        return f'Сессия "{self.name}"'

    class Meta:
        verbose_name = 'Игровая сессия'
        verbose_name_plural = 'Игровые сессии'
    # TODO много логики в методе save!
    # 1. При создании создаем шаги OK
    # 2. При старте игры используем для подсчета первый шаг и каждый шаг это атоинкремент!
    # 3. При завершении хода turn_finished в шаге в статус True

    def save(self, *args, **kwargs):
        create_turn = True if not self.pk else False
        super().save(*args, **kwargs)
        if create_turn:
            for i in range(self.turn_count):
                Turn.objects.create(
                    turn_num=i+1,
                    session=self
                )
        send_sok_get_games()
        send_sok_change_session_id(self.pk)

    def delete(self, *args, **kwargs):
        super().save(*args, **kwargs)
        send_sok_get_games()


class State(models.Model):
    """Модель состояния игровой сессии"""
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='state')
    turn = models.PositiveIntegerField()
    game_state = models.TextField()  # JSONField


class Player(models.Model):
    """Модель игрока в игровой сессии"""

    nickname = models.CharField(max_length=255, verbose_name='Никнейм', default='')
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='player')
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, related_name='player', null=True)
    city = models.CharField(max_length=10, choices=CITIES, verbose_name='Город', null=True)
    role = models.CharField(max_length=20, choices=ROLES, verbose_name='Игровая роль', blank=True, default='')
    balance = models.IntegerField(default=0)
    is_bankrupt = models.BooleanField(default=False)
    turn_finished = models.BooleanField(default=False)

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
    """Модель запроса на производство"""
    manufacturer = models.ForeignKey(Player,
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     related_name='production',
                                     limit_choices_to={'role': 'manufacturer'})
    billets_produced = models.PositiveIntegerField()

    def __str__(self):
        return f'Запрос на производство игрока {self.manufacturer}'

    class Meta:
        verbose_name = 'Запрос на производство'
        verbose_name_plural = 'Запросы на производство'


class Warehouse(models.Model):
    """Модель склада производителей"""
    player = models.ForeignKey(Player,
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='warehouse',
                               limit_choices_to={'role': 'manufacturer'})
    billets = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Склад игрока {self.player}'


class Turn(models.Model):
    """Модель хода"""
    turn_num = models.IntegerField(verbose_name='Номер хода')
    session = models.ForeignKey(Session, verbose_name='Сессия', on_delete=models.CASCADE)
    turn_time = models.PositiveIntegerField(verbose_name='Время хода', blank=True, default=30)

    # FIXME состакать с таймером
    turn_finished = models.BooleanField(default=False)

    def __str__(self):
        return f'Ход № {self.turn_num} Сессия №{self.session.id} {self.pk}'

    class Meta:
        verbose_name = 'Ход'
        verbose_name_plural = 'Ходы'
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Turn.objects.get(pk=self.pk)
            if not orig.turn_finished:
                # FIXME Нужно доставать время следующего хода из пресетов
                Turn.objects.create(session=self.session, turn_time=10)
        super(Turn, self).save(*args, **kwargs)


class Transaction(models.Model):
    """Модель транзакции"""
    manufacturer = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='transaction_m',
                                     limit_choices_to={'role': 'manufacturer'})
    broker = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='transaction_b',
                               limit_choices_to={'role': 'broker'})
    number_of_billets = models.PositiveIntegerField(verbose_name='Количество')
    billet_price = models.PositiveIntegerField(verbose_name="Цена за заготовку")
    costs_transporting_single = models.PositiveIntegerField(default=10)
    approved_by_broker = models.BooleanField(default=False)
    # FIXME Поменял ссылку на номер хода с отдельной модели на ссылку статуса сессии
    turn = models.ForeignKey(Turn, on_delete=models.CASCADE, related_name='transaction', default='')

    def __str__(self):
        return f'Сделка между {self.manufacturer} и {self.broker} на {self.turn} ходу'

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'


class UserWebSocket(models.Model):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=255)
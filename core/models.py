import json

from django.contrib.auth.models import AbstractUser
from django.db import models

BROKER = 'M'
MANUFACTURER = 'P'


class MainUser(AbstractUser):
    pass


class City(models.Model):

    COSTS = (
        ('1', 20),
        ('2', 15),
        ('3', 10)
    )

    name = models.CharField(max_length=30, verbose_name="Название города")
    cost = models.CharField(max_length=1, choices=COSTS)

    def __str__(self):
        return f'{self.name}'


class Profile(models.Model):
    ROLES = (
        (BROKER, "Маклер"),
        (MANUFACTURER, "Производитель")
    )

    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='profile')
    balance = models.IntegerField(verbose_name="Баланс", default=0)
    city = models.ForeignKey(City, verbose_name='Город',
                             related_name='citi',
                             on_delete=models.CASCADE,
                             blank=True
                             )
    role = models.CharField(max_length=1, choices=ROLES, blank=True)

    def __str__(self):
        return f'{self.user.username} {self.city.name}'


class Transaction(models.Model):
    broker = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='broker')
    manufacturer = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='manufacturer')
    material_quantity = models.IntegerField(verbose_name='Количество')
    transaction_price = models.IntegerField(verbose_name="Цена сделки")


class Step(models.Model):
    step_num = models.IntegerField(verbose_name='Игровой шаг', blank=True, default='')
    step_time = models.IntegerField(verbose_name='Время шага', blank=True, default='')
    transaction = models.ManyToManyField(Transaction, related_name='gamestep')

class GameSetting(models.Model):
    manufacturer_balance = models.IntegerField(verbose_name='Баланс производителя')
    broker_balance = models.IntegerField(verbose_name="Баланс маклера")
    crow_balance = models.IntegerField(verbose_name="Баланс короны")
    transaction_limit = models.IntegerField(verbose_name="Лимит сделки")


class Game(models.Model):
    turn_count = models.IntegerField(verbose_name='Количество шагов')
    settings = models.ForeignKey(GameSetting, related_name='settings', on_delete=models.SET_NULL, null=True)
    step = models.ManyToManyField(Step, related_name='gamestep')
    user = models.ManyToManyField(Profile, verbose_name='Профиль игрока', related_name='profile')

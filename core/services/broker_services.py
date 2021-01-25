from ..models import Player, Transaction

costs_fixed = 1000

market_billets_count = 0
# FIXME Фильтровать по сессии и номеру хода
market_transactions = Transaction.objects.filter(turn_id=1)
# TODO Добавить session_id в фильтр
brokers = Player.objects.filter(role='broker', is_bankrupt=False)

for transaction in market_transactions:
    market_billets_count += transaction.number_of_billets

crown_balance = 12000

market_billet_price = int(crown_balance / market_billets_count)

for broker in brokers:

    transactions = broker.transaction_b.filter(approved_by_broker=True)
    costs_purchase = 0
    billets_bought = 0

    for transaction in transactions:
        billets_bought += transaction.number_of_billets
        costs_purchase += transaction.number_of_billets * transaction.billet_price

    balance_updated_1 = broker.balance - costs_purchase

    if balance_updated_1 < 0:
        broker.is_bankrupt = True
        print(f'{broker.nickname}, Вы не смогли оплатить заказанные заготовки!')
        broker.save()
        continue

    balance_updated_2 = balance_updated_1 - costs_fixed

    if balance_updated_2 < 0:
        broker.is_bankrupt = True
        print(f'{broker.nickname}, Вам не хватило средств на доставку товара Короне!')
        broker.save()
        continue

    balance_updated_3 = balance_updated_2 + billets_bought * market_billet_price

    broker.balance = balance_updated_3
    broker.save()

    print(f'Сделки брокера {broker.nickname} прошли успешно! Баланс на следующий ход: {broker.balance}')

# from core.services import services

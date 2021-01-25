from crow.core.services.dummie_brokers import brokers
from crow.core.services.dummie_transactions import transactions

costs_fixed = 1000

market_billets_count = 0
for transaction in transactions:
    market_billets_count += transaction['number_of_billets']

crown_balance = 12000

market_billet_price = int(crown_balance / market_billets_count)

for broker in brokers:

    costs_purchase = 0
    billets_bought = 0

    for transaction in broker['transactions']:
        billets_bought += transaction['number_of_billets']
        costs_purchase += transaction['number_of_billets'] * transaction['billet_price']

    balance_updated_1 = broker['balance'] - costs_purchase

    if balance_updated_1 < 0:
        broker['is_bankrupt'] = True
        print(f'{broker["nickname"]}, Вы не смогли оплатить заказанные заготовки!')
        continue

    balance_updated_2 = balance_updated_1 - costs_fixed

    if balance_updated_2 < 0:
        broker['is_bankrupt'] = True
        print(f'{broker["nickname"]}, Вам не хватило средств на доставку товара Короне!')
        continue

    balance_updated_3 = balance_updated_2 + billets_bought * market_billet_price

    broker['balance'] = balance_updated_3

    print(f'Сделки брокера {broker["nickname"]} прошли успешно! Баланс на следующий ход: {balance_updated_3}')



from .dummie_transactions import *

broker_1 = {
    'nickname': 'i_kstati',
    'user': 'test_user_7',
    'session': 'Dummie Session',
    'city': 'NF',
    'role': 'broker',
    'balance': 8000,
    'transactions': [transaction_1, transaction_4, transaction_7],
    'is_bankrupt': False,
}

broker_2 = {
    'nickname': 'ya_buduschii',
    'user': 'test_user_8',
    'session': 'Dummie Session',
    'city': 'TT',
    'role': 'broker',
    'transactions': [transaction_2, transaction_5],
    'balance': 8000,
    'is_bankrupt': False,
}

broker_3 = {
    'nickname': 'hokage',
    'user': 'test_user_9',
    'session': 'Dummie Session',
    'city': 'WS',
    'role': 'broker',
    'transactions': [transaction_3, transaction_6],
    'balance': 8000,
    'is_bankrupt': False,
}

brokers = [broker_1, broker_2, broker_3]
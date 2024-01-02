
#то что ниже обязательно заполнить своими данными
proxy_use = 0 #  0 - не использовать, 1 - прокси без ссылки , 2 - прокси со ссылкой для смены ip
proxy_login = 'plu'
proxy_password = '5p'
proxy_address = 'gate.nodemaven.com'
proxy_port = '8080'
proxy_changeIPlink = "httpcce3b204"


#то что ниже желательно настроить под себя
minimal_need_balance = 1 # минимальный баланс на кошельке который должен быть чтобы забрать дроп 1 USDC
minimal_need_eth_optimism = 0.5 # минимальный баланс эфира в сети оптимизм указывается в $

#укажите паузу в работе между кошельками, минимальную и максимальную. 
#При смене каждого кошелька будет выбрано случайное число. Значения указываются в секундах
timeoutMin = 10 #минимальная 
timeoutMax = 30 #максимальная
#задержки между операциями в рамках одного кошелька
timeoutTehMin = 10 #минимальная 
timeoutTehMax = 30 #максимальная



#то что ниже можно менять только если понимаешь что делаешь
proxies = { 'all': f'http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}',}
if proxy_use:
    request_kwargs = {"proxies":proxies, "timeout": 120}
else:
    request_kwargs = {"timeout": 120}

slippage = 1    # % 
gas_kef=1.1 #коэфициент допустимого расхода газа на подписание транзакций. можно выставлять от 1.1 до 2

rpc_links = {
    'ETH': 'https://rpc.ankr.com/eth',
    'zkfair': 'https://rpc.zkfair.io',
    'optimism':  'https://rpc.ankr.com/optimism',
}


prices = {
    "ETH": 2400,
    "USDC": 1,
    "last_update": 0
}




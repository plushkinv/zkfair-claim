import json
from statistics import mean
import time
from web3 import Web3
from eth_account.messages import encode_defunct
import requests
import random
from datetime import datetime
import config
import fun
from fun import log, log_error, log_ok, save_wallet_to, timeOut




current_datetime = datetime.now()
print(f"\n\n {current_datetime}")
print(f'============================================= Плюшкин Блог =============================================')
print(f'subscribe to : https://t.me/plushkin_blog \n============================================================================================================\n')

keys_list = []
with open("private_keys_step0.txt", "r") as f:
    for row in f:
        private_key=row.strip()
        if private_key:
            keys_list.append(private_key)

# random.shuffle(keys_list)
i=0
for private_key in keys_list:
    i+=1
    # fun.get_new_prices()
    if config.proxy_use == 2:
        while True:
            try:
                requests.get(url=config.proxy_changeIPlink)
                fun.timeOut("teh")
                result = requests.get(url="https://yadreno.com/checkip/", proxies=config.proxies)
                print(f'Ваш новый IP-адрес: {result.text}')
                break
            except Exception as error:
                print(' !!! Не смог подключиться через Proxy, повторяем через 2 минуты... ! Чтобы остановить программу нажмите CTRL+C или закройте терминал')
                time.sleep(120)

    
    
    try:
        web3 = Web3(Web3.HTTPProvider(config.rpc_links['zkfair'], request_kwargs=config.request_kwargs))
        account = web3.eth.account.from_key(private_key)
        wallet = account.address    
        log(f"I-{i}: Начинаю работу с {wallet}")

        current_date_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        text_origin = current_date_time + "GET/api/airdrop?address=" + wallet
        message = encode_defunct(text=text_origin)
        text_signature = web3.eth.account.sign_message(message, private_key=private_key)
        signature_value = text_signature.signature.hex()
        # print(signature_value)

        url=f"https://airdrop.zkfair.io/api/airdrop?address={wallet}&API-SIGNATURE={signature_value}&TIMESTAMP={current_date_time}"
        # print(url)
        headers = {
            "authority": "airdrop.zkfair.io",
            "accept": "application/json, text/plain, */*",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "origin": "https://zkfair.io",
            "referer": "https://zkfair.io/",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }

        if config.proxy_use:
            result = requests.get(url=url, proxies=config.proxies, headers=headers)
        else:
            result = requests.get(url=url, headers=headers)
        if(result.status_code != 200):
            log("ошибка получения данных с API")
            continue

        # print(result.text)
        response_data = json.loads(result.text)
        account_profit = response_data['data']['account_profit']
        index = response_data['data']['index']

        if not account_profit:
            log("no drop")
            save_wallet_to("no_drop_wa", wallet)
        else:
            account_profit_decimal = int(account_profit) / 10**18
            log_ok(f"drop = {account_profit_decimal}")   
            fun.save_private_key_to("private_keys_step1", private_key)            

        fun.delete_private_key_from_file("private_keys_step0", private_key)
        timeOut("teh")


    except Exception as error:
        fun.log_error(f'step0 false: {error}')    
        save_wallet_to("step0_false_pk", private_key)
        continue


    
log("Ну типа все!")
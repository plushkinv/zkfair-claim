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
from fun import log, save_wallet_to, timeOut




current_datetime = datetime.now()
print(f"\n\n {current_datetime}")
print(f'============================================= Плюшкин Блог =============================================')
print(f'subscribe to : https://t.me/plushkin_blog \n============================================================================================================\n')

i=0
while True:
    keys_list = []
    with open("private_keys_step2.txt", "r") as f:
        for row in f:
            private_key=row.strip()
            if private_key:
                keys_list.append(private_key)

    if len(keys_list) == 0:
        log("НЕт приватных ключей в step2")
        timeOut()
        timeOut("teh")
        continue

    random.shuffle(keys_list)
    for private_key in keys_list:
        i+=1
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
            balance = web3.eth.get_balance(wallet)
            balance_decimal = Web3.from_wei(balance, 'ether')        

            if balance_decimal < config.minimal_need_balance:
                log("Недостаточно USDC.  жду когда пополнишь. на следующем круге попробую снова")
                timeOut("teh")
                continue

            current_date_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            text_origin = current_date_time + "GET/api/airdrop?address=" + wallet
            message = encode_defunct(text=text_origin)
            text_signature = web3.eth.account.sign_message(message, private_key=private_key)
            signature_value = text_signature.signature.hex()
            # print(signature_value)
            gasPrice = web3.eth.gas_price

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

            if account_profit == 0:
                log("no drop")
                fun.delete_private_key_from_file("private_keys_step2", private_key)
                save_wallet_to("no_drop_wa", wallet)
                timeOut("teh")
                continue                

            url=f"https://airdrop.zkfair.io/api/airdrop_merkle?address={wallet}&API-SIGNATURE={signature_value}&TIMESTAMP={current_date_time}"
            if config.proxy_use:
                result = requests.get(url=url, proxies=config.proxies, headers=headers)
            else:
                result = requests.get(url=url, headers=headers)
            if(result.status_code != 200):
                log("ошибка получения данных с API")
                continue
            
            response_data = json.loads(result.text)
            # print(response_data)


            data = "0xae0b51df" + web3.to_bytes(int(index)).hex().zfill(64) + web3.to_bytes(int(account_profit)).hex().zfill(64) + "00000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000014"
            # Извлечение массива proof из JSON-объекта с удалением префикса "0x"
            proof_array = [item.replace("0x", "") for item in response_data["data"]["proof"]]
            # Преобразование массива в формат строки с элементами массива
            data = data + "".join(proof_array)

            # print(data)

            gasPrice = web3.eth.gas_price

            transaction = {
                'chainId': web3.eth.chain_id,
                'from': wallet,
                'to': Web3.to_checksum_address("0x53c390b02339519991897b59eb6d9e0b211eb840"),
                'value': 0,
                "gasPrice": gasPrice ,
                'nonce': web3.eth.get_transaction_count(wallet),
                'data': data
            }
            gasLimit = web3.eth.estimate_gas(transaction)
            transaction['gas'] = int(gasLimit * config.gas_kef)

            # Подписываем и отправляем транзакцию
            signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = web3.to_hex(web3.eth.send_raw_transaction(signed_txn.rawTransaction))
            tx_result = web3.eth.wait_for_transaction_receipt(tx_hash)

            if tx_result['status'] == 1:
                fun.log_ok(f'mint  OK: https://scan.zkfair.io/tx/{tx_hash}')
                save_wallet_to("step2_ok_pk", private_key)
                fun.save_private_key_to("private_keys_step3", private_key)            
                fun.delete_private_key_from_file("private_keys_step2", private_key)
                fun.delete_wallet_from_file("step2_false_pk", private_key)                
            else:
                fun.log_error(f'mint false: https://scan.zkfair.io/tx/{tx_hash}')
                save_wallet_to("step2_false_pk", private_key)
                continue


                    
            

        except Exception as error:
            fun.log_error(f'step2  false: {error}')
            save_wallet_to("step2_false", private_key)
            continue

        timeOut()














    
log("Ну типа все!")
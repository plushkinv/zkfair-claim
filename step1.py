import json
from statistics import mean
import time
from web3 import Web3
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
with open("private_keys_step1.txt", "r") as f:
    for row in f:
        private_key=row.strip()
        if private_key:
            keys_list.append(private_key)

random.shuffle(keys_list)
i=0
for private_key in keys_list:
    i+=1
    fun.get_new_prices()
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
        web3 = Web3(Web3.HTTPProvider(fun.address['optimism']['rpc'], request_kwargs=config.request_kwargs))
        account = web3.eth.account.from_key(private_key)
        wallet = account.address
        log(f"I-{i}: Начинаю работу с {wallet}")
        
        native_balance_USD = fun.get_token_balance_USD(wallet, 'optimism', fun.address['optimism']['native'])
        erc20_balance_USD = fun.get_token_balance_USD(wallet, 'optimism', 'USDC')

        if native_balance_USD < config.minimal_need_eth_optimism:
            log_error("Недостаточно нативнки на кошельке Для транзакций")
            save_wallet_to("no_money_eth_wa", wallet)
            continue
        if erc20_balance_USD < config.minimal_need_balance + 1.2:
            log_error("Недостаточно USDC  ")
            save_wallet_to("no_money_USDC_wa", wallet)
            continue    


        maxPriorityFeePerGas = web3.eth.max_priority_fee
        fee_history = web3.eth.fee_history(10, 'latest', [10, 90])
        baseFee=round(mean(fee_history['baseFeePerGas']))
        maxFeePerGas = maxPriorityFeePerGas + round(baseFee * config.gas_kef)

        #ORBITER
        maxPriorityFeePerGas = web3.eth.max_priority_fee
        fee_history = web3.eth.fee_history(10, 'latest', [10, 90])
        baseFee=round(mean(fee_history['baseFeePerGas']))
        maxFeePerGas = maxPriorityFeePerGas + round(baseFee * config.gas_kef)


        erc20_address = web3.to_checksum_address(fun.address['optimism']['USDC'])
        erc20_contract = web3.eth.contract(address=erc20_address, abi=fun.erc20_abi)
        token_decimals = erc20_contract.functions.decimals().call()
        balance = erc20_contract.functions.balanceOf(wallet).call()
        balance_decimals = balance / 10 ** token_decimals

        value = (balance - 10000) // 10000 * 10000 + 9038

        print(f"потратим  {balance_decimals} USDC")


        transaction = erc20_contract.functions.transfer(
            Web3.to_checksum_address("0x41d3D33156aE7c62c094AAe2995003aE63f587B3"),
            value
            ).build_transaction({
            'from': wallet,
            'maxFeePerGas': maxFeePerGas,
            'maxPriorityFeePerGas': maxPriorityFeePerGas,     
            'nonce': web3.eth.get_transaction_count(wallet),
        })

        # transaction = {
        #         "chainId": web3.eth.chain_id,
        #         'from': wallet,
        #         'to': Web3.to_checksum_address("0x41d3D33156aE7c62c094AAe2995003aE63f587B3"),
        #         'value':value,
        #         'maxFeePerGas': maxFeePerGas,
        #         'maxPriorityFeePerGas': maxPriorityFeePerGas,            
        #         'nonce': web3.eth.get_transaction_count(wallet),
        # }
        gasLimit = web3.eth.estimate_gas(transaction)
        transaction.update({'gas': gasLimit})  

        

        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        txn_hash = web3.to_hex(web3.eth.send_raw_transaction(signed_txn.rawTransaction))
        tx_result = web3.eth.wait_for_transaction_receipt(txn_hash)

        if tx_result['status'] == 1:
            log_ok(f'bridge OK: https://optimistic.etherscan.io/tx/{txn_hash}')
            save_wallet_to("bridge_ok_pk", private_key)
            fun.delete_private_key_from_file("private_keys_step1", private_key)
            fun.save_private_key_to("private_keys_step2", private_key)
            fun.delete_wallet_from_file("no_money_eth_wa", wallet)
            fun.delete_wallet_from_file("no_money_USDC_wa", wallet)
            fun.delete_wallet_from_file("bridge_false_pk", private_key)
        else:
            log_error(f'bridge false: https://optimistic.etherscan.io/tx/{txn_hash}')
            save_wallet_to("bridge_false_pk", private_key)
            fun.delete_wallet_from_file("no_money_eth_wa", wallet)
            fun.delete_wallet_from_file("no_money_USDC_wa", wallet)

    


        timeOut()


    except Exception as error:
        fun.log_error(f'step1 false: {error}')    
        save_wallet_to("bridge_false_pk", private_key)
        continue


    
log("Ну типа все!")
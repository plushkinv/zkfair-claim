# Автор
PLushkin https://t.me/plushkin_blog        

**На чай с плюшками автору:**
Полигон, БСК, Арбитрум - любые токены - `0x79a266c66cf9e71Af1108728e455E0B1D311e95E`

Трон TRC-20 только USDT, остальное не доходит - `TEZG4iSmr31wWnvBixKgUN9Aax4bbgu1s3`

# Чё делает
step1 - перегоняет USDC из сети оптимизм в сеть ZKfair. Перегоняет весь баланс который есть. минимум надо иметь 2.2USDC

step2 - клеймит дроп , если он есть.

step3 - меняет токены ZKF на USDC  на DEX

step4 - перегоняет USDC из сети ZKfair  в сеть оптимизм. Перегоняет весь баланс который есть.

# Настройка
Что бы избежать лищних проблем с ограничениями или блокировками, используйте ротируемые прокси
https://go.nodemaven.com/plushkinva
Промик на 2 бесплатных гигабайта FREE2G  при покупке трафика
Промик просто на 500mb без оплат и привязки карты FREE500

# Установка и запуск: Linux/Mac

Linux/Mac - https://www.youtube.com/watch?v=8rJ-96cPFwU
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python main.py
```
Windows - https://www.youtube.com/watch?v=EqC42mnbByc
```
pip install virtualenv
virtualenv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python main.py
```



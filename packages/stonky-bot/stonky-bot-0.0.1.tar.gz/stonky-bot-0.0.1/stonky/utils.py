from datetime import datetime
from json import dump, load
from os import path

from krakenex import API

k = API()
k.load_key("kraken.key")

# ---- UTILITY


def save_data(strategy, data, file):
    filepath = path.join("data", strategy, f"{strategy}_{file}.json")
    dump(data, open(filepath, "w+"), indent=4)


def load_data(strategy, file):
    filepath = path.join("data", strategy, f"{strategy}_{file}.json")
    return load(open(filepath))


def save_trade(strategy, close, name, action, amount):
    now = datetime.now()
    trade = {
        "timestamp": int(datetime.timestamp(now)),
        "datetime": f"{now:%d.%m.%Y %H:%M:%S}",
        "price": close,
        "action": action,
        "amount": amount,
    }
    trades = load_data(strategy, "trades")
    trades[name].append(trade)
    save_data(strategy, trades, "trades")


def get_balance(strategy):
    # return k.query_private("Balance").get("result")
    return load_data(strategy, "balance")


def update_balance(strategy, name_balance, name, price, amount, sold):
    balance = get_balance(strategy)
    balance.pop(name, None) if sold else balance.update({name: amount})
    balance[name_balance] += (-1, 1)[sold] * amount * price
    save_data(strategy, balance, "balance")


# ---- Operation


def buy_crypto(strategy, name_balance, name, price, amount):
    # TODO: we need to real buy here
    update_balance(strategy, name_balance, name, price, amount, False)
    save_trade(strategy, price, name, "buy", amount)


def sell_crypto(strategy, name_balance, name, price, amount):
    # TODO: we need to real sell here
    update_balance(strategy, name_balance, name, price, amount, True)
    save_trade(strategy, price, name, "sell", amount)

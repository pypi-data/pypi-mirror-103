from functools import reduce
from os import makedirs, path
from re import sub

from utils import buy_crypto, get_balance, load_data, save_data, sell_crypto


class MeanTrend:
    def __init__(
        self, name, currency, budget, pairs, up_power, profit, down_power, loss
    ):
        self.name = sub(r"\s+", "_", name)
        self.interval = 1
        self.main_balance = currency
        self.pairs = pairs
        self.up = up_power
        self.profit = profit
        self.down = down_power
        self.loss = loss
        data_basepath = path.join("data", self.name)
        if not path.exists(data_basepath):
            makedirs(data_basepath)
        save_data(self.name, {self.main_balance: budget}, "balance")
        save_data(self.name, {crypto: [] for crypto in self.pairs}, "trades")
        save_data(
            self.name,
            {
                name: {"high": [], "low": [], "close": [], "last-price": []}
                for name in self.pairs
            },
            "data",
        )

    def iteration(self, main_crypto_data):
        for pair in self.pairs:
            trades = load_data(self.name, "trades")
            crypto_stored = load_data(self.name, "data")
            crypto_data = main_crypto_data.get(f"{pair}-{self.interval}")
            if trades.get(pair) and trades.get(pair)[-1].get("action") == "buy":
                action = self._action(pair, crypto_data, crypto_stored, buy=False)
                if action:
                    sell_crypto(self.name, self.main_balance, *action)
            else:
                action = self._action(pair, crypto_data, crypto_stored)
                if action:
                    buy_crypto(self.name, self.main_balance, *action)

    def _action(self, name, crypto_data, crypto_stored, buy=True):
        # update mean
        crypto = crypto_stored.get(name)
        crypto_data = crypto_data[-60:]
        self._update_crypto_data(crypto_data, crypto)
        save_data(self.name, crypto_stored, "data")
        make_trade = self._check_opportunity(crypto, name, buy=buy)
        if make_trade:
            # amout
            balance = get_balance(self.name)
            price = crypto.get("last-price").get("close")
            if buy:
                money = balance.get(self.main_balance)
                crypto_not_owned = len(self.pairs) - len(balance) + 1
                amount = money / crypto_not_owned * (1 / price)
            else:
                amount = balance.get(name)
            return name, price, amount
        return None

    def _update_crypto_data(self, c_data, c_stored):
        high, low, close = reduce(
            lambda x, y: (x[0] + float(y[2]), x[1] + float(y[3]), x[2] + float(y[4])),
            c_data,
            (0, 0, 0),
        )
        c_stored.update({"high": c_stored.get("high")[-9:] + [high / len(c_data)]})
        c_stored.update({"low": c_stored.get("low")[-9:] + [low / len(c_data)]})
        c_stored.update({"close": c_stored.get("close")[-9:] + [close / len(c_data)]})
        labels = ("timestamp", "open", "high", "low", "close")
        c_stored.update({"last-price": dict(zip(labels, map(float, c_data[-1][:5])))})

    def _check_opportunity(self, data, name, buy):
        # calculate trends
        prices = data.get("close")
        prices = reduce(
            lambda x, y: x + [y] if x[-1] != y else x, prices[1:], prices[:1]
        )
        trends, _ = reduce(
            lambda x, y: (x[0] + [y > x[1]], y), prices[1:], ([], prices[0])
        )
        power, trend = (
            reduce(
                lambda x, y: (x[0] + 1 if x[1] == y else 1, y),
                trends[1:],
                (1, trends[0]),
            )
            if trends
            else (0, None)
        )
        power *= (-1, 1, 0)[trend is None and 2 or trend]
        # check opportunity
        close_prices = data.get("close")
        last_price = float(data.get("last-price").get("close"))
        mean_latest = sum(cp / last_price for cp in close_prices) / len(close_prices)
        if not buy:
            purchase_price = load_data(self.name, "trades").get(name)[-1].get("price")
            if last_price < purchase_price or (
                power <= -self.down and mean_latest <= 1 - self.loss
            ):
                return True
        else:
            if power >= self.up and mean_latest >= 1 + self.profit:
                return True
        return False

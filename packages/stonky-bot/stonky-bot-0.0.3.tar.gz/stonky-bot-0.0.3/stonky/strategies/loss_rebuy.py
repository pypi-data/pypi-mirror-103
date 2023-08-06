from os import makedirs, path
from re import sub

from stornky.utils import save_data


class LossReBuy:
    def __init__(
        self, name, currency, budget, pairs, single_buy, max_open, threshold, rebuy
    ):
        self.name = sub(r"\s+", "_", name)
        self.interval = 5
        self.main_balance = currency
        self.pairs = pairs
        self.single_buy = single_buy
        self.max_open = max_open
        self.threshold = threshold
        self.rebuy = rebuy
        data_basepath = path.join("data", self.name)
        if not path.exists(data_basepath):
            makedirs(data_basepath)
        save_data(self.name, {self.main_balance: budget}, "balance")

    def iteration(self, main_crypto_data):
        ...

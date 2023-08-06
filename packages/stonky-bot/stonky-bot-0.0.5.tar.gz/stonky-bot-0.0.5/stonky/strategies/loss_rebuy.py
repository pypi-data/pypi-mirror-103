from re import sub

from stonky.utils import create_data


class LossReBuy:
    def __init__(
        self, name, currency, budget, pairs, single_buy, max_open, threshold, rebuy
    ):
        self.name = sub(r"\s+", "_", name)
        self.interval = 5
        self.currency = currency
        self.budget = budget
        self.pairs = pairs
        self.single_buy = single_buy
        self.max_open = max_open
        self.threshold = threshold
        self.rebuy = rebuy
        create_data(self.name, self.currency, self.budget)

    def iteration(self, main_crypto_data):
        ...

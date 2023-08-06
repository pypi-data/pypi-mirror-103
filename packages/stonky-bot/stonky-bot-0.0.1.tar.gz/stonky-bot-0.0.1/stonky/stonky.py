#!/Users/Moris/Script/Stonky/.env/bin/python3

from datetime import datetime
from json import load
from time import sleep

from strategies.loss_rebuy import LossReBuy
from strategies.mean_trend import MeanTrend
from utils import k


def bot_instance(bot):
    strategies = {"mean-trend": MeanTrend, "loss-rebuy": LossReBuy}
    return strategies.get(bot.get("strategy"))(*list(bot.values())[1:])


def get_crypto_data(bots):
    since = datetime.timestamp(datetime.now()) - 86400  # 1 day
    search = set((pair, bot.interval) for bot in bots for pair in bot.pairs)
    print(search)
    return {
        f"{pair}-{interval}": k.query_public(
            "OHLC", data={"pair": pair, "interval": interval, "since": since}
        )
        .get("result")
        .get(pair)
        for pair, interval in search
    }


def main():
    bots = [bot_instance(bot) for bot in load(open("bots.json")).get("bots")]
    while True:
        CRYPTO_DATA = get_crypto_data(bots)
        for bot in bots:
            print(f"---- BOT [{bot.name}] ----")
            bot.iteration(CRYPTO_DATA)
        sleep(10)


if __name__ == "__main__":
    main()

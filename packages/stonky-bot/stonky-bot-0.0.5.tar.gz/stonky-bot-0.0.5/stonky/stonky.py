#!/Users/Moris/Script/Stonky/.env/bin/python3

from argparse import ArgumentParser
from datetime import datetime
from json import dump, load
from os import path
from time import sleep

from colorifix.colorifix import Color, paint
from krakenex import API
from stonky.strategies.loss_rebuy import LossReBuy
from stonky.strategies.mean_trend import MeanTrend

KRAKEN = API()
STRATEGIES = {"mean-trend": MeanTrend, "loss-rebuy": LossReBuy}


def verify(conf_path):
    result = True
    abspath = path.join(path.abspath(conf_path))
    # config file
    if not path.exists(path.join(abspath, "config.json")):
        filename = path.join(abspath, "config.json")
        base_config = {"bots": [], "user": "starter", "interval": 60}
        dump(base_config, open(filename, "w+"), indent=4)
        print(paint("Config file not found!", Color.RED))
        print("  # created " + paint(filename, Color.BLUE) + ".")
        print("  # please edit this file before continue!")
        result = False
    # kraken key
    if not path.exists(path.join(abspath, "kraken.key")):
        filename = path.join(abspath, "kraken.key")
        open(filename, "w+").write("publickey\nprivatekey")
        url = "https://www.kraken.com/u/security/api"
        print(paint("Kraken API key not found!", Color.RED))
        print("  # created " + paint(filename, Color.BLUE) + ".")
        print("  # please get your API key here " + paint(url, Color.BLUE))
        result = False
    else:
        KRAKEN.load_key(path.join(abspath, "kraken.key"))
        try:
            KRAKEN.query_private("OpenOrders").get("result").get("open")
        except Exception:
            print(paint("Kraken API key not valid", Color.RED))
            result = False
    # bots
    config_file = load(open(path.join(abspath, "config.json")))
    bots_config = config_file.get("bots")
    # bots properties
    if result:
        bot_result = True
        for i, bot in enumerate(bots_config, 1):
            for label in ("strategy", "name", "currency", "budget", "pairs"):
                if label not in bot:
                    print(paint(f"Missing attribute '{label}' (bot {i})", Color.RED))
                    bot_result = False
        if bot_result:
            bots = list()
            for i, bot in enumerate(bots_config, 1):
                strat = bot.get("strategy")
                if not (b := STRATEGIES.get(strat)):
                    print(paint(f"Invalid strategy '{strat}' (bot {i})", Color.RED))
                    result = False
                else:
                    bots.append(b(*list(bot.values())[1:]))
            # bots = [bot_instance(bot) for bot in bots_config]
            bots_name = [bot.name for bot in bots]
            # unique strategy name
            if len(bots_name) != len(set(bots_name)):
                print(paint("Bots name must have a unique name", Color.RED))
                result = False
            # API calls limit
            pairs = set([(pair, bot.interval) for bot in bots for pair in bot.pairs])
            main_interval = config_file.get("interval")
            user_type = config_file.get("user")
            limit = {"starter": 3, "intermediate": 2, "pro": 1}.get(user_type, 3)
            if main_interval / (len(pairs) or 1) < limit:
                print(paint("API calls limit exceeded", Color.RED))
                max_interval = len(pairs) * limit
                max_pairs = int(main_interval / limit)
                print(f"  # you need to increment the interval to {max_interval}")
                print(f"  # or descrease the number of unique pairs to {max_pairs}")
                result = False
    return result and bot_result and (bots, pairs, main_interval / (len(pairs) or 1))


def get_crypto_data(bots, pairs, interval):
    since = datetime.timestamp(datetime.now()) - 86400  # 1 day
    data = dict()
    for pair, pair_interval in pairs:
        api_call = KRAKEN.query_public(
            "OHLC", data={"pair": pair, "interval": pair_interval, "since": since}
        )
        data_retrieve = api_call and (res := api_call.get("result")) and res.get(pair)
        if not data_retrieve:
            return None
        data[f"{pair}-{pair_interval}"] = data_retrieve
        sleep(interval)
    return data


# ---- MAIN


def argparsing():
    parser = ArgumentParser(
        prog="Stonky",
        description="STONKS!",
        usage=("stonky [-p path : default=.]"),
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="path for storing data and config files",
        metavar=("PATH"),
    )
    return parser.parse_args()


def main():
    args = argparsing()
    path = args.path or "."
    result = verify(path)
    if not result:
        exit(-1)
    print(paint("OK!", Color.GREEN))
    bots, pairs, interval = result
    if bots and pairs:
        while True:
            while not (CRYPTO_DATA := get_crypto_data(bots, pairs, interval)):
                sleep(2)
            for bot in bots:
                bot.iteration(CRYPTO_DATA)


if __name__ == "__main__":
    main()

import os
import sys
sys.path.append(os.getcwd())
import copy
import codecs
from exchange_market.bar import RawBar
from utils.mysql.connect import SQLUtils
from exchange_market.binance.enum import Interval
from examples.bars_generator import BarsGenerator
from exchange_market.binance.future import Future
from examples.binance.strategy.open_rsi_prod import Strategy

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
future = Future()


def raw_bars_generator(datas, bar):
    bars = []
    for data in datas:
        data = data.split(",")
        rb = RawBar(exchange="binance", symbol=data[0].strip(), dt=data[1].strip(), open=float(data[2].strip()),
                    high=float(data[3].strip()), low=float(data[4].strip()), close=float(data[5].strip()),
                    vol=float(data[6].strip()), interval=bar)
        bars.append(copy.deepcopy(rb))
    return bars


if __name__ == '__main__':
    symbol = "BTCUSDT"
    with codecs.open(filename=base_dir+"/data/market/crypto/{}.txt".format(symbol), mode="r", encoding="utf8") as f:
        datas = f.readlines()
    bars_m5 = raw_bars_generator(datas=datas, bar=Interval.min5.value)

    cache = {}
    sql_utils = SQLUtils(mode="debug")
    step_interval = Interval.min5.value
    bars_generator = BarsGenerator(future)
    # bars_m5 = bars_generator.get_bars_from_api(symbol=symbol)
    strategy = Strategy(symbol=symbol, bars_generator=bars_generator, cache=cache, mode="debug",
                        critic_interval=Interval.min30.value, desert_interval=Interval.min30.value, sql_utils=sql_utils)

    for idx, bar_5m in enumerate(bars_m5):
        # if string2mil(bar_5m.dt) < string2mil("2023-06-10 00:00:00"): continue
        bars_generator.compose(bar_5m=bar_5m)
        # if string2mil(bar_5m.dt) < string2mil("2023-01-30 00:00:00"): continue
        print("cur time:{}, cur symbol:{}, {}/{}".format(bar_5m.dt, symbol, idx, len(bars_m5)))
        strategy.run(symbol=symbol, bar_5m=bar_5m)
    sys.exit(0)

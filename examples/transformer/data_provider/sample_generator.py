import os, sys
from abc import ABC

sys.path.append(os.getcwd())
import copy
import codecs
import warnings
from pandas import Series
from torch.utils.data import Dataset
from exchange_market.bar import RawBar
from exchange_market.skeleton import Skeleton
from ta.volatility import BollingerBands
from exchange_market.binance.future import Future
from exchange_market.binance.enum import Interval, PositionSide
from examples.bars_generator import BarsGenerator
future = Future()
warnings.filterwarnings('ignore')
bars_generator = BarsGenerator(future)
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))


def raw_bars_generator(datas, bar):
    bars = []
    for data in datas:
        data = data.split(",")
        rb = RawBar(exchange="binance", symbol=data[0].strip(), dt=data[1].strip(), open=float(data[2].strip()),
                    high=float(data[3].strip()), low=float(data[4].strip()), close=float(data[5].strip()),
                    vol=float(data[6].strip()), interval=bar)
        bars.append(copy.deepcopy(rb))
    return bars


class Dataset5m(Dataset, ABC):
    def __init__(self, root_path=base_dir, flag='train', data_path='/data/market/crypto/BTCUSDT.txt', freq='5m'):
        pass

    @staticmethod
    def discrete_chg(symbol="BTCUSDT"):
        """ 基于k线振幅的差分向量化思路 """
        if os.path.exists(base_dir + "/data/market/crypto/{}_chg.txt".format(symbol)):
            os.remove(base_dir + "/data/market/crypto/{}_chg.txt".format(symbol))
        fx = codecs.open(base_dir + "/data/market/crypto/{}_chg.txt".format(symbol), mode="a", encoding="utf8")
        with codecs.open(filename=base_dir + "/data/market/crypto/{}.txt".format(symbol), mode="r",
                         encoding="utf8") as f:
            datas = f.readlines()
        bars_m5 = raw_bars_generator(datas=datas, bar=Interval.min5.value)

        intervals = [Interval.min5.value,
                     # Interval.min15.value, Interval.min30.value, Interval.hour1.value,
                     # Interval.hour4.value, Interval.day.value, Interval.week.value
                     ]
        for idx, bar_5m in enumerate(bars_m5):
            bars_generator.compose(bar_5m=bar_5m)
            print("cur time:{}, cur symbol:{}, {}/{}".format(bar_5m.dt, symbol, idx, len(bars_m5)))
            for interval in intervals:
                bars = bars_generator.get_bars(symbol=symbol, interval=interval, limit=31, end_time=bar_5m.dt)
                if len(bars) != 31: continue
                closes = Series([float(b.close) for b in bars[0:21]])
                boll = BollingerBands(close=closes, window=21)
                bl = boll.bollinger_lband().values
                bh = boll.bollinger_hband().values
                chg = [round((i.close-i.open)*100/i.open, 2) for i in bars]
                chg = ",".join([str(i) for i in chg[0:21]])
                maxh = max([i.high for i in bars[21:]])
                minl = max([i.low for i in bars[21:]])
                if maxh > bh[-1]:# + (bh[-1]-bl[-1]):
                    flag = 0  # up
                else:
                    flag = 1  # down
                data = str(flag) + " AinanceLabs " + bars[20].dt + "," + chg
                fx.write(data + "\n")
        fx.close()

    @staticmethod
    def discrete_delta(symbol="BTCUSDT"):
        """ 基于方差的向量化思路，收盘价=x*delta """
        if os.path.exists(base_dir + "/data/market/crypto/{}_delta.txt".format(symbol)):
            os.remove(base_dir + "/data/market/crypto/{}_delta.txt".format(symbol))
        fx = codecs.open(base_dir + "/data/market/crypto/{}_delta.txt".format(symbol), mode="a", encoding="utf8")
        with codecs.open(filename=base_dir + "/data/market/crypto/{}.txt".format(symbol), mode="r",
                         encoding="utf8") as f:
            datas = f.readlines()
        bars_m5 = raw_bars_generator(datas=datas, bar=Interval.min5.value)

        intervals = [Interval.min5.value,
                     # Interval.min15.value, Interval.min30.value, Interval.hour1.value,
                     # Interval.hour4.value, Interval.day.value, Interval.week.value
                     ]
        for idx, bar_5m in enumerate(bars_m5):
            bars_generator.compose(bar_5m=bar_5m)
            print("cur time:{}, cur symbol:{}, {}/{}".format(bar_5m.dt, symbol, idx, len(bars_m5)))
            for interval in intervals:
                bars = bars_generator.get_bars(symbol=symbol, interval=interval, limit=31, end_time=bar_5m.dt)
                if len(bars) != 31 or bars[0].taxx.delta == 0: continue
                label_threshold = bars[20].close + 2*bars[20].taxx.delta
                label_min = bars[20].close - bars[20].taxx.delta
                delta = [round((i.close - i.taxx.mavg21)/i.taxx.delta, 3) for i in bars]
                delta = ",".join([str(i) for i in delta[0:21]])
                maxh = max([i.high for i in bars[21:]])
                minl = max([i.low for i in bars[21:]])
                if maxh > label_threshold and minl > label_min:
                    flag = 0  # up
                else:
                    flag = 1  # down
                data = str(flag) + " AinanceLabs " + bars[20].dt + "," + delta
                fx.write(data + "\n")
        fx.close()

    @staticmethod
    def discrete_macd_chg(symbol="BTCUSDT", num_features=7):
        """ 基于macd分型关键点的离散量化思路 """
        if os.path.exists(base_dir + "/data/market/crypto/{}_macd.txt".format(symbol)):
            os.remove(base_dir + "/data/market/crypto/{}_macd.txt".format(symbol))
        fx = codecs.open(base_dir + "/data/market/crypto/{}_macd.txt".format(symbol), mode="a", encoding="utf8")
        with codecs.open(filename=base_dir + "/data/market/crypto/{}.txt".format(symbol), mode="r",
                         encoding="utf8") as f:
            datas = f.readlines()
        bars_m5 = raw_bars_generator(datas=datas, bar=Interval.min5.value)

        intervals = [
            # Interval.min5.value,
                     # Interval.min15.value,
                     # Interval.min30.value,
                     # Interval.hour1.value,
                     Interval.hour4.value,
                     # Interval.day.value, Interval.week.value
                     ]
        skeletons = []
        skeletons_bars = []
        olds = []
        for idx, bar_5m in enumerate(bars_m5):
            bars_generator.compose(bar_5m=bar_5m)
            print("cur time:{}, cur symbol:{}, {}/{}".format(bar_5m.dt, symbol, idx, len(bars_m5)))
            for interval in intervals:
                bars = bars_generator.get_bars(symbol=symbol, interval=interval, limit=21, end_time=bar_5m.dt)
                if len(bars) != 21 or bars[0].taxx.delta == 0: continue
                if 0 > bars[-1].taxx.macd > bars[-2].taxx.macd and bars[-3].taxx.macd > bars[-2].taxx.macd:
                    skeleton = Skeleton(symbol=symbol, price=bars[-2].close, direction=PositionSide.LONG.value, interval=interval, dt=bars[-1].dt)
                    if skeleton.dt+str(skeleton.price) not in olds:
                        olds.append(skeleton.dt+str(skeleton.price))
                        skeletons.append(skeleton)
                        skeletons_bars.append(bars[-1])
                elif 0 < bars[-1].taxx.macd < bars[-2].taxx.macd and bars[-3].taxx.macd < bars[-2].taxx.macd:
                    skeleton = Skeleton(symbol=symbol, price=bars[-2].close, direction=PositionSide.SHORT.value, interval=interval, dt=bars[-1].dt)
                    if skeleton.dt+str(skeleton.price) not in olds:
                        olds.append(skeleton.dt+str(skeleton.price))
                        skeletons.append(skeleton)
                        skeletons_bars.append(bars[-1])

                if len(skeletons) < 7: continue
                if skeletons[-1].dt in olds: continue
                olds.append(skeletons[-1].dt)
                # label_threshold = bars[20].close + 2 * bars[20].taxx.delta
                # label_min = bars[20].close - bars[20].taxx.delta
                # chg = [i.price for i in skeletons[-6:]]
                chg = [round((i.close - i.taxx.mavg21) / i.taxx.delta, 3) for i in skeletons_bars[-7:-1]]
                # chg = [round((j.price-i.price)*100/i.price, 4) for i, j in zip(skeletons[-8:-1], skeletons[-7:-1])]
                delta = ",".join([str(i) for i in chg[0:-1]])
                if delta in olds:continue
                olds.append(delta)
                # maxh = max([i.high for i in bars[21:]])
                # minl = max([i.low for i in bars[21:]])
                if chg[-1] > 0:
                    flag = 0  # up
                else:
                    flag = 1  # down
                data = str(flag) + " AinanceLabs " + skeletons[-1].dt + "," + delta
                fx.write(data + "\n")
        fx.close()


if __name__ == '__main__':
    d = Dataset5m()
    d.discrete_macd_chg(symbol="BTCUSDT")

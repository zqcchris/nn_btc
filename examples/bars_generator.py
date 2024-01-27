# Binance Spot Bars Generator
import os
import sys

sys.path.append(os.getcwd())
import copy
import tqdm
import json
import requests
import multitasking
import pandas as pd
from retry import retry
from config.server_config import crypto_server
from typing import Dict, List, Union
from exchange_market.bar import RawBar
from exchange_market.binance.enum import Interval
from examples.bar_compose import BarCompose


class BarsGenerator(object):
    """
    mode:
        1、dump：          在dump模式下，直接从交易所获取行情数据，且只是5min的行情数据
        2、production：    该模式下，从本地mysql数据库获取行情，不与交易所交互
    """
    def __init__(self, api, mode="debug"):
        self.api = api
        self.mode = mode
        self.bars_compose = BarCompose()
        self.url = "http://{}:8000/binance".format(crypto_server)
        # self.url = "http://{}:8000/binance".format("127.0.0.1")

    @staticmethod
    def raw_bars_generator(symbol, datas, interval=None, separator=None, mode="local"):
        """
        mode: local: 从本地行情服务器获取行情数据
              okex：从okex交易所实时获取行情数据
        """
        bs = []
        for data in datas:
            if mode == "local":
                rb = RawBar(exchange="binance", symbol=symbol, dt=data[1], open=float(data[2]),
                            high=float(data[3]), low=float(data[4]), close=float(data[5]), vol=float(data[6]),
                            interval=interval)
            else:
                rb = RawBar(exchange="binance", symbol=symbol, dt=mil2datetime(int(data[0])), open=float(data[1]),
                            high=float(data[2]), low=float(data[3]), close=float(data[4]), vol=float(data[5]),
                            interval=interval)
            bs.append(copy.deepcopy(rb))
        return bs

    def compose(self, bar_5m=None, mode="composition"):
        """
            注意k线合成顺序必须是大级别优先，5分钟级别最后执行，顺序不得调整
            mode: init:       在初始化模式中，不能随意clear缓存，而要在初始化完成，将合成的k线存入数据库才可以清缓存；
                  production：该模式中历史缓存就没用了，需要及时清理
        """
        if mode != "init":
            self.bars_compose.clear()
        self.bars_compose.update_bar_week_window(bar_5m)
        self.bars_compose.update_bar_day_window(bar_5m)
        self.bars_compose.update_bar_4h_window(bar_5m)
        self.bars_compose.update_bar_60min_window(bar_5m)
        self.bars_compose.update_bar_30min_window(bar_5m)
        self.bars_compose.update_bar_15min_window(bar_5m)
        self.bars_compose.update_bar_5m_window(bar_5m)

    def get_bars_from_api(self, symbol, interval=Interval.min5.value, **kwargs):
        """
        :param: market: choice of ["SZ", "SH"]
        :param: code: 股票代码，如：000063
        :param: limit: string, 最大返回10000，也就是一个月的5min的数据
        """
        post_data = {"symbol": symbol, "interval": interval, **kwargs}
        response = requests.post(self.url, data=post_data)
        rsp = json.loads(response.text)
        datas = rsp.get('data', [])
        bs = self.raw_bars_generator(symbol=symbol, datas=datas, interval=Interval.min5.value, separator=None, mode="local")
        if len(bs) > 0 and interval == Interval.min5.value:
            self.bars_compose.set_latest_dt(bs[-1].dt)
        return bs

    def get_latest_bar(self, symbol="BTCUSDT", interval=Interval.min5.value, limit="50", **kwargs):
        """
        :param: symbol: 交易代码，如：BTC-USDT-SWAP
        :param: interval, 行情级别，枚举类型
        """
        prev_dt = self.bars_compose.get_last_dt()
        if prev_dt == "2023-01-01 10:00:00":
            limit = "10000"  # 如果第一次运行，则直接获取所有历史行情用于初始化
            bars = self.get_bars_from_api(symbol=symbol, interval=interval)
            return bars, prev_dt
        post_data = {"symbol": symbol, "interval": interval, "start_time": prev_dt, "limit": limit, **kwargs}
        response = requests.post(self.url, data=post_data)
        rsp = json.loads(response.text)
        datas = rsp.get('data', [])
        bars = self.raw_bars_generator(symbol=symbol, datas=datas, interval=Interval.min5.value, separator=None, mode="local")
        if len(bars) > 0:
            self.bars_compose.set_latest_dt(bars[-1].dt)
            return bars, prev_dt
        return None, prev_dt

    def get_bars(self, symbol, interval, limit=500, end_time="", **kwargs):
        """  注意这里的api.get_kline方法是获取最新k线，可能包括未完成的k线；而api.get_history_kline方法返回的都是完成的k线 """
        if self.mode != "dump" or self.mode == "debug":
            return self.get_bars_from_cache(interval=interval, symbol=symbol, limit=limit)
        else:
            interval = Interval.min5.value
            rsp = self.api.get_klines(symbol, interval, limit=500, endTime=end_time, **kwargs)
            bars = self.raw_bars_generator(symbol=symbol, datas=rsp[:-1], interval=interval, mode="production")
            # rsp = self.api.get_klines(symbol=symbol, interval=interval, **kwargs)
            # datas = rsp.get('data', [])
            # datas.reverse()
            # datas = datas[:-1]
            # bs = self.raw_bars_generator(symbol=symbol, datas=datas, interval=interval, mode="binance")
            return bars

    def get_bars_from_cache(self, symbol, interval, limit):
        """
        :param: market: choice of ["SZ", "SH"]
        :param: code: 股票代码，如：000063
        :param: limit: string, 最大返回1500，也就是一个月的5min的数据
        """
        limit = int(limit)
        if interval == Interval.min5.value:
            return self.bars_compose.bars_m5[-limit:]
        elif interval == Interval.min15.value:
            return self.bars_compose.bars_m15[-limit:]
        elif interval == Interval.min30.value:
            return self.bars_compose.bars_m30[-limit:]
        elif interval == Interval.hour1.value:
            return self.bars_compose.bars_m60[-limit:]
        elif interval == Interval.hour4.value:
            return self.bars_compose.bars_4h[-limit:]
        elif interval == Interval.day.value:
            return self.bars_compose.bars_day[-limit:]
        elif interval == Interval.week.value:
            return self.bars_compose.bars_week[-limit:]

    def get_price_precision(self, symbol, cache=None):
        return 5

    def get_quote_history(self,
                          symbols: Union[str, List[str]],
                          start_time: str = str(string2mil('2023-01-01 10:00:00')),
                          end_time: str = str(string2mil('2023-08-03 10:00:00')),
                          interval: str = Interval.min5.value,
                          limit: str = '500') -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        df = self.get_quote_history_for_symbol(symbols=symbols, start_time=start_time, end_time=end_time,
                                               interval=interval, limit=limit)
        return df

    def get_quote_history_for_symbol(self,
                                     symbols: Union[str, List[str]],
                                     start_time: str = str(string2mil('2023-07-01 10:00:00')),
                                     end_time: str = str(string2mil('2023-08-03 10:00:00')),
                                     interval: str = Interval.min5.value,
                                     limit: str = '500') -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        if isinstance(symbols, str):
            return self.get_quote_history_single(symbol=symbols, start_time=start_time, end_time=end_time,
                                                 interval=interval, limit=limit)

        elif hasattr(symbols, '__iter__'):
            symbols = list(symbols)
            return self.get_quote_history_multi(symbols=symbols, start_time=start_time, end_time=end_time,
                                                interval=interval, limit=limit)
        raise TypeError(
            '代码数据类型输入不正确！'
        )

    def get_quote_history_single(self,
                                 symbol: str = "BTCUSDT",
                                 start_time: str = str(string2mil('2023-07-01 10:00:00')),
                                 end_time: str = str(string2mil('2023-08-03 10:00:00')),
                                 interval: str = Interval.min5.value,
                                 limit: str = '500') -> pd.DataFrame:
        """ 获取单只股票、债券 K 线数据 """
        result = []
        rsp = self.api.get_klines(symbol, interval, endTime=end_time, limit=limit)
        bars = self.raw_bars_generator(symbol=symbol, datas=rsp[:-1], interval=interval, mode="production")
        for bar in bars:
            result.append(bar.to_dict())
        return pd.DataFrame(result)

    def get_quote_history_multi(self,
                                symbols: List[str],
                                start_time: str = str(string2mil('2023-07-01 10:00:00')),
                                end_time: str = str(string2mil('2023-08-03 10:00:00')),
                                interval: str = Interval.min5.value,
                                tries: int = 3,
                                limit: str = "500") -> Dict[str, pd.DataFrame]:
        """ 获取多只股票、债券历史行情信息 """
        dfs: Dict[str, pd.DataFrame] = {}
        total = len(symbols)

        @multitasking.task
        @retry(tries=tries, delay=1)
        def start(symbol: str):
            _df = self.get_quote_history_single(symbol, start_time=start_time, end_time=end_time, interval=interval,
                                                limit=limit)
            dfs[symbol] = _df
            pbar.update(1)
            pbar.set_description_str(f'Processing => {symbol}')

        pbar = tqdm.tqdm(total=total)
        for symbol in symbols:
            start(symbol)
        multitasking.wait_for_tasks()
        pbar.close()
        return dfs


if __name__ == '__main__':
    start_time = dt2ts_mil(string2datetime("2023-08-07 01:41:00"))
    end_time = dt2ts_mil(string2datetime("2023-11-12 08:30:00"))
    from exchange_market.binance.future import Future

    future = Future()
    bars_generator = BarsGenerator(future, mode="production")
    bars, prev_dt = bars_generator.get_latest_bar(symbol="ATAUSDT", interval=Interval.min5.value)
    bars = bars[-288:]
    first = bars[0]
    last = bars[-1]
    print(bars[0].dt)
    print(bars[-1].dt)
    chg = (last.close - first.open)/first.open
    print("chg 24 hour",  chg)
    # for idx, bar_5m in enumerate(bars):
    #     bars_generator.compose(bar_5m=bar_5m)
    #     if string2mil(bar_5m.dt) < string2mil("2023-01-01 00:00:00"): continue


from dateutil import parser
from exchange_market.bar import RawBar
from exchange_market.binance.enum import Interval
import statistics


class BarCompose(object):
    """ 以5min为基础，合成15min、30min、4H、日线和周线级别的k线 """
    def __init__(self):
        """Constructor"""
        self.last_dt = ""
        self.bars_m5 = []
        self.bars_m15 = []
        self.bars_m30 = []
        self.bars_m60 = []
        self.bars_4h = []
        self.bars_day = []
        self.bars_week = []

        self.bar_15m = None
        self.bar_30m = None
        self.bar_60m = None
        self.bar_4h = None
        self.bar_day = None
        self.week_bar = None

    def get_bars(self, interval):
        if interval == Interval.min5.value:
            return self.bars_m5
        elif interval == Interval.min15.value:
            return self.bars_m15
        elif interval == Interval.min30.value:
            return self.bars_m30
        elif interval == Interval.hour1.value:
            return self.bars_m60
        elif interval == Interval.hour4.value:
            return self.bars_4h
        elif interval == Interval.day.value:
            return self.bars_day
        elif interval == Interval.week.value:
            return self.bars_week
        else:
            return []

    @staticmethod
    def cal_taxx(bars):
        if len(bars) == 1:
            bars[-1].taxx.ema12 = bars[-1].close
            bars[-1].taxx.ema26 = bars[-1].close
            bars[-1].taxx.ema155 = bars[-1].close
            bars[-1].taxx.ema300 = bars[-1].close
            return
        else:
            # RSI指标计算，比较复杂，请不要随意改动
            if len(bars) < 8:
                current_gain_loss = bars[-1].close - bars[-2].close
                if current_gain_loss > 0:
                    bars[-1].taxx.up_sum = bars[-2].taxx.up_sum + current_gain_loss
                    bars[-1].taxx.up_avg6 = bars[-1].taxx.up_sum / 6
                else:
                    bars[-1].taxx.down_sum = bars[-2].taxx.down_sum + abs(current_gain_loss)
                    bars[-1].taxx.down_avg6 = bars[-1].taxx.down_sum / 6
            else:
                current_gain_loss = bars[-1].close - bars[-2].close
                if current_gain_loss > 0:
                    bars[-1].taxx.up_avg6 = (bars[-2].taxx.up_avg6 * 5 + current_gain_loss) / 6
                    bars[-1].taxx.down_avg6 = (bars[-2].taxx.down_avg6 * 5 + 0) / 6
                else:
                    bars[-1].taxx.down_avg6 = (bars[-2].taxx.down_avg6 * 5 + abs(current_gain_loss)) / 6
                    bars[-1].taxx.up_avg6 = (bars[-2].taxx.up_avg6 * 5 + 0) / 6

                # 计算 RSI = up_avg * 100/(up_avg + down_avg)
                if (bars[-1].taxx.up_avg6 + bars[-1].taxx.down_avg6) == 0:
                    bars[-1].taxx.rsi6 = 0
                else:
                    bars[-1].taxx.rsi6 = bars[-1].taxx.up_avg6 * 100 / (bars[-1].taxx.up_avg6 + bars[-1].taxx.down_avg6)

            cur_bar = bars[-1]
            prev_bar = bars[-2]

            # 计算ema12
            prev_ema12 = prev_bar.taxx.ema12
            ema12 = prev_ema12 * (1 - 2 / 13) + (2 / 13) * cur_bar.close
            cur_bar.taxx.ema12 = ema12

            # 计算ema26
            prev_ema26 = prev_bar.taxx.ema26
            ema26 = prev_ema26 * (1 - 2 / 27) + (2 / 27) * cur_bar.close
            cur_bar.taxx.ema26 = ema26

            # 计算diff
            cur_bar.taxx.diff = cur_bar.taxx.ema12 - cur_bar.taxx.ema26

            # 计算dea
            dea = prev_bar.taxx.dea * (1 - 2 / 10) + (2 / 10) * cur_bar.taxx.diff
            cur_bar.taxx.dea = dea

            # 计算ema155
            prev_ema155 = prev_bar.taxx.ema155
            ema155 = prev_ema155 * (1 - 2 / 156) + (2 / 156) * cur_bar.close
            cur_bar.taxx.ema155 = ema155

            # 计算ema300
            prev_ema300 = prev_bar.taxx.ema300
            ema300 = prev_ema300 * (1 - 2 / 301) + (2 / 301) * cur_bar.close
            cur_bar.taxx.ema300 = ema300

            # 计算macd todo: A股的macd是要✖️2，币圈的不需要
            # macd = 2 * (cur_bar.taxx.diff - cur_bar.taxx.dea)
            macd = (cur_bar.taxx.diff - cur_bar.taxx.dea)
            cur_bar.taxx.macd = macd

            # 计算方差
            if len(bars) >= 21:
                close21 = [b.close for b in bars[-20:]]
                var = statistics.pstdev(close21)
                mavg = statistics.mean(close21)
                cur_bar.taxx.delta = var
                cur_bar.taxx.mavg21 = mavg

    def clear(self, limit=50):
        self.bars_week = self.bars_week[-limit:]
        self.bars_day = self.bars_day[-limit:]
        self.bars_4h = self.bars_4h[-limit:]
        self.bars_m60 = self.bars_m60[-limit:]
        self.bars_m30 = self.bars_m30[-limit:]
        self.bars_m15 = self.bars_m15[-limit:]
        self.bars_m5 = self.bars_m5[-1500:]

    def set_latest_dt(self, dt):
        self.last_dt = dt

    def get_last_dt(self):
        if not self.last_dt:
            self.last_dt = "2023-01-01 10:00:00"
        return self.last_dt

    def update_bar_5m_window(self, bar) -> None:
        """ 用5min的k线合成大级别 """
        if bar not in self.bars_m5:
            self.bars_m5.append(bar)
            self.cal_taxx(self.bars_m5)

    def update_bar_15min_window(self, bar) -> None:
        """ 用5min的k线合成大级别 """
        if bar in self.bars_m5: return
        if not self.bar_15m:
            dt = bar.dt
            self.bar_15m = RawBar(symbol=bar.symbol, dt=dt, open=bar.open, high=bar.high, low=bar.low, close=bar.close,
                                  vol=bar.vol, exchange=bar.exchange, interval=Interval.min15.value)
            return

        finished_bar = None
        if parser.parse(bar.dt).minute in [10, 25, 40, 55]:  # okex是16:00切换为新日线
            self.bar_15m.high = max(self.bar_15m.high, bar.high)
            self.bar_15m.low = min(self.bar_15m.low, bar.low)

            self.bar_15m.close = bar.close
            self.bar_15m.vol += int(bar.vol)

            finished_bar = self.bar_15m  # 保存日线bar
            self.bar_15m = None  # 因为日线bar已经保存给finished_bar, 将日线bar设为空等新数据来就会生成新的日线bar
        # 更新 现存的day_bar
        else:
            self.bar_15m.high = max(self.bar_15m.high, bar.high)
            self.bar_15m.low = min(self.bar_15m.low, bar.low)

            self.bar_15m.close = bar.close
            self.bar_15m.vol += int(bar.vol)

        # 推送日线给on_hour_bar处理
        if finished_bar:
            self.bars_m15.append(finished_bar)
            self.cal_taxx(self.bars_m15)

    def update_bar_30min_window(self, bar) -> None:
        """ 用5min的k线合成大级别 , 参考同花顺，(]模式"""
        if bar in self.bars_m5: return
        if not self.bar_30m:
            dt = bar.dt
            self.bar_30m = RawBar(symbol=bar.symbol, dt=dt, open=bar.open, high=bar.high, low=bar.low, close=bar.close,
                                  vol=bar.vol, exchange=bar.exchange, interval=Interval.min30.value)
            return

        finished_bar = None
        if parser.parse(bar.dt).minute in [55, 25]:  # okex是16:00切换为新日线
            self.bar_30m.high = max(self.bar_30m.high, bar.high)
            self.bar_30m.low = min(self.bar_30m.low, bar.low)

            self.bar_30m.close = bar.close
            self.bar_30m.vol += int(bar.vol)
            # self.bar_30m.dt = bar.dt

            finished_bar = self.bar_30m  # 保存日线bar
            self.bar_30m = None  # 因为日线bar已经保存给finished_bar, 将日线bar设为空等新数据来就会生成新的日线bar
        # 更新 现存的day_bar
        else:
            self.bar_30m.high = max(self.bar_30m.high, bar.high)
            self.bar_30m.low = min(self.bar_30m.low, bar.low)

            self.bar_30m.close = bar.close
            self.bar_30m.vol += int(bar.vol)

        # 推送日线给on_hour_bar处理
        if finished_bar:
            self.bars_m30.append(finished_bar)
            self.cal_taxx(self.bars_m30)

    def update_bar_60min_window(self, bar) -> None:
        """ 用5min的k线合成大级别 , 参考同花顺，(]模式"""
        if bar in self.bars_m5: return
        if not self.bar_60m:
            dt = bar.dt
            self.bar_60m = RawBar(symbol=bar.symbol, dt=dt, open=bar.open, high=bar.high, low=bar.low, close=bar.close,
                                  vol=bar.vol, exchange=bar.exchange, interval=Interval.hour1.value)
            return

        finished_bar = None
        if parser.parse(bar.dt).minute in [55]:
            self.bar_60m.high = max(self.bar_60m.high, bar.high)
            self.bar_60m.low = min(self.bar_60m.low, bar.low)

            self.bar_60m.close = bar.close
            self.bar_60m.vol += int(bar.vol)
            # self.bar_60m.dt = bar.dt

            finished_bar = self.bar_60m  # 保存日线bar
            self.bar_60m = None  # 因为日线bar已经保存给finished_bar, 将日线bar设为空等新数据来就会生成新的日线bar
        # 更新 现存的day_bar
        else:
            self.bar_60m.high = max(self.bar_60m.high, bar.high)
            self.bar_60m.low = min(self.bar_60m.low, bar.low)

            self.bar_60m.close = bar.close
            self.bar_60m.vol += int(bar.vol)

        # 推送日线给on_hour_bar处理
        if finished_bar:
            self.bars_m60.append(finished_bar)
            self.cal_taxx(self.bars_m60)

    def update_bar_4h_window(self, bar) -> None:
        """ 用5min的k线合成大级别 , 参考同花顺，(]模式"""
        if bar in self.bars_m5: return
        if not self.bar_4h:
            self.bar_4h = RawBar(symbol=bar.symbol, dt=bar.dt, open=bar.open, high=bar.high, low=bar.low, close=bar.close,
                                 vol=bar.vol, exchange=bar.exchange, interval=Interval.hour4.value)
            return

        finished_bar = None
        if parser.parse(bar.dt).strftime("%H:%M") in ["03:55", "07:55", "11:55", "15:55", "19:55", "23:55"]:  # 4H切换时间
            self.bar_4h.high = max(self.bar_4h.high, bar.high)
            self.bar_4h.low = min(self.bar_4h.low, bar.low)

            self.bar_4h.close = bar.close
            self.bar_4h.vol += int(bar.vol)
            # self.bar_4h.dt = bar.dt

            finished_bar = self.bar_4h  # 保存日线bar
            self.bar_4h = None  # 因为日线bar已经保存给finished_bar, 将日线bar设为空等新数据来就会生成新的日线bar
        # 更新 现存的day_bar
        else:
            self.bar_4h.high = max(self.bar_4h.high, bar.high)
            self.bar_4h.low = min(self.bar_4h.low, bar.low)

            self.bar_4h.close = bar.close
            self.bar_4h.vol += int(bar.vol)

        # 推送日线给on_hour_bar处理
        if finished_bar:
            self.bars_4h.append(finished_bar)
            self.cal_taxx(self.bars_4h)

    def update_bar_day_window(self, bar) -> None:
        """ 用5min的k线合成大级别 """
        if bar in self.bars_m5: return
        if not self.bar_day:
            dt = bar.dt
            self.bar_day = RawBar(symbol=bar.symbol, dt=dt, open=bar.open, high=bar.high, low=bar.low, close=bar.close,
                                  vol=bar.vol, exchange=bar.exchange, interval=Interval.day.value)
            # self.bars_day.append(self.bar_day)  # 一旦有新日线就加入列表，进行指标计算
            # self.cal_taxx(self.bars_day)
            return

        finished_bar = None
        if parser.parse(bar.dt).strftime("%H:%M") in ["07:55"]:   # 日线切换时间
            self.bar_day.high = max(self.bar_day.high, bar.high)
            self.bar_day.low = min(self.bar_day.low, bar.low)

            self.bar_day.close = bar.close
            self.bar_day.vol += int(bar.vol)
            self.bar_day.dt = parser.parse(self.bar_day.dt).strftime("%Y-%m-%d %H:%M")

            finished_bar = self.bar_day  # 保存日线bar
            self.bar_day = None  # 因为日线bar已经保存给finished_bar, 将日线bar设为空等新数据来就会生成新的日线bar
        # 更新 现存的day_bar
        else:
            self.bar_day.high = max(self.bar_day.high, bar.high)
            self.bar_day.low = min(self.bar_day.low, bar.low)

            self.bar_day.close = bar.close
            self.bar_day.vol += int(bar.vol)
            # 实时更新最新的日线数据，进行指标计算
            # self.bars_day[-1] = self.bar_day
            # self.cal_taxx(self.bars_day)

        # 推送日线给on_hour_bar处理
        if finished_bar:
            # self.bars_day[-1] = finished_bar
            self.bars_day.append(finished_bar)
            self.cal_taxx(self.bars_day)

    def update_bar_week_window(self, bar) -> None:
        """ 用5min的k线合成大级别 """
        if bar in self.bars_m5: return
        if not self.week_bar:
            dt = bar.dt
            self.week_bar = RawBar(symbol=bar.symbol, dt=dt, open=bar.open, high=bar.high, low=bar.low, close=bar.close,
                                   vol=bar.vol, exchange=bar.exchange, interval=Interval.week.value)
            return

        finished_bar = None
        # UTC时间每周一0点，作为新周线开始，所以结束条件是周日晚上23：55作为结束条件
        if parser.parse(bar.dt).weekday() == 6 and parser.parse(bar.dt).strftime("%H:%M") in ["07:55"]:
            self.week_bar.high = max(self.week_bar.high, bar.high)
            self.week_bar.low = min(self.week_bar.low, bar.low)

            self.week_bar.close = bar.close
            self.week_bar.vol += int(bar.vol)
            self.week_bar.dt = parser.parse(self.week_bar.dt).strftime("%Y-%m-%d %H:%M")

            finished_bar = self.week_bar  # 保存日线bar
            self.week_bar = None  # 因为日线bar已经保存给finished_bar, 将日线bar设为空等新数据来就会生成新的日线bar
        # 更新 现存的day_bar
        else:
            self.week_bar.high = max(self.week_bar.high, bar.high)
            self.week_bar.low = min(self.week_bar.low, bar.low)

            self.week_bar.close = bar.close
            self.week_bar.vol += int(bar.vol)

        # 推送日线给on_hour_bar处理
        if finished_bar:
            self.bars_week.append(finished_bar)
            self.cal_taxx(self.bars_week)

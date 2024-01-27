import os
import sys
sys.path.append(os.getcwd())


def ping(self):
    """ 测试服务器连通性 PING """
    return self.query("/fapi/v1/ping")


def get_server_time(self):
    """ 获取服务器时间 """
    return self.query("/fapi/v1/time")


def get_exchange_info(self):
    """ 获取交易规则和交易对 """
    return self.query("/fapi/v1/exchangeInfo")


def get_depth(self, symbol: str, limit: int = -1):
    """ 深度信息 """
    params = {"symbol": symbol}
    if limit != -1:
        params.update({"limit": limit})
    return self.query("/fapi/v1/depth", params)


def get_latest_trade(self, symbol: str, limit: int = -1):
    """
    获取近期成交
    Args:
        self:
        symbol: 交易对
        limit:  默认:500，最大1000

    Returns:

    """
    params = {"symbol": symbol}
    if limit != -1:
        params.update({"limit": limit})
    return self.query("/fapi/v1/trades", params)


def get_historic_trade(self, symbol: str, limit: int = -1, fromId: int = -1):
    """
    查询历史成交(MARKET_DATA)
    Args:
        self:
        symbol:    交易度
        limit:     默认值:500 最大值:1000
        fromId:    从哪一条成交id开始返回. 缺省返回最近的成交记录

    Returns:

    """
    params = {"symbol": symbol}
    if limit != -1:
        params.update({"limit": limit})
    if fromId != -1:
        params.update({"fromId": fromId})
    return self.query("/fapi/v1/historicalTrades", params)


def get_agg_trade(self, symbol, fromId: int = -1, startTime: int = -1, endTime: int = -1, limit: int = -1):
    """ 获取近期成交归集：归集交易与逐笔交易的区别在于，同一价格、同一方向、同一时间(按秒计算)的trade会被聚合为一条
        1、如果同时发送startTime和endTime，间隔必须小于一小时
        2、如果没有发送任何筛选参数(fromId, startTime, endTime)，默认返回最近的成交记录
    """
    params = {"symbol": symbol}
    if limit != -1:
        params.update({"limit": limit})
    if fromId != -1:
        params.update({"fromId": fromId})
    if startTime != -1:
        params.update({"startTime": startTime})
    if endTime != -1:
        params.update({"endTime": endTime})
    return self.query("/fapi/v1/aggTrades", params)


def get_klines(self, symbol: str, interval: str, startTime: int = -1, endTime: int = -1, limit: int = -1):
    """
    Args:
        self:
        symbol:     交易对
        interval:   时间间隔
        startTime:  起始时间
        endTime:    结束时间
        limit:      默认值:500 最大值:1500.
    Returns:
    """
    params = {"symbol": symbol,
              "interval": interval}
    if startTime != -1:
        params.update({"startTime": startTime})
    if endTime != -1:
        params.update({"endTime": endTime})
    if limit != -1:
        params.update({"limit": limit})

    return self.query("/fapi/v1/klines", params)


def continous_klines(self, pair: str, contract_type: str, interval: str,
                     startTime: int = -1, endTime: int = -1, limit: int = -1):
    """
    获取连续合约K线数据
    Args:
        self:
        pair:
        contract_type:
        interval:
        startTime:
        endTime:
        limit:
    Returns:
    """
    params = {"pair": pair,
              "contractType": contract_type,
              "interval": interval}
    if startTime != -1:
        params.update({"startTime": startTime})
    if endTime != -1:
        params.update({"endTime": endTime})
    if limit != -1:
        params.update({"limit": limit})

    return self.query("/fapi/v1/continuousKlines", params)


def index_price_klines(self, pair, interval: str, startTime: int = -1, endTime: int = -1, limit: int = -1):
    """
    获取价格指数K线数据
    Args:
        self:
        pair:         标的交易对
        interval:     时间间隔
        startTime:    起始时间
        endTime:      结束时间
        limit:        默认值:500 最大值:1500

    Returns:

    """
    params = {"pair": pair,
              "interval": interval}
    if startTime != -1:
        params.update({"startTime": startTime})
    if endTime != -1:
        params.update({"endTime": endTime})
    if limit != -1:
        params.update({"limit": limit})

    return self.query("/fapi/v1/indexPriceKlines", params)


def mark_price_klines(self, symbol, interval: str, startTime: int = -1, endTime: int = -1, limit: int = -1):
    """
    获取价格指数K线数据
    Args:
        self:
        symbol:       标的交易对
        interval:     时间间隔
        startTime:    起始时间
        endTime:      结束时间
        limit:        默认值:500 最大值:1500

    Returns:

    """
    params = {"symbol": symbol,
              "interval": interval}
    if startTime != -1:
        params.update({"startTime": startTime})
    if endTime != -1:
        params.update({"endTime": endTime})
    if limit != -1:
        params.update({"limit": limit})

    return self.query("/fapi/v1/markPriceKlines", params)


def premium_index(self, symbol):
    """
    最新标记价格和资金费率
    Args:
        self:
        symbol: 交易对

    Returns:

    """
    params = {"symbol": symbol}
    return self.query("/fapi/v1/premiumIndex", params)


def funding_rate(self, symbol: str = "", startTime: int = -1, endTime: int = -1, limit: int = -1):
    """
    查询资金费率历史
    Args:
        self:
        symbol:     交易对
        startTime:  起始时间
        endTime:    结束时间
        limit:      默认值:100 最大值:1000
    Returns:
    """
    params = {}
    if symbol:
        params.update({"symbol": symbol})
    if startTime != -1:
        params.update({"startTime": startTime})
    if endTime != -1:
        params.update({"endTime": endTime})
    if limit != -1:
        params.update({"limit": limit})
    return self.query("/fapi/v1/fundingRate", params)


def change_24hour(self, symbol: str = ""):
    """
    24hr价格变动情况
    Args:
        self:
        symbol: 交易对

    Returns:
    """
    params = {}
    if symbol:
        params.update({"symbol": symbol})
    return self.query("/fapi/v1/ticker/24hr", params)


def get_price(self, symbol: str = ""):
    params = {}
    if symbol:
        params.update({"symbol": symbol})
    return self.query("/fapi/v1/ticker/price", params)


def book_ticker(self, symbol: str = ""):
    """
    获取当前最优挂单
    Args:
        self:
        symbol:
    Returns:

    """
    params = {}
    if symbol:
        params.update({"symbol": symbol})
    return self.query("/fapi/v1/ticker/bookTicker", params)


def open_interest(self, symbol):
    """
    获取未平仓合约数
    Args:
        self:
        symbol:

    Returns:
    """
    params = {"symbol": symbol}
    return self.query("/fapi/v1/openInterest", params)


def open_interest_hist(self, symbol: str, period: str, limit: int = -1, startTime: int = -1, endTime: int = -1):
    """

    Args:
        self:
        symbol:   交易对
        period:   "5m","15m","30m","1h","2h","4h","6h","12h","1d"
        limit:    default 30, max 500
        startTime:
        endTime:
    Returns:
    """
    params = {"symbol": symbol,
              "period": period}
    if limit != -1:
        params.update({"limit": limit})
    if endTime != -1:
        params.update({"endTime": endTime})
    if startTime != -1:
        params.update({"startTime": startTime})
    return self.query("/futures/data/openInterestHist", params)


def top_long_short_account_ratio(self, symbol, period, limit: int = -1, startTime: int = -1, endTime: int = -1):
    """
    大户账户数多空比
    Args:
        self:
        symbol:
        period:
        limit:
        startTime:
        endTime:

    Returns:

    """
    params = {"symbol": symbol,
              "period": period}
    if limit != -1:
        params.update({"limit": limit})
    if endTime != -1:
        params.update({"endTime": endTime})
    if startTime != -1:
        params.update({"startTime": startTime})
    return self.query("/futures/data/topLongShortAccountRatio", params)


def top_long_short_position_ratio(self, symbol, period, limit: int = -1, startTime: int = -1, endTime: int = -1):
    """
    大户持仓量多空比
    Args:
        self:
        symbol:
        period:
        limit:
        startTime:
        endTime:

    Returns:

    """
    params = {"symbol": symbol,
              "period": period}
    if limit != -1:
        params.update({"limit": limit})
    if endTime != -1:
        params.update({"endTime": endTime})
    if startTime != -1:
        params.update({"startTime": startTime})
    return self.query("/futures/data/topLongShortPositionRatio", params)


def global_long_short_account_ratio(self, symbol, period, limit: int = -1, startTime: int = -1, endTime: int = -1):
    """
    大户账户数多空比
    Args:
        self:
        symbol:
        period:
        limit:
        startTime:
        endTime:

    Returns:

    """
    params = {"symbol": symbol,
              "period": period}
    if limit != -1:
        params.update({"limit": limit})
    if endTime != -1:
        params.update({"endTime": endTime})
    if startTime != -1:
        params.update({"startTime": startTime})
    return self.query("/futures/data/globalLongShortAccountRatio", params)


def taker_long_short_ratio(self, symbol, period, limit: int = -1, startTime: int = -1, endTime: int = -1):
    """
    合约主动买卖量
    Args:
        self:
        symbol:
        period:
        limit:
        startTime:
        endTime:
    Returns:
    """
    params = {"symbol": symbol,
              "period": period}
    if limit != -1:
        params.update({"limit": limit})
    if endTime != -1:
        params.update({"endTime": endTime})
    if startTime != -1:
        params.update({"startTime": startTime})
    return self.query("/futures/data/takerlongshortRatio", params)


def get_lvt_klines(self, symbol, period, limit: int = -1, startTime: int = -1, endTime: int = -1):
    """
    杠杆代币历史净值K线
    Args:
        self:
        symbol:
        period:
        limit:
        startTime:
        endTime:

    Returns:

    """
    params = {"symbol": symbol,
              "period": period}
    if limit != -1:
        params.update({"limit": limit})
    if endTime != -1:
        params.update({"endTime": endTime})
    if startTime != -1:
        params.update({"startTime": startTime})
    return self.query("/fapi/v1/lvtKlines", params)


def index_info(self, symbol: str = ""):
    """
    综合指数交易对信息
    Args:
        self:
        symbol:
    Returns:
    """
    params = {}
    if symbol:
        params.update({"symbol": symbol})
    return self.query("/fapi/v1/indexInfo", params)

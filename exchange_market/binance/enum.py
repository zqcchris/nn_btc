from enum import Enum


# 时间间隔
class Interval(Enum):
    min1 = "1m"
    min3 = "3m"
    min5 = "5m"
    min15 = "15m"
    min30 = "30m"
    hour1 = "1h"
    hour2 = "2h"
    hour4 = "4h"
    hour6 = "6h"
    hour8 = "8h"
    hour12 = "12h"
    day = "1d"
    week = "1w"
    mon = "1M"


# 合约类型
class ContractType(Enum):
    PERPETUAL = "PERPETUAL"               # 永续合约
    CURRENT_MONTH = "CURRENT_MONTH"       # 当月交割合约
    NEXT_MONTH = "NEXT_MONTH"             # 次月交割合约
    CURRENT_QUARTER = "CURRENT_QUARTER"   # 当季交割合约
    NEXT_QUARTER = "NEXT_QUARTER"         # 次季交割合约


# 合约状态
class ContractStatus(Enum):
    PENDING_TRADING = "PENDING_TRADING"   # 待上市
    TRADING = "TRADING"                   # 交易中
    PRE_DELIVERING = "PRE_DELIVERING"     # 预交割
    DELIVERING = "DELIVERING"             # 交割中
    DELIVERED = "DELIVERED"               # 已交割
    PRE_SETTLE = "PRE_SETTLE"             # 预结算
    SETTLING = "SETTLING"                 # 结算中
    CLOSE = "CLOSE"                       # 已下架


# 订单状态
class OrderStatus(Enum):
    NEW = "NEW"                              # 新建订单
    PARTIALLY_FILLED = "PARTIALLY_FILLED"    # 部分成交
    FILLED = "FILLED"                        # 全部成交
    CANCELED = "CANCELED"                    # 已撤销
    REJECTED = "REJECTED"                    # 订单被拒绝
    EXPIRED = "EXPIRED"                      # 订单过期(根据timeInForce参数规则)


# 订单类型
class OrderType(Enum):
    LIMIT = "LIMIT"                                # 限价单
    MARKET = "MARKET"                              # 市价单
    STOP = "STOP"                                  # 止损限价单
    STOP_MARKET = "STOP_MARKET"                    # 止损市价单
    TAKE_PROFIT = "TAKE_PROFIT"                    # 止盈限价单
    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"      # 止盈市价单
    TRAILING_STOP_MARKET = "TRAILING_STOP_MARKET"  # 跟踪止损单


# 订单方向
class OrderSide(Enum):
    BUY = "BUY"    # 买入
    SELL = "SELL"  # 卖出


# 持仓方向
class PositionSide(Enum):
    BOTH = "BOTH"     # 单一持仓方向
    LONG = "LONG"     # 多头(双向持仓下)
    SHORT = "SHORT"   # 空头(双向持仓下)


# 有效方式
class TimeInForce(Enum):
    GTC = "GTC"    # Good Till Cancel 成交为止
    IOC = "IOC"    # Immediate or Cancel无法立即成交(吃单)的部分就撤销
    FOK = "FOK"    # Fill or Kill无法全部立即成交就撤销
    GTX = "GTX"    # Good Till Crossing无法成为挂单方就撤销

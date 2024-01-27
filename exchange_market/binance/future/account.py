import os
import sys
sys.path.append(os.getcwd())


def order(self, symbol: str, side: str, type: str, account=None, **kwargs):
    """
    下单 (TRADE)
    Args:
        self:
        symbol:     交易对
        side:       BUY or SELL
        type:       订单类型 LIMIT, MARKET, STOP, TAKE_PROFIT, STOP_MARKET, TAKE_PROFIT_MARKET, TRAILING_STOP_MARKET
        account:
        price：	DECIMAL	NO	委托价格
        **kwargs:   positionSide:     持仓方向，单向持仓模式下非必填，默认且仅可填BOTH;在双向持仓模式下必填,且仅可选择 LONG 或 SHORT
                    quantity:	      DECIMAL	下单数量,使用closePosition不支持此参数。
                    newClientOrderId: STRING	用户自定义的订单号，不可以重复出现在挂单中。如空缺系统会自动赋值。
    """
    params = {"symbol": symbol, "side": side, "type": type, **kwargs}
    url_path = "/fapi/v1/order"
    return self.sign_request("POST", url_path, params, account)


def query_order(self, symbol, account, **kwargs):
    """
    查询订单
    请注意，如果订单满足如下条件，不会被查询到：
        订单的最终状态为 CANCELED 或者 EXPIRED, 并且
        订单没有任何的成交记录, 并且
        订单生成时间 + 7天 < 当前时间
    Args:
        self:
        symbol:
        account:
        **kwargs:
    Returns:
    """
    params = {"symbol": symbol, **kwargs}
    url_path = "/fapi/v1/order"
    return self.sign_request("GET", url_path, params, account)


def cancel_order(self, symbol, account, **kwargs):
    """
    撤销订单
    Args:
        self:
        symbol:
        account:
        **kwargs:   orderId	            系统订单号
                    origClientOrderId	用户自定义的订单号
                    recvWindow
                    orderId 与 origClientOrderId 必须至少发送一个
    Returns:
    """
    params = {"symbol": symbol, **kwargs}
    url_path = "/fapi/v1/order"
    return self.sign_request("DELETE", url_path, params, account)


def cancel_all_order(self, symbol: str, account, **kwargs):
    """
    撤销全部订单
    Args:
        self:
        symbol:
        account:
        **kwargs:       recvWindow
    Returns:
    """
    params = {"symbol": symbol, **kwargs}
    url_path = "/fapi/v1/allOpenOrders"
    return self.sign_request("DELETE", url_path, params, account)


def get_balance(self, account, **kwargs):
    """
    查询账户余额
    Args:
        self:
        account:
        **kwargs:   recvWindow
    Returns:
    """
    params = {**kwargs}
    url_path = "/fapi/v2/balance"
    return self.sign_request("GET", url_path, params, account)


def get_account_info(self, account=None, **kwargs):
    """
    查询指定账户信息
    Args:
        self:
        account:
        **kwargs:   recvWindow
    Returns:
    """
    params = {**kwargs}
    url_path = "/fapi/v2/account"
    return self.sign_request("GET", url_path, params, account)


def set_leverage(self, symbol, leverage, account, **kwargs):
    """
    设置开仓杠杆
    Args:
        self:
        symbol:     交易对
        leverage:   目标杠杆倍数：1 到 125 整数
        account:
        **kwargs:   recvWindow...
    Returns:
    """
    params = {"symbol": symbol, "leverage": leverage, **kwargs}
    url_path = "/fapi/v1/leverage"
    return self.sign_request("POST", url_path, params, account)


def set_margin_type(self, symbol, margin_type, account, **kwargs):
    """
    设置开仓杠杆
    Args:
        self:
        symbol:        交易对
        margin_type:   保证金模式 ISOLATED(逐仓), CROSSED(全仓)
        account:
        **kwargs:      recvWindow...
    Returns:
    """
    params = {"symbol": symbol, "marginType": margin_type, **kwargs}
    url_path = "/fapi/v1/marginType"
    return self.sign_request("POST", url_path, params, account)


def query_open_order(self, symbol, account, **kwargs):
    """
    查询用户当前挂单
    Args:
        self:
        symbol:    交易对
        account:
        **kwargs:  orderId	            LONG	NO	系统订单号
                   origClientOrderId	STRING	NO	用户自定义的订单号
                   recvWindow	        LONG	NO
                   orderId和origClientOrderId必须至少发送一个作为请求参数
    Returns:
    """
    params = {"symbol": symbol, **kwargs}
    url_path = "/fapi/v1/openOrder"
    return self.sign_request("GET", url_path, params, account)


def query_open_orders(self, account, **kwargs):
    """
    查询用户全部挂单
    Args:
        self:
        account:
        **kwargs:  symbol               STRING  NO  交易对
                   orderId	            LONG	NO	系统订单号
                   origClientOrderId	STRING	NO	用户自定义的订单号
                   recvWindow	        LONG	NO
                   不带symbol参数，会返回所有交易对的挂单，但建议带上symbol
    Returns:
    """
    params = {**kwargs}
    url_path = "/fapi/v1/openOrders"
    return self.sign_request("GET", url_path, params, account)


def query_income(self, account, **kwargs):
    """
    获取账户损益资金流水(USER_DATA)
    Args:
        self:
        account:
        **kwargs: symbol:       STRING	NO	交易对
                  incomeType	STRING	NO	收益类型 "TRANSFER"，"WELCOME_BONUS", "REALIZED_PNL"，"FUNDING_FEE",
                                            "COMMISSION", and "INSURANCE_CLEAR"
                  startTime	    LONG	NO	起始时间
                  endTime	    LONG	NO	结束时间
                  limit	        INT	    NO	返回的结果集数量 默认值:100 最大值:1000
                  recvWindow    LONG	NO
    Returns:
    """
    params = {**kwargs}
    url_path = "/fapi/v1/income"
    return self.sign_request("GET", url_path, params, account)


def query_position_side(self, account):
    """ 查询用户在所有symbol上的持仓模式 """
    params = {}
    url_path = "/fapi/v1/positionSide/dual"
    return self.sign_request("GET", url_path, params, account)


def change_position_side(self, dualSidePosition, account):
    """ 更改用户在所有symbol上的持仓模式 """
    params = {"dualSidePosition": dualSidePosition}
    url_path = "/fapi/v1/positionSide/dual"
    return self.sign_request("POST", url_path, params, account)


def query_user_trades(self, symbol, startTime=None, endTime=None, limit=None, account=None, **kwargs):
    """
    获取某交易对的成交历史, 如果startTime 和 endTime 均未发送, 只会返回最近7天的数据, startTime 和 endTime 的最大间隔为7天
    Args:
        self:
        symbol:        交易对
        startTime:     起始时间
        endTime:       结束时间
        limit:         返回的结果集数量 默认值:500 最大值:1000
        account:
        **kwargs:
    Returns:
    """
    params = {"symbol": symbol,
              "startTime": startTime,
              "endTime": endTime,
              "limit": limit}
    url_path = '/fapi/v1/userTrades'
    return self.sign_request("GET", url_path, params, account)

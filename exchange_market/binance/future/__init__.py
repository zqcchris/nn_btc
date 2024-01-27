import os
import sys
sys.path.append(os.getcwd())
from exchange_market.binance.api.future_api import FutureAPI


class Future(FutureAPI):
    def __init__(self, access_key="", secret_key=""):
        super().__init__(access_key=access_key, secret_key=secret_key)

    # market
    from exchange_market.binance.future.market import ping
    from exchange_market.binance.future.market import get_server_time
    from exchange_market.binance.future.market import get_exchange_info
    from exchange_market.binance.future.market import get_depth
    from exchange_market.binance.future.market import get_latest_trade
    from exchange_market.binance.future.market import get_historic_trade
    from exchange_market.binance.future.market import get_agg_trade
    from exchange_market.binance.future.market import get_klines
    from exchange_market.binance.future.market import continous_klines
    from exchange_market.binance.future.market import index_price_klines
    from exchange_market.binance.future.market import mark_price_klines
    from exchange_market.binance.future.market import premium_index
    from exchange_market.binance.future.market import funding_rate
    from exchange_market.binance.future.market import change_24hour
    from exchange_market.binance.future.market import get_price
    from exchange_market.binance.future.market import book_ticker
    from exchange_market.binance.future.market import open_interest
    from exchange_market.binance.future.market import open_interest_hist
    from exchange_market.binance.future.market import top_long_short_account_ratio
    from exchange_market.binance.future.market import top_long_short_position_ratio
    from exchange_market.binance.future.market import global_long_short_account_ratio
    from exchange_market.binance.future.market import taker_long_short_ratio
    from exchange_market.binance.future.market import get_lvt_klines
    from exchange_market.binance.future.market import index_info

    # account
    from exchange_market.binance.future.account import order
    from exchange_market.binance.future.account import query_order
    from exchange_market.binance.future.account import cancel_order
    from exchange_market.binance.future.account import cancel_all_order
    from exchange_market.binance.future.account import get_balance
    from exchange_market.binance.future.account import get_account_info
    from exchange_market.binance.future.account import set_leverage
    from exchange_market.binance.future.account import set_margin_type
    from exchange_market.binance.future.account import query_open_order
    from exchange_market.binance.future.account import query_open_orders
    from exchange_market.binance.future.account import query_income
    from exchange_market.binance.future.account import query_position_side
    from exchange_market.binance.future.account import change_position_side
    from exchange_market.binance.future.account import query_user_trades

    # streams
    from exchange_market.binance.future.data_stream import new_listen_key
    from exchange_market.binance.future.data_stream import renew_listen_key
    from exchange_market.binance.future.data_stream import close_listen_key

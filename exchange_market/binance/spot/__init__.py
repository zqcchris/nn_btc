from exchange_market.binance.api.spot_api import SpotAPI


class Spot(SpotAPI):
    def __init__(self, access_key=None, secret_key=None):
        super().__init__(access_key, secret_key)

    # MARKETS
    from exchange_market.binance.spot.market import ping
    from exchange_market.binance.spot.market import time
    from exchange_market.binance.spot.market import get_exchange_info
    from exchange_market.binance.spot.market import depth
    from exchange_market.binance.spot.market import trades
    from exchange_market.binance.spot.market import historical_trades
    from exchange_market.binance.spot.market import agg_trades
    from exchange_market.binance.spot.market import get_klines
    from exchange_market.binance.spot.market import avg_price
    from exchange_market.binance.spot.market import ticker_24hr
    from exchange_market.binance.spot.market import ticker_price
    from exchange_market.binance.spot.market import book_ticker

    # ACCOUNT(including orders and trades)
    from exchange_market.binance.spot.account import new_order_test
    from exchange_market.binance.spot.account import new_order
    from exchange_market.binance.spot.account import cancel_order
    from exchange_market.binance.spot.account import cancel_open_orders
    from exchange_market.binance.spot.account import get_order
    from exchange_market.binance.spot.account import get_open_orders
    from exchange_market.binance.spot.account import get_orders
    from exchange_market.binance.spot.account import new_oco_order
    from exchange_market.binance.spot.account import cancel_oco_order
    from exchange_market.binance.spot.account import get_oco_order
    from exchange_market.binance.spot.account import get_oco_orders
    from exchange_market.binance.spot.account import get_oco_open_orders
    from exchange_market.binance.spot.account import account
    from exchange_market.binance.spot.account import my_trades

    # STREAMS
    from exchange_market.binance.spot.data_stream import new_listen_key
    from exchange_market.binance.spot.data_stream import renew_listen_key
    from exchange_market.binance.spot.data_stream import close_listen_key
    from exchange_market.binance.spot.data_stream import new_margin_listen_key
    from exchange_market.binance.spot.data_stream import renew_margin_listen_key
    from exchange_market.binance.spot.data_stream import close_margin_listen_key
    from exchange_market.binance.spot.data_stream import new_isolated_margin_listen_key
    from exchange_market.binance.spot.data_stream import renew_isolated_margin_listen_key
    from exchange_market.binance.spot.data_stream import close_isolated_margin_listen_key

    # MARGIN
    from exchange_market.binance.spot.margin import margin_transfer
    from exchange_market.binance.spot.margin import margin_borrow
    from exchange_market.binance.spot.margin import margin_repay
    from exchange_market.binance.spot.margin import margin_asset
    from exchange_market.binance.spot.margin import margin_pair
    from exchange_market.binance.spot.margin import margin_all_assets
    from exchange_market.binance.spot.margin import margin_all_pairs
    from exchange_market.binance.spot.margin import margin_pair_index
    from exchange_market.binance.spot.margin import new_margin_order
    from exchange_market.binance.spot.margin import cancel_margin_order
    from exchange_market.binance.spot.margin import margin_transfer_history
    from exchange_market.binance.spot.margin import margin_load_record
    from exchange_market.binance.spot.margin import margin_repay_record
    from exchange_market.binance.spot.margin import margin_interest_history
    from exchange_market.binance.spot.margin import margin_force_liquidation_record
    from exchange_market.binance.spot.margin import margin_account
    from exchange_market.binance.spot.margin import margin_order
    from exchange_market.binance.spot.margin import margin_open_orders
    from exchange_market.binance.spot.margin import margin_open_orders_cancellation
    from exchange_market.binance.spot.margin import margin_all_orders
    from exchange_market.binance.spot.margin import margin_my_trades
    from exchange_market.binance.spot.margin import margin_max_borrowable
    from exchange_market.binance.spot.margin import margin_max_transferable
    from exchange_market.binance.spot.margin import isolated_margin_transfer
    from exchange_market.binance.spot.margin import isolated_margin_transfer_history
    from exchange_market.binance.spot.margin import isolated_margin_account
    from exchange_market.binance.spot.margin import isolated_margin_pair
    from exchange_market.binance.spot.margin import isolated_margin_all_pairs
    from exchange_market.binance.spot.margin import toggle_bnbBurn
    from exchange_market.binance.spot.margin import bnbBurn_status
    from exchange_market.binance.spot.margin import margin_interest_rate_history

    # SAVINGS
    from exchange_market.binance.spot.savings import savings_flexible_products
    from exchange_market.binance.spot.savings import savings_flexible_user_left_quota
    from exchange_market.binance.spot.savings import savings_purchase_flexible_product
    from exchange_market.binance.spot.savings import savings_flexible_user_redemption_quota
    from exchange_market.binance.spot.savings import savings_flexible_redeem
    from exchange_market.binance.spot.savings import savings_flexible_product_position
    from exchange_market.binance.spot.savings import savings_project_list
    from exchange_market.binance.spot.savings import savings_purchase_project
    from exchange_market.binance.spot.savings import savings_project_position
    from exchange_market.binance.spot.savings import savings_account
    from exchange_market.binance.spot.savings import savings_purchase_record
    from exchange_market.binance.spot.savings import savings_redemption_record
    from exchange_market.binance.spot.savings import savings_interest_history
    from exchange_market.binance.spot.savings import savings_change_position

    # WALLET
    from exchange_market.binance.spot.wallet import system_status
    from exchange_market.binance.spot.wallet import coin_info
    from exchange_market.binance.spot.wallet import account_snapshot
    from exchange_market.binance.spot.wallet import disable_fast_withdraw
    from exchange_market.binance.spot.wallet import enable_fast_withdraw
    from exchange_market.binance.spot.wallet import withdraw
    from exchange_market.binance.spot.wallet import deposit_history
    from exchange_market.binance.spot.wallet import withdraw_history
    from exchange_market.binance.spot.wallet import deposit_address
    from exchange_market.binance.spot.wallet import account_status
    from exchange_market.binance.spot.wallet import api_trading_status
    from exchange_market.binance.spot.wallet import dust_log
    from exchange_market.binance.spot.wallet import user_universal_transfer
    from exchange_market.binance.spot.wallet import user_universal_transfer_history
    from exchange_market.binance.spot.wallet import transfer_dust
    from exchange_market.binance.spot.wallet import asset_dividend_record
    from exchange_market.binance.spot.wallet import asset_detail
    from exchange_market.binance.spot.wallet import trade_fee

    # mining
    from exchange_market.binance.spot.mining import mining_algo_list
    from exchange_market.binance.spot.mining import mining_coin_list
    from exchange_market.binance.spot.mining import mining_worker
    from exchange_market.binance.spot.mining import mining_worker_list
    from exchange_market.binance.spot.mining import mining_earnings_list
    from exchange_market.binance.spot.mining import mining_bonus_list
    from exchange_market.binance.spot.mining import mining_statistics_list
    from exchange_market.binance.spot.mining import mining_account_list
    from exchange_market.binance.spot.mining import mining_hashrate_resale_request
    from exchange_market.binance.spot.mining import mining_hashrate_resale_cancellation
    from exchange_market.binance.spot.mining import mining_hashrate_resale_list
    from exchange_market.binance.spot.mining import mining_hashrate_resale_details

    # SUB-ACCOUNT
    from exchange_market.binance.spot.sub_account import sub_account_create
    from exchange_market.binance.spot.sub_account import sub_account_list
    from exchange_market.binance.spot.sub_account import sub_account_assets
    from exchange_market.binance.spot.sub_account import sub_account_deposit_address
    from exchange_market.binance.spot.sub_account import sub_account_deposit_history
    from exchange_market.binance.spot.sub_account import sub_account_status
    from exchange_market.binance.spot.sub_account import sub_account_enable_margin
    from exchange_market.binance.spot.sub_account import sub_account_margin_account
    from exchange_market.binance.spot.sub_account import sub_account_margin_account_summary
    from exchange_market.binance.spot.sub_account import sub_account_enable_futures
    from exchange_market.binance.spot.sub_account import sub_account_futures_transfer
    from exchange_market.binance.spot.sub_account import sub_account_margin_transfer
    from exchange_market.binance.spot.sub_account import sub_account_transfer_to_sub
    from exchange_market.binance.spot.sub_account import sub_account_transfer_to_master
    from exchange_market.binance.spot.sub_account import sub_account_transfer_sub_account_history
    from exchange_market.binance.spot.sub_account import sub_account_futures_asset_transfer_history
    from exchange_market.binance.spot.sub_account import sub_account_futures_asset_transfer
    from exchange_market.binance.spot.sub_account import sub_account_spot_summary
    from exchange_market.binance.spot.sub_account import sub_account_universal_transfer
    from exchange_market.binance.spot.sub_account import sub_account_universal_transfer_history
    from exchange_market.binance.spot.sub_account import sub_account_futures_account
    from exchange_market.binance.spot.sub_account import sub_account_futures_account_summary
    from exchange_market.binance.spot.sub_account import sub_account_futures_position_risk
    from exchange_market.binance.spot.sub_account import sub_account_spot_transfer_history
    from exchange_market.binance.spot.sub_account import sub_account_enable_leverage_token
    from exchange_market.binance.spot.sub_account import managed_sub_account_deposit
    from exchange_market.binance.spot.sub_account import managed_sub_account_assets
    from exchange_market.binance.spot.sub_account import managed_sub_account_withdraw

    # Futures
    from exchange_market.binance.spot.futures import futures_transfer
    from exchange_market.binance.spot.futures import futures_transfer_history
    from exchange_market.binance.spot.futures import futures_loan_borrow
    from exchange_market.binance.spot.futures import futures_loan_borrow_history
    from exchange_market.binance.spot.futures import futures_loan_repay
    from exchange_market.binance.spot.futures import futures_loan_repay_history
    from exchange_market.binance.spot.futures import futures_loan_wallet
    from exchange_market.binance.spot.futures import futures_loan_configs
    from exchange_market.binance.spot.futures import futures_loan_calc_adjust_level
    from exchange_market.binance.spot.futures import futures_loan_calc_max_adjust_amount
    from exchange_market.binance.spot.futures import futures_loan_adjust_collateral
    from exchange_market.binance.spot.futures import futures_loan_adjust_collateral_history
    from exchange_market.binance.spot.futures import futures_loan_liquidation_history
    from exchange_market.binance.spot.futures import futures_loan_collateral_repay_limit
    from exchange_market.binance.spot.futures import futures_loan_collateral_repay_quote
    from exchange_market.binance.spot.futures import futures_loan_collateral_repay
    from exchange_market.binance.spot.futures import futures_loan_collateral_repay_result
    from exchange_market.binance.spot.futures import futures_loan_interest_history

    # BLVTs
    from exchange_market.binance.spot.blvt import blvt_info
    from exchange_market.binance.spot.blvt import subscribe_blvt
    from exchange_market.binance.spot.blvt import subscription_record
    from exchange_market.binance.spot.blvt import redeem_blvt
    from exchange_market.binance.spot.blvt import redemption_record
    from exchange_market.binance.spot.blvt import user_limit_info

    # BSwap
    from exchange_market.binance.spot.bswap import bswap_pools
    from exchange_market.binance.spot.bswap import bswap_liquidity
    from exchange_market.binance.spot.bswap import bswap_liquidity_add
    from exchange_market.binance.spot.bswap import bswap_liquidity_remove
    from exchange_market.binance.spot.bswap import bswap_liquidity_operation_record
    from exchange_market.binance.spot.bswap import bswap_request_quote
    from exchange_market.binance.spot.bswap import bswap_swap
    from exchange_market.binance.spot.bswap import bswap_swap_history

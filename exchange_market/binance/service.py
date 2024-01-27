from exchange_market.binance.util import http_get_request, api_key_get, api_key_post


class BinanceSpotService:
    def __init__(self, url, access_key, secret_key):
        self.__url = url
        self.access_key = access_key
        self.secret_key = secret_key

    def get_klines(self, symbol="BTCUSDT", interval="5m", **kwargs):
        """
        interval: enum, 1m\3m\5m\15m\30m\1h\2h\4h\6h\8h\12h\1d\3d\1w\1M
        """
        params = {"symbol": symbol,
                  "interval": interval,
                  **kwargs}
        url = self.__url + "/api/v3/klines"
        return http_get_request(url, params=params)

    def spot_order_test(self, symbol, side, type, quantity=1):
        request_path = "/api/v3/order/test"
        params = {"symbol": symbol, "side": side, "type": type, "quantity": quantity}
        return api_key_post(self.__url, request_path, params, self.access_key, self.secret_key)

    def spot_order(self, symbol, side, type, quantity=None):
        request_path = "/api/v3/order"
        params = {"symbol": symbol, "side": side, "type": type, "quantity": quantity}
        return api_key_post(self.__url, request_path, params, self.access_key, self.secret_key)

    def order_query(self, symbol, orderId=0, origClientOrderId="muOrderId"):
        url = self.__url
        params = {"symbol": symbol, "orderId": orderId, "origClientOrderId": origClientOrderId}
        request_path = "/api/v3/order"
        return api_key_get(url, request_path, params, self.access_key, self.secret_key)

    def get_account_info(self, recvWindow=6000):
        url = self.__url
        params = {"recvWindow": recvWindow}
        request_path = "/api/v3/assets"
        return api_key_get(url, request_path, params, self.access_key, self.secret_key)

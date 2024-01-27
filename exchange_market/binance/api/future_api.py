import hmac
import json
import hashlib
import requests
from json import JSONDecodeError
from exchange_market.binance.constant import BASE_URL_FUTURE_REST
from exchange_market.binance.error import ClientError, ServerError
from exchange_market.binance.__version__ import __version__
from exchange_market.binance.lib.utils import cleanNoneValue, encoded_string, get_timestamp


class FutureAPI(object):
    def __init__(self, access_key, secret_key,
                 timeout=None,
                 show_limit_usage=False,
                 show_header=False):
        self.access_key = access_key
        self.secret_key = secret_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json;charset=utf-8",
                "User-Agent": "binance-connector/" + __version__,
                "X-MBX-APIKEY": self.access_key,
            }
        )
        self.base_url = BASE_URL_FUTURE_REST
        self.show_limit_usage = show_limit_usage
        self.show_header = show_header

    def query(self, request_path, payload={}):
        return self.send_request("GET", request_path, payload=payload)

    @staticmethod
    def _prepare_params(params):
        return encoded_string(cleanNoneValue(params))

    def _dispatch_request(self, http_method, account=None):
        # 如果指定了某个账户来做请求分发，则需要用该指定账户的access key来更新session的请求头；否则用全局的account的密钥做请求头
        if account:
            self.session.headers.update(
                {
                    "Content-Type": "application/json;charset=utf-8",
                    "User-Agent": "binance-connector/" + __version__,
                    "X-MBX-APIKEY": account.access_key,
                })

        return {
            "GET": self.session.get,
            "DELETE": self.session.delete,
            "PUT": self.session.put,
            "POST": self.session.post,
        }.get(http_method, "GET")

    def send_request(self, http_method, url_path, payload={}, account=None):
        url = self.base_url + url_path
        # logging.debug("url: " + url)
        params = cleanNoneValue(
            {
                "url": url,
                "params": self._prepare_params(payload),
                "timeout": self.timeout
            }
        )
        response = self._dispatch_request(http_method, account=account)(**params)
        # logging.debug("raw response from server:" + response.text)
        self._handle_exception(response)

        try:
            data = response.json()
        except ValueError:
            data = response.text
        result = {}

        if self.show_limit_usage:
            limit_usage = {}
            for key in response.headers.keys():
                key = key.lower()
                if (
                        key.startswith("x-mbx-used-weight")
                        or key.startswith("x-mbx-order-count")
                        or key.startswith("x-sapi-used")
                ):
                    limit_usage[key] = response.headers[key]
            result["limit_usage"] = limit_usage

        if self.show_header:
            result["header"] = response.headers

        if len(result) != 0:
            result["data"] = data
            return result

        return data

    @staticmethod
    def _handle_exception(response):
        status_code = response.status_code
        if status_code < 400:
            return
        if 400 <= status_code < 500:
            try:
                err = json.loads(response.text)
            except JSONDecodeError:
                raise ClientError(status_code, None, response.text, response.headers)
            raise ClientError(status_code, err["code"], err["msg"], response.headers)
        raise ServerError(status_code, response.text)

    def sign_request(self, http_method, url_path, payload={}, account=None):
        payload["timestamp"] = get_timestamp()
        query_string = self._prepare_params(payload)
        signature = self._get_sign(query_string, account=account)
        payload["signature"] = signature
        return self.send_request(http_method, url_path, payload, account)

    def _get_sign(self, data, account=None):
        """ 如果没有指定account对象，则使用全局account的密钥来做签名，否则针对某个账户的api密钥做签名校验 """
        secret_key = self.secret_key
        if account:
            secret_key = account.secret_key

        m = hmac.new(secret_key.encode("utf-8"), data.encode("utf-8"), hashlib.sha256)
        return m.hexdigest()

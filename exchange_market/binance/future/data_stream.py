def new_listen_key(self, account=None):
    """Create a ListenKey (USER_STREAM)
    POST /fapi/v1/listenKey
    """

    url_path = "/fapi/v1/listenKey"
    return self.send_request("POST", url_path, account=account)


def renew_listen_key(self, account=None):
    """Ping/Keep-alive a ListenKey (USER_STREAM)
    PUT /fapi/v1/listenKey
    """
    url_path = "/fapi/v1/listenKey"
    return self.send_request("PUT", url_path, account=account)


def close_listen_key(self, account=None):
    """Close a ListenKey (USER_STREAM)
    DELETE /fapi/v1/listenKey
    """
    url_path = "/fapi/v1/listenKey"
    return self.send_request("DELETE", url_path, account=account)

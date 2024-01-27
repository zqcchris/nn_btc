class AccountBinance(object):
    # 通过用户账户类相关的信息, 量化每次补仓数等于已持仓张数即可
    def __init__(self, username, access_key, secret_key, passphrase="", exchange=""):
        self.username = username
        self.access_key = access_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.exchange = exchange
        self.telephone = exchange

    def get_account_id(self):
        return self.username


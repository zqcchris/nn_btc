class AccountConfig(object):
    def __init__(self, account_id=None,
                 access_key=None,
                 secret_key=None,
                 contract_code=None,
                 balance_init=None,
                 balance_up_limit=None,
                 balance_low_limit=None,
                 expire_date=None,
                 paid=None,
                 valid=None,
                 email=""):
        self.account_id = account_id
        self.access_key = access_key
        self.secret_key = secret_key
        self.contract_code = contract_code
        self.balance_init = balance_init
        self.balance_up_limit = balance_up_limit
        self.balance_low_limit = balance_low_limit
        self.expire_date = expire_date
        self.paid = paid
        self.valid = valid
        self.email = email


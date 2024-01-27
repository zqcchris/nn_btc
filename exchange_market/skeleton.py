# coding: utf-8


class Skeleton(object):
    """原始K线元素"""
    def __init__(self, symbol, dt, price, direction, interval=None, exchange=""):
        self.exchange = exchange
        self.symbol = symbol
        self.dt = dt
        self.price = price
        self.direction = direction
        self.interval = interval

    def __str__(self):
        return ", ".join([self.symbol, self.dt, str(self.price), str(self.direction)])

    def to_dict(self):
        return self.__dict__


if __name__ == '__main__':
    pass

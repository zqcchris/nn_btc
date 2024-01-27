import os, sys
sys.path.append(os.getcwd())
import codecs
import numpy as np
import pandas as pd
import os
import torch
import warnings

warnings.filterwarnings('ignore')
# import tensorflow as tf
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))


def load_vector(datas):
    pass


class DatasetLoader(object):
    def __init__(self):
        pass

    def load_chg(self, symbol="BTCUSDT"):
        batch_x, batch_y = [], []
        with codecs.open(filename=base_dir + "/data/market/crypto/{}_chg.txt".format(symbol), mode="r", encoding="utf8") as f:
            datas = f.readlines()
            for idx, i in enumerate(datas):
                y, x = i.split("AinanceLabs")
                x = [float(i) for idx, i in enumerate(x.split(",")) if idx > 0]
                batch_x.append(x)
                batch_y.append(float(y))
        return batch_y, batch_x

    def load_delta(self, symbol="BTCUSDT"):
        batch_x, batch_y = [], []
        with codecs.open(filename=base_dir + "/data/market/crypto/{}_delta.txt".format(symbol), mode="r", encoding="utf8") as f:
            datas = f.readlines()
            for idx, i in enumerate(datas):
                # if idx > 100: continue
                y, x = i.split("AinanceLabs")
                x = [float(i) for idx, i in enumerate(x.split(",")) if idx > 0]
                batch_x.append(x)
                batch_y.append(float(y))
        return batch_y, batch_x

    def load_skeleton(self, symbol="BTCUSDT"):
        """  todo: add shuffle"""
        batch_x, batch_y, dts = [], [], []
        with codecs.open(filename=base_dir + "/data/market/crypto/{}_macd.txt".format(symbol), mode="r", encoding="utf8") as f:
            datas = f.readlines()
            for idx, i in enumerate(datas):
                # if idx > 100: continue
                y, x = i.split("AinanceLabs")
                dt = x.split(",")[0]
                dts.append(dt)
                x = [float(i) for idx, i in enumerate(x.split(",")) if idx > 0]
                batch_x.append(x)
                batch_y.append(float(y))
        return batch_y, batch_x, dts


# 创建两个张量作为输入数据
# input_data1 = [1.0, 2.0, 3.0]
# input_data2 = [4.0, 5.0, 6.0]
#
# # 转换为Tensor对象
# tensor1 = tf.constant(input_data1)
# tensor2 = tf.constant(input_data2)
#
# # 构造Batch
# batched_tensors = tf.stack([tensor1, tensor2])
# print("Batched Tensors:\n", batched_tensors)


if __name__ == '__main__':
    d = DatasetLoader()
    uu = torch.tensor(bx)
    print("p")

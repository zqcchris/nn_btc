import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
from examples.transformer.data_provider.data_loader import DatasetLoader


class Model(nn.Module):
    """ Vanilla Transformer with O(L^2) complexity """
    def __init__(self):
        super(Model, self).__init__()
        self.el1 = nn.Linear(in_features=5, out_features=21, bias=True)
        self.el2 = nn.Linear(in_features=21, out_features=21, bias=True)
        self.el3 = nn.Linear(in_features=64, out_features=64, bias=True)
        self.el4 = nn.Linear(in_features=64, out_features=21, bias=True)
        self.el5 = nn.Linear(in_features=21, out_features=2, bias=True)

    def forward(self, src, tgt=None):
        out = F.relu(self.el1(src))
        out = F.sigmoid(self.el2(out))
        # out = F.relu(self.el3(out))
        # out = F.relu(self.el4(out))
        out = F.sigmoid(self.el5(out))
        return out


if __name__ == '__main__':
    d = DatasetLoader()
    batch_y, batch_x, dts = d.load_skeleton(symbol="BTCUSDT")
    batch_x = torch.tensor(batch_x)
    batch_y = torch.tensor(batch_y, dtype=torch.long)
    criterion = nn.CrossEntropyLoss()
    xx = Model()
    model_optim = optim.Adam(params=xx.parameters(), lr=0.0001)
    for i in range(len(batch_y)):
        out = xx.forward(src=batch_x[i])
        loss = criterion(out, batch_y[i])
        # print(loss, out, batch_y[i])
        model_optim.zero_grad()
        loss.backward()
        model_optim.step()
    for k,v in xx.state_dict().items():
        print(k, v)
    torch.save(xx, "linear.model")

    batch_test_y, batch_test_x, dts = d.load_skeleton(symbol="ETHUSDT")
    batch_test_x = torch.tensor(batch_test_x)
    cnt = 0
    cor = 0
    tot = 0
    rec = 0
    for i in range(len(batch_test_y)):
        tot += 1
        out = xx.forward(src=batch_test_x[i])
        a = out.tolist()[0]
        b = out.tolist()[1]
        if batch_test_y[i] == 0:
            cnt += 1
            if a > b:
                cor += 1
                rec += 1
            print(dts[i], out, batch_test_y[i])
        else:
            if a < b:
                cor += 1

    print("accurary:", cor / tot)
    print("recall:", rec / cnt)
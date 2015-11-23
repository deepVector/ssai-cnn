#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'functions')
import chainer.links as L
import chainer.functions as F
from chainer import Chain
from cis import cis


class MnihCNN_cis(Chain):

    def __init__(self):
        super(MnihCNN_cis, self).__init__(
            conv1=L.Convolution2D(3, 64, 16, stride=4, pad=0),
            conv2=L.Convolution2D(64, 112, 4, stride=1, pad=0),
            conv3=L.Convolution2D(112, 80, 3, stride=1, pad=0),
            fc4=L.Linear(5120, 768),
        )
        self.train = True

    def __call__(self, x, t):
        h = F.relu(self.conv1(x))
        h = F.relu(self.conv2(h))
        h = F.relu(self.conv3(h))
        h = self.fc4(h)
        self.pred = F.reshape(h, t.data.shape)

        if t is not None:
            self.loss = cis(self.pred, t)
            return self.loss
        else:
            self.pred = F.sigmoid(self.pred)
            return self.pred

model = MnihCNN_multi()

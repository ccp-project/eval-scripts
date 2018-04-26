#!/usr/bin/python3

import sys
import itertools
import numpy as np
import random

def read(fn):
    with open(fn, 'r') as f:
        for line in f:
            sp = line.split()
            if len(sp) != 7:
                continue
            yield tuple(sp)

def groupByIter(ls):
    ixCol = 3
    iyCol = 4
    sls = sorted(ls,key=lambda x:(x[0], x[1], x[2], x[3], x[4]))
    return itertools.groupby(sls, key=lambda x:(x[0], x[1], x[2], x[3], x[4]))

if __name__ == '__main__':
    fn = sys.argv[1]
    sample = int(sys.argv[2])
    print("Algorithm Impl Scenario IterationX IterationY Time Cwnd")
    ls = read(fn)
    next(ls) # drop first line
    for _, it in groupByIter(ls):
        line = list(it)
        if len(line) > sample:
            line = random.sample(line, sample)
        for l in sorted(line, key=lambda x: float(x[-2])):
            print(*l)

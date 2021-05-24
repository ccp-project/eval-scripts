#!/usr/bin/python3

import sys
import itertools
import numpy as np

def read(fn):
    with open(fn, 'r') as f:
        for line in f:
            sp = line.split()
            if len(sp) != 16:
                continue
            if '4242' not in sp[5]:
                continue
            yield float(sp[2][:-1]), float(sp[10].split('=')[-1]) # rtt = sp[-3]

# filenames: <alg>-<impl>-<scenario>-<i>-tcpprobe.log
def binAlgs(fns):
    plots = {}
    for fn in fns:
        sp = fn.split('-')
        if sp[-1] != "tcpprobe.log":
            continue
        alg, impl, scenario, i = sp[:-1]
        pl = (alg, impl, scenario, i)
        if pl in plots:
            plots[pl].append(fn)
        else:
            plots[pl] = [fn]
    return plots

if __name__ == '__main__':
    print("Algorithm Impl Scenario IterationX IterationY Time Cwnd")
    plots = binAlgs(sys.argv[1:])
    iters = max(int(pl[-1]) for pl in plots) + 1
    for pl in plots:
        for fn in plots[pl]:
            ts, cwnd = zip(*read(fn))
            ts = np.array(ts) - min(ts)
            for t, c in zip(ts, cwnd):
                for iy in range(iters):
                    print(*pl, iy, t, c)

#!/usr/bin/python3

# recompute aggregegate throughput in case iperf doesn't report it properly

import sys
import re
import itertools

sumLineStr = r'.*\[SUM\].*?([0-9]+\.[0-9]+)-.*?([0-9]+\.[0-9]+).sec.*?([0-9]+\.[0-9]+.[GMK])bits/sec.*'
sumLine = re.compile(sumLineStr)

ipLineStr = r'.*\[.*?([0-9]+)\].*?([0-9]+\.[0-9]+)-.*?([0-9]+\.[0-9]+).sec.*?([0-9]+\.[0-9]+.[GMK])Bytes.*?([0-9]+\.?[0-9]+.[GMK])bits/sec.*'
ipLine = re.compile(ipLineStr)

def parseV(s):
    sp = s.split()
    b = float(sp[0])
    if sp[1] == 'K':
        return b * 1e3
    elif sp[1] == 'M':
        return b * 1e6
    elif sp[1] == 'G':
        return b * 1e9


def read(fn):
    with open(fn, 'r') as f:
        for line in f:
            m = sumLine.match(line)
            if m is not None:
                grp = m.groups()
                assert len(grp) == 3
                yield 'SUM', float(grp[0]), float(grp[1]), parseV(grp[2])
                return

            m = ipLine.match(line)
            if m is None:
                continue
            grp = m.groups()
            assert len(grp) == 5
            yield float(grp[0]), float(grp[1]), float(grp[2]), parseV(grp[3]), parseV(grp[4])


def reportTx(fn):
    totTx = 0
    lastTime = 0
    for l in read(fn):
        #print(l)
        if l[0] is 'SUM':
            return l[-1]
        else:
            totTx += l[3]
            if l[2] > lastTime:
                lastTime = l[2]

    return totTx * 8 / lastTime


def reportBw(fn):
    ls = {}
    for l in read(fn):
        #print(l)
        if l[0] is 'SUM':
            return l[-1]
        else:
            #assert l[0] not in ls, (l[0], ls)
            ls[l[0]] = l

    tot = sum(ls[l][-1] for l in ls)
    return tot


if __name__ == '__main__':
    bw = reportBw(sys.argv[1])
    print(bw)

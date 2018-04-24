import sys
from plotMahimahi import get_throughput_data, get_delay_data, get_throughput, get_delays

import numpy as np

def get_times(fn, binsize):
    bin_start = 0
    yield 0
    for t, _ in get_throughput_data(fn):
        if (bin_start + binsize) > t:
            yield t
    yield t

def get_expt_data(fn):
    tp = get_throughput_data(fn)
    td = get_delay_data(fn)

    ts, tp = zip(*get_throughput(tp, 0, 60, 75 * 0.001))
    ts = list(ts)
    dl = get_delays(td, iter(ts))
    return zip(ts, tp, dl)

# filenames: <alg>-<impl>-<i>-<scenario>-mahimahi.log
def binAlgs(fns):
    plots = {}
    for fn in fns:
        sp = fn.split('-')
        if sp[-1] != "mahimahi.log":
            continue
        alg, impl, i, scenario = sp[:-1]
        pl = (alg, impl, scenario, i)
        if pl in plots:
            plots[pl].append(fn)
        else:
            plots[pl] = [fn]
    return plots

if __name__ == '__main__':
    print("Algorithm", "Impl", "Scenario", "Iteration", "TimeBin", "Throughput", "Delay")
    exps = binAlgs(sys.argv[1:])
    for exp in exps:
        for b, t, d in get_expt_data(exps[exp][0]):
            print(*exp, b, t, d)

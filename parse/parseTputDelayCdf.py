#!/usr/bin/python3

import sys
import numpy as np
import subprocess

def get_throughput_data(fn):
    cmd = "grep ' + ' {} | awk '{{print $1, $3}}'".format(fn)
    res = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    for l in res.stdout.decode("utf-8").split('\n'):
        sp = l.split(" ")
        if len(sp) != 2:
            continue
        t, v = sp
        yield float(t) / 1e3, float(v)

def get_delay_data(fn):
    cmd = "grep ' - ' {} | awk '{{print $1, $5}}'".format(fn)
    res = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    for l in res.stdout.decode("utf-8").split('\n'):
        sp = l.split(" ")
        if len(sp) != 2:
            continue
        t, v = sp
        yield float(t) / 1e3, float(v)

def get_throughput(data, start_time, end_time, binsize):
    bin_start = start_time
    last_t = start_time
    current_bin_tput = 0
    for t, p in data:
        if t < start_time or t > end_time:
            continue

        if t > (bin_start + binsize): # start new bin
            yield bin_start, current_bin_tput / binsize
            bin_start = t
            current_bin_tput = 0
        else:
            current_bin_tput += p * 8.0
            last_t = t

    yield bin_start, current_bin_tput / binsize


def get_delays(data, bin_times):
    next_bin = next(bin_times)
    delays = []
    for t, p in data:
        if t < next_bin:
            delays.append(p)
        else:
            if len(delays) > 0:
                yield np.mean(delays)
            else:
                yield 0
            delays = []
            delays.append(p)
            next_bin = next(bin_times)

    yield np.mean(delays)

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

# filenames: <alg>-<impl>-<scenario>-<i>-mahimahi.log
def binAlgs(fns):
    plots = {}
    for fn in fns:
        sp = fn.split('-')
        if sp[-1] != "mahimahi.log":
            continue
        alg, impl, scenario, i = sp[:-1]
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

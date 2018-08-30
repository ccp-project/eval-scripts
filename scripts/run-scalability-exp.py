#!/usr/bin/python3

import argparse
import itertools
import math
import os
import subprocess as sh
import sys
import threading
import time

from setup import setup
from start_ccp import algs, start as ccp_start

parser = argparse.ArgumentParser(description='Run CCP experiments')
parser.add_argument('--dir', dest='dir', type=str)
parser.add_argument('--iters', dest='iters', type=int)
parser.add_argument('--maxNumFlows', dest='numFlows', type=int)
parser.add_argument('--duration', dest='duration', type=int)
parser.add_argument('--alg', dest='algs', action='append', type=str, nargs='+', default=[['all']])
parser.add_argument('--ipcs', dest='ipcs', action='append', type=str, nargs='+', default=[['all']])
parser.add_argument('--scenario', dest='scenarios', action='append', type=str, nargs='+', default=[['all']])
parser.add_argument('--kernel', dest='with_kernel', action='store_true', default=False)
parser.add_argument('--plot-only', dest='plot_only', action='store_true', default=False)
parser.add_argument('--dark-plot', dest='dark_plot', action='store_true', default=False)

scenarios = ('per_ack', 'per_10ms')
ipcs = ('netlink', 'chardev')

def get_outprefix(impl, alg, numflows, dur, i):
    return "{}-{}-{}flows-{}s-{}".format(impl, alg, numflows, dur, i)

def run_exps(dest, exps, maxNumFlows, dur, iters):
    print("Running Experiments")
    print("=========================")
    for impl, ipc, alg in exps:
        # impl = "kernel" or "ccp_per_ack" or "ccp_per_10ms"
        # ipc = "netlink" or "chardev" or "kernel"
        # alg = "reno" or "cubic"
        # log name: dest/impl_ipc_alg-{numFlows}-{dur}-{iter}.log
        for numflows in [1 << i for i in range(maxNumFlows + 1)]:
            for i in range(iters):
                outprefix = get_outprefix(impl, alg, numflows, dur, i)
                if os.path.exists("./{}/{}-iperf.log".format(dest, outprefix)):
                    print(">", outprefix, 'done')
                    continue

                sh.run('killall -9 iperf', shell=True)
                sh.Popen('./scripts/run-iperf-server.sh > {0}/{1}-iperf_server.log 2> /dev/null'.format(dest, outprefix), shell=True)

                if 'ccp' in impl:
                    sh.run('sudo killall reno cubic bbr 2> /dev/null', shell=True)
                    ccp_args = ''
                    if 'per_ack' in impl:
                        ccp_args = '--per_ack'
                    elif 'ccp_per_10ms' in impl:
                        ccp_args = '-i 10'
                    threading.Thread(target=ccp_start, args=(dest, alg, ipc, outprefix, ccp_args), daemon=True).start()
                    time.sleep(1)

                print(">", outprefix)
                sh.run('iperf -c 127.0.0.1 -p 4242 -Z {} -P {} -t {} -w 16M > ./{}/{}-iperf.log'.format('ccp' if 'ccp' in impl else alg, numflows, dur, dest, outprefix), shell=True)

                if 'ccp' in impl:
                    sh.run('sudo killall reno cubic 2> /dev/null', shell=True)
                    time.sleep(1)

def plot(dest, exps, maxNumFlows, dur, iters):
    print("Throughput Plot")
    print("=========================")

    if os.path.exists("./{}/tputs.log".format(dest)):
        print("> ./{}/tputs.log done".format(dest))
    else:
        with open("./{}/tputs.log".format(dest), 'w') as f:
            f.write("Scenario Impl IPC Algorithm NumFlows Iteration Throughput\n")
            for impl, ipc, alg in exps:
                for numflows in [1 << i for i in range(maxNumFlows + 1)]:
                    for i in range(iters):
                        outprefix = get_outprefix(impl, alg, numflows, dur, i)
                        print("> ./{}/{}-iperf.log".format(dest, outprefix))
                        bw = sh.check_output('./parse/parseIperf.py ./{}/{}-iperf.log'.format(dest, outprefix), shell=True)
                        f.write("{0}-{1}-{2} {0} {1} {2} {3} {4} {5}\n".format(impl, ipc, alg, numflows, i, float(bw.strip())))

    if os.path.exists("./{}/tputs.pdf".format(dest)):
        print("> ./{}/tputs.pdf done".format(dest))
    else:
        sh.run("./plot/num-flows-tput.r ./{0}/tputs.log ./{0}/tputs.pdf {1}".format(dest, 'dark' if parsed.dark_plot else 'light'), shell=True)

if __name__ == '__main__':
    parsed = parser.parse_args()

    dest = parsed.dir
    if '-' in dest:
        print("> Don't put '-' in the output directory name")
        sys.exit()
    print("> output directory:", dest)

    iters = parsed.iters
    print("> number of per-experiment iterations:", iters)
    dur = parsed.duration
    print("> per-experiment duration (s):", dur)
    maxNumFlows = int(math.log(parsed.numFlows, 2))
    print("> Up to (flows):", 1 << maxNumFlows)

    scns = list(itertools.chain.from_iterable(parsed.scenarios))
    if 'all' in scns and len(scns) == 1:
        scns = scenarios
    else:
        scns = scns[1:]

    print("> Running reporting scenarios:", ', '.join(scns))

    wanted_algs = list(itertools.chain.from_iterable(parsed.algs))
    if 'all' in wanted_algs and len(wanted_algs) == 1:
        wanted_algs = algs.keys()
    else:
        wanted_algs = [a for a in wanted_algs[1:] if a in algs]

    print("> Running algorithms:", ", ".join(wanted_algs))

    wanted_ipcs = list(itertools.chain.from_iterable(parsed.ipcs))
    if 'all' in wanted_ipcs and len(wanted_ipcs) == 1:
        wanted_ipcs = ipcs
    else:
        wanted_ipcs = [i for i in wanted_ipcs[1:] if i in ipcs]

    print("> Using IPCs:", ",".join(wanted_ipcs))

    # kernel experiments
    kernel_exps = []
    if parsed.with_kernel:
        kernel_exps += [('kernel', 'none', a) for a in wanted_algs if a in algs]
        print("> kernel exps:", ', '.join(e[-1] for e in kernel_exps))
        if not parsed.plot_only:
            setup(dest, startIperf=False)
            run_exps(dest, kernel_exps, maxNumFlows, dur, iters)

    # ccp experiments
    ccp_exps = []
    for i in wanted_ipcs:
        if i not in ipcs:
            continue
        exps = []
        for s in scns:
            exps += [('ccp_{}_{}'.format(i, s), i, alg) for alg in wanted_algs if alg in algs]
        print("> ccp_{} exps:".format(i), ', '.join(e[-1] for e in exps))

        if not parsed.plot_only:
            setup(dest, ipc=i, startIperf=False)
            run_exps(dest, exps, maxNumFlows, dur, iters)
        ccp_exps += exps

    print()

    plot(dest, kernel_exps + ccp_exps, maxNumFlows, dur, iters)

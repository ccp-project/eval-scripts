#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Run CCP experiments')
# experiment configuration
parser.add_argument('--dir', dest='dir', type=str)
parser.add_argument('--iters', dest='iters', type=int)
parser.add_argument('--duration', dest='duration', type=int)
parser.add_argument('--alg', dest='algs', action='append', type=str, nargs='+', default=[['all']])
parser.add_argument('--scenario', dest='scenarios', action='append', type=str, nargs='+', default=[['all']])
parser.add_argument('--kernel', dest='with_kernel', action='store_true', default=False)
# link configuration
parser.add_argument('--delay', dest='linkdelay', type=int default='10')
parser.add_argument('--rate', dest='fixedrate', default='96')
parser.add_argument('--qsize', dest='fixedqsize', type=int, default='1')

scenarios = ('fixed', 'cell', 'drop')
kernel_algs = ['reno', 'cubic', 'bbr', 'vegas']

import itertools
import os
import sys
import subprocess as sh
import time
import threading

from setup import setup
from start_ccp import start as ccp_start
from start_ccp import algs

def run_exps(exps, dest, iters, dur, scenarios):
    print("Running Experiments")
    print("=========================")
    for alg, sockopt, name in exps:
        for trace in scenarios:
            for i in range(iters):
                outprefix = "{}-{}-{}".format(name, trace, i)
                if os.path.exists("./{}/{}-mahimahi.log".format(dest, outprefix)):
                    print(">", outprefix, 'done')
                    continue

                if sockopt == 'ccp':
                    sh.run('sudo killall reno cubic bbr copa 2> /dev/null', shell=True)
                    ccp_args = ''
                    if alg == 'reno' or alg == 'cubic':
                        ccp_args = '--deficit_timeout=20'
                    threading.Thread(target=ccp_start, args=(dest, alg, '{}-{}-{}'.format(name, trace, i), ccp_args), daemon=True).start()
                    time.sleep(1)

                print(">", outprefix)

                sh.run("sudo dd if=/dev/null of=/proc/net/tcpprobe 2> /dev/null", shell=True)
                sh.run('sudo dd if=/proc/net/tcpprobe of="./{}/{}-tmp.log" 2> /dev/null &'.format(dest, outprefix), shell=True)

                if trace == 'fixed':
                    sh.run('mm-delay 10 \
                            mm-link ./mm-traces/bw12.mahi ./mm-traces/bw12.mahi \
                              --uplink-queue=droptail \
                              --downlink-queue=droptail \
                              --uplink-queue-args="packets=40" \
                              --downlink-queue-args="packets=40" \
                              --uplink-log="./{0}/{1}-mahimahi.log" \
                            -- ./scripts/run-iperf.sh {0} {1} {2} {3}'.format(dest, outprefix, sockopt, dur), shell=True)
                elif trace == 'cell':
                    sh.run('mm-delay 10 \
                            mm-link ./mm-traces/Verizon-LTE-short.up ./mm-traces/Verizon-LTE-short.down \
                              --uplink-queue=droptail \
                              --downlink-queue=droptail \
                              --uplink-queue-args="packets=100" \
                              --downlink-queue-args="packets=100" \
                              --uplink-log="./{0}/{1}-mahimahi.log" \
                            -- ./scripts/run-iperf.sh {0} {1} {2} {3}'.format(dest, outprefix, sockopt, dur), shell=True)
                elif trace == 'drop':
                    sh.run('mm-delay 10 \
                            mm-link ./mm-traces/bw96.mahi ./mm-traces/bw96.mahi \
                              --uplink-log="./{0}/{1}-mahimahi.log" \
                            mm-loss uplink 0.0001 \
                            -- ./scripts/run-iperf.sh {0} {1} {2} {3}'.format(dest, outprefix, sockopt, dur), shell=True)
                else:
                    print('unknown', trace)
                    break

                sh.run("sudo killall dd 2> /dev/null", shell=True)
                sh.run('grep ":4242" "./{0}/{1}-tmp.log" > "./{0}/{1}-tcpprobe.log"'.format(dest, outprefix), shell=True)
                sh.run('rm -f "./{}/{}-tmp.log"'.format(dest, outprefix), shell=True)
                sh.run("mm-graph ./{0}/{1}-mahimahi.log 30 > ./{0}/{1}-mahimahi.eps 2> ./{0}/{1}-mmgraph.log".format(dest, outprefix), shell=True)

                if sockopt == 'ccp':
                    sh.run('sudo killall ccp 2> /dev/null', shell=True)
                    time.sleep(1)

    sh.run('sudo killall iperf 2> /dev/null', shell=True)

def plot(dest, algs_to_plot, scenarios_to_plot):
    print("Cwnd Evolution Plots")
    print("=========================")
    print("> Parsing logs")
    sh.run('python3 parse/parseCwndEvo.py {0}/* > {0}/cwndevo.log'.format(dest), shell=True)
    print("> Subsampling logs for plotting")
    sh.run('python3 parse/sampleCwndEvo.py {0}/cwndevo.log 1000 > {0}/cwndevo-subsampled.log'.format(dest), shell=True)

    print("> Plotting")
    for alg in algs_to_plot:
        for s in scenarios_to_plot:
            if not os.path.exists("{0}/{1}-{2}-cwndevo.pdf".format(dest, alg, s)):
                sh.run('./plot/cwnd-evo.r {0}/cwndevo-subsampled.log {1} {2} {0}/{1}-{2}-cwndevo.pdf'.format(dest, alg, s), shell=True)
                print("> wrote {0}/{1}-cwndevo.pdf".format(dest, alg))
            else:
                print("> {0}/{1}-{2}-cwndevo.pdf' already present".format(dest, alg, s))

    print("Throughput-Delay CDF Plots")
    print("=========================")
    if not os.path.exists("{0}/tput-delay-cdf.log".format(dest)):
        print("> Parsing logs")
        sh.run('python3 parse/parseTputDelayCdf.py {0}/* > {0}/tput-delay-cdf.log'.format(dest), shell=True)
    else:
        print("> Logs already parsed")

    print("> Plotting") # all experiments combined, not separate
    if not os.path.exists("{0}/tput-cdf.pdf".format(dest)) or not os.path.exists("{0}/delay-cdf.pdf".format(dest)):
        sh.run('./plot/tput-delay-cdf.r {0}/tput-delay-cdf.log {0}/tput-cdf.pdf {0}/delay-cdf.pdf'.format(dest), shell=True)
        print("> wrote {0}/tput-cdf.pdf, {0}/delay-cdf.pdf".format(dest))
    else:
        print("> {0}/tput-cdf.pdf, {0}/delay-cdf.pdf already present".format(dest))

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

    scns = list(itertools.chain.from_iterable(parsed.scenarios))
    if 'all' in scns and len(scns) == 1:
        scns = scenarios
    else:
        scns = scns[1:]

    print("> Running link scenarios:", ', '.join(scns))

    wanted_algs = list(itertools.chain.from_iterable(parsed.algs))
    if 'all' in wanted_algs and len(wanted_algs) == 1:
        wanted_algs = algs.keys()
    else:
        wanted_algs = wanted_algs[1:]

    exps = [(a, 'ccp', '{}-ccp'.format(a)) for a in wanted_algs if a in algs]
    if parsed.with_kernel:
        kernel_exps = [(a, a, '{}-kernel'.format(a)) for a in wanted_algs if a in kernel_algs]
        exps += kernel_exps

    print("> exps:", ', '.join(e[-1] for e in exps))

    setup(dest)
    run_exps(exps, dest, iters, dur, scns)

    print()
    plot(dest, wanted_algs, scns)
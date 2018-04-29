#!/usr/bin/python3

import os
import sys
import subprocess as sh
import time
import threading

from setup import setup
from start_ccp import start as ccp_start

scenarios = ('fixed', 'cell', 'drop')
algs = {
    'reno': './portus/ccp_generic_cong_avoid/target/debug/reno',
    'cubic': './portus/ccp_generic_cong_avoid/target/debug/cubic',
}

def exps(exps, dest, iters, dur, scenarios):
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
                    sh.run('sudo killall reno cubic bbr 2> /dev/null', shell=True)
                    ccp_args = '--deficit_timeout=20'
                    threading.Thread(target=ccp_start, args=(dest, alg, '{}-{}-{}'.format(name, trace, i), ccp_args), daemon=True).start()
                    time.sleep(1)

                print(">", outprefix)

                sh.run("sudo dd if=/dev/null of=/proc/net/tcpprobe 2> /dev/null", shell=True)
                sh.run('sudo dd if=/proc/net/tcpprobe of="./{}/{}-tmp.log" 2> /dev/null &'.format(dest, outprefix), shell=True)

                if trace == 'fixed':
                    sh.run('mm-delay 10 \
                            mm-link ./mm-traces/bw96.mahi ./mm-traces/bw96.mahi \
                              --uplink-queue=droptail \
                              --downlink-queue=droptail \
                              --uplink-queue-args="packets=320" \
                              --downlink-queue-args="packets=320" \
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

def plot(dest, algs, scenarios):
    print("Cwnd Evolution Plots")
    print("=========================")
    if not os.path.exists("{0}/cwndevo.log".format(dest)):
        print("> Parsing logs")
        sh.run('python3 parse/parseCwndEvo.py {0}/* > {0}/cwndevo.log'.format(dest), shell=True)
    else:
        print("> Logs already parsed")

    if not os.path.exists("{0}/cwndevo-subsampled.log".format(dest)):
        print("> Subsampling logs for plotting")
        sh.run('python3 parse/sampleCwndEvo.py {0}/cwndevo.log 1000 > {0}/cwndevo-subsampled.log'.format(dest), shell=True)
    else:
        print("> Logs already subsampled")

    print("> Plotting")
    for alg in algs:
        for s in scenarios:
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
    dest = sys.argv[1]
    iters = int(sys.argv[2])
    dur = sys.argv[3]

    ccp_exps = [(a, 'ccp', '{}-ccp'.format(a)) for a in algs]
    kernel_exps = [(a, a, '{}-kernel'.format(a)) for a in algs]

    if '-' in dest:
        print("> Don't put '-' in the output directory name")
        sys.exit()

    setup(dest)
    exps(ccp_exps + kernel_exps, dest, iters, dur, scenarios)

    print()
    plot(dest, algs, scenarios)

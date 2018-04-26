#!/usr/bin/python3

import os
import sys
import subprocess
import time
import threading

from start_ccp import start as ccp_start

def setup(dest):
    print("setup")
    print("=========================")
    subprocess.run('./scripts/setup.sh', shell=True)

    print(dest)
    print("=========================")
    for e in exps:
        print(e)

    subprocess.run('mkdir -p {}'.format(dest), shell=True)
    subprocess.Popen('./scripts/run-iperf-server.sh > {0}/iperf-server.log'.format(dest), shell=True)

def exps(exps, dest, iters, dur, scenarios):
    for alg, sockopt, name in exps:
        for trace in scenarios:
            for i in range(iters):
                if sockopt == 'ccp':
                    subprocess.run('sudo killall reno cubic bbr 2> /dev/null', shell=True)
                    threading.Thread(target=ccp_start, args=(dest, alg, '{}-{}-{}'.format(name, trace, i)), daemon=True).start()
                    time.sleep(1)

                if trace == 'fixed':
                    subprocess.run(['bash', './scripts/run-fixed-exp.sh', dest, sockopt, "{}-{}".format(name, i), dur])
                elif trace == 'cell':
                    subprocess.run(['bash', './scripts/run-cell-exp.sh', dest, sockopt, "{}-{}".format(name, i), dur])
                elif trace == 'drop':
                    subprocess.run(['bash', './scripts/run-drop-exp.sh', dest, sockopt, "{}-{}".format(name, i), dur])
                else:
                    print('unknown', trace)
                    break

                if sockopt == 'ccp':
                    subprocess.run('sudo killall ccp 2> /dev/null', shell=True)
                    time.sleep(1)

    subprocess.run('sudo killall iperf 2> /dev/null', shell=True)

def plot(dest, algs):
    print("Cwnd Evolution")
    print("=========================")
    subprocess.run('python3 parse/parseCwndEvo.py {0}/* > {0}/cwndevo.log'.format(dest), shell=True)
    subprocess.run('python3 parse/sampleCwndEvo.py {0}/cwndevo.log 1000 > {0}/cwndevo-subsampled.log'.format(dest), shell=True)
    for alg in algs:
        subprocess.run('./plot/cwnd-evo.r {0}/cwndevo-subsampled.log {1} {0}/{1}-cwndevo.pdf'.format(dest, alg), shell=True)

if __name__ == '__main__':
    dest = sys.argv[1]
    iters = int(sys.argv[2])
    dur = sys.argv[3]
    scenarios = ('fixed', 'cell', 'drop')
    algs = {
        'reno': './portus/ccp_generic_cong_avoid/target/debug/reno',
        'cubic': './portus/ccp_generic_cong_avoid/target/debug/cubic',
    }

    ccp_exps = [(a, 'ccp', '{}-ccp'.format(a)) for a in algs]
    kernel_exps = [(a, a, '{}-kernel'.format(a)) for a in algs]

    if not os.path.exists(dest):
        print("Running Experiments")
        print("=========================")
        setup(dest)
        exps(ccp_exps + kernel_exps, dest, iters, dur, scenarios)
    else:
        print("> Experiments already run, re-plotting")
    plot(dest, algs)

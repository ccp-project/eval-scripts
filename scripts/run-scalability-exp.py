#!/usr/bin/python3

import os
import sys
import subprocess as sh
import time
import threading

from setup import setup
from start_ccp import start as ccp_start

algs = {
    'reno': './portus/ccp_generic_cong_avoid/target/debug/reno',
}

scenarios = ('kernel', 'ccp_per_ack', 'ccp_per_10ms')

def exps(exps, dest, iters, dur, maxNumFlows):
    print("Running Experiments")
    print("=========================")
    for name in exps:
        for i in range(iters):
            for numflows in [1 << i for i in range(maxNumFlows + 1)]:
                outprefix = "{}-{}-{}".format(name, numflows, i)
                if os.path.exists("./{}/{}-iperf.log".format(dest, outprefix)):
                    print(">", outprefix, 'done')
                    continue

                if 'ccp' in name:
                    sh.run('sudo killall reno cubic bbr 2> /dev/null', shell=True)
                    ccp_args = ''
                    if name == 'ccp_per_ack':
                        ccp_args = '--per_ack'
                    elif name == 'ccp_per_10ms':
                        ccp_args = '-i 10'
                    threading.Thread(target=ccp_start, args=(dest, 'reno', outprefix, ccp_args), daemon=True).start()
                    time.sleep(1)

                sh.run('iperf -c 127.0.0.1 -p 4242 -Z {} -P {} -t {} > ./{}/{}-iperf.log'.format('ccp' if 'ccp' in name else 'reno', numflows, dur, dest, outprefix), shell=True)

                if 'ccp' in name:
                    sh.run('sudo killall reno cubic bbr 2> /dev/null', shell=True)
                    time.sleep(1)

def plot(dest, exps, iters, maxNumFlows):
    print("Throughput Plot")
    print("=========================")

    if os.path.exists("./{}/tputs.log".format(dest)):
        print("> ./{}/tputs.log done".format(dest))
    else:
        with open("./{}/tputs.log".format(dest), 'w') as f:
            f.write("Scenario NumFlows Iteration Throughput\n")
            for name in exps:
                for numflows in [1 << i for i in range(maxNumFlows + 1)]:
                    for i in range(iters):
                        outprefix = "{}-{}-{}".format(name, numflows, i)
                        print("> ./{}/{}-iperf.log".format(dest, outprefix))
                        bw = sh.check_output('./parse/parseIperf.py ./{}/{}-iperf.log'.format(dest, outprefix), shell=True)
                        f.write("{} {} {} {}\n".format(name, numflows, i, float(bw.strip())))

    if os.path.exists("./{}/tputs.pdf".format(dest)):
        print("> ./{}/tputs.pdf done".format(dest))
    else:
        sh.run("./plot/num-flows-tput.r ./{0}/tputs.log ./{0}/tputs.pdf".format(dest,), shell=True)

if __name__ == '__main__':
    dest = sys.argv[1]
    maxNumFlows = int(sys.argv[2])
    iters = int(sys.argv[3])
    dur = sys.argv[4]

    if '-' in dest:
        print("> Don't put '-' in the output directory name")
        sys.exit()

    setup(dest)
    exps(scenarios, dest, iters, dur, maxNumFlows)
    plot(dest, scenarios, iters, maxNumFlows)

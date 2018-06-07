#!/usr/bin/python3

import subprocess as sh
import os

def setup(dest, startIperf=True, ipc='netlink'):
    print("setup")
    print("=========================")
    ipc = 'ipc=0' if ipc is 'netlink' else 'ipc=1'
    sh.run('./scripts/setup.sh {}'.format(ipc), shell=True)

    if not os.path.exists(dest):
        sh.run('mkdir -p {}'.format(dest), shell=True)
        print("> created output directory: {}".format(dest))

    if startIperf:
        sh.Popen('./scripts/run-iperf-server.sh > {0}/iperf-server.log'.format(dest), shell=True)
        print("> started iperf server")

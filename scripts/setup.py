#!/usr/bin/python3

import subprocess as sh
import os

def setup(dest, startIperf=True):
    print("setup")
    print("=========================")
    sh.run('./scripts/setup.sh', shell=True)

    if not os.path.exists(dest):
        sh.run('mkdir -p {}'.format(dest), shell=True)
        print("> dest: {}".format(dest))

    if startIperf:
        sh.Popen('./scripts/run-iperf-server.sh > {0}/iperf-server.log'.format(dest), shell=True)
        print("> started iperf server")

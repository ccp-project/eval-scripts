#!/usr/bin/python3

import sys
import subprocess

algs = {
    'reno': './portus/ccp_generic_cong_avoid/target/debug/reno',
    'cubic': './portus/ccp_generic_cong_avoid/target/debug/cubic',
}

def start(dest, alg, name):
    subprocess.run('mkdir ./{} 2> /dev/null'.format(dest), shell=True)
    cmd = 'sudo {0} --ipc=netlink 2> ./{1}/{2}-ccp.log'.format(algs[alg], dest, alg, name)
    ccp_proc = subprocess.run(cmd, shell=True)

if __name__ == '__main__':
    dest = sys.argv[1]
    alg = sys.argv[2]
    name = sys.argv[3]
    start(dest, alg, name)

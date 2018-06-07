#!/usr/bin/python3

import sys
import subprocess

algs = {
    'reno': './portus/ccp_generic_cong_avoid/target/debug/reno',
    'cubic': './portus/ccp_generic_cong_avoid/target/debug/cubic',
#    'copa': './ccp_copa/target/debug/copa',
}

def start(dest, alg, name, args):
    subprocess.run('mkdir ./{} 2> /dev/null'.format(dest), shell=True)
    cmd = 'sudo {0} --ipc=char {3} > ./{1}/ccp-tmp.log 2> ./{1}/{2}-ccp.log'.format(algs[alg], dest, name, args)
    print("> starting ccp: {}", cmd)
    ccp_proc = subprocess.run(cmd, shell=True)

if __name__ == '__main__':
    dest = sys.argv[1]
    alg = sys.argv[2]
    name = sys.argv[3]
    args = ' '.join(sys.argv[4:])
    start(dest, alg, name, args)

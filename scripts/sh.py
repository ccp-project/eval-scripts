#!/usr/bin/python3

import subprocess

'''
shell=False for dry-run
'''
def run(cmd, shell=True):
    print("> ", cmd)
    if shell:
        subprocess.run(cmd, shell=True)

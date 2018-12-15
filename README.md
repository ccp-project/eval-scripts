Reproduce Our Results
=====================

This repository contains a collection of scripts used to run the experiemnts and generate the figures in
our [SIGCOMM 2018 paper](https://akshayn.xyz/res/ccp-sigcomm18.pdf): Restructuring Endpoint Congestion Control.

To make the process of reproducing our results easier, this repository contains
a Vagrantfile that tells Vagrant how to setup a machine running the proper
version of Linux with all of the proper dependencies. Simply install
[Vagrant](https://www.vagrantup.com) and then run `vagrant up`. This will
create a new Linux vm with this current directory (eval-scripts/) linked as `/ccp`
inside the vm. You can access the vm by running `vagrant ssh`.

If you already have a Linux machine or VM you can simply checkout this
repository and run the `ccp-system-setup.sh`. All of our experiments were run on
a machine with Ubuntu 17.10 (Linux 4.13). Other kernel versions should work, but
if you run into any issues, try changing your kernel to 4.13 or using our
Vagrant setup.

Once you have a machine setup, simply running `make` inside this directory (or `/ccp`
inside the Vagrant vm) should build all of the necessary components. 

Below is a list of all figures in the paper and the commands necessary to
reproduce them:

## Figure 3: BBR Example

1. Load ccp-kernel: `cd ccp-kernel && sudo ./ccp_kernel_load ipc=0`
2. Start BBR: `cd bbr && sudo ./target/release/bbr --ipc=netlink`
3. Start an iperf server: `iperf -s -p 5000`
4. Start an iperf client with ccp inside mahimahi and with logging:
`mm-delay 10 mm-link --cbr 48M 48M --uplink-queue="droptail" --downlink-queue="droptail" --uplink-queue-args="packets=160" --downlink-queue-args="packets=160" --log=bbr.log iperf -c $MAHIMAHI_BASE -p 5000 -t 30 -i 1 -Z ccp`
5. Graph the result: `mm-graph mahimahi.log 20`

## Figure 7: Aggregation

This script is not currently available. Please contact us for further information.

## Figure 8: Write-once run-anywhere

This script is not currently available. Please contact us for further information.

## Figure 10: Throughput/Delay Fidelity 

`python3 ./scripts/run-fidelity-exp.py --outdir fidelity --duration 60 --alg cubic --alg reno --scenario fixed --scenario cell --scenario drop --ipcs netlink --kernel --iters 20`

# Figure 9: Cubic Example

Pick one run for cubic for each of the above and run
`./plot/cwnd-evo-single.r <args>`

## Figure 11: FCT Fidelity

`python3 fct_scripts/fct_exp.py`

## Figure 12: IPC Latency

`make ipc100k/ipc.pdf` 

## Figure 13: Scalability/Overheads

`./scripts/run-scalabbility-exp.py`

## Figure 14: Low-rtt, high bandwidth ns-2 simulation

This script is not currently available. Please contact us for further information.

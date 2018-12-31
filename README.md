Reproduce Our Results
=====================

This repository contains a collection of scripts used to run the experiemnts and generate the figures in
our [SIGCOMM 2018 paper](https://akshayn.xyz/res/ccp-sigcomm18.pdf): Restructuring Endpoint Congestion Control.

To make the process of reproducing our results easier, this repository contains
a Vagrantfile that tells Vagrant how to setup a machine running the proper
version of Linux with all of the proper dependencies. Simply install
[Vagrant](https://www.vagrantup.com) and then run `vagrant up`. This will
create a new Linux VM with this directory (eval-scripts/) linked as `/ccp`
inside the VM. You can access the VM by running `vagrant ssh`.

If you already have a Linux machine or VM and you do not wish to use Vagrant you can simply clone this
repository and run the `ccp-system-setup.sh`. All of our experiments were run on
a machine with Ubuntu 17.10 (Linux 4.13). We rely on tcpprobe for congestion window instrumentation, which was removed in the latest Ubuntu LTS release (18.04 -> kernel 4.15). Therefore unfortunately we cannot support these scripts on newer kernels.

Once you have a machine setup, simply running `make` inside this directory (or `/ccp`
inside the Vagrant VM) should build all of the necessary components. 

Below is a list of all figures in the paper and the commands necessary to run the corresponding experiment.

## Figure 3: BBR Example

1. Load ccp-kernel: `cd ccp-kernel && sudo ./ccp_kernel_load ipc=0`
2. Start BBR: `cd bbr && sudo ./target/release/bbr --ipc=netlink`
3. Start an iperf server: `iperf -s -p 5000`
4. Start an iperf client with ccp inside mahimahi and with logging:
`mm-delay 10 mm-link --cbr 48M 48M --uplink-queue="droptail" --downlink-queue="droptail" --uplink-queue-args="packets=160" --downlink-queue-args="packets=160" --log=bbr.log iperf -c $MAHIMAHI_BASE -p 5000 -t 30 -i 1 -Z ccp`
5. Graph the result: `mm-graph mahimahi.log 20`

This process is automated in the following script.

## Figure 10: Throughput/Delay Fidelity and Figure 9: Cubic Example

See the `fidelity` target in the Makefile and modify to your preference. This script can take quite a while to run, and generates a lot of output, so by default the Makefile target does not run the same experiments as described in the paper.

The relevant arguments to the `run-fidelity-exp.py` script are:
- `--alg=(cubic|reno)` for Cubic and Reno
- `--scenario=(fixed|cell|drop)` for the three scenarios described in Section 7.1.1 of the paper
- `--iters` for the number of iterations to run each experiment. As Section 7.1.1 describes, we use a value of 20. However, with this value the `*-*-cwndevo.pdf` graphs become quite large in size: you may have to modify the scripts (perhaps by modifying the sampling on line 105 of run-fidelity-exp.py) to view the results efficiently.

For Figure 9, pick one run for cubic for each of the above and run
`./plot/cwnd-evo-single.r fidelity/cwndevo-subsampled.log cubic fixed <ccp_iteration> <kernel_iteration> <output_file> light`

## Figure 12: IPC Latency

`make ipc` 

## Figure 11: FCT Fidelity

`python3 fct_scripts/fct_exp.py`

## Figure 13: Scalability/Overheads

`./scripts/run-scalability-exp.py`

# Unsupported Figures

The experiments corresponding to Figures 7, 8, and 14 require significant setup external to CCP. As a result we do not currently support them. 
Please contact us for further information.

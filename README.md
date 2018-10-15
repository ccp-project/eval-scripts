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

## Figure 3

TODO 

## Figure 5

TODO

## Figure 7

TODO 

## Figure 8

TODO 

## Figure 9

`python3 ./scripts/run-fidelity-exp.py --outdir fidelity --duration 60 --alg cubic --scenario fixed --ipcs netlink --kernel --iters 1`

## Figure 1

TODO 

## Figure 11

TODO 

## Figure 12

TODO 

## Figure 13

TODO 

## Figure 14

TODO 


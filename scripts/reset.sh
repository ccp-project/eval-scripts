#!/bin/bash

# reset everything
sudo killall -9 iperf
sudo ./ccp-kernel/ccp_kernel_unload
sudo modprobe -r tcp_probe

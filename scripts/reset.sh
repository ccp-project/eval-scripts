#!/bin/bash

# reset everything
sudo pkill -9 iperf
sudo ./ccp-kernel/ccp_kernel_unload
sudo modprobe -r tcp_probe

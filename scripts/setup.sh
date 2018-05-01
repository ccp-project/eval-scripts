#!/bin/bash

# reset everything
sudo killall -9 iperf
sudo rmmod ccp

# don't need to be un-done
sudo modprobe tcp_bbr
sudo modprobe tcp_probe
sudo sysctl -w net.ipv4.ip_forward=1

cd portus && make && cd ..
cd ccp-kernel && make && cd ..

ulimit -Sn 8192
sudo insmod ./ccp-kernel/ccp.ko
sudo sysctl -w net.ipv4.tcp_allowed_congestion_control="cubic reno bbr ccp"

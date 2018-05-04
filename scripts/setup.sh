#!/bin/bash

# reset everything
sudo killall -9 iperf
sudo rmmod ccp
sudo modprobe -r tcp_probe

# don't need to be un-done
sudo modprobe tcp_bbr
sudo modprobe tcp_probe port=4242
sudo sysctl -w net.ipv4.ip_forward=1

echo "---Build portus---"
cd portus && make && cd ..
echo "---Build ccp_copa---"
cd ccp_copa && cargo build && cd ..
echo "---Build ccp-kernel---"
cd ccp-kernel && make && cd ..

ulimit -Sn 8192
sudo insmod ./ccp-kernel/ccp.ko
sudo sysctl -w net.ipv4.tcp_allowed_congestion_control="cubic reno bbr ccp"

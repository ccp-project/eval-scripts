#!/bin/bash

sudo modprobe tcp_bbr
sudo modprobe tcp_probe
sudo sysctl -w net.ipv4.ip_forward=1

cd portus && make && cd ..
cd ccp-kernel && make && cd ..

sudo insmod ./ccp-kernel/ccp.ko
sudo sysctl -w net.ipv4.tcp_allowed_congestion_control="cubic reno bbr ccp"

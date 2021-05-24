#!/bin/bash
sudo trace-cmd record -a -o "./$1/$2-trace-tcpprobe.dat" --date -e tcp:tcp_probe -- iperf -c $MAHIMAHI_BASE -p 4242 -Z $3 -t $4 -i 1 > "./$1/$2-iperf.log"
sleep 2

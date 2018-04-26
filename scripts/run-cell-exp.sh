#!/bin/bash

echo 'cell' $2 $3 $4
sudo dd if=/dev/null of=/proc/net/tcpprobe 2> /dev/null
sudo dd if=/proc/net/tcpprobe of="./$1/$3-cell-tmp.log" 2> /dev/null &
mm-delay 10 mm-link ./mm-traces/Verizon-LTE-short.up ./mm-traces/Verizon-LTE-short.down --uplink-queue=droptail --downlink-queue=droptail --uplink-queue-args="packets=100" --downlink-queue-args="packets=100" --uplink-log="./$1/$3-cell-mahimahi.log" -- ./scripts/run-iperf.sh $1 $2 $3 $4 cell
sudo killall dd 2> /dev/null
grep ":4242" "./$1/$3-cell-tmp.log" > "./$1/$3-cell-tcpprobe.log"
rm -f "./$1/$3-cell-tmp.log"
mm-graph ./$1/$3-cell-mahimahi.log 30 > ./$1/$3-cell-mahimahi.eps 2> ./$1/$3-cell-mmgraph.log

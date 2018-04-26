#!/bin/bash

echo 'fixed' $2 $3 $4
sudo dd if=/dev/null of=/proc/net/tcpprobe 2> /dev/null
sudo dd if=/proc/net/tcpprobe of="./$1/$3-fixed-tmp.log" 2> /dev/null &
mm-delay 10 mm-link ./mm-traces/bw96.mahi ./mm-traces/bw96.mahi --uplink-queue=droptail --downlink-queue=droptail --uplink-queue-args="packets=320" --downlink-queue-args="packets=320" --uplink-log="./$1/$3-fixed-mahimahi.log" -- ./scripts/run-iperf.sh $1 $2 $3 $4 fixed
sudo killall dd 2> /dev/null
grep ":4242" "./$1/$3-fixed-tmp.log" > "./$1/$3-fixed-tcpprobe.log"
rm -f "./$1/$3-fixed-tmp.log"
mm-graph ./$1/$3-fixed-mahimahi.log 30 > ./$1/$3-fixed-mahimahi.eps 2> ./$1/$3-cell-mmgraph.log

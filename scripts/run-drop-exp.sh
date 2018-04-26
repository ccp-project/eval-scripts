#!/bin/bash

echo 'drop' $2 $3 $4
sudo dd if=/dev/null of=/proc/net/tcpprobe 2> /dev/null
sudo dd if=/proc/net/tcpprobe of="./$1/$3-drop-tmp.log" 2> /dev/null &
mm-delay 10 mm-link ./mm-traces/bw96.mahi ./mm-traces/bw96.mahi --uplink-log="./$1/$3-drop-mahimahi.log" mm-loss uplink 0.0001  -- ./scripts/run-iperf.sh $1 $2 $3 $4 drop
sudo killall dd 2> /dev/null
grep ":4242" "./$1/$3-drop-tmp.log" > "./$1/$3-drop-tcpprobe.log"
rm -f "./$1/$3-drop-tmp.log"
mm-graph ./$1/$3-drop-mahimahi.log 30 > ./$1/$3-drop-mahimahi.eps 2> ./$1/$3-cell-mmgraph.log

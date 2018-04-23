#!/bin/bash
iperf -c 100.64.0.1 -p 4242 -Z $2 -t $4 -i 1 > "./$1/$3-$5-iperf.log"
sleep 2

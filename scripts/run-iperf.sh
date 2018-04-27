#!/bin/bash
iperf -c 100.64.0.1 -p 4242 -Z $3 -t $4 -i 1 > "./$1/$2-iperf.log"
sleep 2

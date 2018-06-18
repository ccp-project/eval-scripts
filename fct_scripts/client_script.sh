#!/bin/bash

expConfig=$1
logName=$2

sleep 10
/home/ubuntu/ccp-eval/fct_scripts/empirical-traffic-gen/bin/client -c $expConfig -l $logName -s 123

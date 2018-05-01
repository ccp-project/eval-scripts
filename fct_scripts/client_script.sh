#!/bin/bash

expConfig=$1
logName=$2

sleep 10
/empirical-traffic-gen/bin/client -c $expConfig -l $logName -s 123

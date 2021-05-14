#!/bin/bash

expConfig=$1
logName=$2
dir=$(dirname "$0")

sleep 10
$dir/empirical-traffic-gen/bin/client -c $expConfig -l $logName -s 123

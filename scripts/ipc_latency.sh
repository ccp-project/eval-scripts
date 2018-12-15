#!/bin/bash

./scripts/reset.sh

mkdir $1

if [ ! -f ./$1/ipc.log ]; 
then
    echo "---Build portus---"
    cd portus && cargo build --release --all > ../$1/build_tmp 2> ../$1/build_tmp
    if [ $? -ne 0 ]
    then
        cat ../$1/build_tmp
    else
        rm ../$1/build_tmp
        sudo ./target/release/ipc_latency -i 100000 --impl nl --impl unix --impl kp > ../$1/ipc.log
        cd ..
    fi
else
    echo "../$1/ipc.log done"
fi

./plot/ipc_latency.r ./$1/ipc.log ./$1/ipc.pdf

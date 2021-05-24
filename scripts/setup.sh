#!/bin/bash

./scripts/reset.sh

# don't need to be un-done
sudo modprobe tcp_bbr
sudo sysctl -w net.ipv4.ip_forward=1

echo "---Build cubic, reno---"
cd generic-cong-avoid && cargo build --release > ../$2/build_tmp 2> ../$2/build_tmp
if [ $? -ne 0 ]
then
    cat ../$2/build_tmp
    exit 1
else
    #rm $2/build_tmp
    cd ..
fi
echo "---Build ccp_copa---"
cd ccp_copa && cargo build --release > ../$2/build_tmp 2> ../$2/build_tmp
if [ $? -ne 0 ]
then
    cat ../$2/build_tmp
    exit 1
else
    #rm $2/build_tmp
    cd ..
fi
echo "---Build ccp-kernel---"
cd ccp-kernel && make > ../$2/build_tmp 2> ../$2/build_tmp
if [ $? -ne 0 ]
then
    cat ../$2/build_tmp
    exit 1
else
    #rm $2/build_tmp
    echo "---Load ccp-kernel---"
    ulimit -Sn 8192
    echo $PWD
    echo $1
    sudo ./ccp_kernel_load $1
    cd ..
fi


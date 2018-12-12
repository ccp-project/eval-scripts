all: ccp-kernel/ccp.ko mahimahi cubic reno

########################################
# check that all the submodules are here
########################################

mahimahi/src/frontend/delayshell.cc ccp-kernel/libccp/ccp.h:
	$(error Did you forget to git submodule update --init --recursive ?)

#########################
# compile all the things!
#########################

clean:
	$(MAKE) -C ccp-kernel clean
	$(MAKE) -C mahimahi clean

ccp-kernel/ccp.ko: ccp-kernel/libccp/ccp.h
	$(MAKE) -C ccp-kernel

# Mahimahi

mahimahi/configure:
	cd mahimahi && autoreconf -i

mahimahi/Makefile: mahimahi/configure
	cd mahimahi && ./configure

mahimahi/src/frontend/mm-delay: mahimahi/src/frontend/delayshell.cc mahimahi/Makefile
	$(MAKE) -C mahimahi

mahimahi: mahimahi/src/frontend/mm-delay
	sudo $(MAKE) -C mahimahi install

# CCP algs

./generic-cong-avoid/target/debug/reno ./generic-cong-avoid/target/debug/cubic:
	cd generic-cong-avoid && cargo build

cubic: ./generic-cong-avoid/target/debug/cubic
reno: ./generic-cong-avoid/target/debug/reno 

# Not required for eval, run make python_bindings to install portus as a python lib
#python_bindings:
#	cd portus/python && sudo env PATH=$(PATH) python3 setup.py install

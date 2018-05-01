import math
import sys
import time
import subprocess as sh

tcp_algs = ["ccp"]
num_experiments = 10
NUM_SERVERS = 50
client_config_params = {"load": "72Mbps", "fanout": "1 100", "num_reqs": "10000", "req_size_dist": "CAIDA_CDF"}
server_binary = "./empirical-traffic-gen/bin/server"
client_binary = "./empirical-traffic-gen/bin/client"
tmp_file = "a.txt"
NUM_EXPTS = 10

# should be a multiple of 8
def make_mahimahi_linkfile(name, mbps):
    num_ones = int(mbps/12)
    f = open(name, "w")
    for i in range(num_ones):
        f.write("{}\n".format("1"))
    return name

def kill_processes():
    awk_command = "awk '{printf $2;printf \" \";}'"
    sh.run("ps aux | grep {} | {} > {}".format(server_binary, awk_command, tmp_file), shell=True)
    with open(tmp_file) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for process in content:
        sh.Popen("sudo kill -9 {}".format(process), shell=True)
    sh.run("killall {}".format(client_binary), shell=True)
    sh.run("rm {}".format(tmp_file), shell=True)

# for server - spawn process to listen at specific port
def port(server_num):
    return str(5000 + server_num)

def write_client_config(config_filename, params):
    f = open(config_filename, "w")
    for i in range(NUM_SERVERS):
        f.write("server 100.64.0.1 {}\n".format(port(i)))
    for key in params:
        f.write("{} {}\n".format(key, params[key]))

def spawn_servers(alg):
    processes = []
    for i in range(NUM_SERVERS):
        #processes.append(sh.Popen[server_binary, "-t", alg, "-p", port(i)], shell=True)
        processes.append(sh.Popen(["{} -t {} -p {} >> /dev/null".format(server_binary, alg, port(i))], shell=True))

    return processes

def spawn_clients(mahimahi_file, exp_config, logname):
    # run mahimahi, set fq on the interface & run the client file
    mahimahi_command = "mm-delay 25 mm-link --downlink-queue=droptail --downlink-queue-args=\'packets=800\' {} {} ./client_script.sh {} {}".format(mahimahi_file, mahimahi_file, exp_config, logname)
    # command to set fq on the interface
    find_mahimahi = "sleep 1; x=$(ifconfig | grep delay | awk '{print $1}'| sed 's/://g') && sudo tc qdisc add dev $x root fq && echo $x"
    processes = []
    for command in [mahimahi_command, find_mahimahi]:
        processes.append(sh.Popen(command, shell=True))
    return processes

def get_log(logname):
    # TODO: access logfile
    sh.run("awk '{print $1,$2}' {}_flows.out | egrep -o '[0-9]+' | paste -d ' - - > {}.fct".format(logname, logname))

def setup_ccp():
    # kill any current ccp processes
    sh.run("sudo killall reno", shell=True)

    # run portus
    sh.Popen(["sudo ./../portus/ccp_generic_cong_avoid/target/debug/reno --ipc netlink"], shell=True)
def main():
    client_config_name = "clientConfig"
    kill_processes()
    write_client_config(client_config_name, client_config_params)
    mahimahi_file = make_mahimahi_linkfile("linkfile-96.mahi", 96)

    for it in range((NUM_EXPTS)):
        for alg in tcp_algs:
            algname = alg + '-ccp' if 'ccp' in alg else alg
            # TODO: if ccp, kill all current ccp processes, start ccp
            if 'ccp' in alg:
                setup_ccp()
            logname = "{}-{}-{}-{}-{}".format(algname, it, client_config_params['load'], client_config_params['num_reqs'], client_config_params['req_size_dist'])
            print("Starting experiment for {}".format(logname))

            processes = spawn_servers(alg)
            processes.extend(spawn_clients(mahimahi_file, client_config_name, logname))

            for proc in processes:
                proc.wait()
            get_log(logname)
    


if __name__ == "__main__":
    main()

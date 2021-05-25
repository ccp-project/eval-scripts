import math
import sys
import time
import subprocess as sh

tcp_algs = ["ccp", "reno"]
num_experiments = 1
NUM_SERVERS = 50
CAIDA_FILE =  "./fct_scripts/empirical-traffic-gen/CAIDA_CDF"
client_config_params = {"load": "72Mbps", "fanout": "1 100", "num_reqs": "100000", "req_size_dist": CAIDA_FILE}
server_binary = "./fct_scripts/empirical-traffic-gen/bin/server"
client_binary = "./fct_scripts/empirical-traffic-gen/bin/client"
tmp_file = "a.txt"
NUM_EXPTS = 1
PLOTTING_SCRIPT = "./plot/fct.r"


# should be a multiple of 8
def make_mahimahi_linkfile(name, mbps):
    num_ones = int(mbps/12)
    f = open(name, "w")
    for i in range(num_ones):
        f.write("{}\n".format("1"))
    return name

def kill_processes():
    awk_command = "awk '{printf $2;printf \" \";}'"
    sh.check_output("ps aux | grep {} | {} > {}".format(server_binary, awk_command, tmp_file), shell=True)
    with open(tmp_file) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for process in content:
        sh.Popen("sudo kill -9 {}".format(process), shell=True)
    sh.check_output("rm {}".format(tmp_file), shell=True)
    try:
        sh.check_output("killall {}".format(client_binary), shell=True)
        sh.check_output("sudo pkill reno", shell=True)
    except:
        return

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
    print(f"==> Starting empirical traffic gen server alg={alg} path={server_binary} num={NUM_SERVERS}")
    for i in range(NUM_SERVERS):
        #processes.append(sh.Popen[server_binary, "-t", alg, "-p", port(i)], shell=True)
        sh.Popen(["{} -t {} -p {} >> /dev/null".format(server_binary, alg, port(i))], shell=True)

def spawn_clients(mahimahi_file, exp_config, logname):
    # run mahimahi, set fq on the interface & run the client file
    mahimahi_command = "mm-delay 25 mm-link {} {} --downlink-queue=droptail --downlink-queue-args=\'packets=800\' ./fct_scripts/client_script.sh {} {}".format(mahimahi_file, mahimahi_file, exp_config, logname)
    # command to set fq on the interface
    find_mahimahi = "sleep 1; x=$(ifconfig | grep delay | awk '{print $1}'| sed 's/://g') && sudo tc qdisc add dev $x root fq && echo $x"
    processes = []
    for command in [mahimahi_command, find_mahimahi]:
        processes.append(sh.Popen(command, shell=True))
    return processes

def get_log(logname, impl):
    # TODO: access logfile
    awk_command = "awk '{{print $1,$2}}' {}_flows.out | egrep -o '[0-9]+' | paste -d ' ' - - | awk '{{print $1,$2,\"{}\"}}' > {}.fct".format(logname, impl, logname)
    sh.check_output(awk_command, shell=True)

def setup_ccp():
    try:
        sh.check_output("sudo pkill reno", shell=True)
    except:
        # run portus
        pass
    print("==> Start CCP Reno")
    sh.Popen(["sudo ./generic-cong-avoid/target/release/reno --ipc netlink 2>&1 > ccp.log"], shell=True)


def get_logname(algname, it):
    return "{}-{}-{}-{}-{}".format(algname, it, client_config_params['load'], client_config_params['num_reqs'], "CAIDA_CDF")

def make_graph_file(NUM_EXPTS, outfile):
    sh.check_output("echo 'Size FctUs Impl' > {}".format(outfile), shell=True)
    for it in range((NUM_EXPTS)):
        for alg in tcp_algs:
            algname = 'reno-{}'.format(alg) if 'ccp' in alg else alg
            logname = get_logname(algname, it)
            sh.check_output("cat {}.fct >> {}".format(logname, outfile), shell=True)
            sh.check_output("rm {}_flows.out".format(logname), shell=True)
            sh.check_output("rm {}_reqs.out".format(logname), shell=True)
            sh.check_output("rm {}.fct".format(logname), shell=True)


def main():
    client_config_name = "clientConfig"
    outfile = "fct.log"
    kill_processes()
    write_client_config(client_config_name, client_config_params)
    mahimahi_file = make_mahimahi_linkfile("linkfile-96.mahi", 96)

    for it in range((NUM_EXPTS)):
        for alg in tcp_algs:
            algname = 'reno-{}'.format(alg) if 'ccp' in alg else alg
            # TODO: if ccp, kill all current ccp processes, start ccp
            if 'ccp' in alg:
                setup_ccp()
            logname = get_logname(algname, it)
            print("=> Starting experiment for {}".format(logname))

            spawn_servers(alg)
            processes = spawn_clients(mahimahi_file, client_config_name, logname)

            for proc in processes:
                proc.wait()

            kill_processes()
            if 'ccp' in alg:
                get_log(logname, "ccp_plain")
            else:
                get_log(logname, "kernel_plain")

    make_graph_file(NUM_EXPTS, outfile)
    sh.check_output("{} {}".format(PLOTTING_SCRIPT, outfile), shell=True)

    # shell = true
    sh.check_output("rm {}".format(client_config_name), shell=True)
    sh.check_output("rm ccp.log", shell=True)
    sh.check_output("rm {}".format(outfile), shell=True)

if __name__ == "__main__":
    main()

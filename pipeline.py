import sys
import subprocess
import time
from os import listdir
from os.path import isfile, join

# This specific pipeline is for the cnc-bot communication

# required main pcap file
if len(sys.argv) == 1:
    print("**main pcap file is required")
    exit()

main_pcap_file = sys.argv[1]
filtered_pcap_file = "{}{}.pcap".format(main_pcap_file.split('.')[0],'_f')
temp_dir = 'temp'

def log(msg):
    print("[{}] {}".format('PL', msg))


def clear_temp_dir():
    proc = subprocess.Popen(['rm', 'rf', 'temp'])
    proc.wait()
    proc2 = subprocess.Popen(['mkdir', 'temp'])
    proc2.wait()


def get_files_in_temp_dir():
    return [f for f in listdir(temp_dir) if isfile(join(temp_dir, f))]

def run_zeek(pcapfile, brofile, logfile):
    command = ['zeek', '-C', '-r', pcapfile, brofile, '>', logfile]
    proc = subprocess.Popen(command)
    proc.wait()



def filter_pcap():
    _pcap_filter = 'ip.addr==134.197.42.83&&tcp&&!http&&!ssh&&tcp.port==20001'
    log("using pcap file '{}' and output filtered file to '{}' using filter '{}'".format(main_pcap_file, filtered_pcap_file,_pcap_filter))
    proc = subprocess.Popen(['tshark', '-r', main_pcap_file, '-R', 
                                _pcap_filter, '-w', filtered_pcap_file, '-2'])
    proc.wait()



def split_filtered_file():
    clear_temp_dir()
    command = ['./PcapSplitter', '-f', filtered_pcap_file, '-o', temp_dir, '-m', 'connection'] 
    log("Splitting the '{}' into connection pcap files".format(filtered_pcap_file))
    proc = subprocess.Popen(command)
    proc.wait()


def run_zeek_on_splitted_files():
    files = get_files_in_temp_dir()
    log("There are {} files corresponding to {} connections in the filtered file".format(len(files), len(files)))
    for file in files:
        run_zeek("{}/{}".format(temp_dir, file),'processcnc.bro', "{}/{}.csv".format(temp_dir,file.split(".")[0]))

filter_pcap();
split_filtered_file();
run_zeek_on_splitted_files();

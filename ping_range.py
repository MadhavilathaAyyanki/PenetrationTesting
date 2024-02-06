# Importing necessary libraries
import ipaddress
import socket
import os
import struct
import select
import argparse
import time

# creating a function "generate_checksum" to caluclate the value of checksum
def generate_checksum(info):
    #Initialising the count as 0
    count = 0
    # Iterating through 2 bytes of info at a time
    for i in range(0, len(info), 2):
        # Adding 2 adjacent bytes to 16-bit value and adding it to the count and making sure that count remains within 32 bits
        val = info[i + 1] * 256 + info[i]
        count += val
        count &= 0xffffffff
    # Adding high 16 bits with low 16 bits by adding carry from previous addition and taking 1's complement of low 16 bits
    count = (count >> 16) + (count & 0xffff)
    count += (count >> 16)
    value = ~count & 0xffff
    value = (value & 0xff00) >> 8 | (value & 0x00ff) << 8
    # Returning caluclated checksum value
    return value

# creating a function "ping" to send ICMP Echo ping request 
def ping(ip):
    # Creating socket 
    ms = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    # Masking current process id to 16 bits
    proc_id = os.getpid() & 0xFFFF
    # Defining ICMP header format
    header_format = "bbHHh"
    # Defining ICMP header values
    header_values= (8, 0, 0, proc_id, 1)
    # Using struct function to pack header and payload 
    header = struct.pack(header_format, *header_values)
    info = struct.pack("d", time.time())
    # calcuclating checksum value
    ch_sum = generate_checksum(header + info)
    # updating header values with caluclated checksum
    header_values_with_ch_sum = (8, 0, socket.htons(ch_sum), proc_id, 1)
    # using struct to pack header with updated checksum
    header = struct.pack(header_format, *header_values_with_ch_sum)
    # Sending ICMP echo ping request to target IP and returning socket
    ms.sendto(header + info, (ip, 1))
    return ms

# creating a function "response" to receive ICMP Echo ping response
def response(ms, session_expire):
    # setting duration for response
    duration = session_expire
    # Wait as long as duration time to check for response
    while duration > 0:
        started_select = time.time()
        ready = select.select([ms], [], [], duration)
        if ready[0] == []:
            return False
        # receive header value from response and unpack header fields
        icmp_header = ms.recvfrom(1024)[0][20:28]
        icmp_header_fields = struct.unpack("bbHHh", icmp_header)
        type = icmp_header_fields[0]
        code = icmp_header_fields[1]
        checksum = icmp_header_fields[2]
        id = icmp_header_fields[3]
        sequence = icmp_header_fields[4]
        # Check for ICMP echo response if it matches with process id return true  
        if type == 0 and id == os.getpid() & 0xFFFF:
            return True
        # If no response is received within duration return false
        duration -= (time.time() - started_select)
    return False

# creating a function "find_active_hosts" to check for active hosts within subnet 
def find_active_hosts(subnet):
     # Converting subnet into Network objects
    network = ipaddress.ip_network(subnet, strict=False)
    # returning list of hosts in the network that responds to ping by iterating through hosts
    return [str(ip) for ip in network.hosts() if scan(str(ip))]

# creating a function main to print active hosts within network
def main(network_range):
    #calling find_active_hosts function to get active hosts
    active = find_active_hosts(network_range)
    # check for active hosts, if any found print list of IP address that are active
    if active:
        print("Found Active IP's:")
        print("\n".join(active))
    # If no hosts are found active print no live IP's in network
    else:
        print("There are no Live IP's available in this network")

# Creating a function "scan" to perform ping for a target host IP 
def scan(host, session_expire=1):
    # calling ping function to send ICMP request and generate a socket connection
    ms = ping(host)
    # calling response function to wait for ICMP response
    output = response(ms, session_expire)
    # closing socket connection
    ms.close()
    # Return the output of scan as True if host responds or False if host does not respond
    return output

# creating a function "parse_arguments" that takes an parser object,argument for network range and parse them
def parse_arguments():
    # Referred from https://docs.python.org/3/library/argparse.html
    # creating an parser object
    parser = argparse.ArgumentParser(description='Network Ping Sweep')
    # Creating an argument for network range
    parser.add_argument('network_range', type=str, help='Scan Network for live IP')
    # parse the arguments and return the value 
    args = parser.parse_args()
    return args.network_range

# Main fucntion to call parse_arguments and main functions
if __name__ == "__main__":
    network_range = parse_arguments()
    main(network_range)
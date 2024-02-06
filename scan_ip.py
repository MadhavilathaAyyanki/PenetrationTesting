# Importing necessary libraries
import socket
import argparse

# creating a function "ports_tcp" with two arguments
def ports_tcp(ip, str_ports):
    # Initialising an empty list to store ports that were open
    ports_open = []
    # Initialising an empty list to store parsed ports
    ports = []

    # Adding each port to the parsed empty list by splitting port string
    try:
        for value in str_ports.split(','):
            if '-' in value:
                #Split the range and add all ports to the list
                scale = [map(int, value.split('-'))]
                ports.extend(range(scale[0], scale[1] + 1))
            else:
                # Add the ports to empty parsed list
                ports.append(int(value))

    # To check if there were any errors in converting ports into integers
    except ValueError:
        print("Error: Port format invalid.")
        exit(1)
    # Throws an error if no ports are specified
    if not ports:
        print("Error: Ports not specified.")
        exit(1)
    
    # creating a for loop to create a socket connection for each port
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Creating connection to port with timeout of 1 second
                output = sock.connect_ex((ip, port))
                sock.settimeout(1)
                # If connection is successful,then it is added to empty list ports_open
                if output == 0:
                    ports_open.append(port)
        # Continue to next available port if there is any socket connection error
        except socket.error:
            pass
    
    # Check for any open ports, if found then print TCP ports found
    if not ports_open:
        print(f"No TCP ports found for {ip}.")
        
    else:
        print(f"TCP ports open on {ip}:")
        for port in ports_open:
            print(f"Port {port} is open.")

# Main function that takes parser object,argument for IP range,ports and parse them
if __name__ == "__main__":
    # Referred from https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(description='check TCP ports for specific IP.')
    parser.add_argument('ip', help='IP address for scanning')
    parser.add_argument('--ports', help='scan ports(list or range, separated by commas)')
    args = parser.parse_args()
    # Calling ports_tcp function
    ports_tcp(args.ip, args.ports)
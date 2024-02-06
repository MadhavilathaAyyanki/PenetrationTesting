# Importing required libraries
import socket
import argparse

# Creating a function "fetch_service" taking port as parameter and returning associated service
def fetch_service(port):

    # Creating a dictionary "services" that maps port numbers with associated services
    services = { 
        80: "HTTP",
        21: "FTP", 
    }

    return services.get(port,"Unspecified service")

# Creating a function "file" with parser object, and ip as arguments and parse them
def file():
    # Referred from https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(description='scan services for open ports on particular IP.')
    parser.add_argument('ip', help='scan ip address')
    return parser.parse_args()

# Creating a function "service_scan" that takes 2 arguments ip 
def service_scan(ip):
    # Creating an empty list to store the output of port scanning 
    output = []
    # Creating a list of ports to scan for each ip
    ports = [21, 80]
    # Initialising i as 0
    i = 0

    # Creating a while loop to iterate through the range of ports 
    while i < len(ports):
        try:
            # Creating socket connection with timeout of 1 second
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                result = sock.connect_ex((ip, ports[i]))
                sock.settimeout(1)
                
                # If connection is successful then append ports and service in tuple to the output empty list
                if not result:
                    output.append((ports[i], fetch_service(ports[i])))
        # Check for any socket connection errors and continue the loop
        except socket.error:
            pass
        i += 1
    return output

# Main function to call the defined functions
if __name__ == "__main__":
    # Calling function "file"
    args = file()
    # Fetch IP from parsed arguments 
    ip = args.ip
    
    # Calling "service_scan" function to scan available ports for specific IP address
    output = service_scan(ip)
    
    # If the list is empty then return no services found
    if not output:
        print(f"Found no services on open ports for {ip}.")
    # Iterate through tuple and return specific service for availale ports for particular IP address
    else:
        print(f"Running services on open ports for {ip}:")
        for port, nm_service in output:
            print(f"Port {port} ({nm_service}) is open.")

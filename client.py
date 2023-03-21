import socket
import os

server_addr = "127.0.0.1"
service_discovery_port = 30000
file_sharing_port = 30001
service_discovery_timeout = 10.0
local_dir = "C:/Users/johnh/Desktop/Projects"

# Create TCP socket
tcp_sock = None

# Prompt user to enter a command
while True:
    command = input("\nEnter a command:\nSCAN\nCONNECT <IP address> <port>\nLLIST\nRLIST\nPUT <filename>\nGET <filename>\nBYE\n\n")
    if command.upper() == "BYE":
        break

    elif command.upper() == "SCAN":
        # Perform service discovery
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_sock.settimeout(service_discovery_timeout)
        udp_sock.sendto("SERVICE DISCOVERY".encode(), (server_addr, service_discovery_port))
        try:
            while True:
                data, (server_ip, _) = udp_sock.recvfrom(1024)
                message = data.decode()
                if message.startswith("SERVICE DISCOVERY RESPONSE"):
                    _, service_name = message.split(' ', 1)
                    print(f"{server_ip}:{file_sharing_port} - {service_name}")
                    break
        except socket.timeout:
            print("No service found.")
        udp_sock.close()

    elif command.startswith("CONNECT "):
        args = command.split()
        if len(args) != 3:
            print("Invalid command.")
            continue
        # Connect to server
        server_ip = args[1]
        server_port = int(args[2])
        if tcp_sock:
            print("Closing existing connection.")
            tcp_sock.close()
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.connect((server_ip, server_port))
        print(f"Connected to file sharing service at IP address/port {server_ip}, {server_port}")

    elif command.upper() == "LLIST":
        # Output a directory listing of the local file sharing directory
        for filename in os.listdir(local_dir):
            print(filename)

    elif command.upper() == "RLIST":
        request = f"RLIST"
        tcp_sock.sendall(request.encode()) #send GET command
        response = tcp_sock.recv(999999999) #change this to max number of bytes
        print(response.decode())

    elif command.startswith("GET "):
        filename = command[4:]
        request = f"DOWNLOAD {filename}"
        tcp_sock.sendall(request.encode()) #send GET command
        # receive data 
        response = tcp_sock.recv(999999999) #change this to max number of bytes
        if response.startswith(b"File"):
            print(response.decode())
        else: #goes here
            with open(filename, 'wb') as f:
                f.write(response)
            print(f"Downloaded {filename}")

    elif command.startswith("PUT "):
        filename = command[4:]
        request = f"PUT {filename}"
        tcp_sock.sendall(request.encode()) #send PUT command
        with open(filename, 'rb') as f:
            file_data = f.read()
            tcp_sock.sendall(file_data)
        print(f"Uploaded {filename}")
        

    else:
        print("Invalid command")

# Close TCP connection
tcp_sock.close()

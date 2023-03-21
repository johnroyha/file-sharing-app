import socket
import os
import select

# Set up server configuration
file_sharing_dir = "C:/Users/johnh/Desktop/FSD"
HOSTNAME = "127.0.0.1"
file_sharing_service_name = "John, Sue, and Zayn's File Sharing Service"
file_sharing_port = 30001
service_discovery_port = 30000

# Set up UDP socket for service discovery
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind((HOSTNAME, service_discovery_port))

# Set up TCP socket for file sharing
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.bind((HOSTNAME, file_sharing_port))
tcp_sock.listen(1)

print(f"Server started. File sharing directory: {file_sharing_dir}")
print(f"Listening for service discovery messages on SDP port {service_discovery_port}")
print(f"Listening for file sharing connections on port {file_sharing_port}")

# Set up list of sockets to monitor
sockets_list = [udp_sock, tcp_sock]

while True:
    # Use select to wait for socket activity
    read_sockets, _, _ = select.select(sockets_list, [], [])
    for sock in read_sockets:
        # Handle UDP broadcast
        if sock == udp_sock:
            data, (client_ip, client_port) = udp_sock.recvfrom(1024)
            message = data.decode()
            if message == "SERVICE DISCOVERY":
                response = file_sharing_service_name.encode()
                udp_sock.sendto(f"SERVICE DISCOVERY RESPONSE {file_sharing_service_name}".encode(), (client_ip, client_port))
        
        # Handle TCP client connection
        elif sock == tcp_sock:
            client_sock, client_addr = tcp_sock.accept()
            print(f"New client connected from {client_addr}")
            
            # Handle client request
            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                message = data.decode()
                
                if message.startswith("RLIST"):
                    files = os.listdir(file_sharing_dir)
                    files_str = '\n'.join(files)
                    client_sock.sendall(files_str.encode('utf-8'))

                # Handle file download request
                elif message.startswith("DOWNLOAD"):
                    filename = message.split()[1]
                    file_path = os.path.join(file_sharing_dir, filename)
                    if os.path.isfile(file_path):
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                            client_sock.sendall(file_data)

                    else:
                        error_message = f"File {filename} not found"
                        client_sock.sendall(error_message.encode())

                # Handle file upload request
                elif message.startswith("PUT"):
                    filename = message.split()[1]
                    file_path = os.path.join(file_sharing_dir, filename)
                    with open(file_path, 'wb') as f:
                        file_data = client_sock.recv(999999999)
                        #exit() #doesn't satisfy q11
                        f.write(file_data)
           
                else:
                    error_message = "Invalid request"
                    client_sock.sendall(error_message.encode())
            
            client_sock.close()
            print(f"Client from {client_addr} disconnected")

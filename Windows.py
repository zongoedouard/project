import socket
import threading

def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break
            
            # Broadcast the received message to all clients
            broadcast(data)
        except Exception as e:
            print(f"Error: {e}")
            break
    
    print(f"Connection from {client_address} closed.")
    client_socket.close()

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except Exception as e:
            print(f"Error broadcasting message: {e}")
            client.close()
            clients.remove(client)

# List to keep track of connected clients
clients = []

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind(("localhost", 8888))


# Start listening for incoming connections
server_socket.listen(5)
print("Server is listening for incoming connections...")

while True:
    # Accept a new connection
    client_socket, client_address = server_socket.accept()
    
    # Add the new client to the list
    clients.append(client_socket)
    
    # Create a new thread to handle the client
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()

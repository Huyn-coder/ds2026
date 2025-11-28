import socket
import os
import time

HOST = '127.0.0.1' 
PORT = 65432       

def send_file(filename):
    if not os.path.exists(filename):
        print("File does not exist!")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
        print(f"Connected to Server {HOST}:{PORT}")

        client_socket.sendall(filename.encode('utf-8')) 
        
        ack = client_socket.recv(1024) 
        if ack.decode() != "ACK":
            print("Server Error!")
            return

        print("Sending file...")
        with open(filename, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break 
                client_socket.sendall(data) 
        
        print("File sent successfully.")

    except ConnectionRefusedError:
        print("Could not connect to Server. Please ensure the Server is running.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    fname = input("Enter filename to send: ")
    send_file(fname)
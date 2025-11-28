import socket
import os

HOST = '127.0.0.1'
PORT = 65432

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.bind((HOST, PORT))
    
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}...")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    with conn:
        filename = conn.recv(1024).decode('utf-8')
        print(f"Preparing to receive file: {filename}")
        
        filename = os.path.basename(filename)
        
        conn.sendall(b"ACK")

        with open(f"received_{filename}", 'wb') as f:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                f.write(data)
        
        print(f"File 'received_{filename}' received successfully")
    
    server_socket.close()

if __name__ == "__main__":
    start_server()
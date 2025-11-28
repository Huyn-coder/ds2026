from xmlrpc.server import SimpleXMLRPCServer
import os

HOST = 'localhost'
PORT = 8000

def save_uploaded_file(filename, binary_data):
    try:
        save_path = f"received_{os.path.basename(filename)}"
        
        with open(save_path, "wb") as handle:
            handle.write(binary_data.data)
            
        print(f"File received: {save_path}")
        return True 
    except Exception as e:
        print(f"Error: {e}")
        return False

def start_server():
    print(f"RPC Server running on http://{HOST}:{PORT}...")
    server = SimpleXMLRPCServer((HOST, PORT), allow_none=True)
    
    server.register_function(save_uploaded_file, "upload_file")
    
    server.serve_forever()

if __name__ == "__main__":
    start_server()
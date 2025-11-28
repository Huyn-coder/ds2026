import xmlrpc.client
import os

SERVER_URL = "http://localhost:8000/"

def send_file(filename):
    if not os.path.exists(filename):
        print("File does not exist!")
        return

    print(f"Connecting to {SERVER_URL}...")
    
    proxy = xmlrpc.client.ServerProxy(SERVER_URL)

    try:
        with open(filename, "rb") as handle:
            binary_data = xmlrpc.client.Binary(handle.read())
            
            print(f"Calling remote function 'upload_file' to send {filename}...")
            
            result = proxy.upload_file(filename, binary_data)
            
            if result:
                print("File sent successfully!")
            else:
                print("File send failed (Server error).")
                
    except ConnectionRefusedError:
        print("Could not connect. Please ensure Server is running.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fname = input("Enter filename to send: ")
    send_file(fname)
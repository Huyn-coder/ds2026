import os
import sys
from mpi4py import MPI

class MPIFileTransfer:
    def __init__(self, filename, chunk_size=1024):
        self.filename = filename
        self.chunk_size = chunk_size
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()

    def sender(self):
        """
        Rank 0: Reads file and sends it to Rank 1.
        """
        print(f"[Sender] Rank {self.rank}: Preparing to send '{self.filename}'...")
        
        try:
            if not os.path.exists(self.filename):
                print(f"[Error] File '{self.filename}' not found.")
                self.comm.send(None, dest=1, tag=0) # Signal error
                return

            file_size = os.path.getsize(self.filename)
            # Send metadata (filename, size)
            self.comm.send({'name': self.filename, 'size': file_size}, dest=1, tag=1)
            print(f"[Sender] Metadata sent. Size: {file_size} bytes.")

            # Send file content in chunks
            with open(self.filename, 'rb') as f:
                bytes_sent = 0
                while True:
                    chunk = f.read(self.chunk_size)
                    if not chunk:
                        break
                    self.comm.send(chunk, dest=1, tag=2)
                    bytes_sent += len(chunk)
            
            # Send EOF signal
            self.comm.send(None, dest=1, tag=2)
            print(f"[Sender] Transfer complete. Total sent: {bytes_sent} bytes.")

        except Exception as e:
            print(f"[Sender] Error: {e}")

    def receiver(self):
        """
        Rank 1: Receives data and writes to a new file.
        """
        print(f"[Receiver] Rank {self.rank}: Waiting for data...")
        
        # Receive metadata
        metadata = self.comm.recv(source=0, tag=1)
        if metadata is None: # Handle error from sender
            print("[Receiver] Transfer aborted by sender.")
            return

        original_name = metadata['name']
        new_filename = f"received_{original_name}"
        total_size = metadata['size']
        print(f"[Receiver] Incoming file: {original_name} ({total_size} bytes). Saving as '{new_filename}'.")

        # Receive data chunks
        with open(new_filename, 'wb') as f:
            bytes_received = 0
            while True:
                chunk = self.comm.recv(source=0, tag=2)
                if chunk is None: # EOF signal
                    break
                f.write(chunk)
                bytes_received += len(chunk)

        print("="*40)
        print("RESULT: FILE TRANSFER SUCCESSFUL")
        print("="*40)
        print(f"Path   : {os.path.abspath(new_filename)}")
        print(f"Size   : {bytes_received} bytes")

    def run(self):
        """
        Executes the MPI job based on Rank.
        """
        if self.size < 2:
            print("[Error] This program requires at least 2 MPI processes (Sender and Receiver).")
            return

        if self.rank == 0:
            self.sender()
        elif self.rank == 1:
            self.receiver()
        else:
            print(f"[Rank {self.rank}] Idle.")

if __name__ == "__main__":
    # Usage: mpiexec -n 2 python mpi_file_transfer.py
    # Ensure 'input_file.txt' exists before running
    job = MPIFileTransfer('input_file.txt')
    job.run()
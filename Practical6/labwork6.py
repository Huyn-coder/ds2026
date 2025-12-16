import os
import time
import sys

class GlusterBenchmark:
    def __init__(self, mount_point):
        self.mount_point = mount_point
        self.small_file_dir = os.path.join(mount_point, "small_files")
        self.large_file_dir = os.path.join(mount_point, "large_files")
        self.ensure_dirs()

    def ensure_dirs(self):
        if not os.path.exists(self.small_file_dir):
            os.makedirs(self.small_file_dir)
        if not os.path.exists(self.large_file_dir):
            os.makedirs(self.large_file_dir)

    def benchmark_small_files(self, num_files=1000):
        print(f"Running Small File Benchmark ({num_files} files)...")
        start_time = time.time()
        
        for i in range(num_files):
            with open(os.path.join(self.small_file_dir, f"file_{i}"), 'w') as f:
                f.write("small_content")
        
        for i in range(num_files):
            with open(os.path.join(self.small_file_dir, f"file_{i}"), 'r') as f:
                _ = f.read()
                
        end_time = time.time()
        duration = end_time - start_time
        ops_per_second = (num_files * 2) / duration
        
        print(f"Result: {ops_per_second:.2f} accesses/second")
        return ops_per_second

    def benchmark_large_file(self, size_mb=512):
        print(f"Running Large File Read Benchmark ({size_mb} MB)...")
        file_path = os.path.join(self.large_file_dir, "test_large.dat")
        
        with open(file_path, 'wb') as f:
            f.write(os.urandom(size_mb * 1024 * 1024))
            
        os.system('sync')
        
        start_time = time.time()
        with open(file_path, 'rb') as f:
            while f.read(1024 * 1024):
                pass
        end_time = time.time()
        
        duration = end_time - start_time
        speed_mbps = size_mb / duration
        
        print(f"Result: {speed_mbps:.2f} MB/s")
        return speed_mbps

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python gluster_benchmark.py <path_to_gluster_mount>")
        sys.exit(1)
    
    mount_path = sys.argv[1]
    bench = GlusterBenchmark(mount_path)
    bench.benchmark_small_files()
    bench.benchmark_large_file()
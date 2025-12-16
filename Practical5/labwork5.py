import sys
import os
import concurrent.futures

class LongestPathFinder:
    def __init__(self, input_file, num_workers=3):
        self.input_file = input_file
        self.num_workers = num_workers

    def generate_input_data(self):
        data = [
            "/usr/bin/python3",
            "/var/www/html/index.html",
            "/etc/kubernetes/manifests/kube-apiserver.yaml",
            "/home/user/development/projects/distributed-systems/lab5/longest_path.py",
            "/opt/google/chrome/resources/default_apps/external_extensions.json",
            "/usr/share/icons/hicolor/48x48/apps/firefox.png",
            "/tmp/systemd-private-xyz-httpd.service-AbCdEf/tmp/php-session-cache",
            "/very/long/path/that/is/created/specifically/to/test/if/the/algorithm/can/detect/the/longest/string/in/the/dataset/correctly"
        ]
        with open(self.input_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(data))

    def get_data_chunks(self):
        if not os.path.exists(self.input_file):
            self.generate_input_data()
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        chunk_size = len(lines) // self.num_workers + 1
        return [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

    @staticmethod
    def mapper(paths):
        if not paths:
            return ""
        return max(paths, key=len)

    @staticmethod
    def reducer(local_maxima):
        if not local_maxima:
            return ""
        return max(local_maxima, key=len)

    def execute(self):
        print(f"Starting MapReduce Job with {self.num_workers} workers")
        
        chunks = self.get_data_chunks()
        
        print(f"Phase 1: Mapping {len(chunks)} chunks in parallel")
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            mapped_results = list(executor.map(LongestPathFinder.mapper, chunks))
        
        print("Phase 2: Shuffling and Reducing")
        final_result = self.reducer(mapped_results)
        
        print("-" * 50)
        print("FINAL RESULT")
        print("-" * 50)
        print(f"Length: {len(final_result)}")
        print(f"Path  : {final_result}")

if __name__ == "__main__":
    job = LongestPathFinder("system_paths.txt")
    job.execute()
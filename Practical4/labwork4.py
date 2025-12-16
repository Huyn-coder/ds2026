import sys
import re
import multiprocessing
import os
from collections import defaultdict

def map_worker(text_chunk):
    words = re.findall(r'\b\w+\b', text_chunk.lower())
    return [(word, 1) for word in words]

def reduce_worker(item):
    word, counts = item
    return (word, sum(counts))

class ParallelMapReduceJob:
    def __init__(self, input_file, num_workers=4):
        self.input_file = input_file
        self.num_workers = num_workers

    def read_input(self):
        try:
            with open(self.input_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return content
        except FileNotFoundError:
            print(f"Error: File {self.input_file} not found.")
            return None

    def split_data(self, content):
        length = len(content)
        chunk_size = length // self.num_workers + 1
        return [content[i:i+chunk_size] for i in range(0, length, chunk_size)]

    def run(self):
        print(f"--- Starting MapReduce Job (Workers: {self.num_workers}) ---")
        
        content = self.read_input()
        if not content: return
        chunks = self.split_data(content)
        print(f"[Master] Data split into {len(chunks)} chunks.")

        print("[Master] Distributing tasks to Mappers...")
        with multiprocessing.Pool(processes=self.num_workers) as pool:
            mapped_results_list = pool.map(map_worker, chunks)
        
        all_mapped_data = [item for sublist in mapped_results_list for item in sublist]
        print(f"[Master] Mappers finished. Total key-value pairs generated: {len(all_mapped_data)}")

        print("[Master] Shuffling and Sorting...")
        shuffled_data = defaultdict(list)
        for key, value in all_mapped_data:
            shuffled_data[key].append(value)

        print("[Master] Reducing...")
        final_result = {}
        for key, values in shuffled_data.items():
            final_result[key] = sum(values)

        self.save_output(final_result)

    def save_output(self, result):
        output_file = "output_counts.txt"
        sorted_items = sorted(result.items(), key=lambda x: x[1], reverse=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"{'WORD':<20} {'COUNT':>10}\n")
            f.write("-" * 31 + "\n")
            for word, count in sorted_items:
                f.write(f"{word:<20} {count:>10}\n")
        
        print(f"[Master] Job Finished. Results saved to '{output_file}'.")
        print("Top 5 words:", sorted_items[:5])

if __name__ == "__main__":
    if not os.path.exists("input.txt"):
        with open("input.txt", "w") as f:
            f.write("MapReduce is a programming model and an associated implementation for processing and generating big data sets with a parallel, distributed algorithm on a cluster.")
    
    job = ParallelMapReduceJob("input.txt", num_workers=4)
    job.run()
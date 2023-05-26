import time
import os
import re
from tqdm import tqdm

# Define the file size in bytes
file_size = 1000000000  # 1 GB

# Define the wait interval between updates (in seconds)
wait_interval = 0.5

# Define the dynamic size log pattern
dynamic_size_log_pattern = r"Current Size: (\d+) bytes"

# Simulated download loop
with tqdm(total=file_size, unit='B', unit_scale=True, desc="Downloading") as progress:
    old_size = 0
    while old_size < file_size:
        # Simulate some processing time
        time.sleep(wait_interval)

        # Generate a random new size for demonstration purposes
        new_size = old_size + int(1024 * 1024 * 10)  # Increase by 10 MB

        # Calculate the downloaded data size
        downloaded_data_size = new_size - old_size

        # Update the progress bar with the downloaded data size
        progress.update(downloaded_data_size)

        # Refresh the progress bar
        progress.refresh()

        # Calculate the percentage manually
        percent = (progress.n / progress.total) * 100

        # Log the progress
        # print(f"Progress: {progress.n}/{progress.total} ({percent:.2f}%)")

        old_size = new_size

print("Download completed!")

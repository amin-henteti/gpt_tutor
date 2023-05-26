import sys
import requests
from bs4 import BeautifulSoup
import subprocess
import os
from pathlib import Path
import time
import re
from tqdm import tqdm
import logging
from fuzzywuzzy import fuzz

# Configure logging
log_filename = 'huggingface_download.log'
log_format = '%(levelname)s - %(message)s'

# Create a logger and set the log level
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler to write logs to the log file
file_handler = logging.FileHandler(log_filename, mode='w')  # Set mode to 'w' to overwrite the file
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(file_handler)

# Create a stream handler to write logs to stdout
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(stream_handler)

def get_direct_download_links(repository_url):
    """
    Fetches direct download links from a model repository URL.

    Args:
        repository_url (str): The model repository URL.

    Returns:
        list: A list of direct download links.
    """
    try:
        # Send a GET request to the model repository page
        response = requests.get(repository_url, timeout=100)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the file links
        file_links = soup.find_all('a', title="Download file")

        # Extract the direct download links
        direct_download_links = []
        for link in file_links:
            href = link['href']
            logger.info(f"Found link: {href}")
            if href.startswith('/'):
                href = 'https://huggingface.co' + href
            direct_download_links.append(href)

        return direct_download_links
    except Exception as e:
        logger.error("An error occurred while fetching download links.")
        raise e

def download_with_idm(file_url, download_location, filename):
    """
    Downloads a file using IDM (Internet Download Manager).

    Args:
        file_url (str): The URL of the file to download.
        download_location (str): The location to save the downloaded file.
        filename (str): The name of the downloaded file.
    """
    # Path to IDM executable
    idm_path = r"C:\Program Files (x86)\Internet Download Manager\IDMan.exe"

    # Command to invoke IDM with the file URL and download location
    # Visit https://www.internetdownloadmanager.com/support/command_line.html
    # to know about IDM CLI
    command = f'"{idm_path}" /d "{file_url}" /p "{download_location}" /f {filename} /q /n'

    logger.info(f"Executing command: {command}")
    # Launch IDM to start the download
    subprocess.run(command, shell=False)

    full_download_path = download_location / filename
        
        
    # Wait for the file to be created or the file was downloaded very fast
    while not(find_latest_log_file() or os.path.exists(str(full_download_path))):
        time.sleep(1)

    time.sleep(5)
    if not os.path.exists(str(full_download_path)):
        while not os.path.exists(str(full_download_path)):
            time.sleep(5)
            try:
                latest_log_file = find_latest_log_file(duration=60*5)
                if isinstance(latest_log_file, list):
                    similarities = [fuzz.ratio(str(full_download_path).lower(), str(actual_file_name).lower()) for actual_file_name in latest_log_file]
                    max_similarity_index = similarities.index(max(similarities))
                    latest_log_file = latest_log_file[max_similarity_index]
                    logger.info(f"best match: {latest_log_file}")
                log_file_content = latest_log_file.read_text()
                total_size_log_pattern = "C0:Content.Range: bytes \d+.\d+/(\d+)\n"
                file_size = int(re.search(total_size_log_pattern, log_file_content).group(1))
                break
            except Exception as e:
                logger.error(f"encountered an error while trying to get file_size. Error: {str(e)}")
                continue
                # continue to check if the download has finished
        # Display a progress bar for the download
        wait_interval = get_wait_interval(file_size)
        old_size = 0
        unit = 1024 * 1024
        dynamic_size_log_pattern = "time \d+, speed \d+, downl (\d+) Bytes"
        # Temporarily remove the stream handler because the stream_handler disturb the progress bar
        logger.removeHandler(stream_handler)

        with tqdm(total=file_size, unit='M', unit_scale=True, desc=f"Downloading {filename}") as progress:
            while not os.path.exists(str(full_download_path)):
                time.sleep(wait_interval)
                # need to get the latest logs by re-reading the log file
                try:
                    log_file_content = latest_log_file.read_text()
                    new_size = int(re.findall(dynamic_size_log_pattern, log_file_content)[-1])
                except Exception as e:
                    logger.error(f"encountered an error while trying to get the downloaded size. Error: {str(e)}")
                    continue
                    # continue to check if the download has finished
                downloaded_data_size = (new_size - old_size) / unit
                progress.update(downloaded_data_size)

                # Refresh the progress bar
                progress.refresh()

                percent = (progress.n / progress.total) * 100

                # Log the progress on the same line
                logger.debug(f"Progress: {progress.n}/{progress.total} ({percent:.2f}%)")
                old_size = new_size
    # Restore the stream handler
    logger.addHandler(stream_handler)
    # need to stop 
    logger.info("Download completed.")
    logger.info(f"Downloaded file: {full_download_path}")

def get_wait_interval(file_size):
    """
    Calculates the wait interval based on the file size.

    Args:
        file_size (int): The size of the file in bytes.

    Returns:
        int: The wait interval in seconds.
    """
    if file_size >= 1000 * 1024 * 1024:  # File size >= 1GB
        return 10 * 60  # Wait every 10 minutes
    elif file_size >= 10 * 1024 * 1024:  # File size >= 10MB
        return 30  # Wait every 30 seconds
    else:
        return 1  # Wait every 1 second


def find_latest_log_file(directory=None, duration=60):
    """
    Find the log file that is currently being updated in the specified directory and its subdirectories.

    Args:
        directory (str): The directory to search for log files.
        duration (int): The duration (in seconds) to monitor the log files. Default is 10 seconds.

    Returns:
        str: The path of the latest log file being updated, or None if no log file is found.
    """    
    # Convert the directory path to a Path object and use a default value when directory not provided
    directory_path = Path(directory) if directory else Path(os.getenv('APPDATA')) / r"IDM\DwnlData"

    # Get all log files in the directory
    log_files = directory_path.rglob("*.log")

    # Sort the log files by modification time in descending order
    log_files = sorted(log_files, key=lambda f: f.stat().st_mtime, reverse=True)
    # Get the current time
    current_time = time.time()
    # filter old log file
    latest_log_files = list(filter(lambda log_file: current_time - log_file.stat().st_ctime <= duration, log_files))

    if len(latest_log_files) == 1:
        return latest_log_files[0]
    elif len(latest_log_files) == 0:
        logger.warning(f"could not find a recent log file")
        return latest_log_files
    else:
        logger.warning(f"many recent log file: {latest_log_files}")
        return latest_log_files


def main():
    """
    Main function to initiate the download process.
    """
    
    # Prompt the user for a model repository link
    repository_url = input("Enter the model repository link: ") if not USE_DEFAULT_VALUES else DEFAULT_REPOSITORY_URL

    url_pattern = r"^https://huggingface.co/(.*)/tree/main$"
    match = re.match(url_pattern, repository_url)

    if not match:
        logger.error("repository_url: {repository_url} does not respect the pattern {url_pattern}")
        raise ValueError("Invalid repository URL")
    repo_name = match.group(1).replace("/", "_")
    logger.info(f"Repository name: {repo_name}")

    # Fetch direct download links
    download_links = get_direct_download_links(repository_url)

    # Print the direct download links
    for i, link in enumerate(download_links):
        logger.info(f"{i+1}. {link}")

    # Prompt the user for the download location
    if USE_DEFAULT_VALUES:
        download_location = DEFAULT_DOWNLOAD_LOCATION
    else:
        download_location = input("Enter the download location (or press Enter for default): ") or os.getcwd()
    # download_location = input("Enter the download location: ") if not USE_DEFAULT_VALUES else DEFAULT_DOWNLOAD_LOCATION

    # Join the current working directory and the repo name.
    download_location = Path(download_location) / repo_name
    # Create the folder.
    download_location.mkdir(exist_ok=True)

    # Confirm the download location with the user
    logger.info(f"Download location: {download_location}")
    if not USE_DEFAULT_VALUES:
        confirmation = input("Confirm the download location (Y/ENTER/N): ")
        if confirmation.upper() not in ("Y", ""):
            raise ValueError("Download location confirmation failed.")

    for file_index, file_url in enumerate(download_links):
        # Download the selected file using IDM
        file_url = download_links[file_index]
        filename = os.path.basename(file_url)
        full_download_path = download_location / filename
        try:
            if os.path.exists(str(full_download_path)):
                logger.info(f"File already downloaded: {full_download_path}")
            else:
                # download the file with IDM
                download_with_idm(file_url, download_location, filename)
        except Exception as e:
            logger.error("An error occurred during the download.")
            raise Exception(f"Download error: {str(e)}")

# Input condition to decide whether to always use default values or prompt the user for input
USE_DEFAULT_VALUES = input("Do you want to always use default values? (Y/ENTER/N): ").upper() in ("Y", "")

# Default values
DEFAULT_REPOSITORY_URL = 'https://huggingface.co/facebook/dino-vitb16/tree/main'
DEFAULT_DOWNLOAD_LOCATION = Path(os.getcwd())

if __name__ == "__main__":
    main()

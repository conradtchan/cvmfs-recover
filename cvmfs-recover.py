#!/usr/bin/env python3

import requests
import os
import argparse

# Create the parser
parser = argparse.ArgumentParser(description="Download missing CVMFS files")

# Add the arguments
parser.add_argument('--repo_name', type=str, required=True, help='The repository name')
parser.add_argument('--server_name', type=str, required=True, help='The server name')

# Parse the arguments
args = parser.parse_args()

# Use the arguments
repo_name = args.repo_name
server_name = args.server_name

# Define the base URL for the file download
base_url = f"http://{server_name}/cvmfs/{repo_name}/data/"

# Define the error file path
error_file_path = f"{repo_name}.err"

# Define the directory where the files are stored
storage_directory = f"/srv/cvmfs/{repo_name}/data/"

# Open the error file and read the lines
with open(error_file_path, 'r') as error_file:
    lines = error_file.readlines()

    # Iterate over each line in the error file
    for line in lines:
        # Split the line to get the hash and the file path
        parts = line.split(' ')
        if len(parts) < 3:
            continue

        # Missing chunk
        if parts[0] == "data" and parts[1] == "chunk":
            file_hash = parts[2]

        # Missing catalog
        elif parts[0] == "failed" and parts[2] == "open" and parts[3] == "catalog":
            file_hash = parts[4].strip() + "C"

        else:
            continue

        filepath = file_hash[:2] + "/" + file_hash[2:]

        # Construct the URL for the file download
        download_url = base_url + filepath

        # Download the file
        response = requests.get(download_url)

        # If the download was successful, save the file
        if response.status_code == 200:
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(storage_directory + file_hash[:2] + "/"), exist_ok=True)

            # Write the file
            with open(storage_directory + filepath, 'wb') as file:
                file.write(response.content)

            print(f"Downloaded file: {download_url}")
        else:
            print(f"Failed to download file: {download_url}")
# Importing required Libraries
import requests
import argparse

# creating a function "fetch_list_word" to fetch the list of words
def fetch_list_word(list_word_file):
    # Open the file, read and split them as list
    with open(list_word_file) as f:
        list = f.read().splitlines()
    return list

# creating a function "exec_server" to request server for each path that exists
def exec_server(paths):
    # Create an empty list to store existing paths
    directories = []
    files = []
    
    # Creating a for loop to iterate through each path and make a GET request
    for file_path in paths:
        output = requests.get(file_path)
        # If GET request response is 200 append the path to empty list
        if output.status_code == 200:
            # If file_path ends with .php or .html then append file paths to empty list files else add it to directory empty list
            if file_path.endswith(".php") or file_path.endswith(".html"):
               files.append(file_path)
            else:
               directories.append(file_path)
    return files,directories

# Create a function "get_path" passing 2 parameters url and list to get list of all available paths
def get_path(url, list):
    # For each word in list generate all paths with extensions .php and .html along with no extensions
    return [f"{url}/{word}{ext}" for word in list for ext in ["", ".php", ".html"]]

# Main function that takes an parser object,argument for server URL and parse them
if __name__ == "__main__":
    # Referred from https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(description='Execute web enumeration.')
    parser.add_argument('url', help='Enumerate URL for server.')
    args = parser.parse_args()
    
    # Fetching list of words from word list file path
    list_word_file = "/usr/share/wordlists/dirb/common.txt"
    list = fetch_list_word(list_word_file)
    
    # Generating all available paths and performing server enumeration
    paths = get_path(args.url, list)
    files, directories = exec_server(paths)
    
    # Iterate through each path, if any found return found files and directories
    if files or directories:
        print(f"Directories found for {args.url}:")
        for directory in directories:
            print(directory)
        print(f"Files found for {args.url}:")
        for file in files:
            print(file)
    else:
        print(f" Zero files or directories found for {args.url}.")

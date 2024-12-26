# main.py

import os
import subprocess
import sys

# Function to create a virtual environment
def create_virtual_env(env_name):
    if not os.path.exists(env_name):
        print(f"Creating virtual environment: {env_name}")
        subprocess.check_call([sys.executable, '-m', 'venv', env_name])
    else:
        print(f"Virtual environment '{env_name}' already exists.")

# Function to install a package using pip
def install(package, env_name):
    subprocess.check_call([os.path.join(env_name, 'Scripts', 'pip'), 'install', package])

# Function to install dependencies from requirements.txt
def install_requirements(env_name):
    try:
        install('requests', env_name)  # Ensure requests is installed first
        subprocess.check_call([os.path.join(env_name, 'Scripts', 'pip'), 'install', '-r', 'requirements.txt'])
        print("Dependencies installed successfully.")
    except Exception as e:
        print(f"An error occurred while installing dependencies: {e}")

# Function to download a file from a URL
def download_file(url, filename):
    import requests  # Import here to ensure it's available after installation
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename} successfully.")
    except Exception as e:
        print(f"An error occurred while downloading {filename}: {e}")

if __name__ == "__main__":
    env_name = 'myenv'
    create_virtual_env(env_name)
    
    # Activation reminder
    print(f"Please activate the virtual environment '{env_name}' using:")
    print(f"  {env_name}\\Scripts\\activate")  # For Windows
    # print(f"  source {env_name}/bin/activate")  # Uncomment for macOS/Linux

    install_requirements(env_name)
    
    # URLs of the files to download
    file1_url = "https://mega.nz/file/KlsmwAZA#rdmhqXum3EbwDrHYZUeDNkQVMsXi8bZzHmXSLcYHWbg" 
    file2_url = "https://mega.nz/file/KlcD0QaR#F2Z1ReBf7GUky8WmFTDzSOnuxwbvT_bjGl7H7p7fUME"   
    
    # Download the files
    download_file(file1_url, "yolov3.weights")
    download_file(file2_url, "yolov3.cfg")
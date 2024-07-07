import os
import requests
import zipfile
import logging
import psutil
import pefile

# Configure logging
logging.basicConfig(filename='oxide_update.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
OXIDE_URL = "https://umod.org/games/rust.json"
DOWNLOAD_URL = "https://github.com/OxideMod/Oxide.Rust/releases/latest/download/Oxide.Rust.zip"
INSTALL_DIR = "c:\\rust\\oxide"
DLL_PATH = os.path.join(INSTALL_DIR, "RustDedicated_Data", "Managed", "Oxide.Rust.dll")
CURRENT_VERSION_FILE = os.path.join(INSTALL_DIR, "version.txt")

def is_rust_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() == 'rustdedicated.exe':
            logging.info("RustDedicated is currently running.")
            print("RustDedicated is currently running.")
            return True
    logging.info("RustDedicated is not running.")
    print("RustDedicated is not running.")
    return False

def get_online_version():
    response = requests.get(OXIDE_URL)
    response.raise_for_status()

    data = response.json()
    online_version = data['latest_release_version']

    logging.info(f"Online available version: {online_version}")
    print(f"Online available version: {online_version}")
    return online_version

def get_current_version():
    if not os.path.exists(DLL_PATH):
        logging.info("Oxide.Rust.dll not found.")
        print("Oxide.Rust.dll not found.")
        return None

    try:
        pe = pefile.PE(DLL_PATH)
        for fileinfo in pe.FileInfo:
            for entry in fileinfo:
                if entry.Key == b'StringFileInfo':
                    for st in entry.StringTable:
                        for key, value in st.entries.items():
                            if key.decode() == "FileVersion":
                                current_version = value.decode().rstrip('.0')
                                logging.info(f"Current version: {current_version}")
                                print(f"Current version: {current_version}")
                                return current_version
    except Exception as e:
        logging.error(f"Error getting current version: {e}")
        print(f"Error getting current version: {e}")
        return None

def download_and_install(online_version):
    zip_path = os.path.join(INSTALL_DIR, "oxide.zip")

    logging.info(f"Downloading {online_version} from {DOWNLOAD_URL}")
    print(f"Downloading {online_version} from {DOWNLOAD_URL}")
    
    response = requests.get(DOWNLOAD_URL)
    response.raise_for_status()

    with open(zip_path, 'wb') as file:
        file.write(response.content)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(INSTALL_DIR)
    except Exception as e:
        logging.error(f"Error unzipping the file: {e}")
        print(f"Error unzipping the file: {e}")
        return

    os.remove(zip_path)
    with open(CURRENT_VERSION_FILE, 'w') as file:
        file.write(online_version)

    logging.info(f"Installed Oxide version {online_version}")
    print(f"Installed Oxide version {online_version}")

def main():
    try:
        logging.info("Starting Oxide version check")

        rust_running = is_rust_running()
        online_version = get_online_version()
        current_version = get_current_version()

        if rust_running:
            print("Skipping update since Rust is currently running.")
            logging.info("Skipping update since Rust is currently running.")
            return

        if current_version is None:
            logging.info("Oxide.Rust.dll not found, performing Oxide install.")
            print("Oxide.Rust.dll not found, performing Oxide install.")
            download_and_install(online_version)
        elif current_version != online_version:
            logging.info("Update needed.")
            print("Update needed.")
            download_and_install(online_version)
        else:
            logging.info("No update needed.")
            print("No update needed.")
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

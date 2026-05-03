import os
import requests
import zipfile
import logging
import psutil
import pefile
import tempfile

# Configure logging
logging.basicConfig(filename='oxide_update.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
OXIDE_URL = "https://umod.org/games/rust.json"
DOWNLOAD_URL = "https://github.com/OxideMod/Oxide.Rust/releases/latest/download/Oxide.Rust.zip"
INSTALL_DIR = "c:\\rust\\oxide"
DLL_PATH = os.path.join(INSTALL_DIR, "RustDedicated_Data", "Managed", "Oxide.Rust.dll")
CURRENT_VERSION_FILE = os.path.join(INSTALL_DIR, "version.txt")
REQUEST_TIMEOUT = 30

def normalize_version(version):
    parts = str(version).strip().lstrip("v").split(".")
    while len(parts) > 1 and parts[-1] == "0":
        parts.pop()
    return ".".join(parts)

def is_rust_running():
    for proc in psutil.process_iter(['name']):
        try:
            proc_name = (proc.info.get('name') or '').lower()
            if proc_name == 'rustdedicated.exe':
                logging.info("RustDedicated is currently running.")
                print("RustDedicated is currently running.")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    logging.info("RustDedicated is not running.")
    print("RustDedicated is not running.")
    return False

def get_online_version():
    response = requests.get(OXIDE_URL, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    data = response.json()
    online_version = normalize_version(data['latest_release_version'])

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
                                current_version = normalize_version(value.decode())
                                logging.info(f"Current version: {current_version}")
                                print(f"Current version: {current_version}")
                                return current_version
    except Exception as e:
        logging.error(f"Error getting current version: {e}")
        print(f"Error getting current version: {e}")
        return None

def download_and_install(online_version):
    logging.info(f"Downloading {online_version} from {DOWNLOAD_URL}")
    print(f"Downloading {online_version} from {DOWNLOAD_URL}")

    os.makedirs(INSTALL_DIR, exist_ok=True)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    zip_path = temp_file.name

    try:
        with requests.get(DOWNLOAD_URL, stream=True, timeout=REQUEST_TIMEOUT) as response:
            response.raise_for_status()
            with temp_file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        temp_file.write(chunk)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            install_root = os.path.abspath(INSTALL_DIR)
            for member in zip_ref.infolist():
                target_path = os.path.abspath(os.path.join(INSTALL_DIR, member.filename))
                if not target_path.startswith(install_root + os.sep) and target_path != install_root:
                    raise ValueError(f"Unsafe zip path: {member.filename}")
            zip_ref.extractall(INSTALL_DIR)
    except Exception as e:
        logging.error(f"Error installing Oxide: {e}")
        print(f"Error installing Oxide: {e}")
        return
    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)

    with open(CURRENT_VERSION_FILE, 'w', encoding='utf-8') as file:
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

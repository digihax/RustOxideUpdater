# RustOxideUpdater

RustOxideUpdater is a Python script for checking and updating Oxide/uMod for a Windows Rust dedicated server.

It compares the locally installed Oxide Rust DLL version with the latest version published by uMod. If the versions differ and the Rust server process is not running, it downloads and extracts the latest Oxide release.

## What It Does

- Checks whether `RustDedicated.exe` is running
- Reads the installed `Oxide.Rust.dll` file version
- Fetches the latest Oxide Rust version from uMod
- Downloads the latest Oxide release from GitHub when an update is needed
- Extracts the zip into the configured Rust/Oxide install folder
- Writes the installed version to `version.txt`
- Logs activity to `oxide_update.log`

## Requirements

- Windows
- Python 3
- A Rust dedicated server install
- Python packages:

```powershell
pip install requests pefile psutil
```

## Configuration

Edit `RustOxideUpdater.py` and set:

```python
INSTALL_DIR = "c:\\rust\\oxide"
```

This should point at the folder where the Oxide zip should be extracted.

The script expects the local Oxide DLL at:

```text
<INSTALL_DIR>\RustDedicated_Data\Managed\Oxide.Rust.dll
```

## Running

Run:

```powershell
python RustOxideUpdater.py
```

Suggested use is to call the script from your Rust server startup batch file before launching `RustDedicated.exe`.

Example:

```bat
python RustOxideUpdater.py
RustDedicated.exe -batchmode ...
```

## Safety Behavior

- If `RustDedicated.exe` is running, the script reports the version state but does not update.
- Downloads use a timeout so failed network calls do not hang forever.
- The release zip is downloaded to a temporary file first.
- Zip entries are checked before extraction to avoid writing outside the install folder.

## Notes And Cautions

- Test this on a staging server first.
- Stop the Rust server before applying updates.
- Keep backups of your server and Oxide folders before changing production installs.
- This script updates Oxide itself, not individual plugins.

# RustOxideUpdater

by Digihax, aka The Professor, and Admin/Owner of AZ Casual rust server  
     v.01: Initial Release  
     v.02: Fixed issue with local version check reliability.  Add cleanup at start, of local txt files created.  
     v.03: Updated to Python, more robust and accurate version confirmation

CAUTION:
As with any resource available on the Internet, use at your own risk.  
Use on a test server first.  
I have tested this on multiple servers, but it may not work for you.  
The server needs to be offline to update.  The script checks for RustDedicated.exe prior to running

DESCRIPTION

This python script checks your local version of Oxide, as well as the latest version release of Oxide.    
If there is a mismatch, it downloads and installs the latest version available online.  
It also performs a check to see if RustDedicated.exe is running, if so, only reports a mismatch, no update attempt made.

INSTRUCTIONS

1) You *must* edit the python script, and update the locations of your Rust/Oxide Installation (such as c:\rust\oxide)   
   Example: INSTALL_DIR = "c:\\rust\\oxide"

Suggested implementation:
   Add a line, "call python RustOxideUpdater.py" to your startup script, PRIOR to the start of your server startup line (RustDedicated.exe ...)  
   Your startup batch file run the commands in RustOxideUpdater.bat, and continue once RustOxideUpdater is complete  


REQUIREMENTS   

0) Python.
1) Rust
2) pip install requests pefile psutil
  


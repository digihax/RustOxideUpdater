# RustOxideUpdater

by Digihax, aka The Professor, and Admin/Owner of AZ Casual rust server  
     v.01: Initial Release  
     v.02: Fixed issue with local version check reliability.  Add cleanup at start, of local txt files created.  

CAUTION:
As with any resource available on the Internet, use at your own risk.  
Use on a test server first.  
I have tested this on multiple servers, but it may not work for you.  

DESCRIPTION

This batch file checks your local version of Oxide, as well as the latest version release of Oxide.    
If there is a mismatch, it downloads and installs the latest version available online.  

INSTRUCTIONS

1) You *must* edit the batch file, and add the location of your Rust Installation , such as c:\RustServer  
   Example: Set RustPath=c:\Rustserver  
2) You *must* add a switch to your Rust startup line, like -logFile "c:/RustServer/ConsoleOutput.txt", which places ConsoleOutput.txt file in same location as your RustPath.  

Suggested implementation:
   Add a line, "start /wait RustOxideUpdater.bat" to your startup script, PRIOR to the start of your server startup line (RustDedicated.exe ...)  
   Your startup batch file will pause, launch RustOxideUpdater.bat, and continue once RustOxideUpdater is complete  


REQUIREMENTS   

0) Windows.  
1) Your Rust server, with Oxide, must have had at least one startup, to create the \ConsoleOutput.txt file  
2) Your Rust server must not currently be running  
3) You must be able to run powershell commands.  
4) On some systems, you may need to run Internet Explorer if it has not previously been run.  

I suggest adding a line, such as "start RustOxideUpdater.bat" to your startup script, PRIOR to the start of your server-start line (RustDedicated.exe etc)
This allows the batch file to launch in another window, and complete, and then return control back to your startup script.  

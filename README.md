# RustOxideUpdater

This batch file checks your local version of Oxide, as well as the latest version release of Oxide.  
If there is a mismatch, it downloads and installs the latest version available online.

You *must* edit the batch file and with your Rust Installation Path, such as c:\RustServer
Rust/Oxide must a) have run once, and b) not currently be running
You must be able to run powershell commands.

I suggest adding a line, such as "start RustOxideUpdater.bat" to your startup script, PRIOR to the start of your server-start line (RustDedicated.exe etc)
This allows the batch file to launch in another window, and complete, and then return control back to your startup script.


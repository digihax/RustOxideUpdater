:: This script brought to you by Digihax, aka The Professor, Admin of AZ Casual Rust Server
:: Published 2/9/2022
:: Updated 2/10/2022 - Initial local version check was not reliable.  Created an alternate version check

:: CHANGE THIS to your local rust installation, with no trailing "\"
Set RustPath=c:\Your\Rust\Root\Folder
cd %RustPath%

::Cleanup
@del %RustPath%\*Oxide_Version.txt

@echo on
::Grabbing the version of your local oxide install, and storing in root rust directory as Local_Oxide_Version.txt
@echo Grabbing your installed Oxide version
@powershell select-string %RustPath%\ConsoleOutput.txt -Pattern 'Loaded plugin Rust v' -SimpleMatch | powershell -Command "$input | foreach-object {$_ -split ' '} | select -index 4 | foreach-object {$_ -replace('v','')} | Out-File %RustPath%\Local_Oxide_Version.txt"

@echo.
@echo Your oxide version is: 
@type %RustPath%\Local_Oxide_Version.txt

::Grabbing the current version Oxide from umod.org, and storing in root rust directory as Latest_Oxide_Version.txt
@echo Grabbing the version number of the latest Oxide
powershell (invoke-webrequest https://umod.org/games/rust.json).Content.split([Environment]::NewLine) |powershell -Command "$input | convertfrom-json | select latest_release_version -ExpandProperty latest_release_version | Out-File %RustPath%\Latest_Oxide_Version.txt"

@echo.
@echo The most recent Oxide version is: 
@type %RustPath%\Latest_Oxide_Version.txt

::Compare the two files, and report no update needed, or update if there is a version mismatch
@powershell if ((get-filehash %RustPath%\Local_Oxide_Version.txt).hash -eq (get-filehash %RustPath%\Latest_Oxide_Version.txt).hash) {(write-host "No Update Required")} else {(write-host "Updating Required");(Invoke-WebRequest -Uri "https://github.com/OxideMod/Oxide.Rust/releases/latest/download/Oxide.Rust.zip" -OutFile "%rustpath%\oxide.rust.zip");(expand-archive -force -literalpath '%rustpath%\oxide.rust.zip' -destinationpath %rustpath%)}

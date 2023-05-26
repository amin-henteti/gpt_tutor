# PowerShell script that installs Python version 3.11.3 on a Windows machine

$version = "3.11.3"
$url = "https://www.python.org/ftp/python/$version/python-$version-amd64.exe"
$installer = "python-$version-amd64.exe"
$installPath = "C:\Python$version"

# Download Python installer
Invoke-WebRequest -Uri $url -OutFile $installer

# Install Python
Start-Process -Wait -FilePath $installer -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0", "Include_pip=1", "TargetDir=$installPath"

# Remove installer
Remove-Item -Path $installer

# Display installed Python version
Write-Host "Python $version has been successfully installed at $installPath"

# Check if Nmap is already installed
if (!(Get-Command "nmap" -ErrorAction SilentlyContinue)) {
    # Define the download URL for the Nmap installer
    $nmapDownloadUrl = "https://nmap.org/dist/nmap-7.91-setup.exe"

    # Define the path to save the downloaded installer
    $installerPath = "$env:TEMP\nmap-setup.exe"

    # Download the Nmap installer
    Invoke-WebRequest -Uri $nmapDownloadUrl -OutFile $installerPath

    # Install Nmap silently
    Start-Process -FilePath $installerPath -Wait

    # Clean up the installer file
    Remove-Item -Path $installerPath -Force
}
# by default the nmap will be installed in this path
$NmapFolder = "C:\Program Files (x86)\Nmap"

# Add Nmap to the system's PATH environment variable
$envPath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
$updatedEnvPath = $envPath + ";" + $NmapFolder

[System.Environment]::SetEnvironmentVariable("Path", $updatedEnvPath, "Machine")

# Verify if Nmap is installed
if (Get-Command "nmap" -ErrorAction SilentlyContinue) {
    Write-Host "Nmap has been installed successfully."
} else {
    Write-Host "Failed to install Nmap."
}


# Define the download URL for Ettercap
$ettercapDownloadUrl = "https://github.com/Ettercap/ettercap/releases/download/v0.8.3/ettercap-0.8.3-windows.zip"

# Define the installation directory
$installDirectory = Join-Path $env:ProgramFiles "Ettercap"

# Create the installation directory if it doesn't exist
Write-Host "Creating installation directory..."
New-Item -ItemType Directory -Path $installDirectory -ErrorAction SilentlyContinue | Out-Null

# Download the Ettercap zip file
$zipFilePath = Join-Path $installDirectory "ettercap.zip"
Write-Host "Downloading Ettercap..."
Invoke-WebRequest -Uri $ettercapDownloadUrl -OutFile $zipFilePath

# Extract the contents of the zip file
Write-Host "Extracting Ettercap..."
$ettercapFolder = Join-Path $installDirectory "Ettercap"
Expand-Archive -Path $zipFilePath -DestinationPath $ettercapFolder -Force

# Clean up the downloaded zip file
Write-Host "Cleaning up..."
Remove-Item -Path $zipFilePath -Force

# Add Ettercap to the system's PATH environment variable
$envPath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
$updatedEnvPath = $envPath + ";" + $ettercapFolder

[System.Environment]::SetEnvironmentVariable("Path", $updatedEnvPath, "Machine")

Write-Host "Ettercap installed successfully to $ettercapFolder"

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

# Verify if Nmap is installed
if (Get-Command "nmap" -ErrorAction SilentlyContinue) {
    Write-Host "Nmap has been installed successfully."
} else {
    Write-Host "Failed to install Nmap."
}

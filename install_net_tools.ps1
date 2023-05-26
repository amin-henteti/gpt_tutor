# Function to download a file
function DownloadFile {
    param (
        [string]$Url,
        [string]$FilePath
    )

    try {
        Invoke-WebRequest -Uri $Url -OutFile $FilePath
        Write-Host "Download successful."
    } catch {
        Write-Host "Failed to download the file: $_"
        throw
    }
}

# Function to add a directory to the system's PATH environment variable
function AddToPath {
    param (
        [string]$Directory
    )

    $envPath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
    $updatedEnvPath = $envPath + ";" + $Directory

    [System.Environment]::SetEnvironmentVariable("Path", $updatedEnvPath, "Machine")
    Write-Host "Added $Directory to the system's PATH environment variable."
}

# Function to install a program
function InstallProgram {
    param (
        [string]$DownloadUrl,
        [string]$InstallerPath,
        [string]$InstallDirectory,
        [string]$ProgramName
    )

    Write-Host "Checking if $ProgramName is already installed..."
    if (Get-Command $ProgramName -ErrorAction SilentlyContinue) {
        Write-Host "$ProgramName is already installed."
        return
    }

    # Check if the installer file exists
    if (!(Test-Path $InstallerPath)) {
        # Download the installer
        Write-Host "Downloading $ProgramName..."
        DownloadFile -Url $DownloadUrl -FilePath $InstallerPath
    } else {
        Write-Host "$ProgramName installer already downloaded. Skipping download."
    }

    # Check if the installer file exists before proceeding with installation
    if (Test-Path $InstallerPath) {
        # Install the program silently
        Write-Host "Installing $ProgramName..."
        Start-Process -FilePath $InstallerPath -Wait

        # Clean up the installer file
        Write-Host "Cleaning up..."
        Remove-Item -Path $InstallerPath -Force
    } else {
        Write-Host "Failed to download $ProgramName installer. Installation aborted."
    }

    # Add the program to the system's PATH environment variable
    AddToPath -Directory $InstallDirectory

    Write-Host "$ProgramName installed successfully to $InstallDirectory"
}

# Define the Nmap installation details
$nmapDownloadUrl = "https://nmap.org/dist/nmap-7.91-setup.exe"
$nmapInstallerPath = "$env:TEMP\nmap-setup.exe"
$nmapInstallDirectory = "$env:ProgramFiles\Nmap"
$nmapProgramName = "nmap"

# Install Nmap
InstallProgram -DownloadUrl $nmapDownloadUrl -InstallerPath $nmapInstallerPath -InstallDirectory $nmapInstallDirectory -ProgramName $nmapProgramName

# Define the WinPcap installation details
$winPcapDownloadUrl = "https://www.winpcap.org/install/bin/WinPcap_4_1_3.exe"
$winPcapInstallerPath = "$env:TEMP\winpcap-setup.exe"
$winPcapInstallDirectory = "$env:ProgramFiles\WinPcap"
$winPcapProgramName = "WinPcap"

# Install WinPcap
InstallProgram -DownloadUrl $winPcapDownloadUrl -InstallerPath $winPcapInstallerPath -InstallDirectory $winPcapInstallDirectory -ProgramName $winPcapProgramName


# Retrieve the local IP address and subnet mask
$localIPAddress = (Get-NetIPAddress | Where-Object {$_.AddressFamily -eq "IPv4" -and $_.PrefixOrigin -eq "Manual"}).IPAddress
$subnetMask = (Get-NetIPAddress | Where-Object {$_.AddressFamily -eq "IPv4" -and $_.PrefixOrigin -eq "Manual"}).PrefixLength
$subnet = $localIPAddress + "/" + $subnetMask

echo "subnet = $subnet"
Write-Host "Scanning network for active devices..."

# Perform an ARP scan to get active devices on the network
$arpResults = arp -a | Select-String -Pattern "(?i)([0-9A-F]{2}[:-]){5}([0-9A-F]{2})"

$activeDevices = @()

foreach ($arpResult in $arpResults) {
    $macAddress = $arpResult -replace ".*\b([0-9A-F]{2}[:-]){5}([0-9A-F]{2})\b.*", '$0'
    $ipAddress = $arpResult -replace ".*\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b.*", '$0'
    
    # Exclude the local machine and broadcast addresses from the list of active devices
    if ($ipAddress -ne $localIPAddress -and $ipAddress -notlike "$localIPAddress*") {
        $activeDevices += [PSCustomObject]@{
            "IP Address" = $ipAddress
            "MAC Address" = $macAddress
        }
    }
}

Write-Host "Active devices on the network:"
$activeDevices

Write-Host "Scan completed."



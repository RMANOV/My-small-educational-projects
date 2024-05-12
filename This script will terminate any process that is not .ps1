

while ($true) {
    $currentUserName = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
    $processes = Get-Process | Where-Object { $_.StartInfo.UserName -ne $null -and $_.StartInfo.UserName -ne $currentUserName }
    foreach ($process in $processes) {
        if ($process.StartInfo.EnvironmentVariables["USERPROFILE"] -notmatch "System32") {
            Stop-Process -Id $process.Id -Force
            Write-Output "Terminated process $($process.ProcessName) running under $($process.StartInfo.UserName)"
        }
    }
    Start-Sleep -Seconds 200
}

# This script will terminate any process that is not running under the current user's account and is not running under the System32 directory.
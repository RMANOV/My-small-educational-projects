# Получаване на списък с всички не-администраторски потребителски процеси
$nonAdminProcesses = Get-CimInstance Win32_Process | 
Select-Object Name, ProcessId, @{Name = "UserName"; Expression = { $_.GetOwner().User } } | 
Where-Object { $_.UserName -ne "Administrator" }

# Убиване на процесите
foreach ($process in $nonAdminProcesses) {
    Stop-Process -Id $process.ProcessId -Force
}

# Извеждане на съобщение за успешно приключване на скрипта
Write-Host "Successfully terminated all non-administrator processes."

# Изчистване на променливите
Remove-Variable nonAdminProcesses
```

# # Получаване на списък с всички не-администраторски потребителски процеси
# $nonAdminProcesses = Get-CimInstance Win32_Process | 
# Select-Object Name, ProcessId, @{Name = "UserName"; Expression = { $_.GetOwner().User } } | 
# Where-Object { $_.UserName -ne "Administrator" }

# # Убиване на процесите
# foreach ($process in $nonAdminProcesses) {
#     Stop-Process -Id $process.ProcessId -Force
# }
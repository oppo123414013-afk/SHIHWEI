# ============================================================
# setup_task_scheduler.ps1
# 一鍵設定 Windows 工作排程器：每天 09:00 自動上傳 PGY 報告
# 請以「系統管理員身份執行」
# ============================================================

$TaskName   = "PGY每日報告自動上傳"
$ScriptPath = "C:\Users\User\Desktop\my project\scripts\auto_upload_pgy.ps1"
$RunTime    = "09:00"

Write-Host "===== 設定 PGY 每日自動上傳排程 =====" -ForegroundColor Cyan

# 確認腳本存在
if (-not (Test-Path $ScriptPath)) {
    Write-Host "❌ 找不到上傳腳本：$ScriptPath" -ForegroundColor Red
    exit 1
}

# 移除已存在的同名工作
$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "已移除舊排程工作" -ForegroundColor Yellow
}

# 建立執行動作
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$ScriptPath`""

# 建立觸發條件：每天 09:00
$trigger = New-ScheduledTaskTrigger -Daily -At $RunTime

# 建立設定（工作失敗時最多重試 3 次，間隔 5 分鐘）
$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 5) `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

# 使用目前登入的使用者執行
$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Limited

# 註冊工作
Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "每天早上 09:00 自動掃描 Pagaya_Daily/ 新報告並上傳至 GitHub" `
    -Force

if ($LASTEXITCODE -eq 0 -or $?) {
    Write-Host ""
    Write-Host "✅ 排程設定完成！" -ForegroundColor Green
    Write-Host "   工作名稱  : $TaskName" -ForegroundColor White
    Write-Host "   執行時間  : 每天 $RunTime（台北時間）" -ForegroundColor White
    Write-Host "   腳本路徑  : $ScriptPath" -ForegroundColor White
    Write-Host "   執行紀錄  : C:\Users\User\Desktop\my project\scripts\upload_log.txt" -ForegroundColor White
    Write-Host ""
    Write-Host "⚡ 立即測試執行（可選）:" -ForegroundColor Yellow
    Write-Host "   Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "📋 查看排程狀態:" -ForegroundColor Yellow
    Write-Host "   Get-ScheduledTask -TaskName '$TaskName' | Format-List" -ForegroundColor Gray
} else {
    Write-Host "❌ 排程設定失敗，請確認以系統管理員身份執行此腳本" -ForegroundColor Red
}

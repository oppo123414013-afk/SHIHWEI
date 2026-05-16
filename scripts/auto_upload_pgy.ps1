# ============================================================
# auto_upload_pgy.ps1
# 每日自動掃描 Pagaya_Daily/ 新報告並上傳 GitHub
# 執行時機：Windows 工作排程器 每天 09:00
# ============================================================

$RepoPath  = "C:\Users\User\Desktop\my project"
$LogFile   = "C:\Users\User\Desktop\my project\scripts\upload_log.txt"
$Today     = Get-Date -Format "yyyy-MM-dd"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Write-Log($msg) {
    $line = "[$Timestamp] $msg"
    Write-Host $line
    Add-Content -Path $LogFile -Value $line -Encoding UTF8
}

Write-Log "===== PGY 每日報告自動上傳開始 ====="
Write-Log "目標日期：$Today"

# ── 切換到專案目錄 ────────────────────────────────────────────
Set-Location $RepoPath

# ── 確認 git 可用 ─────────────────────────────────────────────
$gitVersion = git --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Log "❌ 錯誤：找不到 git，請確認 git 已安裝並加入 PATH"
    exit 1
}
Write-Log "git 版本：$gitVersion"

# ── 掃描今日新報告檔案 ────────────────────────────────────────
$patterns = @(
    "Pagaya_Daily\reports\$Today*.md",
    "Pagaya_Daily\raw\$Today*.md",
    "Pagaya_Daily\pdf\$Today*.pdf",
    "pagaya\daily\md\$Today*.md",
    "pagaya\daily\pdf\$Today*.pdf"
)

$newFiles = @()
foreach ($pattern in $patterns) {
    $found = Get-ChildItem -Path (Join-Path $RepoPath $pattern) -ErrorAction SilentlyContinue
    if ($found) {
        $newFiles += $found
        Write-Log "找到檔案：$($found.FullName)"
    }
}

if ($newFiles.Count -eq 0) {
    Write-Log "⚠️  今日（$Today）尚未找到新報告檔案，跳過上傳"
    Write-Log "  請確認報告已儲存至：Pagaya_Daily\reports\ 或 Pagaya_Daily\raw\ 或 Pagaya_Daily\pdf\"
    exit 0
}

Write-Log "共找到 $($newFiles.Count) 個新檔案，準備上傳…"

# ── git pull 確保本地最新 ─────────────────────────────────────
Write-Log "執行 git pull…"
$pullResult = git pull origin main 2>&1
Write-Log "git pull 結果：$pullResult"

# ── git add 新檔案 ────────────────────────────────────────────
foreach ($file in $newFiles) {
    $relativePath = $file.FullName.Replace($RepoPath + "\", "").Replace("\", "/")
    git add $relativePath 2>&1 | Out-Null
    Write-Log "git add：$relativePath"
}

# ── 檢查是否有東西要 commit ───────────────────────────────────
$status = git status --porcelain 2>&1
if (-not $status) {
    Write-Log "⚠️  沒有新變更需要提交（檔案可能已在上次 commit 中）"
    exit 0
}

# ── 讀取報告摘要（取第一行 MD 檔的標題）─────────────────────
$summary = ""
$mdFile = $newFiles | Where-Object { $_.Extension -eq ".md" -and $_.DirectoryName -match "reports" } | Select-Object -First 1
if ($mdFile) {
    $firstLine = Get-Content $mdFile.FullName -TotalCount 3 -Encoding UTF8 | Where-Object { $_ -match "\S" } | Select-Object -First 1
    if ($firstLine) {
        $summary = $firstLine -replace "^#+\s*", "" -replace "[^\x20-\x7E一-鿿　-〿＀-￯]", ""
        $summary = $summary.Substring(0, [Math]::Min(60, $summary.Length))
    }
}

# ── git commit ────────────────────────────────────────────────
$commitMsg = "Pagaya 每日報告 $Today（含 PDF）"
if ($summary) {
    $commitMsg += "`n`n$summary"
}

Write-Log "執行 git commit：$commitMsg"
$env:GIT_AUTHOR_NAME    = "Pagaya Daily Bot"
$env:GIT_AUTHOR_EMAIL   = "pagaya-bot@auto.com"
$env:GIT_COMMITTER_NAME = "Pagaya Daily Bot"
$env:GIT_COMMITTER_EMAIL= "pagaya-bot@auto.com"

git commit -m $commitMsg 2>&1 | ForEach-Object { Write-Log "  $_" }

if ($LASTEXITCODE -ne 0) {
    Write-Log "❌ git commit 失敗，請檢查錯誤訊息"
    exit 1
}

# ── git push ──────────────────────────────────────────────────
Write-Log "執行 git push origin main…"
git push origin main 2>&1 | ForEach-Object { Write-Log "  $_" }

if ($LASTEXITCODE -ne 0) {
    Write-Log "❌ git push 失敗（可能需要重新驗證 GitHub 憑證）"
    exit 1
}

Write-Log "✅ 上傳成功！$($newFiles.Count) 個檔案已推送至 GitHub"
Write-Log "===== 完成 ====="
exit 0

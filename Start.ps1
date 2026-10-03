#Requires -Version 5.1
<#
.SYNOPSIS
  Start GitHub Presentation Optimizer (local API + browser wizard).
#>
param(
  [int]$Port = 8000,
  [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$py = Get-Command py -ErrorAction SilentlyContinue
if (-not $py) {
  Write-Host "Python launcher 'py' not found. Install Python 3.10+ and retry." -ForegroundColor Red
  exit 1
}

Write-Host "Installing package (editable) + backend deps..." -ForegroundColor Cyan
py -3.13 -m pip install -e ".[dev]" -q
py -3.13 -m pip install -r backend/requirements.txt -q

$env:PYTHONPATH = "$Root\backend;$Root\src"
if (-not $env:GH_OAUTH_CLIENT_ID) {
  Write-Host "Note: GH_OAUTH_CLIENT_ID not set — Connect UI will use PAT fallback." -ForegroundColor DarkYellow
}

$url = "http://127.0.0.1:$Port/ui/wizard.html"
Write-Host "Starting local engine on $url ..." -ForegroundColor Cyan

$uvicornArgs = @(
  "-3.13", "-m", "uvicorn", "main:app",
  "--app-dir", "backend",
  "--host", "127.0.0.1",
  "--port", "$Port"
)

$proc = Start-Process -FilePath "py" -ArgumentList $uvicornArgs -PassThru -WindowStyle Minimized

# Wait for health
$ready = $false
for ($i = 0; $i -lt 40; $i++) {
  Start-Sleep -Milliseconds 250
  try {
    $h = Invoke-WebRequest -Uri "http://127.0.0.1:$Port/health" -UseBasicParsing -TimeoutSec 2
    if ($h.StatusCode -eq 200) { $ready = $true; break }
  } catch { }
}

if (-not $ready) {
  Write-Host "Backend did not become ready. Check the minimized uvicorn window." -ForegroundColor Red
  exit 1
}

if (-not $NoBrowser) {
  Start-Process $url
}

Write-Host ""
Write-Host "Wizard: $url" -ForegroundColor Green
Write-Host "API:    http://127.0.0.1:$Port/health" -ForegroundColor Green
Write-Host "Press Ctrl+C in this window to stop (or close the uvicorn process PID $($proc.Id))." -ForegroundColor DarkGray
try {
  Wait-Process -Id $proc.Id
} finally {
  if (-not $proc.HasExited) {
    Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
  }
}

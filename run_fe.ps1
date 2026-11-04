# Start Vite Frontend dev server (port 5174)
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$SCRIPT_DIR\frontend"

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pnpm install
}

Write-Host "Starting Dual-Engine RAG frontend on port 5174..." -ForegroundColor Cyan
pnpm dev


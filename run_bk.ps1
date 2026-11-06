# Start FastAPI backend (port 8080)
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Test-Path "$SCRIPT_DIR\venv\Scripts\uvicorn.exe")) {
    Write-Error "Virtual environment or uvicorn not found. Please run .\setup.ps1 first."
    exit 1
}

$env:TEMP = "D:\ai_cache\temp"
$env:TMP = "D:\ai_cache\temp"
$env:TMPDIR = "D:\ai_cache\temp"
$env:HF_HOME = "D:\ai_cache\hf"
$env:TORCH_HOME = "D:\ai_cache\torch"
$env:DOCLING_CACHE_DIR = "D:\ai_cache\docling"

# Check if PostgreSQL is reachable on port 5433
$pgAlive = (Test-NetConnection -ComputerName 127.0.0.1 -Port 5433 -WarningAction SilentlyContinue -InformationLevel Quiet)
if (-not $pgAlive) {
    Write-Host "[!] PostgreSQL is not responding on port 5433. Attempting to start via Docker..." -ForegroundColor Yellow
    docker compose -f "$SCRIPT_DIR\docker-compose.services.yml" up -d postgres 2>$null
    Start-Sleep -Seconds 3
    $pgAlive = (Test-NetConnection -ComputerName 127.0.0.1 -Port 5433 -WarningAction SilentlyContinue -InformationLevel Quiet)
    if (-not $pgAlive) {
        Write-Host ""
        Write-Host "==========================================================================" -ForegroundColor Red
        Write-Host " [ERROR] PostgreSQL Database is offline on port 5433!" -ForegroundColor Red
        Write-Host "==========================================================================" -ForegroundColor Red
        Write-Host " The backend requires PostgreSQL to store workspaces, documents, and chat."
        Write-Host " Please follow these 2 steps:"
        Write-Host "   1. Open Docker Desktop from your Windows Start Menu" -ForegroundColor Cyan
        Write-Host "   2. Once Docker is running, launch start_all.bat (or rerun this script)" -ForegroundColor Cyan
        Write-Host "==========================================================================" -ForegroundColor Red
        Write-Host ""
        Read-Host "Press Enter to exit..."
        exit 1
    }
}

Set-Location "$SCRIPT_DIR\backend"
Write-Host "Starting Dual-Engine RAG backend on port 8080..." -ForegroundColor Cyan
& "$SCRIPT_DIR\venv\Scripts\uvicorn.exe" app.main:app --reload --port 8080

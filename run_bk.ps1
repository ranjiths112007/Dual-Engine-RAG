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

Set-Location "$SCRIPT_DIR\backend"
Write-Host "Starting Dual-Engine RAG backend on port 8080..." -ForegroundColor Cyan
& "$SCRIPT_DIR\venv\Scripts\uvicorn.exe" app.main:app --reload --port 8080

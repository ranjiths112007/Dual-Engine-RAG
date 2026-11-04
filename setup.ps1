Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Dual-Engine RAG — Local Development Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# 1. Prerequisites
Write-Host "[1/6] Checking prerequisites..." -ForegroundColor Yellow
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Error "Python not found. Please install Python 3.10+."
    exit 1
}
Write-Host "  Python: $(python --version)"

$node = Get-Command node -ErrorAction SilentlyContinue
if (-not $node) {
    Write-Error "Node.js not found. Please install Node.js 18+."
    exit 1
}
Write-Host "  Node: $(node --version)"

$pnpm = Get-Command pnpm -ErrorAction SilentlyContinue
if (-not $pnpm) {
    Write-Host "  Installing pnpm globally..."
    npm install -g pnpm
}
Write-Host "  pnpm: $(pnpm --version)"

# 2. Virtual environment
Write-Host "[2/6] Setting up Python virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "  Created venv/"
} else {
    Write-Host "  venv/ already exists"
}

# 3. Dependencies
Write-Host "[3/6] Installing Python dependencies..." -ForegroundColor Yellow
& ".\venv\Scripts\python.exe" -m pip install -q --upgrade pip
& ".\venv\Scripts\python.exe" -m pip install -q -r backend\requirements.txt
Write-Host "  Done."

# 4. .env
Write-Host "[4/6] Checking .env configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "  Created .env from .env.example"
} else {
    Write-Host "  .env already exists"
}

# 5. Database Services
Write-Host "[5/6] Checking database services..." -ForegroundColor Yellow
$null = docker info 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  Starting Docker services (PostgreSQL + ChromaDB)..."
    docker compose -f docker-compose.services.yml up -d
} else {
    Write-Host "  Docker daemon not running. Please start Docker Desktop or ensure PostgreSQL (port 5433) and ChromaDB (port 8002) are running." -ForegroundColor Yellow
}

# 6. Frontend
Write-Host "[6/6] Installing frontend dependencies..." -ForegroundColor Yellow
Set-Location frontend
pnpm install
Set-Location ..

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "Start backend:  .\run_bk.ps1"
Write-Host "Start frontend: .\run_fe.ps1"


@echo off
title Dual-Engine RAG Launcher
cd /d "%~dp0"

echo [1/4] Checking Docker status...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Docker Desktop is not running. Attempting to start Docker Desktop...
    if exist "%LOCALAPPDATA%\Programs\DockerDesktop\Docker Desktop.exe" (
        start "" "%LOCALAPPDATA%\Programs\DockerDesktop\Docker Desktop.exe"
    ) else if exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
        start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    )
    echo [*] Waiting for Docker engine to become ready...
    :wait_docker
    timeout /t 3 /nobreak >nul
    docker info >nul 2>&1
    if %errorlevel% neq 0 (
        echo     Still waiting for Docker...
        goto wait_docker
    )
    echo [*] Docker engine is ready!
)

echo [2/4] Starting PostgreSQL...
docker compose -f docker-compose.services.yml up -d postgres

echo [3/4] Starting ChromaDB on port 8002...
start "ChromaDB (Port 8002)" cmd /k ".\venv\Scripts\chroma.exe run --path .\chroma_data --port 8002"

echo [4/4] Starting Backend & Frontend...
start "Backend API (Port 8080)" cmd /k "powershell -ExecutionPolicy Bypass -File .\run_bk.ps1"
start "Frontend UI (Port 5174)" cmd /k "powershell -ExecutionPolicy Bypass -File .\run_fe.ps1"

echo.
echo ======================================================
echo   All Dual-Engine RAG services started successfully!
echo   Frontend:  http://localhost:5174
echo   API Docs:  http://localhost:8080/docs
echo ======================================================
echo.


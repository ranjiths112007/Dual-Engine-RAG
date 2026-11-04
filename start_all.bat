@echo off
title Dual-Engine RAG Launcher
cd /d "%~dp0"

echo [1/3] Starting PostgreSQL...
docker compose -f docker-compose.services.yml up -d postgres

echo [2/3] Starting ChromaDB on port 8002...
start "ChromaDB (Port 8002)" cmd /k ".\venv\Scripts\chroma.exe run --path .\chroma_data --port 8002"

echo [3/3] Starting Backend & Frontend...
start "Backend API (Port 8080)" cmd /k "powershell -ExecutionPolicy Bypass -File .\run_bk.ps1"
start "Frontend UI (Port 5174)" cmd /k "powershell -ExecutionPolicy Bypass -File .\run_fe.ps1"

echo.
echo ======================================================
echo   All Dual-Engine RAG services started successfully!
echo   Frontend:  http://localhost:5174
echo   API Docs:  http://localhost:8080/docs
echo ======================================================
echo.


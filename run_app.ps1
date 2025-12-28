# Script untuk menjalankan Pokemon Card Detector App
# Double-click file ini atau jalankan: .\run_app.ps1

# Pindah ke direktori script
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Aktifkan virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

# Cek apakah streamlit terinstall
$streamlitCheck = & ".\venv\Scripts\python.exe" -m pip show streamlit 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Streamlit tidak ditemukan. Menginstall dependencies..." -ForegroundColor Yellow
    & ".\venv\Scripts\python.exe" -m pip install -r requirements.txt
}

# Jalankan aplikasi
Write-Host "`nStarting Pokemon Card Detector App..." -ForegroundColor Green
Write-Host "Server akan berjalan di: http://localhost:8501`n" -ForegroundColor Cyan
& ".\venv\Scripts\python.exe" -m streamlit run app.py


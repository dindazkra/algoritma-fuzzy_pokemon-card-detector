# 🚀 Cara Menjalankan Website di Localhost

## ⚡ Cara Termudah (Recommended)

**Double-click file:** `run_app.ps1`

Atau jalankan di PowerShell:
```powershell
.\run_app.ps1
```

---

## 📋 Cara Manual (Step by Step):

### 1. Buka PowerShell di Folder Project
Pastikan Anda berada di folder: `test-ai-enginge-dinda`

### 2. Aktifkan Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

**Jika muncul error "execution policy", jalankan dulu:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Lalu coba lagi aktivasi venv.

### 3. Jalankan Website
```powershell
python -m streamlit run app.py
```

Atau jika aktivasi venv tidak berfungsi:
```powershell
.\venv\Scripts\python.exe -m streamlit run app.py
```

### 4. Buka Browser
Setelah menjalankan perintah di atas, Streamlit akan otomatis membuka browser di:
- **URL:** http://localhost:8501
- Atau klik link yang muncul di terminal

---

## 🎯 Quick Start (Copy-Paste Saja)

```powershell
# Pindah ke folder project
cd "D:\01DindaTelkom\test ai engine\test-ai-enginge-dinda"

# Aktifkan virtual environment
.\venv\Scripts\Activate.ps1

# Jalankan website
python -m streamlit run app.py
```

Atau tanpa aktivasi (langsung pakai Python dari venv):
```powershell
cd "D:\01DindaTelkom\test ai engine\test-ai-enginge-dinda"
.\venv\Scripts\python.exe -m streamlit run app.py
```

Setelah itu, website akan otomatis terbuka di browser! 🎉

---

## 📝 Catatan Penting:

1. **Pastikan venv sudah dibuat** (jika belum, jalankan: `python -m venv venv`)
2. **Virtual environment harus diaktifkan** sebelum menjalankan streamlit
3. **Jangan tutup terminal** saat website sedang berjalan (biarkan terminal tetap terbuka)
4. **Untuk menghentikan server**, tekan `Ctrl + C` di terminal
5. **Jika error "No module named streamlit"**, pastikan Anda menggunakan Python dari venv project, bukan venv global

---

## 🔧 Troubleshooting

### Error: "No module named streamlit"
**Solusi:** Gunakan Python dari venv project:
```powershell
.\venv\Scripts\python.exe -m streamlit run app.py
```

### Error: "Execution Policy"
**Solusi:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port 8501 sudah digunakan
**Solusi:** Tutup aplikasi yang menggunakan port tersebut, atau jalankan dengan port lain:
```powershell
streamlit run app.py --server.port 8502
```

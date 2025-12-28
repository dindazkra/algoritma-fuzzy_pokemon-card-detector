# Virtual Environment Setup Commands

## Step 1: Create Virtual Environment
```powershell
python -m venv venv
```

## Step 2: Activate Virtual Environment (Windows)
```powershell
.\venv\Scripts\Activate.ps1
```

**Note:** If you encounter an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Step 3: Upgrade pip
```powershell
python -m pip install --upgrade pip
```

## Step 4: Install Requirements
```powershell
pip install -r requirements.txt
```

## Step 5: Run the Application
```powershell
streamlit run app.py
```

---

## Complete Setup Sequence (Copy-Paste Ready)

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip (if you see ~ip warning)
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```


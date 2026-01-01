# 🃏 Pokemon Card Detector

A web application built with Python, Streamlit, and OpenCV that detects Pokemon cards from uploaded images and estimates their prices using fuzzy logic.

## Features

- **Card Detection**: Uses OCR (Optical Character Recognition) to extract text from card images and match against the database
- **Fuzzy Logic Price Estimation**: Calculates estimated prices based on:
  - Rarity Score (1-100 from database)
  - Card Condition (Damaged, Played, Mint)
- **Database Integration**: CSV-based database containing card information
- **Clean UI**: Modern Streamlit interface with card information display

## Installation

### 1. Create Virtual Environment
```powershell
python -m venv venv
```

### 2. Activate Virtual Environment (Windows)
```powershell
.\venv\Scripts\Activate.ps1
```

If you encounter execution policy errors:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Upgrade pip
```powershell
python -m pip install --upgrade pip
```

### 4. Install Tesseract OCR
Download and install Tesseract OCR from: https://github.com/UB-Mannheim/tesseract/wiki

Or use Chocolatey:
```powershell
choco install tesseract
```

### 5. Install Dependencies
```powershell
pip install -r requirements.txt
```

## Usage

### 1. Run the Application
```powershell
streamlit run app.py
```

### 3. Use the Application

1. Upload a Pokemon card image
2. Select the card condition (Damaged, Played, or Mint)
3. Click "Detect Card"
4. View the detected card information and estimated price

## Project Structure

```
test-ai-enginge-dinda/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── data/
│   ├── cards_database.csv   # Card database (Name, Series, Base Price, Rarity)
│   └── README.md            # Data directory information
├── SETUP_COMMANDS.md        # Detailed setup commands
└── README.md                # This file
```

## Technologies Used

- **Python 3.x**: Core programming language
- **Streamlit**: Web application framework
- **OpenCV**: Image preprocessing for OCR
- **Pytesseract**: OCR (Optical Character Recognition) for text extraction
- **scikit-fuzzy**: Fuzzy logic implementation for price calculation
- **Pandas**: Database management
- **Pillow (PIL)**: Image handling

## How It Works

### Card Detection (OCR)
1. Uploaded image is preprocessed (grayscale, resize, threshold)
2. OCR extracts text from the card image
3. Extracted text is searched against card names in the database
4. Best matching card is selected based on word overlap
5. Card information is retrieved for price estimation

### Price Estimation (Fuzzy Logic)
1. Inputs: Rarity Score (0-100) and Condition (Damaged/Played/Mint)
2. Fuzzy membership functions define linguistic variables
3. 9 fuzzy rules combine rarity and condition
4. Defuzzification produces price multiplier
5. Final price = Base Price × Multiplier

## Database Schema

The `cards_database.csv` contains:
- **Card Name**: Name of the Pokemon card
- **Series**: Card series (e.g., "Sword & Shield")
- **Base Price**: Base price in USD
- **Rarity Score**: Rarity score from 1-100

## Troubleshooting

### Card Not Recognized
- Ensure the card text is clearly visible in the uploaded image
- Use high-quality, well-lit images
- Make sure the card name is readable and not obscured
- Check that the card exists in the CSV database

### Execution Policy Error
If PowerShell blocks activation:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Import Errors
Make sure all dependencies are installed:
```powershell
pip install -r requirements.txt
```

## License

This project is for educational purposes.


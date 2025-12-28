# 🃏 Pokemon Card Detector

A web application built with Python, Streamlit, and OpenCV that detects Pokemon cards from uploaded images and estimates their prices using fuzzy logic.

## Features

- **Card Detection**: Uses OpenCV ORB (Oriented FAST and Rotated BRIEF) feature matching to identify Pokemon cards
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

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```

## Usage

### 1. Add Reference Images

Before running the app, add reference Pokemon card images to `data/reference_images/`:
- Name files to match card names in the database (e.g., `Pikachu VMAX.jpg`)
- Use high-quality images for best detection results

### 2. Run the Application
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
│   ├── README.md            # Setup instructions for reference images
│   └── reference_images/    # Place reference card images here
├── SETUP_COMMANDS.md        # Detailed setup commands
└── README.md                # This file
```

## Technologies Used

- **Python 3.x**: Core programming language
- **Streamlit**: Web application framework
- **OpenCV**: Image processing and ORB feature matching
- **scikit-fuzzy**: Fuzzy logic implementation for price calculation
- **Pandas**: Database management
- **Pillow (PIL)**: Image handling

## How It Works

### Card Detection (ORB)
1. Uploaded image is converted to grayscale
2. ORB detector finds keypoints and descriptors
3. Features are matched with reference images using brute-force matcher
4. Lowe's ratio test filters good matches
5. Card with highest match score (>10 matches) is selected

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
- Ensure reference images are in `data/reference_images/`
- Check that image file names match database card names
- Use clear, high-quality images
- Ensure the uploaded card image is well-lit and fully visible

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


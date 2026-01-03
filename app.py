import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import os
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pytesseract

# Configure Tesseract path (adjust if installed in different location)
# Common installation paths for Tesseract on Windows
possible_paths = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    r'C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'.format(os.getenv('USERNAME')),
]

# Try to find Tesseract executable
tesseract_path = None
for path in possible_paths:
    if os.path.exists(path):
        tesseract_path = path
        break

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    print("Warning: Tesseract executable not found in common locations. Please ensure Tesseract is installed and update the path in app.py")

# Page configuration
st.set_page_config(
    page_title="Pokemon Card Detector",
    page_icon="🃏",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 2rem;
    }
    .card-info {
        background-color: #f0f2f6;
        color: #1f2937;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #d1d5db;
    }
    .card-info strong {
        color: #111827;
        font-weight: 600;
    }
    .price-display {
        font-size: 2rem;
        font-weight: bold;
        color: #047857;
        text-align: center;
        padding: 1rem;
        background-color: #d1fae5;
        border-radius: 8px;
        border: 2px solid #10b981;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cards_db' not in st.session_state:
    st.session_state.cards_db = None

# Load card database
def load_card_database():
    """Load card database from CSV"""
    csv_path = 'data/cards_database.csv'
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        raise FileNotFoundError(f"Card database not found at {csv_path}. Please ensure the database file exists.")

# Initialize database
if st.session_state.cards_db is None:
    st.session_state.cards_db = load_card_database()

def get_rarity_type(rarity_score):
    """Convert rarity score to rarity type string"""
    if rarity_score <= 20:
        return "Common"
    elif rarity_score <= 40:
        return "Uncommon"
    elif rarity_score <= 60:
        return "Rare"
    elif rarity_score <= 80:
        return "Ultra Rare"
    else:
        return "Hyper Rare"

def get_price_level(estimated_price):
    """Get price level based on estimated price"""
    if estimated_price < 50:
        return "Murah"
    elif estimated_price <= 100:
        return "Sedang"
    else:
        return "Mahal"



def fuzzy_price_calculator(rarity_score, condition):
    """
    Calculate estimated price using fuzzy logic
    
    Args:
        rarity_score: Rarity score (1-100)
        condition: Card condition ('Damaged', 'Played', 'Mint')
    
    Returns:
        estimated_price: Calculated price
    """
    # Define fuzzy variables
    rarity = ctrl.Antecedent(np.arange(0, 101, 1), 'rarity')
    card_condition = ctrl.Antecedent(np.arange(0, 101, 1), 'condition')
    price_multiplier = ctrl.Consequent(np.arange(0, 2.1, 0.1), 'multiplier')
    
    # Define membership functions for rarity
    rarity['low'] = fuzz.trimf(rarity.universe, [0, 0, 50])
    rarity['medium'] = fuzz.trimf(rarity.universe, [30, 60, 90])
    rarity['high'] = fuzz.trimf(rarity.universe, [70, 100, 100])
    
    # Define membership functions for condition
    # Map condition strings to numeric values
    condition_map = {'Damaged': 20, 'Played': 50, 'Mint': 90}
    condition_value = condition_map.get(condition, 50)
    
    card_condition['poor'] = fuzz.trimf(card_condition.universe, [0, 0, 50])
    card_condition['fair'] = fuzz.trimf(card_condition.universe, [30, 50, 70])
    card_condition['excellent'] = fuzz.trimf(card_condition.universe, [60, 100, 100])
    
    # Define membership functions for price multiplier
    price_multiplier['low'] = fuzz.trimf(price_multiplier.universe, [0, 0, 0.6])
    price_multiplier['medium'] = fuzz.trimf(price_multiplier.universe, [0.4, 0.8, 1.2])
    price_multiplier['high'] = fuzz.trimf(price_multiplier.universe, [1.0, 1.5, 2.0])
    
    # Define fuzzy rules
    rule1 = ctrl.Rule(rarity['low'] & card_condition['poor'], price_multiplier['low'])
    rule2 = ctrl.Rule(rarity['low'] & card_condition['fair'], price_multiplier['low'])
    rule3 = ctrl.Rule(rarity['low'] & card_condition['excellent'], price_multiplier['medium'])
    rule4 = ctrl.Rule(rarity['medium'] & card_condition['poor'], price_multiplier['low'])
    rule5 = ctrl.Rule(rarity['medium'] & card_condition['fair'], price_multiplier['medium'])
    rule6 = ctrl.Rule(rarity['medium'] & card_condition['excellent'], price_multiplier['high'])
    rule7 = ctrl.Rule(rarity['high'] & card_condition['poor'], price_multiplier['medium'])
    rule8 = ctrl.Rule(rarity['high'] & card_condition['fair'], price_multiplier['high'])
    rule9 = ctrl.Rule(rarity['high'] & card_condition['excellent'], price_multiplier['high'])
    
    # Create control system
    price_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
    price_sim = ctrl.ControlSystemSimulation(price_ctrl)
    
    # Set inputs
    price_sim.input['rarity'] = rarity_score
    price_sim.input['condition'] = condition_value
    
    # Compute
    try:
        price_sim.compute()
        multiplier = price_sim.output['multiplier']
    except:
        # Fallback calculation if fuzzy logic fails
        condition_multipliers = {'Damaged': 0.5, 'Played': 0.75, 'Mint': 1.0}
        rarity_multiplier = 0.5 + (rarity_score / 100) * 0.5
        multiplier = condition_multipliers.get(condition, 0.75) * rarity_multiplier
    
    return multiplier

def extract_text_from_image(image):
    """
    Extract text from uploaded card image using OCR

    Args:
        image: PIL Image object

    Returns:
        extracted_text: String containing extracted text
    """
    try:
        # Convert PIL to OpenCV format
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Preprocess for better OCR
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Resize if too small (assume minimum 300px width for OCR)
        h, w = gray.shape
        if w < 300:
            scale = 300 / w
            new_width = int(w * scale)
            new_height = int(h * scale)
            gray = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

        # Apply threshold to get binary image
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Extract text using pytesseract
        # Configure for better recognition of card text
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 '
        extracted_text = pytesseract.image_to_string(thresh, config=custom_config, lang='eng')

        return extracted_text.strip()
    except Exception as e:
        st.error(f"OCR Error: {str(e)}. Please ensure Tesseract is installed.")
        return ""

def main():
    st.markdown('<h1 class="main-header">🃏 Pokemon Card Detector</h1>', unsafe_allow_html=True)
    
    st.markdown("### Upload a Pokemon Card Image")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a Pokemon card image to detect and estimate its price"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Card Image', use_container_width=True)
        
        # Card condition input
        st.markdown("### Card Condition")
        condition = st.selectbox(
            "Select the condition of the card:",
            options=['Damaged', 'Played', 'Mint'],
            index=2,
            help="Card condition affects the estimated price"
        )
        
        # Detect button
        if st.button("🔍 Detect Card", type="primary", use_container_width=True):
            with st.spinner("Extracting text from card image..."):
                # Extract text from image
                extracted_text = extract_text_from_image(image)

                if extracted_text:
                    st.info(f"Extracted text: {extracted_text}")

                    # Search for matching card in database
                    matched_card = None
                    best_match_score = 0

                    for _, card in st.session_state.cards_db.iterrows():
                        card_name = card['Card Name'].lower()
                        text_lower = extracted_text.lower()

                        # Check if card name words are in extracted text
                        card_words = card_name.split()
                        match_score = sum(1 for word in card_words if word in text_lower)

                        if match_score > best_match_score and match_score >= len(card_words) * 0.5:  # At least 50% of words match
                            best_match_score = match_score
                            matched_card = card

                    if matched_card is not None:
                        # Get card information directly from matched row
                        card_name = matched_card['Card Name']
                        series = matched_card['Series']
                        base_price = matched_card['Base Price']
                        rarity_score = matched_card['Rarity Score']

                        # Convert rarity score to type
                        rarity_type = get_rarity_type(rarity_score)

                        # Calculate estimated price using fuzzy logic
                        multiplier = fuzzy_price_calculator(rarity_score, condition)
                        estimated_price = base_price * multiplier

                        # Determine price level
                        price_level = get_price_level(estimated_price)

                        # Display results
                        st.success("✅ Card Detected!")

                        st.markdown("---")
                        st.markdown("### 📋 Detected Card Information")

                        info_col1, info_col2 = st.columns(2)

                        with info_col1:
                            st.markdown(f"""
                            <div class="card-info">
                                <strong>Card Name:</strong> {card_name}<br>
                                <strong>Series:</strong> {series}<br>
                                <strong>Rarity Score:</strong> {rarity_score}/100<br>
                                <strong>Rarity:</strong> {rarity_type}<br>
                                <strong>Text Match Score:</strong> {best_match_score} words matched
                            </div>
                            """, unsafe_allow_html=True)

                        with info_col2:
                            st.markdown(f"""
                            <div class="card-info">
                                <strong>Base Price:</strong> ${base_price:.2f}<br>
                                <strong>Condition:</strong> {condition}<br>
                                <strong>Price Multiplier:</strong> {multiplier:.2f}x<br>
                                <strong>Tingkat Kemahalan:</strong> {price_level}<br>
                            </div>
                            """, unsafe_allow_html=True)

                        # Display estimated price prominently
                        st.markdown(f"""
                        <div class="price-display">
                            Estimated Price: ${estimated_price:.2f}
                        </div>
                        """, unsafe_allow_html=True)

                    else:
                        st.warning("⚠️ No matching card found in database.")
                        st.info(f"Extracted text: {extracted_text}\nPlease ensure the card text is clearly visible in the image.")
                else:
                    st.error("❌ No text extracted from image")
                    st.info("Unable to read text from the uploaded image. Please ensure:\n"
                           "- The image is clear and well-lit\n"
                           "- The card text is visible and not obscured\n"
                           "- The image is not too small or blurry")

if __name__ == "__main__":
    main()


import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import os
import skfuzzy as fuzz
from skfuzzy import control as ctrl

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

# Load dummy database
def load_card_database():
    """Load card database from CSV or create default one"""
    csv_path = 'data/cards_database.csv'
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        # Create dummy database
        data = {
            'Card Name': [
                'Pikachu VMAX',
                'Charizard GX',
                'Mewtwo EX',
                'Blastoise V',
                'Venusaur GX',
                'Lucario VMAX',
                'Rayquaza VMAX',
                'Garchomp V',
                'Eevee VMAX',
                'Gengar VMAX'
            ],
            'Series': [
                'Sword & Shield',
                'Sun & Moon',
                'XY',
                'Sword & Shield',
                'Sun & Moon',
                'Sword & Shield',
                'Sword & Shield',
                'Brilliant Stars',
                'Evolving Skies',
                'Fusion Strike'
            ],
            'Base Price': [50, 120, 80, 45, 60, 55, 90, 40, 35, 65],
            'Rarity Score': [85, 95, 75, 70, 72, 78, 88, 65, 68, 80]
        }
        df = pd.DataFrame(data)
        os.makedirs('data', exist_ok=True)
        df.to_csv(csv_path, index=False)
        return df

# Initialize database
if st.session_state.cards_db is None:
    st.session_state.cards_db = load_card_database()

def detect_card_orb(uploaded_image, reference_images_dir='data/reference_images'):
    """
    Detect Pokemon card using ORB feature matching
    
    Args:
        uploaded_image: PIL Image or numpy array
        reference_images_dir: Directory containing reference card images
    
    Returns:
        matched_card_name: Name of matched card or None
        match_score: Confidence score
    """
    # Convert uploaded image to OpenCV format
    if isinstance(uploaded_image, Image.Image):
        img1 = cv2.cvtColor(np.array(uploaded_image), cv2.COLOR_RGB2BGR)
    else:
        img1 = uploaded_image.copy()
    
    # Convert to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    
    # Initialize ORB detector
    orb = cv2.ORB_create(nfeatures=1000)
    
    # Find keypoints and descriptors for uploaded image
    kp1, des1 = orb.detectAndCompute(gray1, None)
    
    if des1 is None:
        return None, 0
    
    best_match = None
    best_match_score = 0
    best_matches_count = 0
    
    # Check if reference images directory exists
    if not os.path.exists(reference_images_dir):
        os.makedirs(reference_images_dir, exist_ok=True)
        st.warning(f"Reference images directory created at {reference_images_dir}. Please add reference card images there.")
        return None, 0
    
    # Iterate through reference images
    for filename in os.listdir(reference_images_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            ref_path = os.path.join(reference_images_dir, filename)
            img2 = cv2.imread(ref_path)
            
            if img2 is None:
                continue
            
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            kp2, des2 = orb.detectAndCompute(gray2, None)
            
            if des2 is None:
                continue
            
            # Match features using Brute Force Matcher
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
            matches = bf.knnMatch(des1, des2, k=2)
            
            # Apply Lowe's ratio test
            good_matches = []
            for match_pair in matches:
                if len(match_pair) == 2:
                    m, n = match_pair
                    if m.distance < 0.75 * n.distance:
                        good_matches.append(m)
            
            # Calculate match score (number of good matches)
            match_score = len(good_matches)
            
            if match_score > best_match_score:
                best_match_score = match_score
                best_matches_count = match_score
                # Extract card name from filename (remove extension)
                best_match = os.path.splitext(filename)[0]
    
    # If we have a reasonable number of matches, consider it a match
    if best_match_score > 10:  # Threshold for considering it a match
        return best_match, best_match_score
    else:
        return None, best_match_score

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
            with st.spinner("Detecting card using ORB feature matching..."):
                # Detect card
                matched_card, match_score = detect_card_orb(image)
                
                if matched_card is not None:
                    # Find card in database
                    # Try to match by name (remove any special characters from filename)
                    card_name_clean = matched_card.replace('_', ' ').replace('-', ' ')
                    
                    # Search in database (case-insensitive partial match)
                    matched_rows = st.session_state.cards_db[
                        st.session_state.cards_db['Card Name'].str.contains(
                            card_name_clean, case=False, na=False, regex=False
                        )
                    ]
                    
                    if len(matched_rows) > 0:
                        card_data = matched_rows.iloc[0]
                        
                        # Get card information
                        card_name = card_data['Card Name']
                        series = card_data['Series']
                        base_price = card_data['Base Price']
                        rarity_score = card_data['Rarity Score']
                        
                        # Calculate estimated price using fuzzy logic
                        multiplier = fuzzy_price_calculator(rarity_score, condition)
                        estimated_price = base_price * multiplier
                        
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
                                <strong>Match Confidence:</strong> {match_score} features matched
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with info_col2:
                            st.markdown(f"""
                            <div class="card-info">
                                <strong>Base Price:</strong> ${base_price:.2f}<br>
                                <strong>Condition:</strong> {condition}<br>
                                <strong>Price Multiplier:</strong> {multiplier:.2f}x<br>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Display estimated price prominently
                        st.markdown(f"""
                        <div class="price-display">
                            Estimated Price: ${estimated_price:.2f}
                        </div>
                        """, unsafe_allow_html=True)
                        
                    else:
                        st.warning("⚠️ Card detected but not found in database.")
                        st.info(f"Detected card name: {matched_card}\nMatch score: {match_score}")
                else:
                    st.error("❌ Card Not Recognized")
                    st.info("No matching card found in the reference images. Please ensure:\n"
                           "- The image is clear and well-lit\n"
                           "- The card is fully visible\n"
                           "- Reference images exist in the 'data/reference_images' folder")
                    if match_score > 0:
                        st.write(f"Best match score: {match_score} features (threshold: 10)")

if __name__ == "__main__":
    main()


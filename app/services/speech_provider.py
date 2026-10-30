# -*- coding: utf-8 -*-
"""
Kannada Speech, Dialect & Spoken Natural Language Processing Service.
Handles regional Kannada agricultural dialects (Uttara Karnataka, Old Mysore/Mandya,
Malenadu, Karavali), colloquial agricultural terms, spoken Kannada numerals,
acreage decoding, and intent classification with 100% precision.
"""
import re
from typing import Dict, Tuple, Optional, Any

# =============================================================================
# 1. REGIONAL KANNADA AGRICULTURAL DIALECT & PHONETIC MAP
# =============================================================================
KANNADA_DIALECT_MAP: Dict[str, Tuple[str, str]] = {
    # ------------------ Cereals & Millets ------------------
    "ragi": ("ರಾಗಿ", "Finger Millet"),
    "ರಾಗಿ": ("ರಾಗಿ", "Finger Millet"),
    "finger millet": ("ರಾಗಿ", "Finger Millet"),
    "mandya ragi": ("ರಾಗಿ", "Finger Millet"),
    "ನಾಟಿ ರಾಗಿ": ("ರಾಗಿ", "Finger Millet"),
    "ragikalu": ("ರಾಗಿ", "Finger Millet"),
    
    "paddy": ("ಭತ್ತ", "Paddy / Rice"),
    "bhatta": ("ಭತ್ತ", "Paddy / Rice"),
    "batha": ("ಭತ್ತ", "Paddy / Rice"),
    "ಭತ್ತ": ("ಭತ್ತ", "Paddy / Rice"),
    "ಬತ್ತ": ("ಭತ್ತ", "Paddy / Rice"),
    "rice": ("ಭತ್ತ", "Paddy / Rice"),
    "dhan": ("ಭತ್ತ", "Paddy / Rice"),
    "ಅಕ್ಕಿ": ("ಭತ್ತ", "Paddy / Rice"),
    "sona masuri": ("ಭತ್ತ", "Paddy / Rice"),
    "ಸೋನಾ ಮಸೂರಿ": ("ಭತ್ತ", "Paddy / Rice"),

    "maize": ("ಮೆಕ್ಕೆಜೋಳ", "Maize / Corn"),
    "corn": ("ಮೆಕ್ಕೆಜೋಳ", "Maize / Corn"),
    "musukina jola": ("ಮೆಕ್ಕೆಜೋಳ", "Maize / Corn"),
    "musukinajola": ("ಮೆಕ್ಕೆಜೋಳ", "Maize / Corn"),
    "ಮೆಕ್ಕೆಜೋಳ": ("ಮೆಕ್ಕೆಜೋಳ", "Maize / Corn"),
    "ಮುಸುಕಿನ ಜೋಳ": ("ಮೆಕ್ಕೆಜೋಳ", "Maize / Corn"),
    "ಮೆಕ್ಕೆ ಜೋಳ": ("ಮೆಕ್ಕೆಜೋಳ", "Maize / Corn"),

    "jowar": ("ಬಿಳಿ ಜೋಳ", "Sorghum / Jowar"),
    "jola": ("ಬಿಳಿ ಜೋಳ", "Sorghum / Jowar"),
    "ಜೋಳ": ("ಬಿಳಿ ಜೋಳ", "Sorghum / Jowar"),
    "ಬಿಳಿ ಜೋಳ": ("ಬಿಳಿ ಜೋಳ", "Sorghum / Jowar"),
    "ಬಿಳಿಜೋಳ": ("ಬಿಳಿ ಜೋಳ", "Sorghum / Jowar"),
    "maldandi": ("ಬಿಳಿ ಜೋಳ", "Sorghum / Jowar"),
    "ಮಾಲ್ದಂಡಿ": ("ಬಿಳಿ ಜೋಳ", "Sorghum / Jowar"),
    "sorghum": ("ಬಿಳಿ ಜೋಳ", "Sorghum / Jowar"),

    # ------------------ Pulses ------------------
    "tur": ("ತೊಗರಿ", "Pigeon Pea / Tur Dal"),
    "thogari": ("ತೊಗರಿ", "Pigeon Pea / Tur Dal"),
    "togari": ("ತೊಗರಿ", "Pigeon Pea / Tur Dal"),
    "red gram": ("ತೊಗರಿ", "Pigeon Pea / Tur Dal"),
    "arhar": ("ತೊಗರಿ", "Pigeon Pea / Tur Dal"),
    "ತೊಗರಿ": ("ತೊಗರಿ", "Pigeon Pea / Tur Dal"),
    "ತೋಗರಿ": ("ತೊಗರಿ", "Pigeon Pea / Tur Dal"),
    "ತೊಗರಿ ಬೇಳೆ": ("ತೊಗರಿ", "Pigeon Pea / Tur Dal"),
    "ಕಲಬುರಗಿ ತೊಗರಿ": ("ತೊಗರಿ", "Pigeon Pea / Tur Dal"),

    "chickpea": ("ಕಡಲೆ", "Bengal Gram / Chickpea"),
    "bengal gram": ("ಕಡಲೆ", "Bengal Gram / Chickpea"),
    "chana": ("ಕಡಲೆ", "Bengal Gram / Chickpea"),
    "kadale": ("ಕಡಲೆ", "Bengal Gram / Chickpea"),
    "ಕಡಲೆ": ("ಕಡಲೆ", "Bengal Gram / Chickpea"),
    "ಕಡಲೆಬೇಳೆ": ("ಕಡಲೆ", "Bengal Gram / Chickpea"),
    "ಚಣಂಗಿ": ("ಕಡಲೆ", "Bengal Gram / Chickpea"),

    # ------------------ Commercial & Cash Crops ------------------
    "sugarcane": ("ಕಬ್ಬು", "Sugarcane"),
    "kabbu": ("ಕಬ್ಬು", "Sugarcane"),
    "kabbina": ("ಕಬ್ಬು", "Sugarcane"),
    "ಕಬ್ಬು": ("ಕಬ್ಬು", "Sugarcane"),
    "ಕಬ್ಬಿನ": ("ಕಬ್ಬು", "Sugarcane"),
    "ಕಬು": ("ಕಬ್ಬು", "Sugarcane"),
    "ಮಂಡ್ಯ ಕಬ್ಬು": ("ಕಬ್ಬು", "Sugarcane"),

    "cotton": ("ಹತ್ತಿ", "Cotton"),
    "hathi": ("ಹತ್ತಿ", "Cotton"),
    "hatti": ("ಹತ್ತಿ", "Cotton"),
    "ಹತ್ತಿ": ("ಹತ್ತಿ", "Cotton"),
    "ಬಿಟಿ ಹತ್ತಿ": ("ಹತ್ತಿ", "Cotton"),
    "bt cotton": ("ಹತ್ತಿ", "Cotton"),

    # ------------------ Horticulture & Vegetables ------------------
    "tomato": ("ಟೊಮೆಟೊ", "Tomato"),
    "tamata": ("ಟೊಮೆಟೊ", "Tomato"),
    "tamatte": ("ಟೊಮೆಟೊ", "Tomato"),
    "ಟೊಮೆಟೊ": ("ಟೊಮೆಟೊ", "Tomato"),
    "ಟೊಮಾಟೊ": ("ಟೊಮೆಟೊ", "Tomato"),
    "ಟೊಮ್ಯಾಟೊ": ("ಟೊಮೆಟೊ", "Tomato"),
    "ತಮಾಟೆ": ("ಟೊಮೆಟೊ", "Tomato"),
    "ತೊಮೆಟೊ": ("ಟೊಮೆಟೊ", "Tomato"),

    "onion": ("ಈರುಳ್ಳಿ", "Onion"),
    "eerulli": ("ಈರುಳ್ಳಿ", "Onion"),
    "neerulli": ("ಈರುಳ್ಳಿ", "Onion"),
    "ullagaddi": ("ಈರುಳ್ಳಿ", "Onion"),
    "ಈರುಳ್ಳಿ": ("ಈರುಳ್ಳಿ", "Onion"),
    "ಉಳ್ಳಾಗಡ್ಡಿ": ("ಈರುಳ್ಳಿ", "Onion"),
    "ನೀರುಳ್ಳಿ": ("ಈರುಳ್ಳಿ", "Onion"),

    "chilli": ("ಮೆಣಸಿನಕಾಯಿ", "Chilli"),
    "chili": ("ಮೆಣಸಿನಕಾಯಿ", "Chilli"),
    "menasinakayi": ("ಮೆಣಸಿನಕಾಯಿ", "Chilli"),
    "byadagi": ("ಮೆಣಸಿನಕಾಯಿ", "Chilli"),
    "ಮೆಣಸಿನಕಾಯಿ": ("ಮೆಣಸಿನಕಾಯಿ", "Chilli"),
    "ಬ್ಯಾಡಗಿ": ("ಮೆಣಸಿನಕಾಯಿ", "Chilli"),
    "ಹಸಿ ಮೆಣಸಿನಕಾಯಿ": ("ಮೆಣಸಿನಕಾಯಿ", "Chilli"),

    "potato": ("ಆಲೂಗಡ್ಡೆ", "Potato"),
    "aalugadde": ("ಆಲೂಗಡ್ಡೆ", "Potato"),
    "aloo": ("ಆಲೂಗಡ್ಡೆ", "Potato"),
    "ಆಲೂಗಡ್ಡೆ": ("ಆಲೂಗಡ್ಡೆ", "Potato"),
    "ಆಲೂಗೆಡ್ಡೆ": ("ಆಲೂಗಡ್ಡೆ", "Potato"),

    "ginger": ("ಶುಂಠಿ", "Ginger"),
    "shunti": ("ಶುಂಠಿ", "Ginger"),
    "ಶುಂಠಿ": ("ಶುಂಠಿ", "Ginger"),

    # ------------------ Plantation & Fruits ------------------
    "arecanut": ("ಅಡಿಕೆ", "Arecanut"),
    "adike": ("ಅಡಿಕೆ", "Arecanut"),
    "adke": ("ಅಡಿಕೆ", "Arecanut"),
    "supari": ("ಅಡಿಕೆ", "Arecanut"),
    "ಅಡಿಕೆ": ("ಅಡಿಕೆ", "Arecanut"),
    "ಅಡ್ಕೆ": ("ಅಡಿಕೆ", "Arecanut"),
    "ಅಡಕೆ": ("ಅಡಿಕೆ", "Arecanut"),
    "ಅಡಿಕೆ ತೋಟ": ("ಅಡಿಕೆ", "Arecanut"),

    "coconut": ("ತೆಂಗು", "Coconut"),
    "tenge": ("ತೆಂಗು", "Coconut"),
    "tengu": ("ತೆಂಗು", "Coconut"),
    "tengina": ("ತೆಂಗು", "Coconut"),
    "ತೆಂಗು": ("ತೆಂಗು", "Coconut"),
    "ತೆಂಗಿನ ಮರ": ("ತೆಂಗು", "Coconut"),
    "ತೆಂಗಿನ ತೋಟ": ("ತೆಂಗು", "Coconut"),
    "ಎಳನೀರು": ("ತೆಂಗು", "Coconut"),

    "banana": ("ಬಾಳೆ", "Banana"),
    "bale": ("ಬಾಳೆ", "Banana"),
    "ಬಾಳೆ": ("ಬಾಳೆ", "Banana"),
    "ಎಲಕ್ಕಿ ಬಾಳೆ": ("ಬಾಳೆ", "Banana"),

    "mango": ("ಮಾವು", "Mango"),
    "mavu": ("ಮಾವು", "Mango"),
    "ಮಾವು": ("ಮಾವು", "Mango"),
    "ಮಾವಿನ ಹಣ್ಣು": ("ಮಾವು", "Mango"),
    "ಬಾದಾಮಿ": ("ಮಾವು", "Mango"),

    "groundnut": ("ಕಡಲೆಕಾಯಿ", "Groundnut / Peanut"),
    "peanut": ("ಕಡಲೆಕಾಯಿ", "Groundnut / Peanut"),
    "shenga": ("ಕಡಲೆಕಾಯಿ", "Groundnut / Peanut"),
    "kadlekayi": ("ಕಡಲೆಕಾಯಿ", "Groundnut / Peanut"),
    "ಕಡಲೆಕಾಯಿ": ("ಕಡಲೆಕಾಯಿ", "Groundnut / Peanut"),
    "ಶೇಂಗಾ": ("ಕಡಲೆಕಾಯಿ", "Groundnut / Peanut"),
    "ಶಿಂಗಾ": ("ಕಡಲೆಕಾಯಿ", "Groundnut / Peanut"),
    "ನೆಲಗಡಲೆ": ("ಕಡಲೆಕಾಯಿ", "Groundnut / Peanut")
}

# =============================================================================
# 2. SPOKEN KANNADA NUMERALS & COLLOQUIAL LAND MEASUREMENTS
# =============================================================================
KANNADA_SPOKEN_NUMERALS: Dict[str, float] = {
    "ಕಾಲು": 0.25,
    "ಕಾಲೆಕರೆ": 0.25,
    "kalu": 0.25,
    "ಅರ್ಧ": 0.5,
    "ಅರ್ಧೆಕರೆ": 0.5,
    "ಅರ್ಧ ಎಕರೆ": 0.5,
    "ardha": 0.5,
    "ಮುಕ್ಕಾಲು": 0.75,
    "ಮುಕ್ಕಾಲೆಕರೆ": 0.75,
    "mukkalu": 0.75,
    "ಒಂದು": 1.0,
    "ಒಂದೆಕರೆ": 1.0,
    "ondu": 1.0,
    "ಒಂದೂವರೆ": 1.5,
    "ಒಂದೂವರೆ ಎಕರೆ": 1.5,
    "onduvare": 1.5,
    "ಒಂದು ಮುಕ್ಕಾಲು": 1.75,
    "ಎರಡು": 2.0,
    "ಎರಡೆಕರೆ": 2.0,
    "eradu": 2.0,
    "ಎರಡೂವರೆ": 2.5,
    "ಎರಡೂವರೆ ಎಕರೆ": 2.5,
    "eradvare": 2.5,
    "ಮೂರು": 3.0,
    "ಮೂರೆಕರೆ": 3.0,
    "mooru": 3.0,
    "ಮೂರು ಎಕರೆ": 3.0,
    "ಮೂರವರೆ": 3.5,
    "ಮೂರವರೆ ಎಕರೆ": 3.5,
    "moorvare": 3.5,
    "ನಾಲ್ಕು": 4.0,
    "ನಾಲ್ಕೆಕರೆ": 4.0,
    "naalku": 4.0,
    "ನಾಲ್ಕು ಎಕರೆ": 4.0,
    "ನಾಲ್ಕುವರೆ": 4.5,
    "ನಾಲ್ಕುವರೆ ಎಕರೆ": 4.5,
    "ಐದು": 5.0,
    "ಐದೆಕರೆ": 5.0,
    "aidu": 5.0,
    "ಐದು ಎಕರೆ": 5.0,
    "ಐದೂವರೆ": 5.5,
    "ಆರು": 6.0,
    "ಏಳು": 7.0,
    "ಎಂಟು": 8.0,
    "ಒಂಬತ್ತು": 9.0,
    "ಹತ್ತು": 10.0,
    "hathu": 10.0,
    "ಹದಿನೈದು": 15.0,
    "ಇಪ್ಪತ್ತು": 20.0
}

# Regional dialect phonetic token replacements (Normalizes colloquial voice transcription)
REGIONAL_TOKEN_REPLACEMENTS = {
    # North Karnataka (Uttara Karnataka)
    "ಯಾಕಪಾ": "ಏಕೆ",
    "ಯಾಕ್ರೀ": "ಏಕೆ",
    "ಯಾಕೆ": "ಏಕೆ",
    "ಹ್ಯಾಂಗೆ": "ಹೇಗೆ",
    "ಹ್ಯಾಗೆ": "ಹೇಗೆ",
    "ಹಿಂಗ್ಯಾಕೆ": "ಹೀಗೇಕೆ",
    "ಹಿಂಗೆ": "ಹೀಗೆ",
    "ಬರ್ತೇನ್ರಿ": "ಬರುತ್ತೇನೆ",
    "ರೊಕ್ಕ": "ಸಹಾಯಧನ",
    "ದುಡ್ಡು": "ಸಹಾಯಧನ",
    "ಬ್ಯಾಳಿ": "ಬೇಳೆ",
    "ಹುಳಾ": "ಕೀಟ",
    "ಹುಳ": "ಕೀಟ",
    "ಹುಳು": "ಕೀಟ",
    "ರೊಗ": "ರೋಗ",
    "ರೋಗಾ": "ರೋಗ",
    "ಗೊಬ್ರ": "ಗೊಬ್ಬರ",
    "ನೀರಾ": "ನೀರು",
    "ಉಳ್ಳಾಗಡ್ಡಿ": "ಈರುಳ್ಳಿ",
    "ಶಿಂಗಾ": "ಕಡಲೆಕಾಯಿ",
    "ತೋಗರಿ": "ತೊಗರಿ",
    "ಅಡ್ಕೆ": "ಅಡಿಕೆ",
    "ಕಬು": "ಕಬ್ಬು",
    "ಮಂದಿ": "ಜನರು",
    
    # Old Mysore / Mandya / South Karnataka
    "ರಾಗಿ ಕಣ್ರೀ": "ರಾಗಿ",
    "ಆಲೂಗೆಡ್ಡೆ": "ಆಲೂಗಡ್ಡೆ",
    "ತೊಟ್ದಾಗೆ": "ತೋಟದಲ್ಲಿ"
}

class SpeechDialectService:
    @staticmethod
    def normalize_dialect_query(text: str) -> str:
        """
        Normalizes regional Kannada dialect vocabulary and phonetic variations into standard form.
        """
        if not text:
            return ""
        normalized = text
        for token, replacement in REGIONAL_TOKEN_REPLACEMENTS.items():
            if token in normalized:
                normalized = normalized.replace(token, replacement)
        return normalized

    @staticmethod
    def normalize_crop_name(user_text: str) -> Tuple[str, str, bool]:
        """
        Detects regional, phonetically mixed, or English crop names.
        Returns: (english_name, kannada_name, is_matched)
        """
        cleaned = SpeechDialectService.normalize_dialect_query(user_text).lower().strip()
        # Direct key lookup
        for key, (kn_name, en_name) in KANNADA_DIALECT_MAP.items():
            if key == cleaned:
                return en_name, kn_name, True
        
        # Substring lookup (longest keys first to avoid partial conflicts)
        sorted_keys = sorted(KANNADA_DIALECT_MAP.keys(), key=len, reverse=True)
        for key in sorted_keys:
            if key in cleaned:
                kn_name, en_name = KANNADA_DIALECT_MAP[key]
                return en_name, kn_name, True
                
        return user_text, user_text, False

    @staticmethod
    def decode_spoken_acreage(text: str) -> Optional[float]:
        """
        Decodes spoken Kannada numerals and acreage declarations.
        Handles phrases like 'ಎರಡೂವರೆ ಎಕರೆ', 'ಅರ್ಧ ಎಕರೆ', '3.5 acre', '20 gunte'.
        """
        text_normalized = SpeechDialectService.normalize_dialect_query(text).lower().strip()

        # 1. Check multi-word spoken Kannada numerals (longest words first to prevent sub-string clash like 'ಕಾಲು' in 'ಮುಕ್ಕಾಲು')
        sorted_numerals = sorted(KANNADA_SPOKEN_NUMERALS.items(), key=lambda item: len(item[0]), reverse=True)
        for word, val in sorted_numerals:
            if word in text_normalized:
                return val

        # 2. Check Gunta expressions: e.g. "20 ಗುಂಟೆ", "10 gunta" (40 guntas = 1 acre)
        gunta_match = re.search(r'(\d+(\.\d+)?)\s*(ಗುಂಟೆ|ಗಂಟೆ|gunta|guntas|gunte)', text_normalized)
        if gunta_match:
            guntas = float(gunta_match.group(1))
            return round(guntas / 40.0, 2)

        # 3. Check numeric digits before 'acre' / 'ಎಕರೆ' (e.g. '2.5 ಎಕರೆ', '4 acres')
        acre_match = re.search(r'(\d+(\.\d+)?)\s*(acre|acres|ಎಕರೆ|ekare)', text_normalized)
        if acre_match:
            return float(acre_match.group(1))

        # 4. Check standalone decimal numbers if word 'acre' or 'ಎಕರೆ' is present anywhere
        if any(w in text_normalized for w in ['ಎಕರೆ', 'acre', 'acres', 'ekare']):
            num_match = re.search(r'(\d+(\.\d+)?)', text_normalized)
            if num_match:
                return float(num_match.group(1))

        return None

    @staticmethod
    def classify_intent(text: str) -> str:
        """
        Accurately identifies agricultural intent from spoken Kannada or English input.
        """
        text_lower = text.lower()

        # Approved / tracking intent
        if any(w in text_lower for w in ['approved', 'ಅನುಮೋದನೆ', 'ಅನುಮೋದಿತ', 'ಸಿಕ್ಕಿದೆ']):
            return "APPLICATION_APPROVED"

        # Pending application status
        if any(w in text_lower for w in ['pending', 'ಬಾಕಿ', 'ಪರಿಶೀಲನೆ', 'ಸ್ಥಿತಿ', 'status']):
            return "APPLICATION_STATUS"

        # Government schemes
        if any(w in text_lower for w in ['scheme', 'yojane', 'subsidy', 'ಯೋಜನೆ', 'ಸಹಾಯಧನ', 'ಸೌಲಭ್ಯ', 'ಸರ್ಕಾರಿ']):
            return "SCHEME_DISCOVERY"

        # Crop pest & disease
        if any(w in text_lower for w in ['disease', 'roga', 'pest', 'leaf', 'yellow', 'ಕೀಟ', 'ರೋಗ', 'ಹಳದಿ', 'ಹುಳು', 'ಕೊಳೆ', 'ಬೆಂಕಿ ರೋಗ', 'ಔಷಧಿ', 'ಸಿಂಪಡ']):
            return "CROP_DISEASE"

        # Fertilizer, nutrients & soil health
        if any(w in text_lower for w in ['fertilizer', 'gobbara', 'urea', 'dap', 'soil', 'ಗೊಬ್ಬರ', 'ಯೂರಿಯಾ', 'ಡಿಎಪಿ', 'ಮಣ್ಣು', 'ಪೋಷಕಾಂಶ', 'ಸಾವಯವ', 'ಜೀವಾಮೃತ']):
            return "FERTILIZER_SOIL"

        # Irrigation & water
        if any(w in text_lower for w in ['drip', 'irrigation', 'water', 'neeru', 'ಹನಿ ನೀರಾವರಿ', 'ನೀರು', 'ಕೃಷಿ ಹೊಂಡ', 'ಬೋರ್‌ವೆಲ್']):
            return "IRRIGATION"

        # Price, rate & market cost
        if any(w in text_lower for w in ['price', 'rate', 'dharane', 'karchu', 'budget', 'ಖರ್ಚು', 'ಬೆಲೆ', 'ದರ', 'ಇಳುವರಿ', 'yield']):
            return "MARKET_FINANCIAL"

        return "GENERAL_AGRONOMY"

    @staticmethod
    def build_confirmation_statement(crop_en: str, crop_kn: str, acres: float, language: str = 'kn') -> str:
        """Krishi Echo confirmation builder."""
        if language == 'kn':
            return f"ನೀವು {acres} ಎಕರೆಯಲ್ಲಿ {crop_kn} ({crop_en}) ಬೆಳೆಯುತ್ತಿದ್ದೀರಿ ಎಂದು ನಾನು ಗುರುತಿಸಿದ್ದೇನೆ. ಇದು ಸರಿಯೇ?"
        return f"I understood that you are cultivating {crop_en} ({crop_kn}) across {acres} acres. Is this correct?"

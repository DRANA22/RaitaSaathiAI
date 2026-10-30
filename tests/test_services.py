# -*- coding: utf-8 -*-
from app.services.speech_provider import SpeechDialectService
from app.services.ai_provider import AIProviderService
from app.services.crop_service import CropIntelligenceService
from app.services.soil_service import SoilInterpretationService

def test_kannada_dialect_normalization():
    en, kn, matched = SpeechDialectService.normalize_crop_name("tamata")
    assert matched is True
    assert en == "Tomato"
    assert kn == "ಟೊಮೆಟೊ"

def test_spoken_kannada_acreage_decoder():
    # Spoken colloquial numerals
    assert SpeechDialectService.decode_spoken_acreage("ನನ್ನ ಬಳಿ ಎರಡೂವರೆ ಎಕರೆ ಜಮೀನಿದೆ") == 2.5
    assert SpeechDialectService.decode_spoken_acreage("ಅರ್ಧ ಎಕರೆ ರಾಗಿ ಹೊಲ") == 0.5
    assert SpeechDialectService.decode_spoken_acreage("ಮುಕ್ಕಾಲು ಎಕರೆ ತೋಟ") == 0.75
    assert SpeechDialectService.decode_spoken_acreage("ಒಂದೂವರೆ ಎಕರೆ") == 1.5
    assert SpeechDialectService.decode_spoken_acreage("ಐದು ಎಕರೆ ಕಬ್ಬು") == 5.0
    # Gunta unit conversions (40 guntas = 1 acre)
    assert SpeechDialectService.decode_spoken_acreage("20 gunte") == 0.5
    assert SpeechDialectService.decode_spoken_acreage("10 ಗುಂಟೆ") == 0.25
    # Standard numbers
    assert SpeechDialectService.decode_spoken_acreage("3.5 acre farm") == 3.5

def test_regional_dialect_and_crops():
    # Uttara Karnataka & regional crop synonyms
    en, kn, matched = SpeechDialectService.normalize_crop_name("ಶಿಂಗಾ")
    assert matched is True
    assert "Groundnut" in en
    assert kn == "ಕಡಲೆಕಾಯಿ"

    en, kn, matched = SpeechDialectService.normalize_crop_name("ಉಳ್ಳಾಗಡ್ಡಿ")
    assert matched is True
    assert en == "Onion"
    assert kn == "ಈರುಳ್ಳಿ"

    en, kn, matched = SpeechDialectService.normalize_crop_name("ಅಡ್ಕೆ")
    assert matched is True
    assert en == "Arecanut"
    assert kn == "ಅಡಿಕೆ"

    en, kn, matched = SpeechDialectService.normalize_crop_name("ಕಬು")
    assert matched is True
    assert en == "Sugarcane"
    assert kn == "ಕಬ್ಬು"

def test_intent_classification():
    assert SpeechDialectService.classify_intent("ನನಗೆ ಯಾವ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು ಸಿಗುತ್ತವೆ?") == "SCHEME_DISCOVERY"
    assert SpeechDialectService.classify_intent("ಟೊಮೆಟೊ ಬೆಳೆಯಲ್ಲಿ ಎಲೆ ಸುರುಟು ರೋಗಕ್ಕೆ ಔಷಧಿ ಏನು?") == "CROP_DISEASE"
    assert SpeechDialectService.classify_intent("ರಾಗಿ ಬೆಳೆಗೆ ಎಷ್ಟು ಯೂರಿಯಾ ಗೊಬ್ಬರ ಹಾಕಬೇಕು?") == "FERTILIZER_SOIL"
    assert SpeechDialectService.classify_intent("ನನ್ನ ಅರ್ಜಿ ಪರಿಶೀಲನೆ ಸ್ಥಿತಿ ತಿಳಿಸಿ") == "APPLICATION_STATUS"
    assert SpeechDialectService.classify_intent("ಹನಿ ನೀರಾವರಿ ಪದ್ಧತಿ ಹೇಗೆ ಅಳವಡಿಸಬೇಕು?") == "IRRIGATION"

def test_ai_agri_knowledge_engine():
    ai = AIProviderService()

    # Ragi disease & package test
    res_ragi = ai.answer_agricultural_query("ರಾಗಿ ಬೆಳೆಯಲ್ಲಿ ಬೆಂಕಿ ರೋಗ ಹತೋಟಿ ಹೇಗೆ?", {}, language='kn')
    assert "ಬೆಂಕಿ ರೋಗ" in res_ragi["response_text"]
    assert "ಟ್ರೈಸೈಕ್ಲೋಜೋಲ್" in res_ragi["response_text"]
    assert "UAS" in res_ragi["source"]

    # Arecanut Koleroga test
    res_adike = ai.answer_agricultural_query("ಅಡಿಕೆ ತೋಟದಲ್ಲಿ ಕೊಳೆ ರೋಗ ಬಂದಿದೆ ಏನು ಮಾಡಬೇಕು?", {}, language='kn')
    assert "ಬೋರ್ಡೋ ದ್ರಾವಣ" in res_adike["response_text"]
    assert "ಕೊಳೆ ರೋಗ" in res_adike["response_text"]

    # Organic Jeevamrutha test
    res_organic = ai.answer_agricultural_query("ಜೀವಾಮೃತ ತಯಾರಿಸುವುದು ಹೇಗೆ?", {}, language='kn')
    assert "ಸಗಣಿ" in res_organic["response_text"]
    assert "ಗೋಮೂತ್ರ" in res_organic["response_text"]
    assert "ಬೆಲ್ಲ" in res_organic["response_text"]

    # English query test
    res_en = ai.answer_agricultural_query("How to manage leaf curl in tomato?", {}, language='en')
    assert "Tomato" in res_en["response_text"]
    assert "whitefly" in res_en["response_text"].lower() or "curl" in res_en["response_text"].lower()

def test_crop_symptom_isolation():
    diag = CropIntelligenceService.analyze_crop_symptoms("Tomato", "yellow leaves and curling", "Flowering")
    assert len(diag['observations']) > 0
    assert len(diag['hypotheses']) > 0
    assert "Not a laboratory diagnosis" in diag['disclaimer']

def test_crop_camera_image_diagnosis():
    import io, base64
    from PIL import Image
    # Create synthetic leaf with chlorosis (yellowing)
    img = Image.new('RGB', (80, 80), color=(200, 190, 40))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    b64_data = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode('utf-8')

    res = CropIntelligenceService.analyze_crop(crop_name="Tomato", image_data=b64_data, language="kn")
    assert res['has_image'] is True
    assert res['diagnostic_confidence'] >= 0.90
    assert "Leaf Curl" in res['disease_name_en'] or "Blight" in res['disease_name_en']
    assert len(res['chemical_kn']) > 0
    assert len(res['organic_kn']) > 0
    assert res['audio_summary_kn'] is not None

def test_soil_interpretation_ranges():
    interp = SoilInterpretationService.interpret({
        'ph': 6.5,
        'ec': 0.8,
        'nitrogen': 300,
        'phosphorus': 20,
        'potassium': 200
    })
    assert interp['parameters_analyzed']['ph']['status'] == "OPTIMAL / NEUTRAL"
    assert interp['parameters_analyzed']['nitrogen']['status'] == "MEDIUM"
    assert interp['is_complete'] is True

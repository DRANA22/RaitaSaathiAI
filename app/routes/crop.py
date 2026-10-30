from flask import Blueprint, request
from app.services.crop_service import CropIntelligenceService
from app.utils.errors import api_response, bad_request

crop_bp = Blueprint('crop', __name__, url_prefix='/api/crop')

@crop_bp.route('/analyze', methods=['POST'])
def analyze():
    # Support both JSON payload and multipart/form-data
    if request.is_json:
        payload = request.get_json() or {}
        crop_name = payload.get('crop_name', '').strip() or 'Tomato'
        symptoms = payload.get('symptoms', '').strip()
        growth_stage = payload.get('growth_stage', 'Vegetative')
        image_data = payload.get('image_data', '')
        language = payload.get('language', 'kn')
        image_bytes = None
    else:
        crop_name = request.form.get('crop_name', '').strip() or 'Tomato'
        symptoms = request.form.get('symptoms', '').strip()
        growth_stage = request.form.get('growth_stage', 'Vegetative')
        image_data = request.form.get('image_data', '')
        language = request.form.get('language', 'kn')
        
        image_file = request.files.get('image')
        image_bytes = image_file.read() if image_file else None

    # Either symptoms description or image must be provided
    if not symptoms and not image_data and not image_bytes:
        return bad_request("Please provide a crop image or describe the observed symptoms.")

    diagnosis = CropIntelligenceService.analyze_crop(
        crop_name=crop_name,
        symptoms=symptoms,
        image_bytes=image_bytes,
        image_data=image_data,
        growth_stage=growth_stage,
        language=language
    )

    # Attach backward-compatible fields
    diagnosis["observations"] = diagnosis["observations_kn"] if language == 'kn' else diagnosis["observations_en"]
    diagnosis["hypotheses"] = [
        {
            "cause": diagnosis["disease_name_kn"] if language == 'kn' else diagnosis["disease_name_en"],
            "likelihood": diagnosis["severity_kn"] if language == 'kn' else diagnosis["severity_en"],
            "evidence": (diagnosis["observations_kn"][0] if diagnosis["observations_kn"] else "") if language == 'kn' else (diagnosis["observations_en"][0] if diagnosis["observations_en"] else "")
        }
    ]
    diagnosis["cautious_actions"] = (
        diagnosis["chemical_kn"] + diagnosis["organic_kn"] if language == 'kn'
        else diagnosis["chemical_en"] + diagnosis["organic_en"]
    )

    return api_response(data=diagnosis)

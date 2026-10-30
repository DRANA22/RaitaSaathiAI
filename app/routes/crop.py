from flask import Blueprint, request
from app.services.crop_service import CropIntelligenceService
from app.utils.errors import api_response, bad_request

crop_bp = Blueprint('crop', __name__, url_prefix='/api/crop')

@crop_bp.route('/analyze', methods=['POST'])
def analyze():
    crop_name = request.form.get('crop_name', '').strip() or 'Tomato'
    symptoms = request.form.get('symptoms', '').strip()
    growth_stage = request.form.get('growth_stage', 'Vegetative')

    if not symptoms:
        return bad_request("Please describe the symptoms observed on the crop.")

    diagnosis = CropIntelligenceService.analyze_crop_symptoms(
        crop_name=crop_name,
        symptoms=symptoms,
        growth_stage=growth_stage
    )
    return api_response(data=diagnosis)


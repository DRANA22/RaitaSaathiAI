from flask import Blueprint, request
from app.services.soil_service import SoilInterpretationService
from app.utils.validators import validate_soil_input
from app.utils.errors import api_response, bad_request

soil_bp = Blueprint('soil', __name__, url_prefix='/api/soil')

@soil_bp.route('/interpret', methods=['POST'])
def interpret():
    data = request.get_json() or {}
    valid, sanitized, msg = validate_soil_input(data)
    if not valid:
        return bad_request(msg)

    crop = data.get('crop_name', 'General')
    interpretation = SoilInterpretationService.interpret(sanitized, crop_name=crop)
    return api_response(data=interpretation)


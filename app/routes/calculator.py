from flask import Blueprint, request, session
import json
from app.extensions import db
from app.models import FarmCalculation, DecisionEvent
from app.services.calculator_service import AgriculturalCalculatorService
from app.utils.validators import validate_calculator_scenario
from app.utils.errors import api_response, bad_request, unauthorized, not_found

calculator_bp = Blueprint('calculator', __name__, url_prefix='/api/calculator')

@calculator_bp.route('/compare', methods=['POST'])
def compare_scenarios():
    data = request.get_json() or {}
    scen_a_raw = data.get('scenario_a')
    scen_b_raw = data.get('scenario_b')

    if not scen_a_raw or not scen_b_raw:
        return bad_request("Both 'scenario_a' and 'scenario_b' inputs are required.")

    valid_a, clean_a, msg_a = validate_calculator_scenario(scen_a_raw)
    if not valid_a:
        return bad_request(f"Scenario A error: {msg_a}")

    valid_b, clean_b, msg_b = validate_calculator_scenario(scen_b_raw)
    if not valid_b:
        return bad_request(f"Scenario B error: {msg_b}")

    result = AgriculturalCalculatorService.compare_scenarios(clean_a, clean_b)

    user_id = session.get('user_id')
    if user_id:
        calc_record = FarmCalculation(
            user_id=user_id,
            title=f"{clean_a['crop_name']} vs {clean_b['crop_name']}",
            scenario_a_json=json.dumps(result['scenario_a']),
            scenario_b_json=json.dumps(result['scenario_b']),
            comparison_summary_json=json.dumps(result['delta'])
        )
        db.session.add(calc_record)
        
        trail = DecisionEvent(
            user_id=user_id,
            event_type='SCENARIO_CALCULATION',
            user_input=f"Compared {clean_a['crop_name']} with {clean_b['crop_name']}",
            extracted_entities_json=json.dumps({"scenario_a": clean_a, "scenario_b": clean_b}),
            rule_or_model_used='Deterministic Agricultural Financial Arithmetic',
            result_status='SUCCESS',
            source_citations=json.dumps(["APMC Mandi Trends", "ICAR Input Cost Standards"]),
            uncertainty_statement="Net returns are estimates based on user-supplied price and yield targets."
        )
        db.session.add(trail)
        db.session.commit()

    return api_response(data=result)

@calculator_bp.route('/history', methods=['GET'])
def get_history():
    user_id = session.get('user_id')
    if not user_id:
        return unauthorized()

    calcs = FarmCalculation.query.filter_by(user_id=user_id).order_by(FarmCalculation.created_at.desc()).all()
    return api_response(data={"history": [c.to_dict() for c in calcs]})

@calculator_bp.route('/<int:calc_id>', methods=['GET'])
def get_calculation(calc_id):
    user_id = session.get('user_id')
    if not user_id:
        return unauthorized()

    calc = FarmCalculation.query.filter_by(id=calc_id, user_id=user_id).first()
    if not calc:
        return not_found("Calculation record not found.")

    return api_response(data={"calculation": calc.to_dict()})

@calculator_bp.route('/<int:calc_id>', methods=['DELETE'])
def delete_calculation(calc_id):
    user_id = session.get('user_id')
    if not user_id:
        return unauthorized()

    calc = FarmCalculation.query.filter_by(id=calc_id, user_id=user_id).first()
    if not calc:
        return not_found("Calculation record not found.")

    db.session.delete(calc)
    db.session.commit()
    return api_response(data={"message": "Calculation deleted successfully."})



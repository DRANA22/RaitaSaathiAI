from flask import Blueprint, request, session
import json
from app.extensions import db
from app.models import Scheme, SchemeAssessment, SchemeApplication, User, DecisionEvent
from app.services.scheme_engine import SchemeEligibilityEngine
from app.utils.errors import api_response, not_found, unauthorized

schemes_bp = Blueprint('schemes', __name__, url_prefix='/api/schemes')

def get_or_create_active_user():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return user
    from flask import current_app
    if current_app and current_app.config.get('TESTING'):
        user = User.query.first()
        if user:
            session['user_id'] = user.id
        return user
    return None

@schemes_bp.route('', methods=['GET'])
def list_schemes():
    """List all available government schemes with filters."""
    category = request.args.get('category')
    level = request.args.get('level') # CENTRAL or STATE_KARNATAKA
    search = request.args.get('query', '').strip().lower()
    only_open = request.args.get('open_only')

    query = Scheme.query.filter_by(is_active=True)
    if category and category != 'ALL':
        query = query.filter_by(category=category.upper())
    if level and level != 'ALL':
        query = query.filter_by(level=level.upper())
    if only_open and only_open.lower() in ('true', '1'):
        query = query.filter_by(is_application_open=True)

    schemes = query.all()
    if search:
        schemes = [
            s for s in schemes 
            if search in s.name_en.lower() or search in s.name_kn.lower() or search in s.brief_summary_en.lower()
        ]

    # Map with application status for current user if logged in
    user = get_or_create_active_user()
    user_apps = {}
    if user:
        for app in SchemeApplication.query.filter_by(user_id=user.id).all():
            user_apps[app.scheme_id] = {
                "application_id": app.id,
                "application_ref": app.application_ref,
                "status": app.status
            }

    results = []
    for s in schemes:
        d = s.to_dict()
        d["name"] = s.name_en
        d["description"] = s.brief_summary_en
        d["description_kn"] = s.brief_summary_kn
        d["department"] = s.department_en
        d["official_url"] = s.official_portal
        d["max_benefit_amount"] = s.max_benefit
        d["eligibility_category"] = "ELIGIBLE"
        d["why_eligible_en"] = s.eligibility_criteria_en or "Applicable for verified Karnataka farmers."
        d["why_eligible_kn"] = s.eligibility_criteria_kn or "ಕರ್ನಾಟಕದ ಎಲ್ಲಾ ಅರ್ಹ ರೈತರಿಗೆ ಅನ್ವಯಿಸುತ್ತದೆ."
        d["applied_info"] = user_apps.get(s.id, None)
        results.append(d)

    return api_response(data={"schemes": results, "recommendations": results, "total": len(results)})


@schemes_bp.route('/<int:scheme_id>', methods=['GET'])
def get_scheme(scheme_id):
    scheme = Scheme.query.get(scheme_id)
    if not scheme:
        return not_found("Scheme not found.")
    
    user = get_or_create_active_user()
    applied_info = None
    if user:
        app = SchemeApplication.query.filter_by(user_id=user.id, scheme_id=scheme.id).first()
        if app:
            applied_info = {
                "application_id": app.id,
                "application_ref": app.application_ref,
                "status": app.status
            }

    d = scheme.to_dict()
    d["name"] = scheme.name_en
    d["description"] = scheme.brief_summary_en
    d["description_kn"] = scheme.brief_summary_kn
    d["department"] = scheme.department_en
    d["official_url"] = scheme.official_portal
    d["max_benefit_amount"] = scheme.max_benefit
    d["applied_info"] = applied_info
    return api_response(data={"scheme": d})


@schemes_bp.route('/recommendations', methods=['GET', 'POST'])
def get_scheme_recommendations():
    """
    AI-Based Scheme Recommendation Engine.
    Categorizes all 20 official schemes for the active farmer:
    - ELIGIBLE
    - POSSIBLY_ELIGIBLE
    - NOT_ELIGIBLE
    Includes explainable 'Why you are eligible' & required document checklists.
    """
    user = get_or_create_active_user()
    profile = user.profile if user else None
    land = user.land_details if user else None
    crops = [c.crop_name_english.upper() for c in profile.crops] if (profile and profile.crops) else ['PADDY', 'RAGI']

    eval_context = {
        'total_land_acres': profile.total_land_acres if profile else 2.5,
        'land_ownership': land.land_ownership if land else 'OWNED',
        'farmer_category': profile.farmer_category if profile else 'SMALL',
        'social_category': profile.social_category if profile else 'GENERAL',
        'irrigation_type': profile.irrigation_type if profile else 'BOREWELL',
        'soil_type': profile.soil_type if profile else 'RED_LOAM',
        'state': (profile.state if profile else None) or 'Karnataka',
        'district': (profile.district if profile else None) or 'Mandya',
        'has_aadhaar': profile.has_aadhaar if profile else True,
        'has_pm_kisan': profile.has_pm_kisan if profile else True,
        'has_kisan_credit_card': profile.has_kisan_credit_card if profile else False,
        'crops': crops
    }

    schemes = Scheme.query.filter_by(is_active=True).all()
    user_apps = {}
    if user:
        user_apps = {app.scheme_id: app.to_dict() for app in SchemeApplication.query.filter_by(user_id=user.id).all()}

    eligible = []
    possibly_eligible = []
    not_eligible = []

    for scheme in schemes:
        res = SchemeEligibilityEngine.evaluate_scheme(scheme, eval_context)
        res["id"] = scheme.id
        res["code"] = scheme.code
        res["name"] = scheme.name_en
        res["name_en"] = scheme.name_en
        res["name_kn"] = scheme.name_kn
        res["department"] = scheme.department_en
        res["department_en"] = scheme.department_en
        res["department_kn"] = scheme.department_kn
        res["category"] = scheme.category
        res["level"] = scheme.level
        res["max_benefit"] = scheme.max_benefit
        res["max_benefit_amount"] = scheme.max_benefit
        res["description"] = scheme.brief_summary_en
        res["description_kn"] = scheme.brief_summary_kn
        res["brief_summary_en"] = scheme.brief_summary_en
        res["brief_summary_kn"] = scheme.brief_summary_kn
        res["official_url"] = scheme.official_portal
        res["official_portal"] = scheme.official_portal
        try:
            res["required_documents"] = json.loads(scheme.required_documents) if scheme.required_documents else ["Aadhaar Card", "Pahani (RTC)", "Bank Passbook"]
        except Exception:
            res["required_documents"] = ["Aadhaar Card", "Pahani (RTC)", "Bank Passbook"]
        res["applied_info"] = user_apps.get(scheme.id, None)

        cat = res["eligibility_category"]
        if cat == "ELIGIBLE":
            eligible.append(res)
        elif cat == "POSSIBLY_ELIGIBLE":
            possibly_eligible.append(res)
        else:
            not_eligible.append(res)

    all_recommendations = eligible + possibly_eligible + not_eligible

    return api_response(data={
        "farmer_name": user.full_name if user else "Karnataka Farmer",
        "farmer_id": (user.farmer_id if user else None) or (profile.farmer_id if profile else "KM-KA-2026-0842"),
        "district": profile.district if profile else "Mandya",
        "eligible_count": len(eligible),
        "possibly_eligible_count": len(possibly_eligible),
        "not_eligible_count": len(not_eligible),
        "total_schemes_analyzed": len(schemes),
        "recommendations": all_recommendations,
        "schemes": all_recommendations,
        "eligible": eligible,
        "possibly_eligible": possibly_eligible,
        "not_eligible": not_eligible
    })


@schemes_bp.route('/assess', methods=['POST'])
def assess_schemes():
    user = get_or_create_active_user()
    if not user or not user.profile:
        return api_response(success=False, error={"message": "Please complete your farmer profile first."}, status_code=400)

    profile_dict = user.profile.to_dict()
    eval_context = {
        'total_land_acres': profile_dict['total_land_acres'],
        'farmer_category': profile_dict['farmer_category'],
        'social_category': profile_dict['social_category'],
        'irrigation_type': profile_dict['irrigation_type'],
        'has_aadhaar': profile_dict['has_aadhaar'],
        'has_pm_kisan': profile_dict['has_pm_kisan'],
        'has_kisan_credit_card': profile_dict['has_kisan_credit_card'],
        'district': profile_dict['district']
    }

    schemes = Scheme.query.filter_by(is_active=True).all()
    results = []

    for scheme in schemes:
        eval_result = SchemeEligibilityEngine.evaluate_scheme(scheme, eval_context)
        
        # Save or update assessment
        assessment = SchemeAssessment(
            user_id=user.id,
            scheme_id=scheme.id,
            overall_status=eval_result['overall_status'],
            rules_evaluated_json=json.dumps(eval_result['rules_evaluated']),
            missing_fields_json=json.dumps(eval_result['missing_fields'])
        )
        db.session.add(assessment)
        results.append(eval_result)

    db.session.commit()
    return api_response(data={"passport": results})


@schemes_bp.route('/assessments', methods=['GET'])
def get_assessments():
    user = get_or_create_active_user()
    if not user:
        return unauthorized()

    assessments = SchemeAssessment.query.filter_by(user_id=user.id).order_by(SchemeAssessment.created_at.desc()).all()
    return api_response(data={"assessments": [a.to_dict() for a in assessments]})

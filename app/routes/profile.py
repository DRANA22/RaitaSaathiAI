from flask import Blueprint, request, session
from app.extensions import db
from app.models import FarmerProfile, FarmerLandDetails, FarmCrop, User
from app.utils.errors import api_response, not_found, bad_request, unauthorized

profile_bp = Blueprint('profile', __name__, url_prefix='/api/profile')

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

@profile_bp.route('', methods=['GET'])
def get_profile():
    user = get_or_create_active_user()
    if not user:
        return unauthorized("Farmer authentication required.")
    if not user.profile:
        return not_found("Farmer profile not initialized.")

    profile_dict = user.profile.to_dict()
    land_dict = user.land_details.to_dict() if user.land_details else None

    return api_response(data={
        "farmer_id": user.farmer_id or user.profile.farmer_id,
        "full_name": user.full_name,
        "phone_number": user.phone_number,
        "preferred_language": user.preferred_language,
        "profile": profile_dict,
        "land_details": land_dict,
        "completion_percentage": user.profile.calculate_completion()
    })

@profile_bp.route('', methods=['PATCH'])
def update_profile():
    """Update personal and agricultural profile information."""
    user = get_or_create_active_user()
    if not user or not user.profile:
        return not_found("Profile not found.")

    profile = user.profile
    land = user.land_details
    data = request.get_json() or {}

    # User level updates
    if 'full_name' in data and data['full_name'].strip():
        user.full_name = data['full_name'].strip()
    if 'preferred_language' in data:
        user.preferred_language = data['preferred_language']

    # Location updates
    if 'district' in data:
        profile.district = str(data['district']).strip()
    if 'taluk' in data:
        profile.taluk = str(data['taluk']).strip()
    if 'village' in data:
        profile.village = str(data['village']).strip()
    if 'pincode' in data:
        profile.pincode = str(data['pincode']).strip()

    # Land and agricultural updates
    if 'total_land_acres' in data:
        profile.total_land_acres = float(data['total_land_acres'])
        if land: land.total_land_acres = profile.total_land_acres
        if profile.total_land_acres < 2.5:
            profile.farmer_category = 'MARGINAL'
        elif profile.total_land_acres <= 5.0:
            profile.farmer_category = 'SMALL'
        elif profile.total_land_acres <= 10.0:
            profile.farmer_category = 'MEDIUM'
        else:
            profile.farmer_category = 'LARGE'

    if 'irrigation_type' in data:
        profile.irrigation_type = data['irrigation_type']
        if land: land.irrigation_type = data['irrigation_type']
    if 'soil_type' in data:
        profile.soil_type = data['soil_type']
        if land: land.soil_type = data['soil_type']
    if 'land_ownership' in data and land:
        land.land_ownership = data['land_ownership']
    if 'farming_type' in data and land:
        land.farming_type = data['farming_type']
    if 'farming_experience_years' in data:
        profile.farming_experience_years = int(data['farming_experience_years'])
    if 'annual_season' in data:
        profile.annual_season = data['annual_season']
    if 'has_pm_kisan' in data:
        profile.has_pm_kisan = bool(data['has_pm_kisan'])
    if 'has_kisan_credit_card' in data:
        profile.has_kisan_credit_card = bool(data['has_kisan_credit_card'])

    profile.profile_completion_pct = profile.calculate_completion()
    db.session.commit()

    return api_response(data={
        "profile": profile.to_dict(),
        "completion_percentage": profile.profile_completion_pct
    })


@profile_bp.route('/crop', methods=['POST'])
def add_or_update_crop():
    """Add a new crop to the farmer's profile."""
    user = get_or_create_active_user()
    if not user or not user.profile:
        return not_found("Profile not found.")

    data = request.get_json() or {}
    crop_en = data.get('crop_name_english', '').strip()
    crop_kn = data.get('crop_name_kannada', '').strip()
    acres = float(data.get('acres', 1.0) or 1.0)
    season = data.get('season', 'KHARIF')
    growth = data.get('growth_stage', 'VEGETATIVE')
    crop_type = data.get('crop_type', 'MAIN')

    if not crop_en:
        return bad_request("Crop name in English is required.")

    crop = FarmCrop(
        profile_id=user.profile.id,
        crop_name_english=crop_en,
        crop_name_kannada=crop_kn or crop_en,
        crop_type=crop_type,
        acres=acres,
        season=season,
        growth_stage=growth
    )
    db.session.add(crop)
    db.session.commit()

    return api_response(data={"crop": crop.to_dict()}, status_code=201)


@profile_bp.route('/crop/<int:crop_id>', methods=['DELETE'])
def remove_crop(crop_id):
    """Remove a crop from profile."""
    user = get_or_create_active_user()
    if not user or not user.profile:
        return not_found("Profile not found.")

    crop = FarmCrop.query.filter_by(id=crop_id, profile_id=user.profile.id).first()
    if crop:
        db.session.delete(crop)
        db.session.commit()
    return api_response(data={"success": True})


@profile_bp.route('/location', methods=['POST'])
def update_location():
    user = get_or_create_active_user()
    if not user or not user.profile:
        return not_found("Profile not found.")

    data = request.get_json() or {}
    district = data.get('district', '').strip()
    state = data.get('state', 'Karnataka').strip()

    if district:
        user.profile.district = district
    if state:
        user.profile.state = state

    db.session.commit()
    return api_response(data={
        "state": user.profile.state,
        "district": user.profile.district,
        "profile": user.profile.to_dict()
    })


@profile_bp.route('/name', methods=['POST'])
def update_name():
    user = get_or_create_active_user()
    if not user:
        return not_found("User not found.")

    data = request.get_json() or {}
    name = data.get('name', '').strip()
    if name:
        user.full_name = name
        db.session.commit()

    return api_response(data={
        "farmer_name": user.full_name
    })

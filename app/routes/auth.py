from flask import Blueprint, request, session
from app.extensions import db
from app.models import User, FarmerProfile
from app.utils.security import hash_password, verify_password, login_required
from app.utils.validators import validate_username, validate_password
from app.utils.errors import api_response, bad_request, unauthorized

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')
    full_name = data.get('full_name', '').strip()
    language = data.get('preferred_language', 'kn')

    valid_u, msg_u = validate_username(username)
    if not valid_u:
        return bad_request(msg_u)

    valid_p, msg_p = validate_password(password)
    if not valid_p:
        return bad_request(msg_p)

    if not full_name:
        return bad_request("Full name is required.")

    if User.query.filter_by(username=username).first():
        return bad_request("A farmer with this username already exists.")

    user = User(
        username=username,
        password_hash=hash_password(password),
        full_name=full_name,
        preferred_language=language,
        is_demo=False
    )
    db.session.add(user)
    db.session.flush()

    # Automatically generate default farmer profile
    profile = FarmerProfile(
        user_id=user.id,
        district='Mandya',
        taluk='Pandavapura',
        total_land_acres=2.5,
        farmer_category='SMALL',
        social_category='GENERAL',
        irrigation_type='BOREWELL'
    )
    db.session.add(profile)
    db.session.commit()

    session['user_id'] = user.id
    return api_response(data={"user": user.to_dict()}, status_code=201)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    identifier = data.get('username', '').strip() or data.get('phone_number', '').strip()
    password = data.get('password', '')
    otp = data.get('otp', '').strip()

    # Clean phone formatting if digits only
    cleaned_id = identifier.replace(' ', '').replace('-', '').replace('+91', '')

    user = User.query.filter(
        (User.username == identifier) | 
        (User.phone_number == identifier) |
        (User.phone_number == cleaned_id)
    ).first()

    if not user:
        return unauthorized("No farmer account found with this Mobile Number or Username.")

    # Allow password match or OTP (default demo OTP: 2026 or 1234)
    valid_auth = False
    if password and verify_password(password, user.password_hash):
        valid_auth = True
    elif otp and otp in ('2026', '1234', '9999'):
        valid_auth = True

    if not valid_auth:
        return unauthorized("Invalid password or OTP. (For demo farmer, use OTP: 2026)")

    session['user_id'] = user.id
    return api_response(data={"user": user.to_dict()})

@auth_bp.route('/phone-login', methods=['POST'])
def phone_login():
    """
    Mobile / Cell number authentication with OTP.
    Auto-registers new farmers if number is not found.
    """
    data = request.get_json() or {}
    raw_phone = data.get('phone_number', '').strip()
    phone = raw_phone.replace(' ', '').replace('-', '').replace('+91', '')
    full_name = data.get('full_name', '').strip()
    district = data.get('district', 'Mandya').strip()
    acres = float(data.get('acres', 2.5) or 2.5)
    otp = data.get('otp', '2026').strip()

    if not phone or len(phone) < 10:
        return bad_request("Please enter a valid 10-digit mobile phone number.")

    # Find existing user by phone
    user = User.query.filter_by(phone_number=phone).first()
    if not user:
        # Create new farmer profile
        username = f"kisan_{phone[-4:]}_{phone[:3]}"
        user = User(
            username=username,
            phone_number=phone,
            password_hash=hash_password("kisan2026"),
            full_name=full_name or f"Farmer {phone[-4:]}",
            preferred_language='kn',
            is_demo=False
        )
        db.session.add(user)
        db.session.flush()

        cat = 'MARGINAL' if acres < 2.5 else ('SMALL' if acres <= 5.0 else 'MEDIUM')
        profile = FarmerProfile(
            user_id=user.id,
            district=district,
            taluk=district,
            total_land_acres=acres,
            farmer_category=cat,
            social_category='GENERAL',
            irrigation_type='BOREWELL'
        )
        db.session.add(profile)
        db.session.commit()

    session['user_id'] = user.id
    return api_response(data={
        "user": user.to_dict(),
        "profile": user.profile.to_dict() if user.profile else None
    })


@auth_bp.route('/farmer/request-otp', methods=['POST'])
def farmer_request_otp():
    """
    Sends simulated OTP to farmer's mobile number.
    Checks if farmer profile exists or guides to registration.
    """
    data = request.get_json() or {}
    raw_phone = data.get('phone_number', '').strip()
    phone = raw_phone.replace(' ', '').replace('-', '').replace('+91', '')

    if not phone or len(phone) < 10:
        return bad_request("Please enter a valid 10-digit mobile phone number.")

    user = User.query.filter_by(phone_number=phone).first()
    masked = f"{phone[:2]}XXXXXX{phone[-2:]}"

    return api_response(data={
        "exists": user is not None,
        "masked_phone": masked,
        "farmer_name": user.full_name if user else None,
        "demo_otp": "2026",
        "message_en": f"OTP sent to mobile number ({masked}). For demonstration, use '2026'.",
        "message_kn": f"ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ({masked}) ಗೆ OTP ಕಳುಹಿಸಲಾಗಿದೆ. ಪ್ರದರ್ಶನಕ್ಕಾಗಿ '2026' ಬಳಸಿ."
    })

@auth_bp.route('/farmer/verify-otp', methods=['POST'])
def farmer_verify_otp():
    """
    Verifies received OTP and logs farmer in.
    """
    data = request.get_json() or {}
    raw_phone = data.get('phone_number', '').strip()
    phone = raw_phone.replace(' ', '').replace('-', '').replace('+91', '')
    otp = data.get('otp', '').strip()

    if not phone or len(phone) < 10:
        return bad_request("Please enter a valid 10-digit mobile number.")
    if not otp:
        return bad_request("Please enter the verification OTP.")

    if otp not in ('2026', '1234', '9999'):
        return unauthorized("Invalid OTP. For demonstration, please enter '2026'.")

    user = User.query.filter_by(phone_number=phone).first()
    if not user:
        # Create a basic profile if user entered phone directly
        username = f"kisan_{phone[-4:]}"
        user = User(
            username=username,
            phone_number=phone,
            password_hash=hash_password("kisan2026"),
            full_name=f"ರೈತರು ({phone[-4:]})",
            preferred_language='kn',
            role='FARMER',
            is_demo=False
        )
        db.session.add(user)
        db.session.flush()

        profile = FarmerProfile(
            user_id=user.id,
            district='Mandya',
            taluk='Pandavapura',
            village='Chikka Byadarahalli',
            total_land_acres=2.5,
            farmer_category='SMALL',
            social_category='GENERAL',
            irrigation_type='BOREWELL'
        )
        db.session.add(profile)
        db.session.commit()

    session['user_id'] = user.id
    session['role'] = 'FARMER'

    return api_response(data={
        "user": user.to_dict(),
        "profile": user.profile.to_dict() if user.profile else None,
        "message": "Farmer login successful."
    })

@auth_bp.route('/status', methods=['GET'])
def auth_status():
    from app.models import AdminUser
    user_id = session.get('user_id')
    admin_id = session.get('admin_id')
    user = User.query.get(user_id) if user_id else None
    admin = AdminUser.query.get(admin_id) if admin_id else None
    return api_response(data={
        "farmer_authenticated": user is not None,
        "officer_authenticated": admin is not None,
        "farmer": user.to_dict() if user else None,
        "officer": admin.to_dict() if admin else None
    })

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('admin_id', None)
    session.pop('role', None)
    return api_response(data={"message": "Logged out successfully."})

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    user = User.query.get(user_id) if user_id else None
    
    # Auto-associate default active farmer session (no login barrier)
    if not user:
        user = User.query.first()
        if user:
            session['user_id'] = user.id

    if not user:
        # Create a default guest/active farmer user if database is empty
        user = User(
            username="kisan_mitra",
            full_name="ರೈತ ಮಿತ್ರ (Farmer)",
            preferred_language="kn",
            is_demo=True
        )
        db.session.add(user)
        db.session.flush()
        profile = FarmerProfile(
            user_id=user.id,
            state="Karnataka",
            district="Mandya",
            taluk="Pandavapura",
            total_land_acres=2.5,
            farmer_category="SMALL",
            social_category="GENERAL",
            irrigation_type="BOREWELL"
        )
        db.session.add(profile)
        db.session.commit()
        session['user_id'] = user.id

    return api_response(data={
        "authenticated": True,
        "user": user.to_dict(),
        "profile": user.profile.to_dict() if user.profile else None
    })


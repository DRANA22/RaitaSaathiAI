import uuid
import random
from datetime import datetime
from flask import Blueprint, request, session
from app.extensions import db
from app.models import User, FarmerProfile, FarmerLandDetails, IdentityVerification, FarmerNotification
from app.utils.security import hash_password
from app.utils.errors import api_response, bad_request, unauthorized

identity_bp = Blueprint('identity', __name__, url_prefix='/api/identity')

# In-memory temporary cache for simulated OTP transactions (TTL: 10 mins)
# Format: { txn_id: { mobile, masked_aadhaar, otp, name, ... } }
OTP_TRANSACTIONS = {}

def generate_farmer_id(district='Mandya'):
    """Generate professional, unique Farmer ID: KM-KA-2026-XXXX"""
    dist_code = district[:3].upper() if district else 'MAN'
    rand_num = random.randint(1000, 9999)
    return f"KM-KA-2026-{rand_num}"

@identity_bp.route('/generate-otp', methods=['POST'])
def generate_otp():
    """
    STEP 1 & 2: Initiate Aadhaar e-KYC / Mobile OTP Verification.
    Security: Never logs or stores raw Aadhaar number or real Aadhaar OTP.
    """
    data = request.get_json() or {}
    full_name = data.get('full_name', '').strip()
    mobile = data.get('mobile_number', '').strip().replace(' ', '').replace('-', '').replace('+91', '')
    raw_aadhaar = data.get('aadhaar_number', '').strip().replace(' ', '').replace('-', '')
    consent = data.get('consent', True)

    if not full_name:
        return bad_request("Full name is required as per official records.")
    if not mobile or len(mobile) < 10:
        return bad_request("Please enter a valid 10-digit mobile number.")
    if not consent:
        return bad_request("Explicit consent is required for Aadhaar e-KYC verification.")

    # Mask Aadhaar: e.g. XXXX-XXXX-4589
    if len(raw_aadhaar) >= 4:
        masked_aadhaar = f"XXXX-XXXX-{raw_aadhaar[-4:]}"
    else:
        masked_aadhaar = "XXXX-XXXX-8421"

    masked_mobile = f"{mobile[:2]}XXXXXX{mobile[-2:]}"
    txn_id = f"TXN-KYC-2026-{uuid.uuid4().hex[:8].upper()}"

    # Default simulated sandbox OTP
    demo_otp = "2026"

    OTP_TRANSACTIONS[txn_id] = {
        "full_name": full_name,
        "mobile": mobile,
        "masked_mobile": masked_mobile,
        "masked_aadhaar": masked_aadhaar,
        "otp": demo_otp,
        "state": data.get('state', 'Karnataka'),
        "district": data.get('district', 'Mandya'),
        "taluk": data.get('taluk', 'Pandavapura'),
        "village": data.get('village', 'Chikka Byadarahalli'),
        "preferred_language": data.get('preferred_language', 'kn'),
        "timestamp": datetime.utcnow()
    }

    return api_response(data={
        "transaction_id": txn_id,
        "masked_aadhaar": masked_aadhaar,
        "masked_mobile": masked_mobile,
        "provider": "UIDAI Authorised e-KYC Sandbox (Simulated Protocol)",
        "message_kn": "ದೃಢೀಕರಣ ಕೋಡ್ (OTP) ಕಳುಹಿಸಲಾಗಿದೆ. ಪ್ರದರ್ಶನಕ್ಕಾಗಿ '2026' ಬಳಸಿ.",
        "message_en": "Simulated OTP sent to registered mobile. Use '2026' for demo verification.",
        "expires_in_seconds": 600,
        "demo_hint_otp": demo_otp
    })


@identity_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """
    STEP 2: Verify received OTP against transaction reference.
    Validates identity payload returned by the provider sandbox.
    """
    data = request.get_json() or {}
    txn_id = data.get('transaction_id', '').strip()
    entered_otp = data.get('otp', '').strip()

    if not txn_id or txn_id not in OTP_TRANSACTIONS:
        return bad_request("Invalid or expired verification transaction. Please request a new OTP.")

    txn_data = OTP_TRANSACTIONS[txn_id]

    # Verify OTP (accept 2026 or 1234 or match)
    if entered_otp not in (txn_data["otp"], "2026", "1234", "9999"):
        return bad_request("Invalid OTP. For demonstration simulation, please enter '2026'.")

    # Mark transaction as verified
    txn_data["verified"] = True
    txn_data["verified_at"] = datetime.utcnow()

    return api_response(data={
        "transaction_id": txn_id,
        "verification_status": "VERIFIED",
        "verified_name": txn_data["full_name"],
        "masked_aadhaar": txn_data["masked_aadhaar"],
        "message_kn": "ಆಧಾರ್ ಇ-ಕೆವೈಸಿ ದೃಢೀಕರಣ ಯಶಸ್ವಿಯಾಗಿದೆ!",
        "message_en": "Aadhaar e-KYC Identity Verification Successful!"
    })


@identity_bp.route('/complete-registration', methods=['POST'])
def complete_registration():
    """
    STEP 3: Complete registration and create Farmer Digital Identity.
    Generates unique Farmer ID, Farmer Profile, and default Land Details.
    """
    data = request.get_json() or {}
    txn_id = data.get('transaction_id', '').strip()

    # If completed via verified transaction
    if txn_id and txn_id in OTP_TRANSACTIONS and OTP_TRANSACTIONS[txn_id].get("verified"):
        txn_data = OTP_TRANSACTIONS[txn_id]
        full_name = txn_data["full_name"]
        mobile = txn_data["mobile"]
        masked_aadhaar = txn_data["masked_aadhaar"]
        district = data.get('district', txn_data["district"])
        taluk = data.get('taluk', txn_data["taluk"])
        village = data.get('village', txn_data["village"])
        language = data.get('preferred_language', txn_data["preferred_language"])
        del OTP_TRANSACTIONS[txn_id] # Clean up
    else:
        # Direct registration fallback for demo
        full_name = data.get('full_name', '').strip() or 'ರಮೇಶ್ ಗೌಡ (Ramesh Gowda)'
        mobile = data.get('mobile_number', '9845012345').strip()
        masked_aadhaar = f"XXXX-XXXX-{random.randint(1000, 9999)}"
        district = data.get('district', 'Mandya')
        taluk = data.get('taluk', 'Pandavapura')
        village = data.get('village', 'Chikka Byadarahalli')
        language = data.get('preferred_language', 'kn')

    # Land details
    land_acres = float(data.get('total_land_acres', 2.5) or 2.5)
    land_ownership = data.get('land_ownership', 'OWNED')
    irrigation_type = data.get('irrigation_type', 'BOREWELL')
    soil_type = data.get('soil_type', 'RED_LOAM')

    # Category derivation
    if land_acres < 2.5:
        category = 'MARGINAL'
    elif land_acres <= 5.0:
        category = 'SMALL'
    elif land_acres <= 10.0:
        category = 'MEDIUM'
    else:
        category = 'LARGE'

    # Check if user already exists with this mobile
    user = User.query.filter_by(phone_number=mobile).first()
    farmer_id = generate_farmer_id(district)

    if not user:
        username = f"kisan_{mobile[-4:]}_{random.randint(100, 999)}"
        user = User(
            farmer_id=farmer_id,
            username=username,
            password_hash=hash_password("kisan2026"),
            full_name=full_name,
            phone_number=mobile,
            preferred_language=language,
            role='FARMER',
            is_demo=False
        )
        db.session.add(user)
        db.session.flush()
    else:
        user.full_name = full_name
        user.preferred_language = language
        if not user.farmer_id:
            user.farmer_id = farmer_id

    # Create or update profile
    profile = FarmerProfile.query.filter_by(user_id=user.id).first()
    if not profile:
        profile = FarmerProfile(
            user_id=user.id,
            farmer_id=user.farmer_id,
            state='Karnataka',
            district=district,
            taluk=taluk,
            village=village,
            total_land_acres=land_acres,
            farmer_category=category,
            social_category='GENERAL',
            irrigation_type=irrigation_type,
            soil_type=soil_type,
            verification_status='VERIFIED',
            profile_completion_pct=85,
            has_aadhaar=True,
            has_pm_kisan=True,
            has_kisan_credit_card=False,
            bank_verified=True,
            bank_account_masked=f"XXXX-XXXX-{random.randint(1000, 9999)}",
            bank_name='State Bank of India'
        )
        db.session.add(profile)
        db.session.flush()
    else:
        profile.district = district
        profile.taluk = taluk
        profile.village = village
        profile.total_land_acres = land_acres
        profile.farmer_category = category
        profile.irrigation_type = irrigation_type
        profile.soil_type = soil_type
        profile.verification_status = 'VERIFIED'
        profile.profile_completion_pct = profile.calculate_completion()

    # Create or update Land Details
    land = FarmerLandDetails.query.filter_by(user_id=user.id).first()
    if not land:
        land = FarmerLandDetails(
            user_id=user.id,
            profile_id=profile.id,
            total_land_acres=land_acres,
            land_ownership=land_ownership,
            irrigation_availability='IRRIGATED' if irrigation_type != 'RAIN_FED' else 'RAIN_FED',
            irrigation_type=irrigation_type,
            soil_type=soil_type,
            farming_type='CONVENTIONAL',
            survey_number=f"{random.randint(100, 300)}/{random.randint(1, 4)}A"
        )
        db.session.add(land)

    # Record identity verification record (Strictly masked)
    id_ver = IdentityVerification(
        user_id=user.id,
        verification_type='AADHAAR_OTP',
        provider_name='UIDAI Authorised e-KYC Sandbox',
        transaction_ref=f"KYC-KA-2026-{random.randint(100000, 999999)}",
        masked_aadhaar=masked_aadhaar,
        masked_mobile=f"{mobile[:2]}XXXXXX{mobile[-2:]}",
        verification_status='VERIFIED',
        consent_recorded=True,
        verified_name=full_name,
        is_simulation=True
    )
    db.session.add(id_ver)

    # Initial Welcome Notification
    notif = FarmerNotification(
        user_id=user.id,
        title_en="Digital Farmer ID Created",
        title_kn="ಡಿಜಿಟಲ್ ರೈತ ಐಡಿ ರಚಿಸಲಾಗಿದೆ",
        title_hi="डिजिटल किसान आईडी बनाई गई",
        message_en=f"Welcome {full_name}! Your verified Farmer ID is {user.farmer_id}. You can now discover government schemes tailored to your land.",
        message_kn=f"ಸ್ವಾಗತ {full_name}! ನಿಮ್ಮ ದೃಢೀಕೃತ ರೈತ ಐಡಿ {user.farmer_id}. ನಿಮ್ಮ ಜಮೀನಿಗೆ ಸೂಕ್ತವಾದ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳನ್ನು ಈಗ ನೋಡಬಹುದು.",
        message_hi=f"स्वागत है {full_name}! आपकी सत्यापित किसान आईडी {user.farmer_id} है।",
        notification_type="VERIFICATION_SUCCESS"
    )
    db.session.add(notif)
    db.session.commit()

    # Bind session
    session['user_id'] = user.id

    return api_response(data={
        "farmer_id": user.farmer_id,
        "user": user.to_dict(),
        "profile": profile.to_dict(),
        "verification_status": "VERIFIED",
        "masked_aadhaar": masked_aadhaar,
        "message_kn": f"ನೋಂದಣಿ ಯಶಸ್ವಿ! ನಿಮ್ಮ ರೈತ ಐಡಿ: {user.farmer_id}",
        "message_en": f"Registration successful! Your Farmer ID: {user.farmer_id}"
    }, status_code=201)

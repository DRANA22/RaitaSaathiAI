from datetime import datetime
import json
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.String(32), unique=True, nullable=True, index=True) # e.g. KM-KA-2026-0842
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True, index=True)
    role = db.Column(db.String(20), default='FARMER') # FARMER, ADMIN
    preferred_language = db.Column(db.String(8), default='kn') # kn, en, hi
    is_demo = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    profile = db.relationship('FarmerProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    land_details = db.relationship('FarmerLandDetails', backref='user', uselist=False, cascade='all, delete-orphan')
    identity_verifications = db.relationship('IdentityVerification', backref='user', cascade='all, delete-orphan')
    applications = db.relationship('SchemeApplication', backref='user', cascade='all, delete-orphan', order_by='SchemeApplication.applied_at.desc()')
    notifications = db.relationship('FarmerNotification', backref='user', cascade='all, delete-orphan', order_by='FarmerNotification.created_at.desc()')
    conversations = db.relationship('Conversation', backref='user', cascade='all, delete-orphan')
    tasks = db.relationship('FarmTask', backref='user', cascade='all, delete-orphan')
    calculations = db.relationship('FarmCalculation', backref='user', cascade='all, delete-orphan')
    assessments = db.relationship('SchemeAssessment', backref='user', cascade='all, delete-orphan')
    decision_events = db.relationship('DecisionEvent', backref='user', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id or (self.profile.farmer_id if self.profile else None),
            'username': self.username,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'role': self.role,
            'preferred_language': self.preferred_language,
            'is_demo': self.is_demo,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'has_profile': self.profile is not None
        }


class FarmerProfile(db.Model):
    __tablename__ = 'farmer_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    farmer_id = db.Column(db.String(32), unique=True, nullable=True, index=True)
    photo_url = db.Column(db.String(256), nullable=True)

    # Location Details (Karnataka Focused)
    state = db.Column(db.String(64), default='Karnataka')
    district = db.Column(db.String(64), nullable=False, default='Mandya')
    taluk = db.Column(db.String(64), nullable=True, default='Pandavapura')
    village = db.Column(db.String(64), nullable=True, default='Chikka Byadarahalli')
    pincode = db.Column(db.String(10), default='571434')

    # Verification and Status
    verification_status = db.Column(db.String(32), default='VERIFIED') # UNVERIFIED, PENDING_VERIFICATION, VERIFIED
    profile_completion_pct = db.Column(db.Integer, default=85)
    
    # Farming Info
    total_land_acres = db.Column(db.Float, default=2.5)
    farmer_category = db.Column(db.String(32), default='SMALL') # MARGINAL (<2.5 ac), SMALL (2.5-5 ac), MEDIUM, LARGE
    social_category = db.Column(db.String(16), default='GENERAL') # GENERAL, OBC, SC, ST
    irrigation_type = db.Column(db.String(32), default='BOREWELL') # RAIN_FED, BOREWELL, CANAL, DRIP
    soil_type = db.Column(db.String(32), default='RED_LOAM') # RED_LOAM, BLACK_COTTON, ALLUVIAL, SANDY
    farming_experience_years = db.Column(db.Integer, default=12)
    annual_season = db.Column(db.String(32), default='KHARIF_RABI')
    
    # Flags and Credentials
    has_aadhaar = db.Column(db.Boolean, default=True)
    has_pm_kisan = db.Column(db.Boolean, default=True)
    has_kisan_credit_card = db.Column(db.Boolean, default=False)
    bank_verified = db.Column(db.Boolean, default=True)
    bank_account_masked = db.Column(db.String(32), default='XXXX-XXXX-4589')
    bank_name = db.Column(db.String(64), default='State Bank of India')
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Crops cultivated
    crops = db.relationship('FarmCrop', backref='profile', cascade='all, delete-orphan')

    def calculate_completion(self):
        score = 0
        if self.farmer_id: score += 15
        if self.verification_status == 'VERIFIED': score += 20
        if self.district and self.taluk and self.village: score += 15
        if self.total_land_acres and self.total_land_acres > 0: score += 15
        if self.irrigation_type: score += 10
        if self.soil_type: score += 10
        if self.crops and len(self.crops) > 0: score += 15
        return min(score, 100)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'farmer_id': self.farmer_id,
            'photo_url': self.photo_url,
            'state': self.state,
            'district': self.district,
            'taluk': self.taluk,
            'village': self.village,
            'pincode': self.pincode,
            'verification_status': self.verification_status,
            'profile_completion_pct': self.profile_completion_pct or self.calculate_completion(),
            'total_land_acres': self.total_land_acres,
            'farmer_category': self.farmer_category,
            'social_category': self.social_category,
            'irrigation_type': self.irrigation_type,
            'soil_type': self.soil_type,
            'farming_experience_years': self.farming_experience_years,
            'annual_season': self.annual_season,
            'has_aadhaar': self.has_aadhaar,
            'has_pm_kisan': self.has_pm_kisan,
            'has_kisan_credit_card': self.has_kisan_credit_card,
            'bank_verified': self.bank_verified,
            'bank_account_masked': self.bank_account_masked,
            'bank_name': self.bank_name,
            'crops': [c.to_dict() for c in self.crops],
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class FarmerLandDetails(db.Model):
    __tablename__ = 'farmer_land_details'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('farmer_profiles.id', ondelete='CASCADE'), nullable=True)
    total_land_acres = db.Column(db.Float, default=2.5)
    land_ownership = db.Column(db.String(32), default='OWNED') # OWNED, LEASED, TENANT
    irrigation_availability = db.Column(db.String(32), default='IRRIGATED') # IRRIGATED, PARTIALLY_IRRIGATED, RAIN_FED
    irrigation_type = db.Column(db.String(32), default='BOREWELL') # BOREWELL, CANAL, DRIP, SPRINKLER, RAIN_FED
    soil_type = db.Column(db.String(32), default='RED_LOAM') # RED_LOAM, BLACK_COTTON, ALLUVIAL, SANDY, CLAY
    farming_type = db.Column(db.String(32), default='CONVENTIONAL') # ORGANIC, CONVENTIONAL, NATURAL_FARMING, MIXED
    survey_number = db.Column(db.String(64), default='142/2A')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'total_land_acres': self.total_land_acres,
            'land_ownership': self.land_ownership,
            'irrigation_availability': self.irrigation_availability,
            'irrigation_type': self.irrigation_type,
            'soil_type': self.soil_type,
            'farming_type': self.farming_type,
            'survey_number': self.survey_number
        }


class FarmCrop(db.Model):
    __tablename__ = 'farm_crops'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('farmer_profiles.id', ondelete='CASCADE'), nullable=False)
    crop_name_english = db.Column(db.String(64), nullable=False)
    crop_name_kannada = db.Column(db.String(64), nullable=False)
    crop_type = db.Column(db.String(16), default='MAIN') # MAIN, SECONDARY, INTERCROP
    acres = db.Column(db.Float, default=1.0)
    season = db.Column(db.String(16), default='KHARIF') # KHARIF, RABI, SUMMER, ANNUAL
    growth_stage = db.Column(db.String(32), default='VEGETATIVE') # SOWING, VEGETATIVE, FLOWERING, HARVEST

    def to_dict(self):
        return {
            'id': self.id,
            'crop_name_english': self.crop_name_english,
            'crop_name_kannada': self.crop_name_kannada,
            'crop_type': self.crop_type,
            'acres': self.acres,
            'season': self.season,
            'growth_stage': self.growth_stage
        }


class IdentityVerification(db.Model):
    __tablename__ = 'identity_verifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    verification_type = db.Column(db.String(32), default='AADHAAR_OTP')
    provider_name = db.Column(db.String(64), default='UIDAI_AUTHORISED_SANDBOX')
    transaction_ref = db.Column(db.String(64), unique=True, index=True)
    masked_aadhaar = db.Column(db.String(20), nullable=False) # STRICT: Only masked 'XXXX-XXXX-1234'
    masked_mobile = db.Column(db.String(20), nullable=False)
    verification_status = db.Column(db.String(32), default='VERIFIED') # VERIFIED, PENDING, FAILED
    consent_recorded = db.Column(db.Boolean, default=True)
    consent_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    verified_name = db.Column(db.String(128), nullable=True)
    verified_gender = db.Column(db.String(10), default='M')
    verified_dob_year = db.Column(db.String(10), default='1982')
    is_simulation = db.Column(db.Boolean, default=True)
    verified_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'verification_type': self.verification_type,
            'provider_name': self.provider_name,
            'transaction_ref': self.transaction_ref,
            'masked_aadhaar': self.masked_aadhaar,
            'masked_mobile': self.masked_mobile,
            'verification_status': self.verification_status,
            'consent_recorded': self.consent_recorded,
            'verified_name': self.verified_name,
            'is_simulation': self.is_simulation,
            'verified_at': self.verified_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Scheme(db.Model):
    __tablename__ = 'schemes'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name_en = db.Column(db.String(160), nullable=False)
    name_kn = db.Column(db.String(160), nullable=False)
    name_hi = db.Column(db.String(160), nullable=True)
    department_en = db.Column(db.String(160), nullable=False, default='Ministry of Agriculture and Farmers Welfare')
    department_kn = db.Column(db.String(160), nullable=False, default='ಕೃಷಿ ಮತ್ತು ರೈತರ ಕಲ್ಯಾಣ ಇಲಾಖೆ')
    category = db.Column(db.String(32), nullable=False) # FINANCIAL, SUBSIDY, INSURANCE, INFRASTRUCTURE, ORGANIC, IRRIGATION
    level = db.Column(db.String(32), default='CENTRAL') # CENTRAL, STATE_KARNATAKA
    official_portal = db.Column(db.String(256), nullable=False)
    brief_summary_en = db.Column(db.Text, nullable=False)
    brief_summary_kn = db.Column(db.Text, nullable=False)
    brief_summary_hi = db.Column(db.Text, nullable=True)
    main_benefits_en = db.Column(db.Text, nullable=True)
    main_benefits_kn = db.Column(db.Text, nullable=True)
    max_benefit = db.Column(db.String(128), nullable=False)
    eligibility_criteria_en = db.Column(db.Text, nullable=True)
    eligibility_criteria_kn = db.Column(db.Text, nullable=True)
    required_documents = db.Column(db.Text, nullable=False) # JSON list
    application_process = db.Column(db.Text, nullable=False)
    application_opening_date = db.Column(db.String(32), default='Open Year-Round')
    application_closing_date = db.Column(db.String(32), default='Active')
    is_application_open = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    last_verified_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    rules = db.relationship('EligibilityRule', backref='scheme', cascade='all, delete-orphan')
    applications = db.relationship('SchemeApplication', backref='scheme', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name_en': self.name_en,
            'name_kn': self.name_kn,
            'name_hi': self.name_hi or self.name_en,
            'department_en': self.department_en,
            'department_kn': self.department_kn,
            'category': self.category,
            'level': self.level,
            'official_portal': self.official_portal,
            'brief_summary_en': self.brief_summary_en,
            'brief_summary_kn': self.brief_summary_kn,
            'brief_summary_hi': self.brief_summary_hi or self.brief_summary_en,
            'main_benefits_en': self.main_benefits_en or self.max_benefit,
            'main_benefits_kn': self.main_benefits_kn or self.max_benefit,
            'max_benefit': self.max_benefit,
            'eligibility_criteria_en': self.eligibility_criteria_en,
            'eligibility_criteria_kn': self.eligibility_criteria_kn,
            'required_documents': json.loads(self.required_documents) if self.required_documents else [],
            'application_process': self.application_process,
            'application_opening_date': self.application_opening_date,
            'application_closing_date': self.application_closing_date,
            'is_application_open': self.is_application_open,
            'last_verified_at': self.last_verified_at.strftime('%Y-%m-%d'),
            'rules_count': len(self.rules)
        }


class EligibilityRule(db.Model):
    __tablename__ = 'eligibility_rules'

    id = db.Column(db.Integer, primary_key=True)
    scheme_id = db.Column(db.Integer, db.ForeignKey('schemes.id', ondelete='CASCADE'), nullable=False)
    field_name = db.Column(db.String(64), nullable=False) # total_land_acres, land_ownership, irrigation_availability, district
    operator = db.Column(db.String(8), nullable=False) # '<=', '>=', '==', 'IN', 'BOOLEAN'
    expected_value = db.Column(db.String(128), nullable=False)
    rule_explanation_en = db.Column(db.Text, nullable=False)
    rule_explanation_kn = db.Column(db.Text, nullable=False)
    rule_explanation_hi = db.Column(db.Text, nullable=True)
    source_clause = db.Column(db.String(128), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'field_name': self.field_name,
            'operator': self.operator,
            'expected_value': self.expected_value,
            'rule_explanation_en': self.rule_explanation_en,
            'rule_explanation_kn': self.rule_explanation_kn,
            'rule_explanation_hi': self.rule_explanation_hi or self.rule_explanation_en,
            'source_clause': self.source_clause
        }


class SchemeApplication(db.Model):
    __tablename__ = 'scheme_applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    scheme_id = db.Column(db.Integer, db.ForeignKey('schemes.id', ondelete='CASCADE'), nullable=False)
    application_ref = db.Column(db.String(64), unique=True, nullable=False, index=True) # e.g. APP-2026-KM-1001
    
    applicant_name = db.Column(db.String(128), nullable=False)
    applicant_mobile = db.Column(db.String(20), nullable=False)
    district = db.Column(db.String(64), default='Mandya')
    taluk = db.Column(db.String(64), default='Pandavapura')
    village = db.Column(db.String(64), default='Chikka Byadarahalli')
    land_acres = db.Column(db.Float, default=2.5)
    crops_summary = db.Column(db.String(128), default='Paddy, Ragi')
    
    benefit_amount_expected = db.Column(db.String(64), default='₹6,000 / year')
    benefit_amount_disbursed = db.Column(db.String(64), default='₹0')
    
    # Application statuses
    status = db.Column(db.String(32), default='SUBMITTED') # NOT_APPLIED, APPLICATION_STARTED, SUBMITTED, UNDER_VERIFICATION, PENDING, APPROVED, REJECTED, BENEFIT_DISBURSED, ADDITIONAL_DOCUMENTS_REQUIRED
    status_notes = db.Column(db.Text, nullable=True)
    
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_demo_submission = db.Column(db.Boolean, default=True)

    # Status Timeline History
    status_history = db.relationship('ApplicationStatusHistory', backref='application', cascade='all, delete-orphan', order_by='ApplicationStatusHistory.timestamp.asc()')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'scheme_id': self.scheme_id,
            'scheme_code': self.scheme.code if self.scheme else 'UNKNOWN',
            'scheme_name_en': self.scheme.name_en if self.scheme else 'Scheme',
            'scheme_name_kn': self.scheme.name_kn if self.scheme else 'ಯೋಜನೆ',
            'application_ref': self.application_ref,
            'applicant_name': self.applicant_name,
            'applicant_mobile': self.applicant_mobile,
            'district': self.district,
            'taluk': self.taluk,
            'village': self.village,
            'land_acres': self.land_acres,
            'crops_summary': self.crops_summary,
            'benefit_amount_expected': self.benefit_amount_expected,
            'benefit_amount_disbursed': self.benefit_amount_disbursed,
            'status': self.status,
            'status_notes': self.status_notes,
            'applied_at': self.applied_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_updated_at': self.last_updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_demo_submission': self.is_demo_submission,
            'timeline': [h.to_dict() for h in self.status_history]
        }


class ApplicationStatusHistory(db.Model):
    __tablename__ = 'application_status_history'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('scheme_applications.id', ondelete='CASCADE'), nullable=False)
    previous_status = db.Column(db.String(32), nullable=True)
    new_status = db.Column(db.String(32), nullable=False)
    stage_name = db.Column(db.String(64), nullable=False) # 'Application Submitted', 'Document Verification', 'Department Review', 'Application Approved', 'Benefit Disbursed'
    remarks = db.Column(db.Text, nullable=True)
    updated_by = db.Column(db.String(64), default='SYSTEM')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'stage_name': self.stage_name,
            'previous_status': self.previous_status,
            'new_status': self.new_status,
            'remarks': self.remarks,
            'updated_by': self.updated_by,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }


class FarmerNotification(db.Model):
    __tablename__ = 'farmer_notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title_en = db.Column(db.String(128), nullable=False)
    title_kn = db.Column(db.String(128), nullable=False)
    title_hi = db.Column(db.String(128), nullable=True)
    message_en = db.Column(db.Text, nullable=False)
    message_kn = db.Column(db.Text, nullable=False)
    message_hi = db.Column(db.Text, nullable=True)
    notification_type = db.Column(db.String(32), default='APPLICATION_UPDATE') # SCHEME_ELIGIBLE, APPLICATION_UPDATE, BENEFIT_DISBURSED, DEADLINE_REMINDER, VERIFICATION_SUCCESS
    related_scheme_id = db.Column(db.Integer, nullable=True)
    related_application_id = db.Column(db.Integer, nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title_en': self.title_en,
            'title_kn': self.title_kn,
            'title_hi': self.title_hi or self.title_en,
            'message_en': self.message_en,
            'message_kn': self.message_kn,
            'message_hi': self.message_hi or self.message_en,
            'notification_type': self.notification_type,
            'related_scheme_id': self.related_scheme_id,
            'related_application_id': self.related_application_id,
            'is_read': self.is_read,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class AdminUser(db.Model):
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    department = db.Column(db.String(128), default='Karnataka Department of Agriculture')
    phone_number = db.Column(db.String(20), nullable=True, index=True)
    role = db.Column(db.String(32), default='SUPER_ADMIN') # SUPER_ADMIN, DISTRICT_OFFICER, AGRONOMIST
    district = db.Column(db.String(64), default='Karnataka State')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'department': self.department,
            'role': self.role,
            'district': self.district,
            'is_active': self.is_active
        }


class AdminActivityLog(db.Model):
    __tablename__ = 'admin_activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_users.id', ondelete='SET NULL'), nullable=True)
    action_type = db.Column(db.String(64), nullable=False) # STATUS_UPDATE, SCHEME_EDIT, NOTIFICATION_SENT, FARMER_VERIFY
    target_entity = db.Column(db.String(64), nullable=False)
    target_id = db.Column(db.String(64), nullable=False)
    details_json = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), default='127.0.0.1')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'admin_id': self.admin_id,
            'action_type': self.action_type,
            'target_entity': self.target_entity,
            'target_id': self.target_id,
            'details': json.loads(self.details_json) if self.details_json else {},
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }


# ============================================================================
# Existing Models Preserved for Backwards Compatibility
# ============================================================================

class SchemeAssessment(db.Model):
    __tablename__ = 'scheme_assessments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    scheme_id = db.Column(db.Integer, db.ForeignKey('schemes.id', ondelete='CASCADE'), nullable=False)
    overall_status = db.Column(db.String(16), nullable=False) # MATCH, NO_MATCH, UNKNOWN
    rules_evaluated_json = db.Column(db.Text, nullable=False)
    missing_fields_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    scheme = db.relationship('Scheme')

    def to_dict(self):
        return {
            'id': self.id,
            'scheme_code': self.scheme.code if self.scheme else 'UNKNOWN',
            'scheme_name_en': self.scheme.name_en if self.scheme else 'Scheme',
            'scheme_name_kn': self.scheme.name_kn if self.scheme else 'ಯೋಜನೆ',
            'portal': self.scheme.official_portal if self.scheme else '',
            'overall_status': self.overall_status,
            'rules_evaluated': json.loads(self.rules_evaluated_json) if self.rules_evaluated_json else [],
            'missing_fields': json.loads(self.missing_fields_json) if self.missing_fields_json else [],
            'assessed_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(128), default='New Interaction')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    messages = db.relationship('Message', backref='conversation', cascade='all, delete-orphan', order_by='Message.created_at')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'message_count': len(self.messages)
        }


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False)
    sender = db.Column(db.String(16), nullable=False)
    content = db.Column(db.Text, nullable=False)
    audio_transcript = db.Column(db.Text, nullable=True)
    language = db.Column(db.String(8), default='kn')
    metadata_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'content': self.content,
            'language': self.language,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'metadata': json.loads(self.metadata_json) if self.metadata_json else {}
        }


class FarmCalculation(db.Model):
    __tablename__ = 'farm_calculations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(128), default='Crop Budget Comparison')
    scenario_a_json = db.Column(db.Text, nullable=False)
    scenario_b_json = db.Column(db.Text, nullable=False)
    comparison_summary_json = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'scenario_a': json.loads(self.scenario_a_json),
            'scenario_b': json.loads(self.scenario_b_json),
            'comparison': json.loads(self.comparison_summary_json),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class FarmTask(db.Model):
    __tablename__ = 'farm_tasks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(32), default='FIELD_WORK')
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(16), default='PENDING')
    source_reference = db.Column(db.String(128), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'due_date': self.due_date.strftime('%Y-%m-%d'),
            'status': self.status,
            'source_reference': self.source_reference,
            'notes': self.notes
        }


class DecisionEvent(db.Model):
    __tablename__ = 'decision_events'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    event_type = db.Column(db.String(32), nullable=False)
    user_input = db.Column(db.Text, nullable=True)
    extracted_entities_json = db.Column(db.Text, nullable=True)
    rule_or_model_used = db.Column(db.String(64), nullable=False)
    result_status = db.Column(db.String(32), nullable=False)
    source_citations = db.Column(db.Text, nullable=True)
    uncertainty_statement = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'event_type': self.event_type,
            'user_input': self.user_input,
            'extracted_entities': json.loads(self.extracted_entities_json) if self.extracted_entities_json else {},
            'rule_or_model_used': self.rule_or_model_used,
            'result_status': self.result_status,
            'source_citations': json.loads(self.source_citations) if self.source_citations else [],
            'uncertainty_statement': self.uncertainty_statement,
            'timestamp': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

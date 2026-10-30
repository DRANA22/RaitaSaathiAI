import random
from datetime import datetime
from flask import Blueprint, request, session
from app.extensions import db
from app.models import User, Scheme, SchemeApplication, ApplicationStatusHistory, FarmerNotification
from app.utils.errors import api_response, bad_request, not_found, unauthorized

applications_bp = Blueprint('applications', __name__, url_prefix='/api/applications')

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

@applications_bp.route('', methods=['GET'])
def list_applications():
    """Retrieve all applications for the current farmer."""
    user = get_or_create_active_user()
    if not user:
        return api_response(data={"applications": [], "counts": {}})

    status_filter = request.args.get('status')
    query = SchemeApplication.query.filter_by(user_id=user.id)
    if status_filter and status_filter != 'ALL':
        query = query.filter_by(status=status_filter.upper())

    apps = query.order_by(SchemeApplication.applied_at.desc()).all()

    # Aggregate counts for dashboard
    all_apps = SchemeApplication.query.filter_by(user_id=user.id).all()
    counts = {
        "total": len(all_apps),
        "submitted": sum(1 for a in all_apps if a.status in ('SUBMITTED', 'APPLICATION_STARTED')),
        "pending": sum(1 for a in all_apps if a.status in ('PENDING', 'UNDER_VERIFICATION', 'SUBMITTED')),
        "approved": sum(1 for a in all_apps if a.status in ('APPROVED', 'BENEFIT_DISBURSED')),
        "rejected": sum(1 for a in all_apps if a.status == 'REJECTED'),
        "disbursed": sum(1 for a in all_apps if a.status == 'BENEFIT_DISBURSED')
    }

    return api_response(data={
        "applications": [a.to_dict() for a in apps],
        "statistics": counts
    })


@applications_bp.route('', methods=['POST'])
def submit_application():
    """
    Simulated Government Scheme Application Submission.
    Generates unique application reference number, records initial timeline stage,
    and dispatches confirmation notification.
    """
    user = get_or_create_active_user()
    if not user:
        return bad_request("Active farmer session required.")

    data = request.get_json() or {}
    scheme_id = data.get('scheme_id')
    if not scheme_id:
        return bad_request("Scheme ID is required.")

    scheme = Scheme.query.get(scheme_id)
    if not scheme:
        return not_found("Scheme not found.")

    # Check if already applied
    existing = SchemeApplication.query.filter_by(user_id=user.id, scheme_id=scheme.id).first()
    if existing:
        return api_response(data={
            "already_applied": True,
            "application": existing.to_dict(),
            "message_kn": "ನೀವು ಈಗಾಗಲೇ ಈ ಯೋಜನೆಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಿದ್ದೀರಿ.",
            "message_en": "You have already applied for this scheme."
        })

    profile = user.profile
    app_ref = f"APP-2026-KM-{random.randint(1000, 9999)}"

    # Create application
    application = SchemeApplication(
        user_id=user.id,
        scheme_id=scheme.id,
        application_ref=app_ref,
        applicant_name=user.full_name,
        applicant_mobile=user.phone_number or '9845012345',
        district=profile.district if profile else 'Mandya',
        taluk=profile.taluk if profile else 'Pandavapura',
        village=profile.village if profile else 'Chikka Byadarahalli',
        land_acres=profile.total_land_acres if profile else 2.5,
        crops_summary=", ".join([c.crop_name_english for c in profile.crops]) if (profile and profile.crops) else 'Paddy, Ragi',
        benefit_amount_expected=scheme.max_benefit,
        benefit_amount_disbursed='₹0',
        status='SUBMITTED',
        status_notes='Application successfully lodged on RaitaSaathiAI portal. Under preliminary departmental review.',
        is_demo_submission=True
    )
    db.session.add(application)
    db.session.flush()

    # Create Initial Timeline History Stage
    stage = ApplicationStatusHistory(
        application_id=application.id,
        previous_status=None,
        new_status='SUBMITTED',
        stage_name='Application Submitted',
        remarks='Application successfully submitted with verified digital farmer credentials.',
        updated_by='SYSTEM'
    )
    db.session.add(stage)

    # In-App Notification
    notif = FarmerNotification(
        user_id=user.id,
        title_en=f"Application Lodged: {scheme.name_en}",
        title_kn=f"ಅರ್ಜಿ ಸಲ್ಲಿಸಲಾಗಿದೆ: {scheme.name_kn}",
        title_hi=f"आवेदन जमा किया गया: {scheme.name_en}",
        message_en=f"Your application for '{scheme.name_en}' is submitted. Reference ID: {app_ref}.",
        message_kn=f"'{scheme.name_kn}' ಯೋಜನೆಗೆ ನಿಮ್ಮ ಅರ್ಜಿ ಸ್ವೀಕರಿಸಲಾಗಿದೆ. ಅರ್ಜಿ ಸಂಖ್ಯೆ: {app_ref}.",
        message_hi=f"'{scheme.name_en}' के लिए आपका आवेदन जमा हो गया है। संदर्भ आईडी: {app_ref}।",
        notification_type="APPLICATION_UPDATE",
        related_scheme_id=scheme.id,
        related_application_id=application.id
    )
    db.session.add(notif)
    db.session.commit()

    return api_response(data={
        "application": application.to_dict(),
        "application_ref": app_ref,
        "official_portal": scheme.official_portal,
        "message_kn": f"ಅರ್ಜಿ ಯಶಸ್ವಿಯಾಗಿ ಸಲ್ಲಿಸಲಾಗಿದೆ! ಅರ್ಜಿ ಸಂಖ್ಯೆ: {app_ref}",
        "message_en": f"Application submitted successfully! Reference Number: {app_ref}"
    }, status_code=201)


@applications_bp.route('/<int:app_id>/timeline', methods=['GET'])
def get_application_timeline(app_id):
    """Retrieve visual 5-stage timeline for a scheme application."""
    user = get_or_create_active_user()
    application = SchemeApplication.query.get(app_id)
    if not application:
        return not_found("Application not found.")

    # 5 Master Stages
    master_stages = [
        {"key": "SUBMITTED", "name_en": "Application Submitted", "name_kn": "ಅರ್ಜಿ ಸಲ್ಲಿಕೆ", "name_hi": "आवेदन जमा"},
        {"key": "UNDER_VERIFICATION", "name_en": "Document Verification", "name_kn": "ದಾಖಲೆಗಳ ಪರಿಶೀಲನೆ", "name_hi": "दस्तावेज़ सत्यापन"},
        {"key": "DEPARTMENT_REVIEW", "name_en": "Department Review", "name_kn": "ಇಲಾಖಾ ಪರಿಶೀಲನೆ", "name_hi": "विभागीय समीक्षा"},
        {"key": "APPROVED", "name_en": "Application Approved", "name_kn": "ಅರ್ಜಿ ಅನುಮೋದನೆ", "name_hi": "आवेदन स्वीकृत"},
        {"key": "BENEFIT_DISBURSED", "name_en": "Benefit Disbursed", "name_kn": "ಸೌಲಭ್ಯ ವರ್ಗಾವಣೆ", "name_hi": "लाभ संवितरित"}
    ]

    # Map current status to step index (1-based)
    status_order = {
        'SUBMITTED': 1,
        'UNDER_VERIFICATION': 2,
        'PENDING': 3,
        'APPROVED': 4,
        'BENEFIT_DISBURSED': 5,
        'REJECTED': 4,
        'ADDITIONAL_DOCUMENTS_REQUIRED': 2
    }
    current_step = status_order.get(application.status, 1)

    return api_response(data={
        "application": application.to_dict(),
        "current_step": current_step,
        "is_approved": application.status in ('APPROVED', 'BENEFIT_DISBURSED'),
        "is_rejected": application.status == 'REJECTED',
        "master_stages": master_stages,
        "history": [h.to_dict() for h in application.status_history]
    })


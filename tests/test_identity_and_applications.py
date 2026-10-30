import pytest
import json
from app import create_app
from app.extensions import db
from app.models import User, Scheme, SchemeApplication, FarmerNotification, AdminUser

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_aadhaar_otp_generation_and_registration(client):
    # Step 1: Generate OTP
    res1 = client.post('/api/identity/generate-otp', json={
        "full_name": "Suresh Gowda",
        "mobile_number": "9845112233",
        "aadhaar_number": "548912348421",
        "consent": True
    })
    assert res1.status_code == 200
    data1 = res1.get_json()["data"]
    assert "transaction_id" in data1
    assert data1["masked_aadhaar"] == "XXXX-XXXX-8421"
    txn_id = data1["transaction_id"]

    # Step 2: Verify OTP
    res2 = client.post('/api/identity/verify-otp', json={
        "transaction_id": txn_id,
        "otp": "2026"
    })
    assert res2.status_code == 200
    assert res2.get_json()["data"]["verification_status"] == "VERIFIED"

    # Step 3: Complete Registration
    res3 = client.post('/api/identity/complete-registration', json={
        "transaction_id": txn_id,
        "district": "Mandya",
        "taluk": "Pandavapura",
        "village": "Chikka Byadarahalli",
        "total_land_acres": 3.0,
        "irrigation_type": "BOREWELL"
    })
    assert res3.status_code == 201
    data3 = res3.get_json()["data"]
    assert "KM-KA-2026-" in data3["farmer_id"]
    assert data3["profile"]["district"] == "Mandya"
    assert data3["profile"]["verification_status"] == "VERIFIED"

def test_scheme_application_submission_and_tracking(client):
    # Create test scheme
    scheme = Scheme(
        code="PM_KISAN_TEST",
        name_en="PM-KISAN",
        name_kn="ಪಿಎಂ-ಕಿಸಾನ್",
        department_en="Ministry of Agriculture",
        department_kn="ಕೃಷಿ ಇಲಾಖೆ",
        category="FINANCIAL",
        official_portal="https://pmkisan.gov.in",
        brief_summary_en="Income support",
        brief_summary_kn="ಆದಾಯ ಬೆಂಬಲ",
        max_benefit="₹6,000 / year",
        required_documents='["Aadhaar", "RTC"]',
        application_process="Online",
        is_active=True
    )
    db.session.add(scheme)
    db.session.commit()

    # Register farmer
    reg = client.post('/api/identity/complete-registration', json={
        "full_name": "Ramesh Gowda",
        "mobile_number": "9845012345",
        "district": "Mandya",
        "total_land_acres": 2.5
    })
    assert reg.status_code == 201

    # Submit application
    app_res = client.post('/api/applications', json={"scheme_id": scheme.id})
    assert app_res.status_code == 201
    app_data = app_res.get_json()["data"]
    assert "APP-2026-KM-" in app_data["application_ref"]
    app_id = app_data["application"]["id"]

    # Check tracking
    track_res = client.get('/api/applications')
    assert track_res.status_code == 200
    assert len(track_res.get_json()["data"]["applications"]) == 1

    # Check 5-stage timeline
    time_res = client.get(f'/api/applications/{app_id}/timeline')
    assert time_res.status_code == 200
    assert len(time_res.get_json()["data"]["master_stages"]) == 5
    assert time_res.get_json()["data"]["current_step"] == 1

    # Admin updates status to APPROVED
    admin_res = client.patch(f'/api/admin/applications/{app_id}/status', json={
        "status": "APPROVED",
        "remarks": "Land RTC verified against FRUITS database."
    })
    assert admin_res.status_code == 200
    assert admin_res.get_json()["data"]["application"]["status"] == "APPROVED"

    # Check farmer notification
    notif_res = client.get('/api/notifications')
    assert notif_res.status_code == 200
    notifs = notif_res.get_json()["data"]["notifications"]
    assert len(notifs) >= 1
    assert "APPROVED" in notifs[0]["title_en"].upper() or "APPROVED" in notifs[0]["message_en"].upper()

def test_voice_assistant_approved_schemes_intent(client):
    # Register and submit application
    scheme = Scheme(
        code="RAITHA_SIRI_TEST",
        name_en="Raitha Siri",
        name_kn="ರೈತ ಸಿರಿ",
        department_en="Dept of Agriculture",
        department_kn="ಕೃಷಿ ಇಲಾಖೆ",
        category="FINANCIAL",
        official_portal="https://raitamitra.karnataka.gov.in",
        brief_summary_en="Millet incentive",
        brief_summary_kn="ಸಿರಿಧಾನ್ಯ ಪ್ರೋತ್ಸಾಹಧನ",
        max_benefit="₹10,000 / ha",
        required_documents='["RTC"]',
        application_process="Online",
        is_active=True
    )
    db.session.add(scheme)
    db.session.commit()

    client.post('/api/identity/complete-registration', json={
        "full_name": "Ramesh Gowda",
        "mobile_number": "9845012345"
    })
    app_res = client.post('/api/applications', json={"scheme_id": scheme.id})
    app_id = app_res.get_json()["data"]["application"]["id"]

    # Approve application
    client.patch(f'/api/admin/applications/{app_id}/status', json={"status": "APPROVED"})

    # Ask voice assistant in Kannada
    msg_res = client.post('/api/assistant/message', json={
        "message": "ನನ್ನ ಅನುಮೋದಿತ ಯೋಜನೆಗಳನ್ನು ತೋರಿಸು (Show my approved schemes)",
        "language": "kn"
    })
    assert msg_res.status_code == 200
    msg_data = msg_res.get_json()["data"]
    assert msg_data["action"] == "FILTER_APPLICATIONS_APPROVED"
    assert "ಅನುಮೋದನೆಗೊಂಡಿವೆ" in msg_data["answer_kn"] or "Raitha Siri" in msg_data["answer_kn"]

def test_voice_assistant_kannada_agronomic_queries(client):
    # Test spoken Kannada agronomic advice for Ragi
    res_ragi = client.post('/api/assistant/message', json={
        "message": "ರಾಗಿ ಬೆಳೆಗೆ ಎಷ್ಟು ಗೊಬ್ಬರ ಹಾಕಬೇಕು?",
        "language": "kn"
    })
    assert res_ragi.status_code == 200
    data_ragi = res_ragi.get_json()["data"]
    assert "ರಾಗಿ" in data_ragi["answer"]
    assert "NPK" in data_ragi["answer"] or "ಗೊಬ್ಬರ" in data_ragi["answer"]
    assert "UAS" in data_ragi["source"] or "ICAR" in data_ragi["source"]

    # Test spoken Kannada crop disease query for Tomato
    res_tomato = client.post('/api/assistant/message', json={
        "message": "ಟೊಮೆಟೊ ಬೆಳೆಯಲ್ಲಿ ಎಲೆ ಸುರುಟು ರೋಗಕ್ಕೆ ಔಷಧಿ ತಿಳಿಸಿ",
        "language": "kn"
    })
    assert res_tomato.status_code == 200
    data_tomato = res_tomato.get_json()["data"]
    assert "ಟೊಮೆಟೊ" in data_tomato["answer"]
    assert "ಇಮಿಡಾಕ್ಲೋಪ್ರಿಡ್" in data_tomato["answer"] or "ಎಲೆ ಸುರುಟು" in data_tomato["answer"]

    # Test Krishi Echo confirmation trigger on farm profile declaration
    res_echo = client.post('/api/assistant/message', json={
        "message": "ನಾನು ಎರಡೂವರೆ ಎಕರೆಯಲ್ಲಿ ಟೊಮೆಟೊ ಬೆಳೆಯುತ್ತಿದ್ದೇನೆ",
        "language": "kn"
    })
    assert res_echo.status_code == 200
    data_echo = res_echo.get_json()["data"]
    assert data_echo["status"] == "AWAITING_CONFIRMATION"
    assert "2.5" in data_echo["confirmation_card"]["prompt"] or "ಎರಡೂವರೆ" in data_echo["confirmation_card"]["prompt"]
    assert "ಟೊಮೆಟೊ" in data_echo["confirmation_card"]["prompt"]




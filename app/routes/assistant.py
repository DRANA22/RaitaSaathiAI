from flask import Blueprint, request, session
import json
from app.extensions import db
from app.models import Conversation, Message, DecisionEvent, User, SchemeApplication, Scheme
from app.services.ai_provider import AIProviderService
from app.services.speech_provider import SpeechDialectService
from app.services.scheme_engine import SchemeEligibilityEngine
from app.utils.errors import api_response, bad_request, unauthorized

assistant_bp = Blueprint('assistant', __name__, url_prefix='/api/assistant')

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

@assistant_bp.route('/message', methods=['POST'])
def handle_message():
    user = get_or_create_active_user()
    data = request.get_json() or {}
    user_text = data.get('message', '').strip()
    language = data.get('language', user.preferred_language if user else 'kn')
    confirmed_entities = data.get('confirmed_entities', None)

    if not user_text:
        return bad_request("Message content cannot be empty.")

    lower_text = user_text.lower()

    # =========================================================================
    # INTENT 1: Approved Schemes Query
    # Commands: "Show my approved schemes", "ಯಾವ ಯೋಜನೆಗಳು ಅನುಮೋದನೆಗೊಂಡಿವೆ?", "ಅನುಮೋದಿತ ಯೋಜನೆಗಳು"
    # =========================================================================
    if any(k in lower_text for k in [
        "approved", "ಅನುಮೋದನೆ", "ಅನುಮೋದಿತ", "स्वीकृत", "approve", "ಯಾವ ಯೋಜನೆ ಸಿಕ್ಕಿದೆ"
    ]):
        approved = []
        if user:
            approved = SchemeApplication.query.filter(
                SchemeApplication.user_id == user.id,
                SchemeApplication.status.in_(['APPROVED', 'BENEFIT_DISBURSED'])
            ).all()

        if approved:
            names_kn = [a.scheme.name_kn for a in approved if a.scheme]
            names_en = [a.scheme.name_en for a in approved if a.scheme]
            count = len(approved)

            ans_kn = f"ನಿಮ್ಮ {count} ಯೋಜನೆಗಳು ಅನುಮೋದನೆಗೊಂಡಿವೆ: {', '.join(names_kn)}. ನಿಮ್ಮ ಅರ್ಜಿಗಳನ್ನು ಕೆಳಗೆ ತೋರಿಸಲಾಗುತ್ತಿದೆ."
            ans_en = f"You have {count} approved schemes: {', '.join(names_en)}. Displaying them on your tracking dashboard."
            ans_hi = f"आपकी {count} योजनाएं स्वीकृत हो चुकी हैं: {', '.join(names_en)}।"
        else:
            ans_kn = "ಪ್ರಸ್ತುತ ಯಾವುದೇ ಅನುಮೋದಿತ ಅರ್ಜಿಗಳಿಲ್ಲ. ನಿಮ್ಮ ಸಲ್ಲಿಸಿದ ಅರ್ಜಿಗಳು ಪರಿಶೀಲನೆಯಲ್ಲಿವೆ."
            ans_en = "You do not have any approved schemes yet. Submitted applications are under review."
            ans_hi = "वर्तमान में कोई स्वीकृत योजना नहीं है। आपके आवेदन समीक्षाधीन हैं।"

        speech_ans = ans_kn if language == 'kn' else (ans_hi if language == 'hi' else ans_en)
        return api_response(data={
            "action": "FILTER_APPLICATIONS_APPROVED",
            "answer": speech_ans,
            "answer_kn": ans_kn,
            "answer_en": ans_en,
            "answer_hi": ans_hi,
            "count": len(approved),
            "source": "RaitaSaathiAI Application Tracking System",
            "verification": "100% Deterministic Database Records"
        })

    # =========================================================================
    # INTENT 2: Pending Applications Query
    # Commands: "Tell me my pending applications", "ಬಾಕಿ ಅರ್ಜಿಗಳ ವಿವರ", "लंबित योजनाएं"
    # =========================================================================
    if any(k in lower_text for k in [
        "pending", "ಬಾಕಿ", "ಪರಿಶೀಲನೆ", "लंबित", "status of application", "ಅರ್ಜಿ ಸ್ಥಿತಿ"
    ]):
        pending = []
        if user:
            pending = SchemeApplication.query.filter(
                SchemeApplication.user_id == user.id,
                SchemeApplication.status.in_(['SUBMITTED', 'UNDER_VERIFICATION', 'DEPARTMENT_REVIEW', 'PENDING'])
            ).all()

        if pending:
            names_kn = [a.scheme.name_kn for a in pending if a.scheme]
            names_en = [a.scheme.name_en for a in pending if a.scheme]
            count = len(pending)

            ans_kn = f"ನಿಮ್ಮ {count} ಅರ್ಜಿಗಳು ಪ್ರಸ್ತುತ ಇಲಾಖಾ ಪರಿಶೀಲನೆಯಲ್ಲಿವೆ (Pending): {', '.join(names_kn)}."
            ans_en = f"You have {count} pending applications currently under review: {', '.join(names_en)}."
            ans_hi = f"आपके {count} आवेदन वर्तमान में समीक्षाधीन हैं: {', '.join(names_en)}।"
        else:
            ans_kn = "ನಿಮ್ಮ ಯಾವುದೇ ಅರ್ಜಿಗಳು ಬಾಕಿ ಉಳಿದಿಲ್ಲ."
            ans_en = "You have no pending applications at this time."
            ans_hi = "आपका कोई आवेदन लंबित नहीं है।"

        speech_ans = ans_kn if language == 'kn' else (ans_hi if language == 'hi' else ans_en)
        return api_response(data={
            "action": "FILTER_APPLICATIONS_PENDING",
            "answer": speech_ans,
            "answer_kn": ans_kn,
            "answer_en": ans_en,
            "answer_hi": ans_hi,
            "count": len(pending),
            "source": "RaitaSaathiAI Application Tracking System",
            "verification": "100% Deterministic Database Records"
        })

    # =========================================================================
    # INTENT 3: Recommended / Eligible Schemes Query
    # Commands: "ನನಗೆ ಯಾವ ಯೋಜನೆಗಳು ಸಿಗುತ್ತವೆ?", "Show eligible schemes", "मुझे कौन सी योजनाएं मिल सकती हैं?"
    # =========================================================================
    if any(k in lower_text for k in [
        "ಯಾವ ಯೋಜನೆ", "ಯೋಜನೆಗಳು ಸಿಗುತ್ತವೆ", "eligible schemes", "schemes for me", "योजनाएं मिल सकती", "ಯಾವ ಸರ್ಕಾರಿ ಯೋಜನೆ"
    ]):
        eligible_schemes = []
        if user and user.profile:
            eval_context = {
                'total_land_acres': user.profile.total_land_acres,
                'farmer_category': user.profile.farmer_category,
                'social_category': user.profile.social_category,
                'irrigation_type': user.profile.irrigation_type,
                'state': 'Karnataka',
                'district': user.profile.district,
                'has_aadhaar': True,
                'has_pm_kisan': True,
                'has_kisan_credit_card': False
            }
            all_s = Scheme.query.filter_by(is_active=True).all()
            for s in all_s:
                ev = SchemeEligibilityEngine.evaluate_scheme(s, eval_context)
                if ev["eligibility_category"] == "ELIGIBLE":
                    eligible_schemes.append(s)

        count = len(eligible_schemes)
        names_kn = [s.name_kn for s in eligible_schemes[:3]]
        names_en = [s.name_en for s in eligible_schemes[:3]]

        ans_kn = f"ನಿಮ್ಮ {user.profile.total_land_acres if user and user.profile else 2.5} ಎಕರೆ ಕೃಷಿ ವಿವರಗಳಿಗೆ ಒಟ್ಟು {count} ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು ಲಭ್ಯವಿವೆ: {', '.join(names_kn)} ಇತ್ಯಾದಿ. ಕೆಳಗೆ ಶಿಫಾರಸುಗಳನ್ನು ನೋಡಬಹುದು."
        ans_en = f"Based on your farm profile, you are eligible for {count} government schemes including: {', '.join(names_en)}. Displaying recommendations on your dashboard."
        ans_hi = f"आपके कृषि विवरण के आधार पर आप {count} सरकारी योजनाओं के लिए पात्र हैं, जिनमें {', '.join(names_en)} शामिल हैं।"

        speech_ans = ans_kn if language == 'kn' else (ans_hi if language == 'hi' else ans_en)
        return api_response(data={
            "action": "NAVIGATE_RECOMMENDED_SCHEMES",
            "answer": speech_ans,
            "answer_kn": ans_kn,
            "answer_en": ans_en,
            "answer_hi": ans_hi,
            "count": count,
            "source": "AI-Based Scheme Recommendation Engine",
            "verification": "Grounded in Karnataka Seva Sindhu & PM-Kisan Official Rules"
        })

    # =========================================================================
    # INTENT 4: General Agronomic Advice & Crop Intelligence (Fallback to AIProvider)
    # =========================================================================
    ai_service = AIProviderService()
    context = {}
    if user and user.profile:
        context = {
            "district": user.profile.district,
            "acres": user.profile.total_land_acres,
            "farmer_category": user.profile.farmer_category,
            "irrigation": user.profile.irrigation_type,
            "crops": [c.crop_name_english for c in user.profile.crops]
        }

    # Extract entities and detect dialect
    extracted = ai_service.extract_farm_entities(user_text)
    
    # Krishi Echo: If entities are detected and user hasn't confirmed yet, return confirmation card
    if extracted["needs_confirmation"] and confirmed_entities is None:
        echo_prompt = SpeechDialectService.build_confirmation_statement(
            crop_en=extracted["crop"] or "Crop",
            crop_kn=extracted["crop_kannada"] or "ಬೆಳೆ",
            acres=extracted["acres"] or context.get("acres", 2.0),
            language=language
        )
        return api_response(data={
            "status": "AWAITING_CONFIRMATION",
            "confirmation_card": {
                "prompt": echo_prompt,
                "entities": extracted,
                "action_type": extracted["intent"]
            }
        })

    # Run agricultural knowledge logic
    ai_result = ai_service.answer_agricultural_query(user_text, context=context, language=language)

    # Save to Conversation thread
    if user:
        conv = Conversation.query.filter_by(user_id=user.id).order_by(Conversation.created_at.desc()).first()
        if not conv:
            conv = Conversation(user_id=user.id, title=user_text[:40] or "Krishi Discussion")
            db.session.add(conv)
            db.session.flush()

        user_msg = Message(conversation_id=conv.id, sender='user', content=user_text, language=language)
        bot_msg = Message(
            conversation_id=conv.id,
            sender='assistant',
            content=ai_result["response_text"],
            language=language,
            metadata_json=json.dumps({
                "source": ai_result.get("source"),
                "verification": ai_result.get("verification")
            })
        )
        db.session.add(user_msg)
        db.session.add(bot_msg)
        db.session.commit()

    return api_response(data={
        "status": "COMPLETED",
        "answer": ai_result["response_text"],
        "source": ai_result["source"],
        "verification": ai_result["verification"]
    })

"""
AI & Deterministic Rule-Based Scheme Eligibility Engine.
Categorizes schemes into:
1. ELIGIBLE: The farmer satisfies all verified eligibility conditions.
2. POSSIBLY_ELIGIBLE: Minor information is missing or pending manual verification.
3. NOT_ELIGIBLE: The farmer does not satisfy one or more criteria.
4. APPLICATION_OPEN / APPLICATION_CLOSED: Scheme application window availability.

Provides explainable reasoning:
- "Why are you eligible for this scheme?" (Kn/En/Hi)
- "What documents do you need?"
"""
from typing import Dict, Any, List
import json

STATUS_ELIGIBLE = "ELIGIBLE"
STATUS_POSSIBLY_ELIGIBLE = "POSSIBLY_ELIGIBLE"
STATUS_NOT_ELIGIBLE = "NOT_ELIGIBLE"

# Backward compatibility aliases
STATUS_MATCH = "MATCH"
STATUS_NO_MATCH = "NO_MATCH"
STATUS_UNKNOWN = "UNKNOWN"

class SchemeEligibilityEngine:
    @staticmethod
    def evaluate_single_rule(rule, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        field = rule.field_name
        operator = rule.operator
        expected = rule.expected_value
        
        # Check if farmer profile contains the field
        if field not in profile_data or profile_data[field] is None:
            return {
                "rule_id": rule.id,
                "field": field,
                "operator": operator,
                "expected": expected,
                "actual": None,
                "status": STATUS_UNKNOWN,
                "is_match": False,
                "explanation_en": f"Information for '{field}' needs verification.",
                "explanation_kn": f"'{field}' ಬಗೆಗಿನ ವಿವರ ಪರಿಶೀಲನೆಯಲ್ಲಿದೆ.",
                "explanation_hi": f"'{field}' की जानकारी सत्यापन योग्य है।",
                "source_clause": rule.source_clause
            }
            
        actual = profile_data[field]
        is_match = False
        
        # Numeric comparisons
        if operator in ('<=', '>=', '<', '>', '=='):
            try:
                num_actual = float(actual)
                num_expected = float(expected)
                
                if operator == '<=' and num_actual <= num_expected:
                    is_match = True
                elif operator == '>=' and num_actual >= num_expected:
                    is_match = True
                elif operator == '<' and num_actual < num_expected:
                    is_match = True
                elif operator == '>' and num_actual > num_expected:
                    is_match = True
                elif operator == '==' and num_actual == num_expected:
                    is_match = True
            except (ValueError, TypeError):
                if str(actual).strip().lower() == str(expected).strip().lower():
                    is_match = True
                    
        elif operator == 'BOOLEAN':
            bool_actual = bool(actual)
            bool_expected = str(expected).strip().lower() in ('true', '1', 'yes')
            if bool_actual == bool_expected:
                is_match = True
                
        elif operator == 'IN':
            allowed_values = [v.strip().upper() for v in expected.split(',')]
            if str(actual).strip().upper() in allowed_values:
                is_match = True

        status = STATUS_MATCH if is_match else STATUS_NO_MATCH

        explanation_en = (
            rule.rule_explanation_en if is_match 
            else f"Criteria requirement: {field} must be {operator} {expected} (Current: {actual})."
        )
        explanation_kn = (
            rule.rule_explanation_kn if is_match
            else f"ಷರತ್ತು: {field} {operator} {expected} ಆಗಿರಬೇಕು (ಪ್ರಸ್ತುತ: {actual})."
        )
        explanation_hi = (
            getattr(rule, 'rule_explanation_hi', None) or rule.rule_explanation_en if is_match
            else f"शर्त: {field} {operator} {expected} होना चाहिए (वर्तमान: {actual})."
        )

        return {
            "rule_id": rule.id,
            "field": field,
            "operator": operator,
            "expected": expected,
            "actual": actual,
            "status": status,
            "is_match": is_match,
            "explanation_en": explanation_en,
            "explanation_kn": explanation_kn,
            "explanation_hi": explanation_hi,
            "source_clause": rule.source_clause
        }

    @classmethod
    def evaluate_scheme(cls, scheme, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        rule_evaluations: List[Dict[str, Any]] = []
        has_no_match = False
        has_unknown = False
        missing_fields: List[str] = []
        matched_rules_en: List[str] = []
        matched_rules_kn: List[str] = []
        
        for rule in scheme.rules:
            eval_res = cls.evaluate_single_rule(rule, profile_data)
            rule_evaluations.append(eval_res)
            
            if eval_res["status"] == STATUS_NO_MATCH:
                has_no_match = True
            elif eval_res["status"] == STATUS_UNKNOWN:
                has_unknown = True
                missing_fields.append(eval_res["field"])
            elif eval_res["status"] == STATUS_MATCH:
                matched_rules_en.append(eval_res["explanation_en"])
                matched_rules_kn.append(eval_res["explanation_kn"])

        # Tri-State Determination
        if has_no_match:
            overall_status = STATUS_NOT_ELIGIBLE
            legacy_status = STATUS_NO_MATCH
        elif has_unknown:
            overall_status = STATUS_POSSIBLY_ELIGIBLE
            legacy_status = STATUS_UNKNOWN
        else:
            overall_status = STATUS_ELIGIBLE
            legacy_status = STATUS_MATCH

        # Check application window
        app_window_status = "APPLICATION_OPEN" if getattr(scheme, 'is_application_open', True) else "APPLICATION_CLOSED"

        # Generate Explainable "Why are you eligible?" answer
        if overall_status == STATUS_ELIGIBLE:
            why_en = f"You meet all recorded criteria: {'; '.join(matched_rules_en[:2])}."
            why_kn = f"ನಿಮ್ಮ ಭೂಮಿ ಮತ್ತು ಕೃಷಿ ವಿವರಗಳು ಈ ಯೋಜನೆಯ ಎಲ್ಲಾ ಅಧಿಕೃತ ನಿಯಮಗಳನ್ನು ಪೂರೈಸುತ್ತವೆ: {'; '.join(matched_rules_kn[:2])}."
            why_hi = f"आपकी भूमि और कृषि विवरण इस योजना के सभी आवश्यक मानदंडों को पूरा करते हैं।"
        elif overall_status == STATUS_POSSIBLY_ELIGIBLE:
            why_en = f"You appear partially eligible. Please verify: {', '.join(missing_fields)}."
            why_kn = f"ನೀವು ಭಾಗಶಃ ಅರ್ಹರಾಗಿದ್ದೀರಿ. ದಯವಿಟ್ಟು {', '.join(missing_fields)} ವಿವರಗಳನ್ನು ದೃಢೀಕರಿಸಿ."
            why_hi = f"आप आंशिक रूप से पात्र हैं। कृपया शेष विवरण सत्यापित करें।"
        else:
            why_en = "You currently do not meet one or more primary criteria for this scheme."
            why_kn = "ಪ್ರಸ್ತುತ ನಿಮ್ಮ ಜಮೀನು ಅಥವಾ ರೈತ ವರ್ಗವು ಈ ಯೋಜನೆಯ ಪ್ರಾಥಮಿಕ ಷರತ್ತುಗಳನ್ನು ಪೂರೈಸುತ್ತಿಲ್ಲ."
            why_hi = "वर्तमान में आप इस योजना के प्राथमिक मानदंडों को पूरा नहीं करते हैं।"

        docs = []
        try:
            req_docs = getattr(scheme, 'required_documents', None)
            docs = json.loads(req_docs) if req_docs else []
        except Exception:
            docs = ["Aadhaar Card", "Pahani (RTC)", "Bank Passbook"]

        return {
            "scheme_id": getattr(scheme, 'id', 1),
            "scheme_code": getattr(scheme, 'code', 'SCHEME'),
            "scheme_name_en": getattr(scheme, 'name_en', 'Scheme'),
            "scheme_name_kn": getattr(scheme, 'name_kn', 'ಯೋಜನೆ'),
            "scheme_name_hi": getattr(scheme, 'name_hi', getattr(scheme, 'name_en', 'Scheme')),
            "category": getattr(scheme, 'category', 'FINANCIAL'),
            "level": getattr(scheme, 'level', 'CENTRAL'),
            "max_benefit": getattr(scheme, 'max_benefit', 'Government Benefit'),
            "overall_status": legacy_status, # Backwards compatible: MATCH, NO_MATCH, UNKNOWN
            "eligibility_category": overall_status, # New: ELIGIBLE, POSSIBLY_ELIGIBLE, NOT_ELIGIBLE
            "application_window": app_window_status,
            "why_eligible_en": why_en,
            "why_eligible_kn": why_kn,
            "why_eligible_hi": why_hi,
            "required_documents": docs,
            "official_portal": getattr(scheme, 'official_portal', ''),
            "rules_evaluated": rule_evaluations,
            "missing_fields": missing_fields,
            "disclaimer": "AI recommendations are preliminary guidelines based on farmer profile. Final approval is subject to departmental verification."
        }

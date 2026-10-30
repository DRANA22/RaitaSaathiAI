import pytest
from app.services.scheme_engine import SchemeEligibilityEngine, STATUS_MATCH, STATUS_NO_MATCH, STATUS_UNKNOWN

class MockRule:
    def __init__(self, id, field_name, operator, expected_value, source_clause="Test"):
        self.id = id
        self.field_name = field_name
        self.operator = operator
        self.expected_value = expected_value
        self.rule_explanation_en = "Pass"
        self.rule_explanation_kn = "ಉತ್ತೀರ್ಣ"
        self.source_clause = source_clause

class MockScheme:
    def __init__(self, rules):
        self.id = 1
        self.code = "TEST_SCHEME"
        self.name_en = "Test Scheme"
        self.name_kn = "ಪರೀಕ್ಷಾ ಯೋಜನೆ"
        self.rules = rules
        self.official_portal = "https://example.com"
        self.max_benefit = "Rs. 1000"
        import datetime
        self.last_verified_at = datetime.datetime.utcnow()

def test_scheme_engine_match():
    rule = MockRule(1, 'total_land_acres', '<=', '5.0')
    scheme = MockScheme([rule])
    profile = {'total_land_acres': 2.5}
    
    res = SchemeEligibilityEngine.evaluate_scheme(scheme, profile)
    assert res['overall_status'] == STATUS_MATCH

def test_scheme_engine_no_match():
    rule = MockRule(1, 'total_land_acres', '<=', '2.0')
    scheme = MockScheme([rule])
    profile = {'total_land_acres': 3.5}
    
    res = SchemeEligibilityEngine.evaluate_scheme(scheme, profile)
    assert res['overall_status'] == STATUS_NO_MATCH

def test_scheme_engine_unknown_missing_field():
    rule = MockRule(1, 'caste_category', '==', 'SC')
    scheme = MockScheme([rule])
    profile = {'total_land_acres': 2.5} # missing caste_category
    
    res = SchemeEligibilityEngine.evaluate_scheme(scheme, profile)
    assert res['overall_status'] == STATUS_UNKNOWN
    assert 'caste_category' in res['missing_fields']


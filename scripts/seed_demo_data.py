import os
import sys
import json
from datetime import datetime, timedelta

# Configure UTF-8 output on Windows consoles
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.models import (
    User, FarmerProfile, FarmerLandDetails, FarmCrop,
    IdentityVerification, Scheme, EligibilityRule,
    SchemeApplication, ApplicationStatusHistory, FarmerNotification,
    AdminUser, FarmTask
)
from app.utils.security import hash_password

def seed_all():
    app = create_app('development')
    with app.app_context():
        print("[INIT] Creating/updating all database tables...")
        db.create_all()

        # =====================================================================
        # 1. SEED ADMIN USER
        # =====================================================================
        admin = AdminUser.query.filter_by(username='admin_krishi').first()
        if not admin:
            print("[SEED] Creating Admin: Dr. Basavaraj Patil (District Agriculture Officer)...")
            admin = AdminUser(
                username='admin_krishi',
                password_hash=hash_password('krishiadmin2026'),
                full_name='Dr. Basavaraj Patil (District Agriculture Officer)',
                email='dao.mandya@agri.karnataka.gov.in',
                department='Department of Agriculture, Govt. of Karnataka',
                role='SUPER_ADMIN',
                district='Mandya'
            )
            db.session.add(admin)
            db.session.commit()

        # =====================================================================
        # 2. SEED 20 VERIFIED GOVERNMENT SCHEMES (14 Central + 6 Karnataka)
        # =====================================================================
        SCHEMES_DATA = [
            # CENTRAL SCHEMES (1-14)
            {
                "code": "PM_KISAN",
                "name_en": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
                "name_kn": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಕಿಸಾನ್ ಸಮ್ಮಾನ್ ನಿಧಿ (ಪಿಎಂ-ಕಿಸಾನ್)",
                "name_hi": "प्रधानमंत्री किसान सम्मान निधि (पीएम-किसान)",
                "department_en": "Ministry of Agriculture and Farmers Welfare, Govt. of India",
                "department_kn": "ಕೃಷಿ ಮತ್ತು ರೈತರ ಕಲ್ಯಾಣ ಸಚಿವಾಲಯ, ಭಾರತ ಸರ್ಕಾರ",
                "category": "FINANCIAL",
                "level": "CENTRAL",
                "official_portal": "https://pmkisan.gov.in",
                "brief_summary_en": "Direct income support of ₹6,000 per year in three equal instalments of ₹2,000 to all landholding farmer families.",
                "brief_summary_kn": "ಎಲ್ಲಾ ಸಣ್ಣ ಮತ್ತು ಮಧ್ಯಮ ಜಮೀನು ಹೊಂದಿರುವ ರೈತ ಕುಟುಂಬಗಳಿಗೆ ವಾರ್ಷಿಕ ₹6,000 ನೇರ ಆದಾಯ ಬೆಂಬಲ (ಪ್ರತಿ 4 ತಿಂಗಳಿಗೊಮ್ಮೆ ₹2,000).",
                "max_benefit": "₹6,000 / year (Direct DBT)",
                "eligibility_criteria_en": "All landholding farmer families with cultivable land in their names. Excludes institutional landholders and income tax payees.",
                "eligibility_criteria_kn": "ತಮ್ಮ ಹೆಸರಿನಲ್ಲಿ ಕೃಷಿ ಜಮೀನು ಹೊಂದಿರುವ ಎಲ್ಲಾ ರೈತ ಕುಟುಂಬಗಳು. ಆದಾಯ ತೆರಿಗೆ ಪಾವತಿದಾರರಿಗೆ ಅನ್ವಯಿಸುವುದಿಲ್ಲ.",
                "required_documents": json.dumps(["Aadhaar Card", "Land Ownership Record (RTC/Pahani)", "Active Bank Account linked with Aadhaar"]),
                "application_process": "Online application via PM-KISAN portal, Common Service Centres (CSC), or Karnataka Raitha Samparka Kendra.",
                "rules": [
                    {"field": "total_land_acres", "op": ">=", "val": "0.1", "en": "Must possess cultivable land holding", "kn": "ಕೃಷಿ ಯೋಗ್ಯ ಜಮೀನು ಹೊಂದಿರಬೇಕು", "source": "PM-KISAN Operational Guidelines Clause 3.1"},
                    {"field": "has_aadhaar", "op": "BOOLEAN", "val": "true", "en": "Aadhaar e-KYC authentication is mandatory", "kn": "ಆಧಾರ್ ಇ-ಕೆವೈಸಿ ಕಡ್ಡಾಯವಾಗಿದೆ", "source": "PM-KISAN DBT Mandate"}
                ]
            },
            {
                "code": "PMFBY",
                "name_en": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
                "name_kn": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಫಸಲ್ ಬಿಮಾ ಯೋಜನೆ (ಬೆಳೆ ವಿಮೆ)",
                "name_hi": "प्रधानमंत्री फसल बीमा योजना (पीएमएफबीवाई)",
                "department_en": "Ministry of Agriculture and Farmers Welfare, Govt. of India",
                "department_kn": "ಕೃಷಿ ಮತ್ತು ರೈತರ ಕಲ್ಯಾಣ ಸಚಿವಾಲಯ",
                "category": "INSURANCE",
                "level": "CENTRAL",
                "official_portal": "https://pmfby.gov.in",
                "brief_summary_en": "Comprehensive risk insurance cover against non-preventable natural risks from pre-sowing to post-harvest.",
                "brief_summary_kn": "ನೈಸರ್ಗಿಕ ವಿಕೋಪಗಳು, ಅನಾವೃಷ್ಟಿ, ಪ್ರವಾಹ ಮತ್ತು ಕೀಟ ಬಾಧೆಯಿಂದ ಉಂಟಾಗುವ ಬೆಳೆ ನಷ್ಟಕ್ಕೆ ಸಮಗ್ರ ವಿಮಾ ರಕ್ಷಣೆ.",
                "max_benefit": "Full Sum Insured (Up to ₹50,000 / acre based on crop scale of finance)",
                "eligibility_criteria_en": "All farmers growing notified crops in notified areas including sharecroppers and tenant farmers.",
                "eligibility_criteria_kn": "ಅಧಿಸೂಚಿತ ಪ್ರದೇಶದಲ್ಲಿ ಅಧಿಸೂಚಿತ ಬೆಳೆಗಳನ್ನು ಬೆಳೆಯುವ ಎಲ್ಲಾ ರೈತರು ಮತ್ತು ಗೇಣಿದಾರರು ಅರ್ಹರು.",
                "required_documents": json.dumps(["Land RTC / Sowing Certificate", "Bank Account Passbook", "Aadhaar Card", "Crop Sowing Declaration"]),
                "application_process": "Enroll through Samrakshane portal (Karnataka), bank branches, or CSC before seasonal cut-off date.",
                "rules": [
                    {"field": "total_land_acres", "op": ">=", "val": "0.1", "en": "Applicable for all land sizes", "kn": "ಎಲ್ಲಾ ಜಮೀನು ವಿಸ್ತೀರ್ಣಕ್ಕೆ ಅನ್ವಯ", "source": "PMFBY Revised Guidelines 2020"},
                    {"field": "has_aadhaar", "op": "BOOLEAN", "val": "true", "en": "Aadhaar mandatory for DBT claim settlement", "kn": "ಡಿಬಿಟಿ ಕ್ಲೈಮ್ ಇತ್ಯರ್ಥಕ್ಕೆ ಆಧಾರ್ ಕಡ್ಡಾಯ", "source": "PMFBY Clause 8"}
                ]
            },
            {
                "code": "KCC",
                "name_en": "Kisan Credit Card (KCC) Scheme",
                "name_kn": "ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್ (ಕೆಸಿಸಿ) ಯೋಜನೆ",
                "name_hi": "किसान क्रेडिट कार्ड (केसीसी)",
                "department_en": "Department of Agriculture & Reserve Bank of India",
                "department_kn": "ಕೃಷಿ ಇಲಾಖೆ ಹಾಗೂ ಭಾರತೀಯ ರಿಸರ್ವ್ ಬ್ಯಾಂಕ್",
                "category": "FINANCIAL",
                "level": "CENTRAL",
                "official_portal": "https://www.myscheme.gov.in/schemes/kcc",
                "brief_summary_en": "Adequate and timely credit support from the banking system with 3% interest subvention for prompt repayment (effective 4% p.a.).",
                "brief_summary_kn": "ಕೃಷಿ ವೆಚ್ಚಗಳಿಗೆ ಕಡಿಮೆ ಬಡ್ಡಿದರದಲ್ಲಿ (ಕೇವಲ 4%) ₹3 ಲಕ್ಷದವರೆಗೆ ಸಕಾಲಿಕ ಬ್ಯಾಂಕ್ ಸಾಲ ಸೌಲಭ್ಯ.",
                "max_benefit": "Credit limit up to ₹3,00,000 at concessional 4% interest rate",
                "eligibility_criteria_en": "Owner cultivators, tenant farmers, oral lessees, sharecroppers, and SHGs of farmers.",
                "eligibility_criteria_kn": "ಸ್ವಂತ ಜಮೀನು ಹೊಂದಿರುವ ರೈತರು, ಗೇಣಿದಾರರು ಹಾಗೂ ಸ್ವಸಹಾಯ ಸಂಘಗಳು ಅರ್ಹರು.",
                "required_documents": json.dumps(["Land Record (Pahani/RTC)", "Aadhaar Card", "Voter ID / PAN Card", "Passport Photo"]),
                "application_process": "Submit single-page KCC application form at any commercial, rural, or cooperative bank branch.",
                "rules": [
                    {"field": "total_land_acres", "op": ">=", "val": "0.1", "en": "Credit based on scale of finance per acre", "kn": "ಎಕರೆವಾರು ಕೃಷಿ ವೆಚ್ಚಕ್ಕೆ ಅನುಗುಣವಾಗಿ ಮಿತಿ", "source": "RBI Master Circular - KCC"}
                ]
            },
            {
                "code": "PMKSY",
                "name_en": "Pradhan Mantri Krishi Sinchayee Yojana (PMKSY - Per Drop More Crop)",
                "name_kn": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಕೃಷಿ ಸಿಂಚಾಯಿ ಯೋಜನೆ (ಹನಿ/ತುಂತುರು ನೀರಾವರಿ)",
                "name_hi": "प्रधानमंत्री कृषि सिंचाई योजना (पीएमकेएसवाई)",
                "department_en": "Department of Agriculture & Farmers Welfare, GoI",
                "department_kn": "ಕೃಷಿ ಮತ್ತು ರೈತರ ಕಲ್ಯಾಣ ಇಲಾಖೆ",
                "category": "IRRIGATION",
                "level": "CENTRAL",
                "official_portal": "https://pmksy.gov.in",
                "brief_summary_en": "Micro-irrigation support (Drip and Sprinkler systems) to maximize water use efficiency with up to 90% subsidy for small farmers.",
                "brief_summary_kn": "ಹನಿ ಮತ್ತು ತುಂತುರು ನೀರಾವರಿ ಘಟಕ ಸ್ಥಾಪನೆಗೆ ಶೇಕಡಾ 90 ರವರೆಗೆ ಸಹಾಯಧನ.",
                "max_benefit": "Up to 90% subsidy on Drip/Sprinkler micro-irrigation installation",
                "eligibility_criteria_en": "Farmers possessing agricultural land with assured irrigation water source (borewell/well/canal).",
                "eligibility_criteria_kn": "ನೀರಾವರಿ ಜಲಮೂಲ (ಬೋರ್‌ವೆಲ್/ಬಾವಿ) ಹೊಂದಿರುವ ರೈತರು ಅರ್ಹರು.",
                "required_documents": json.dumps(["Land Record (RTC)", "Water Source Certificate", "Electricity/Borewell RR Number", "Bank Passbook", "Aadhaar Card"]),
                "application_process": "Register on Karnataka Horticulture/Agriculture micro-irrigation portal or RSK office.",
                "rules": [
                    {"field": "irrigation_type", "op": "IN", "val": "BOREWELL,CANAL,DRIP,SPRINKLER", "en": "Must have an active irrigation water source", "kn": "ಸಕ್ರಿಯ ನೀರಾವರಿ ಮೂಲ ಹೊಂದಿರಬೇಕು", "source": "PMKSY PDMC Operational Norms Clause 4.2"}
                ]
            },
            {
                "code": "SOIL_HEALTH_CARD",
                "name_en": "Soil Health Card Scheme",
                "name_kn": "ಮಣ್ಣು ಆರೋಗ್ಯ ಕಾರ್ಡ್ ಯೋಜನೆ",
                "name_hi": "मृदा स्वास्थ्य कार्ड योजना",
                "department_en": "Ministry of Agriculture and Farmers Welfare",
                "department_kn": "ಕೃಷಿ ಇಲಾಖೆ",
                "category": "SUBSIDY",
                "level": "CENTRAL",
                "official_portal": "https://soilhealth.dac.gov.in",
                "brief_summary_en": "Provides printed soil health cards with crop-wise nutrient recommendations to reduce excess fertilizer expenditure.",
                "brief_summary_kn": "ಪ್ರತಿ 3 ವರ್ಷಕ್ಕೊಮ್ಮೆ ಉಚಿತ ಮಣ್ಣು ಪರೀಕ್ಷೆ ನಡೆಸಿ 12 ಪೋಷಕಾಂಶಗಳ ಸಮಗ್ರ ಆರೋಗ್ಯ ಕಾರ್ಡ್ ವಿತರಣೆ.",
                "max_benefit": "100% Free Soil Nutrient Testing & Customized Advisory",
                "eligibility_criteria_en": "All farm holdings across rural India.",
                "eligibility_criteria_kn": "ಎಲ್ಲಾ ಕೃಷಿ ಜಮೀನು ಹೊಂದಿರುವ ರೈತರು.",
                "required_documents": json.dumps(["Survey Number details", "Aadhaar Card", "Mobile Number"]),
                "application_process": "Soil sample collected by Agriculture Officer or submitted directly to Raitha Samparka Kendra.",
                "rules": [
                    {"field": "total_land_acres", "op": ">=", "val": "0.1", "en": "Applicable for any cultivable land", "kn": "ಯಾವುದೇ ಕೃಷಿ ಜಮೀನಿಗೆ ಅನ್ವಯ", "source": "SHC Guidelines"}
                ]
            },
            {
                "code": "PM_SAMRIDDHI_KENDRA",
                "name_en": "PM Kisan Samriddhi Kendra (PMKSK)",
                "name_kn": "ಪ್ರಧಾನಮಂತ್ರಿ ಕಿಸಾನ್ ಸಮೃದ್ಧಿ ಕೇಂದ್ರ",
                "name_hi": "पीएम किसान समृद्धि केंद्र",
                "department_en": "Department of Fertilizers, Ministry of Chemicals & Fertilizers",
                "department_kn": "ರಸಗೊಬ್ಬರ ಇಲಾಖೆ",
                "category": "SUBSIDY",
                "level": "CENTRAL",
                "official_portal": "https://fert.gov.in",
                "brief_summary_en": "One-stop retail centres catering to agri-inputs (fertilizers, seeds, pesticides) and crop testing at subsidized government rates.",
                "brief_summary_kn": "ರೈತರಿಗೆ ರಿಯಾಯಿತಿ ದರದಲ್ಲಿ ಗುಣಮಟ್ಟದ ರಸಗೊಬ್ಬರ, ಬಿತ್ತನೆ ಬೀಜ ಮತ್ತು ಕೃಷಿ ಸಲಕರಣೆ ಒದಗಿಸುವ ಏಕಗವಾಕ್ಷಿ ಕೇಂದ್ರ.",
                "max_benefit": "Access to subsidized urea/DAP at statutory MRP and modern sprayers",
                "eligibility_criteria_en": "Open to all practicing farmers.",
                "eligibility_criteria_kn": "ಎಲ್ಲಾ ಸಕ್ರಿಯ ರೈತರು.",
                "required_documents": json.dumps(["Aadhaar Card", "Kisan Card (optional)"]),
                "application_process": "Walk-in purchase at designated PMKSK retail outlets in every taluk.",
                "rules": [
                    {"field": "has_aadhaar", "op": "BOOLEAN", "val": "true", "en": "Aadhaar authentication required for POS fertilizer purchase", "kn": "ಪಿಓಎಸ್ ರಸಗೊಬ್ಬರ ಖರೀದಿಗೆ ಆಧಾರ್ ಅಗತ್ಯ", "source": "DBT Fertilizers Norms"}
                ]
            },
            {
                "code": "PM_KMY",
                "name_en": "Pradhan Mantri Kisan Maandhan Yojana (PM-KMY)",
                "name_kn": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಕಿಸಾನ್ ಮಾನ್‌ಧನ್ ಯೋಜನೆ (ರೈತ ಪಿಂಚಣಿ)",
                "name_hi": "प्रधानमंत्री किसान मानधन योजना",
                "department_en": "Ministry of Agriculture and Farmers Welfare & LIC",
                "department_kn": "ಕೃಷಿ ಇಲಾಖೆ ಹಾಗೂ ಎಲ್‌ಐಸಿ",
                "category": "FINANCIAL",
                "level": "CENTRAL",
                "official_portal": "https://maandhan.in",
                "brief_summary_en": "Old age pension scheme providing an assured monthly pension of ₹3,000 to small and marginal farmers on attaining 60 years.",
                "brief_summary_kn": "ಸಣ್ಣ ಮತ್ತು ಅತಿ ಸಣ್ಣ ರೈತರಿಗೆ 60 ವರ್ಷ ತುಂಬಿದ ನಂತರ ಮಾಸಿಕ ₹3,000 ಖಾತರಿ ಪಿಂಚಣಿ ಸೌಲಭ್ಯ.",
                "max_benefit": "Monthly Pension of ₹3,000 for life",
                "eligibility_criteria_en": "Small and marginal farmers aged 18 to 40 years holding cultivable land up to 5 acres.",
                "eligibility_criteria_kn": "18 ರಿಂದ 40 ವರ್ಷ ವಯಸ್ಸಿನ 5 ಎಕರೆಗಿಂತ ಕಡಿಮೆ ಜಮೀನು ಹೊಂದಿರುವ ಸಣ್ಣ ರೈತರು.",
                "required_documents": json.dumps(["Aadhaar Card", "Savings Bank Account / Jan Dhan Account", "Land RTC"]),
                "application_process": "Enroll at nearest CSC center or through Maandhan online portal with nominal monthly contribution.",
                "rules": [
                    {"field": "total_land_acres", "op": "<=", "val": "5.0", "en": "Restricted to Small and Marginal Farmers (<= 5 acres)", "kn": "ಸಣ್ಣ ಮತ್ತು ಅತಿ ಸಣ್ಣ ರೈತರಿಗೆ ಮಾತ್ರ (೫ ಎಕರೆ ಅಥವಾ ಕಡಿಮೆ)", "source": "PM-KMY Scheme Rules Clause 2"}
                ]
            },
            {
                "code": "AIF",
                "name_en": "Agriculture Infrastructure Fund (AIF)",
                "name_kn": "ಕೃಷಿ ಮೂಲಸೌಕರ್ಯ ನಿಧಿ (ಎಐಎಫ್)",
                "name_hi": "कृषि अवसंरचना कोष",
                "department_en": "Ministry of Agriculture and Farmers Welfare",
                "department_kn": "ಕೃಷಿ ಮತ್ತು ರೈತರ ಕಲ್ಯಾಣ ಸಚಿವಾಲಯ",
                "category": "INFRASTRUCTURE",
                "level": "CENTRAL",
                "official_portal": "https://agriinfra.dac.gov.in",
                "brief_summary_en": "Medium-long term debt financing facility for post-harvest management infrastructure with 3% per annum interest subvention.",
                "brief_summary_kn": "ಗೋದಾಮು, ಕೋಲ್ಡ್ ಸ್ಟೋರೇಜ್ ಮತ್ತು ಸಂಸ್ಕರಣಾ ಘಟಕ ನಿರ್ಮಾಣಕ್ಕೆ ಶೇ.3 ಬಡ್ಡಿ ಸಹಾಯಧನ ಹಾಗೂ ಕ್ರೆಡಿಟ್ ಗ್ಯಾರಂಟಿ.",
                "max_benefit": "Interest subvention of 3% p.a. on loans up to ₹2 Crores for 7 years",
                "eligibility_criteria_en": "Farmers, FPOs, PACS, Agri-entrepreneurs, and Startups.",
                "eligibility_criteria_kn": "ರೈತರು, ಎಫ್‌ಪಿಒಗಳು, ಕೃಷಿ ಉದ್ಯಮಿಗಳು ಹಾಗೂ ಸಹಕಾರ ಸಂಘಗಳು.",
                "required_documents": json.dumps(["Project DPR", "Land Ownership/Lease Agreement", "Bank KYC", "IT Returns/Estimate"]),
                "application_process": "Apply online at AIF portal; fast-track bank sanctioning mechanism.",
                "rules": [
                    {"field": "total_land_acres", "op": ">=", "val": "1.0", "en": "Viable land holding for agri-infrastructure", "kn": "ಕೃಷಿ ಮೂಲಸೌಕರ್ಯ ಸ್ಥಾಪನೆಗೆ ಜಮೀನು ಅಗತ್ಯ", "source": "AIF Operational Guidelines"}
                ]
            },
            {
                "code": "SMAM",
                "name_en": "Sub-Mission on Agricultural Mechanization (SMAM)",
                "name_kn": "ಕೃಷಿ ಯಾಂತ್ರೀಕರಣ ಉಪ-ಅಭಿಯಾನ (ಎಸ್.ಎಂ.ಎ.ಎಂ)",
                "name_hi": "कृषि यंत्रीकरण उप-मिशन",
                "department_en": "Department of Agriculture & Farmers Welfare",
                "department_kn": "ಕೃಷಿ ಇಲಾಖೆ",
                "category": "SUBSIDY",
                "level": "CENTRAL",
                "official_portal": "https://agrimachinery.nic.in",
                "brief_summary_en": "Financial assistance of 40% to 50% for procurement of modern agricultural machinery (tractors, power tillers, rotavators).",
                "brief_summary_kn": "ಟ್ರ್ಯಾಕ್ಟರ್, ಪವರ್ ಟಿಲ್ಲರ್, ರೋಟವೇಟರ್ ಖರೀದಿಗಾಗಿ ಶೇ. 40 ರಿಂದ 50 ರವರೆಗೆ ಸಹಾಯಧನ.",
                "max_benefit": "Up to 50% subsidy (maximum ₹1.5 Lakhs per machine / ₹10 Lakhs for custom hiring centres)",
                "eligibility_criteria_en": "Individual farmers with preference to small, marginal, women, and SC/ST farmers.",
                "eligibility_criteria_kn": "ವೈಯಕ್ತಿಕ ರೈತರು (ಸಣ್ಣ, ಅತಿ ಸಣ್ಣ ಹಾಗೂ ಎಸ್‌ಸಿ/ಎಸ್‌ಟಿ ರೈತರಿಗೆ ಆದ್ಯತೆ).",
                "required_documents": json.dumps(["Land RTC", "Aadhaar Card", "Bank Account Passbook", "Quotation from Authorized Dealer"]),
                "application_process": "Apply via DBT in Agricultural Machinery portal or Karnataka Krishi Yantra portal.",
                "rules": [
                    {"field": "total_land_acres", "op": ">=", "val": "0.5", "en": "Minimum 0.5 acres cultivable land required", "kn": "ಕನಿಷ್ಠ 0.5 ಎಕರೆ ಜಮೀನು ಇರಬೇಕು", "source": "SMAM Norms 2024"}
                ]
            },
            {
                "code": "PM_AASHA",
                "name_en": "Pradhan Mantri Annadata Aay Sanraksan Abhiyan (PM-AASHA)",
                "name_kn": "ಪಿಎಂ-ಆಶಾ (ಬೆಳೆ ಬೆಂಬಲ ಬೆಲೆ ರಕ್ಷಣೆ)",
                "name_hi": "पीएम-आशा",
                "department_en": "Ministry of Agriculture and Farmers Welfare",
                "department_kn": "ಕೃಷಿ ಇಲಾಖೆ",
                "category": "FINANCIAL",
                "level": "CENTRAL",
                "official_portal": "https://pmaasha.nic.in",
                "brief_summary_en": "Price Support Scheme (PSS) and Price Deficiency Payment Scheme (PDPS) ensuring MSP for pulses, oilseeds, and copra.",
                "brief_summary_kn": "ದ್ವಿದಳ ಧಾನ್ಯ, ಎಣ್ಣೆಕಾಳು ಹಾಗೂ ಕೊಬ್ಬರಿಗೆ ಕನಿಷ್ಠ ಬೆಂಬಲ ಬೆಲೆ (MSP) ಖಾತರಿ ಯೋಜನೆ.",
                "max_benefit": "Direct payment of price deficit below MSP directly to farmer bank account",
                "eligibility_criteria_en": "Farmers producing notified pulses, oilseeds, and coarse grains.",
                "eligibility_criteria_kn": "ದ್ವಿದಳ ಧಾನ್ಯ ಮತ್ತು ಎಣ್ಣೆಕಾಳು ಬೆಳೆಯುವ ಎಲ್ಲಾ ರೈತರು.",
                "required_documents": json.dumps(["Farmer Registration / FID", "Crop Sowing RTC", "Aadhaar Linked Bank Account"]),
                "application_process": "Registration on e-Procurement / FRUITS portal during notified harvest window.",
                "rules": [
                    {"field": "total_land_acres", "op": ">=", "val": "0.2", "en": "Registered farmer under MSP portal", "kn": "ಎಂಎಸ್‌ಪಿ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ನೋಂದಾಯಿತ ರೈತರು", "source": "PM-AASHA Guidelines"}
                ]
            },
            {
                "code": "PKVY",
                "name_en": "Paramparagat Krishi Vikas Yojana (PKVY)",
                "name_kn": "ಪರಂಪರಾಗತ್ ಕೃಷಿ ವಿಕಾಸ್ ಯೋಜನೆ (ಸಾವಯವ ಕೃಷಿ)",
                "name_hi": "परंपरागत कृषि विकास योजना",
                "department_en": "Ministry of Agriculture and Farmers Welfare",
                "department_kn": "ಕೃಷಿ ಇಲಾಖೆ",
                "category": "ORGANIC",
                "level": "CENTRAL",
                "official_portal": "https://pgsindia-ncof.gov.in",
                "brief_summary_en": "Financial assistance of ₹50,000 per hectare over 3 years for cluster-based organic farming adoption and PGS certification.",
                "brief_summary_kn": "ಸಾವಯವ ಕೃಷಿ ಅಳವಡಿಕೆ ಮತ್ತು ಪ್ರಮಾಣೀಕರಣಕ್ಕಾಗಿ 3 ವರ್ಷಗಳಲ್ಲಿ ಪ್ರತಿ ಹೆಕ್ಟೇರ್‌ಗೆ ₹50,000 ಧನಸಹಾಯ.",
                "max_benefit": "₹50,000 / hectare over 3 years (₹31,000 directly for organic inputs)",
                "eligibility_criteria_en": "Farmers willing to form clusters of 20 or more farmers adopting chemical-free organic agriculture.",
                "eligibility_criteria_kn": "ಸಾವಯವ ಕೃಷಿ ಕೈಗೊಳ್ಳಲು ಇಚ್ಛಿಸುವ ರೈತರ ಗುಂಪುಗಳು.",
                "required_documents": json.dumps(["Land RTC", "Aadhaar Card", "Cluster Member Form", "Bank Passbook"]),
                "application_process": "Form an organic farmer cluster through local RSK or certified NGO facilitator.",
                "rules": [
                    {"field": "total_land_acres", "op": ">=", "val": "0.5", "en": "Cultivable land for organic practices", "kn": "ಸಾವಯವ ಕೃಷಿಗೆ ಜಮೀನು ಅಗತ್ಯ", "source": "PKVY Operational Guidelines"}
                ]
            },
            {
                "code": "MIDH",
                "name_en": "Mission for Integrated Development of Horticulture (MIDH)",
                "name_kn": "ತೋಟಗಾರಿಕೆ ಸಮಗ್ರ ಅಭಿವೃದ್ಧಿ ಮಿಷನ್ (ಎಂಐಡಿಎಚ್)",
                "name_hi": "एकीकृत बागवानी विकास मिशन",
                "department_en": "Department of Agriculture, Cooperation & Farmers Welfare",
                "department_kn": "ತೋಟಗಾರಿಕೆ ಇಲಾಖೆ, ಕರ್ನಾಟಕ ಸರ್ಕಾರ",
                "category": "SUBSIDY",
                "level": "CENTRAL",
                "official_portal": "https://midh.gov.in",
                "brief_summary_en": "Holistic growth of the horticulture sector covering fruits, vegetables, spices, polyhouses, and pack-houses.",
                "brief_summary_kn": "ಹಣ್ಣು, ತರಕಾರಿ, ಹೂವು ಹಾಗೂ ಪಾಲಿಹೌಸ್ ಕೃಷಿಗೆ ಶೇಕಡಾ 40 ರಿಂದ 50 ರವರೆಗೆ ಸಹಾಯಧನ.",
                "max_benefit": "Up to 50% subsidy on greenhouse construction, drip irrigation, and planting material",
                "eligibility_criteria_en": "All growers of horticultural crops with suitable land and water availability.",
                "eligibility_criteria_kn": "ತೋಟಗಾರಿಕೆ ಬೆಳೆ ಬೆಳೆಯುವ ಎಲ್ಲಾ ರೈತರು.",
                "required_documents": json.dumps(["RTC / Pahani", "Soil & Water Quality Test Report", "Aadhaar Card", "Bank Details"]),
                "application_process": "Submit application to Senior Assistant Director of Horticulture (SADH) at taluk level.",
                "rules": [
                    {"field": "total_land_acres", "op": ">=", "val": "0.5", "en": "Sufficient land holding for horticulture", "kn": "ತೋಟಗಾರಿಕೆಗೆ ಜಮೀನು ಅಗತ್ಯ", "source": "MIDH Operational Framework"}
                ]
            },
            {
                "code": "FPO_SCHEME",
                "name_en": "Formation & Promotion of 10,000 FPOs Scheme",
                "name_kn": "10,000 ರೈತ ಉತ್ಪಾದಕ ಸಂಸ್ಥೆಗಳ (FPO) ರಚನೆ ಯೋಜನೆ",
                "name_hi": "10,000 किसान उत्पादक संगठन योजना",
                "department_en": "Ministry of Agriculture & NABARD / SFAC",
                "department_kn": "ಕೃಷಿ ಇಲಾಖೆ ಹಾಗೂ ನಬಾರ್ಡ್",
                "category": "FINANCIAL",
                "level": "CENTRAL",
                "official_portal": "https://sfacindia.com",
                "brief_summary_en": "Equity grant of up to ₹15 Lakhs per FPO and credit guarantee to enhance bargaining power and collective marketing.",
                "brief_summary_kn": "ರೈತರು ಒಗ್ಗೂಡಿ ಎಫ್‌ಪಿಒ ರಚಿಸಲು ₹15 ಲಕ್ಷದವರೆಗೆ ಇಕ್ವಿಟಿ ಅನುದಾನ ಮತ್ತು ಸಾಲ ಖಾತರಿ ಸೌಲಭ್ಯ.",
                "max_benefit": "Matching equity grant up to ₹2,000 per member (Max ₹15 Lakhs per FPO)",
                "eligibility_criteria_en": "Small, marginal and landless farmers joining a registered Farmer Producer Company.",
                "eligibility_criteria_kn": "ಸಣ್ಣ, ಅತಿ ಸಣ್ಣ ರೈತರು ಸದಸ್ಯರಾಗಿರುವ ನೋಂದಾಯಿತ ಕೃಷಿ ಉತ್ಪಾದಕ ಸಂಸ್ಥೆಗಳು.",
                "required_documents": json.dumps(["FPO Registration Certificate", "Shareholder List", "Aadhaar Cards of Board", "Bank Details"]),
                "application_process": "Through Implementing Agencies (NABARD, SFAC, NCDC).",
                "rules": [
                    {"field": "has_aadhaar", "op": "BOOLEAN", "val": "true", "en": "Member Aadhaar registration required", "kn": "ಸದಸ್ಯರ ಆಧಾರ್ ನೋಂದಣಿ ಕಡ್ಡಾಯ", "source": "SFAC FPO Guidelines"}
                ]
            },
            {
                "code": "DIGITAL_AGRI_MISSION",
                "name_en": "Digital Agriculture Mission",
                "name_kn": "ಡಿಜಿಟಲ್ ಕೃಷಿ ಮಿಷನ್ (ಡಿಜಿಟಲ್ ಅಗ್ರಿಕಲ್ಚರ್)",
                "name_hi": "डिजिटल कृषि मिशन",
                "department_en": "Ministry of Agriculture and Farmers Welfare, GoI",
                "department_kn": "ಕೃಷಿ ಮತ್ತು ರೈತರ ಕಲ್ಯಾಣ ಸಚಿವಾಲಯ",
                "category": "INFRASTRUCTURE",
                "level": "CENTRAL",
                "official_portal": "https://agristack.gov.in",
                "brief_summary_en": "Creation of open digital agriculture ecosystem including AgriStack (Farmer Registry, Village Maps, Crop Registry).",
                "brief_summary_kn": "ಪ್ರತಿಯೊಬ್ಬ ರೈತರಿಗೆ ವಿಶಿಷ್ಟ ಡಿಜಿಟಲ್ ಗುರುತಿನ ಚೀಟಿ (Digital Farmer ID) ಮತ್ತು ತಂತ್ರಜ್ಞಾನ ಆಧಾರಿತ ಸೇವೆಗಳು.",
                "max_benefit": "Instant access to customized weather, pest warnings, and automated DBT subsidy routing",
                "eligibility_criteria_en": "All verified landholders and tenant farmers registered with digital farmer registry.",
                "eligibility_criteria_kn": "ಡಿಜಿಟಲ್ ರೈತ ನೋಂದಣಿ ಹೊಂದಿರುವ ಎಲ್ಲಾ ರೈತರು.",
                "required_documents": json.dumps(["Aadhaar Card", "Mobile Linked with Aadhaar", "Land Records"]),
                "application_process": "Self-registration via RaitaSaathiAI / AgriStack mobile interface.",
                "rules": [
                    {"field": "has_aadhaar", "op": "BOOLEAN", "val": "true", "en": "Digital authentication via Aadhaar OTP", "kn": "ಆಧಾರ್ ಮೂಲಕ ಡಿಜಿಟಲ್ ದೃಢೀಕರಣ", "source": "AgriStack Architecture Paper 2024"}
                ]
            },

            # KARNATAKA STATE SCHEMES (15-20)
            {
                "code": "KRISHI_BHAGYA",
                "name_en": "Krishi Bhagya Yojana (Karnataka)",
                "name_kn": "ಕೃಷಿ ಭಾಗ್ಯ ಯೋಜನೆ (ಕರ್ನಾಟಕ ಸರ್ಕಾರ)",
                "name_hi": "कृषि भाग्य योजना (कर्नाटक)",
                "department_en": "Department of Agriculture, Government of Karnataka",
                "department_kn": "ಕೃಷಿ ಇಲಾಖೆ, ಕರ್ನಾಟಕ ಸರ್ಕಾರ",
                "category": "IRRIGATION",
                "level": "STATE_KARNATAKA",
                "official_portal": "https://raitamitra.karnataka.gov.in",
                "brief_summary_en": "Flagship rainfed farming package: Krishi Honda (Farm Pond), polythene lining, diesel pump, and micro-irrigation.",
                "brief_summary_kn": "ಮಳೆಯಾಶ್ರಿತ ಪ್ರದೇಶಗಳ ರೈತರಿಗೆ ಕೃಷಿ ಹೊಂಡ ನಿರ್ಮಾಣ, ಪಾಲಿಥೀನ್ ಹೊದಿಕೆ ಹಾಗೂ ಡೀಸೆಲ್ ಪಂಪ್‌ಸೆಟ್‌ಗೆ ಶೇ. 80-90 ರಿಯಾಯಿತಿ.",
                "max_benefit": "80% to 90% subsidy (up to ₹1,50,000 for Farm Pond + Micro-Irrigation Package)",
                "eligibility_criteria_en": "Dryland / rainfed farmers residing in notified taluks of Karnataka. SC/ST farmers get 90% subsidy, General farmers get 80%.",
                "eligibility_criteria_kn": "ಕರ್ನಾಟಕದ ಮಳೆಯಾಶ್ರಿತ ತಾಲ್ಲೂಕುಗಳ ರೈತರು. ಸಾಮಾನ್ಯ ರೈತರಿಗೆ 80%, ಪ.ಜಾ/ಪ.ಪಂ ರೈತರಿಗೆ 90% ಸಹಾಯಧನ.",
                "required_documents": json.dumps(["Pahani/RTC", "Aadhaar Card", "Caste Certificate (for SC/ST)", "Bank Passbook", "FRUITS ID (FID)"]),
                "application_process": "Apply online at Raitha Mitra portal or visit local Raitha Samparka Kendra (RSK).",
                "rules": [
                    {"field": "total_land_acres", "op": ">=", "val": "1.0", "en": "Minimum 1 acre land required for farm pond installation", "kn": "ಕೃಷಿ ಹೊಂಡಕ್ಕೆ ಕನಿಷ್ಠ 1 ಎಕರೆ ಜಮೀನು ಇರಬೇಕು", "source": "Krishi Bhagya Official Guidelines Clause 4"},
                    {"field": "district", "op": "IN", "val": "Mandya,Mysuru,Hassan,Tumakuru,Dharwad,Belagavi,Kalaburagi,Raichur,Koppal,Ballari,Vijayanagara,Bagalkote,Vijayapura,Bidar,Yadgir,Gadag,Haveri,Chitradurga,Chikkamagaluru,Chamarajanagar,Kolar,Chikkaballapura,Ramanagara,Shivamogga,Davanagere,Uttara Kannada,Dakshina Kannada,Udupi,Kodagu,Bengaluru Rural,Bengaluru Urban", "en": "Valid for all Karnataka agricultural districts", "kn": "ಕರ್ನಾಟಕದ ಎಲ್ಲಾ ಕೃಷಿ ಜಿಲ್ಲೆಗಳಿಗೆ ಅನ್ವಯ", "source": "Karnataka Govt Order 2024"}
                ]
            },
            {
                "code": "RAITHA_SIRI",
                "name_en": "Raitha Siri (Millet Promotion Scheme)",
                "name_kn": "ರೈತ ಸಿರಿ (ಸಿರಿಧಾನ್ಯ ಪ್ರೋತ್ಸಾಹ ಧನ)",
                "name_hi": "रैथा सिरी (बाजरा प्रोत्साहन योजना)",
                "department_en": "Department of Agriculture, Government of Karnataka",
                "department_kn": "ಕೃಷಿ ಇಲಾಖೆ, ಕರ್ನಾಟಕ ಸರ್ಕಾರ",
                "category": "FINANCIAL",
                "level": "STATE_KARNATAKA",
                "official_portal": "https://raitamitra.karnataka.gov.in",
                "brief_summary_en": "Cash incentive of ₹10,000 per hectare directly credited to bank accounts of farmers cultivating certified minor millets.",
                "brief_summary_kn": "ಸಿರಿಧಾನ್ಯಗಳನ್ನು (ರಾಗಿ, ನವಣೆ, ಸಾಮೆ, ಹಾರಕ, ಕೊರಲೆ, ಬದಲು) ಬೆಳೆಯುವ ರೈತರಿಗೆ ಪ್ರತಿ ಹೆಕ್ಟೇರ್‌ಗೆ ₹10,000 ನೇರ ಪ್ರೋತ್ಸಾಹಧನ.",
                "max_benefit": "₹10,000 / hectare (Direct Benefit Transfer)",
                "eligibility_criteria_en": "Karnataka farmers growing Ragi, Foxtail millet, Little millet, Kodo millet, Proso millet, or Barnyard millet.",
                "eligibility_criteria_kn": "ಸಿರಿಧಾನ್ಯಗಳನ್ನು ಬೆಳೆಯುವ ಕರ್ನಾಟಕದ ರೈತರು (ಗರಿಷ್ಠ 2 ಹೆಕ್ಟೇರ್‌ವರೆಗೆ).",
                "required_documents": json.dumps(["Land RTC showing Millet crop entry", "Aadhaar Card", "FRUITS ID (FID)", "Bank Account linked to Aadhaar"]),
                "application_process": "Register crop sowing in Karnataka Crop Survey (Bele Jarip) app; incentive disbursed automatically via FRUITS portal.",
                "rules": [
                    {"field": "total_land_acres", "op": ">=", "val": "0.5", "en": "Minimum 0.5 acres millet cultivation", "kn": "ಕನಿಷ್ಠ 0.5 ಎಕರೆ ಸಿರಿಧಾನ್ಯ ಬೆಳೆದಿರಬೇಕು", "source": "Raitha Siri Scheme Order 2024"}
                ]
            },
            {
                "code": "FARM_MECHANIZATION_KA",
                "name_en": "Karnataka Farm Mechanization Scheme (ಕೃಷಿ ಯಾಂತ್ರೀಕರಣ)",
                "name_kn": "ಕೃಷಿ ಯಾಂತ್ರೀಕರಣ ಮತ್ತು ಕೃಷಿ ಉತ್ಪನ್ನ ಸಂಸ್ಕರಣೆ ಯೋಜನೆ",
                "name_hi": "कर्नाटक कृषि यंत्रीकरण योजना",
                "department_en": "Department of Agriculture, Government of Karnataka",
                "department_kn": "ಕೃಷಿ ಇಲಾಖೆ, ಕರ್ನಾಟಕ ಸರ್ಕಾರ",
                "category": "SUBSIDY",
                "level": "STATE_KARNATAKA",
                "official_portal": "https://raitamitra.karnataka.gov.in",
                "brief_summary_en": "Direct subsidy on power weeders, multi-crop threshers, tarpaulins, diesel engines, and paddy transplanters.",
                "brief_summary_kn": "ಪವರ್ ವೀಡರ್, ಒಕ್ಕಣೆ ಯಂತ್ರ, ಪ್ಲಾಸ್ಟಿಕ್ ತಾಡಪತ್ರಿ ಮತ್ತು ಪಂಪ್‌ಸೆಟ್‌ಗಳಿಗೆ ಶೇ. 50 ರಿಂದ 90 ರವರೆಗೆ ಸಹಾಯಧನ.",
                "max_benefit": "Up to 50% for General farmers, 90% for SC/ST farmers (Max ₹1,00,000)",
                "eligibility_criteria_en": "Farmers possessing valid RTC in Karnataka with active FRUITS ID.",
                "eligibility_criteria_kn": "ಕರ್ನಾಟಕದಲ್ಲಿ ಜಮೀನು ಹೊಂದಿರುವ ಹಾಗೂ ಫ್ರೂಟ್ಸ್ ಐಡಿ ಹೊಂದಿರುವ ರೈತರು.",
                "required_documents": json.dumps(["FRUITS ID", "Pahani/RTC", "Aadhaar Card", "Bank Passbook", "Caste Certificate"]),
                "application_process": "Apply through Karnataka Seva Sindhu or Raitha Samparka Kendra.",
                "rules": [
                    {"field": "total_land_acres", "op": ">=", "val": "0.5", "en": "Possess agricultural land holding", "kn": "ಕೃಷಿ ಜಮೀನು ಹೊಂದಿರಬೇಕು", "source": "Karnataka Agri Mechanization Norms"}
                ]
            },
            {
                "code": "SEED_DISTRIBUTION_KA",
                "name_en": "Certified Seed Distribution Programme (ಬೀಜ ವಿತರಣೆ)",
                "name_kn": "ರಿಯಾಯಿತಿ ದರದಲ್ಲಿ ಪ್ರಮಾಣಿತ ಬಿತ್ತನೆ ಬೀಜ ವಿತರಣೆ",
                "name_hi": "रियायती बीज वितरण कार्यक्रम",
                "department_en": "Karnataka State Seeds Corporation (KSSC) & Agri Dept",
                "department_kn": "ಕರ್ನಾಟಕ ರಾಜ್ಯ ಬೀಜ ನಿಗಮ ಹಾಗೂ ಕೃಷಿ ಇಲಾಖೆ",
                "category": "SUBSIDY",
                "level": "STATE_KARNATAKA",
                "official_portal": "https://seed.karnataka.gov.in",
                "brief_summary_en": "Subsidized certified seeds of Paddy, Ragi, Maize, Groundnut, Red gram, and Soyabean distributed for Kharif and Rabi seasons.",
                "brief_summary_kn": "ಭತ್ತ, ರಾಗಿ, ಮೆಕ್ಕೆಜೋಳ, ತೊಗರಿ, ಕಡಲೆ ಬಿತ್ತನೆ ಬೀಜಗಳಿಗೆ ಶೇಕಡಾ 50 ರಷ್ಟು ರಿಯಾಯಿತಿ ದರ.",
                "max_benefit": "50% to 75% subsidy on certified seeds at Raitha Samparka Kendra",
                "eligibility_criteria_en": "All cultivating farmers in Karnataka holding valid Pahani.",
                "eligibility_criteria_kn": "ಚಾಲ್ತಿ ಪಹಣಿ ಹೊಂದಿರುವ ಕರ್ನಾಟಕದ ಎಲ್ಲಾ ರೈತರು.",
                "required_documents": json.dumps(["RTC/Pahani copy", "Aadhaar Card", "FRUITS ID"]),
                "application_process": "Direct purchase at subsidized price through POS machine at local RSK.",
                "rules": [
                    {"field": "total_land_acres", "op": ">=", "val": "0.2", "en": "Valid cultivable area", "kn": "ಕೃಷಿ ಯೋಗ್ಯ ಜಮೀನು ಇರಬೇಕು", "source": "KSSC Distribution Rules"}
                ]
            },
            {
                "code": "MSP_PROCUREMENT_KA",
                "name_en": "Minimum Support Price (MSP) Procurement Scheme",
                "name_kn": "ಬೆಂಬಲ ಬೆಲೆ ಯೋಜನೆಯಡಿ ಕೃಷಿ ಉತ್ಪನ್ನ ಖರೀದಿ",
                "name_hi": "न्यूनतम समर्थन मूल्य (एमएसपी) खरीद योजना",
                "department_en": "Food, Civil Supplies & Consumer Affairs and Agriculture Dept",
                "department_kn": "ಆಹಾರ, ನಾಗರಿಕ ಸರಬರಾಜು ಹಾಗೂ ಕೃಷಿ ಇಲಾಖೆ",
                "category": "FINANCIAL",
                "level": "STATE_KARNATAKA",
                "official_portal": "https://ahara.kar.nic.in",
                "brief_summary_en": "Government procurement of Paddy, Ragi, Jowar, Tur at announced MSP with bonus directly deposited into farmers' bank accounts.",
                "brief_summary_kn": "ಭತ್ತ, ರಾಗಿ, ಜೋಳ, ಬಿಳಿ ಜೋಳ ಮತ್ತು ತೊಗರಿಯನ್ನು ನಿಗದಿತ ಬೆಂಬಲ ಬೆಲೆಯಲ್ಲಿ ಸರ್ಕಾರದ ಖರೀದಿ ಕೇಂದ್ರಗಳ ಮೂಲಕ ಖರೀದಿ.",
                "max_benefit": "Guaranteed price (e.g., Ragi ₹4,290 / quintal, Paddy ₹2,320 / quintal)",
                "eligibility_criteria_en": "Farmers registered in Karnataka FRUITS database with verified crop survey data.",
                "eligibility_criteria_kn": "ಕರ್ನಾಟಕದ ಫ್ರೂಟ್ಸ್ ತಂತ್ರಾಂಶದಲ್ಲಿ ನೋಂದಾಯಿತ ರೈತರು.",
                "required_documents": json.dumps(["FRUITS ID (FID)", "Pahani", "Aadhaar Linked Bank Account"]),
                "application_process": "Register at APMC / Primary Agriculture Cooperative Society (PACS) procurement center during harvest window.",
                "rules": [
                    {"field": "total_land_acres", "op": ">=", "val": "0.1", "en": "Registered farmer holding", "kn": "ನೋಂದಾಯಿತ ರೈತ ಜಮೀನು", "source": "Karnataka MSP Notification 2024-25"}
                ]
            },
            {
                "code": "CM_KRISHI_VISTARA",
                "name_en": "Chief Minister's Krishi Vistara Yojana",
                "name_kn": "ಮುಖ್ಯಮಂತ್ರಿಗಳ ಕೃಷಿ ವಿಸ್ತಾರ ಯೋಜನೆ",
                "name_hi": "मुख्यमंत्री कृषि विस्तार योजना",
                "department_en": "Department of Agriculture, Government of Karnataka",
                "department_kn": "ಕೃಷಿ ಇಲಾಖೆ, ಕರ್ನಾಟಕ ಸರ್ಕಾರ",
                "category": "INFRASTRUCTURE",
                "level": "STATE_KARNATAKA",
                "official_portal": "https://raitamitra.karnataka.gov.in",
                "brief_summary_en": "Technology-driven extension services, mobile soil testing laboratories, drone spraying demonstrations, and farmer field schools.",
                "brief_summary_kn": "ರೈತರ ಮನೆಬಾಗಿಲಿಗೆ ಸಂಚಾರಿ ಮಣ್ಣು ಪರೀಕ್ಷಾ ಪ್ರಯೋಗಾಲಯ, ಡ್ರೋನ್ ಕೀಟನಾಶಕ ಸಿಂಪಡಣೆ ಪ್ರಾತ್ಯಕ್ಷಿಕೆ ಹಾಗೂ ಕೃಷಿ ತಜ್ಞರ ನೇರ ಸಲಹೆ.",
                "max_benefit": "Free mobile diagnostic testing and subsidized drone spraying service",
                "eligibility_criteria_en": "All farming households in Karnataka.",
                "eligibility_criteria_kn": "ಕರ್ನಾಟಕದ ಎಲ್ಲಾ ರೈತ ಕುಟುಂಬಗಳು.",
                "required_documents": json.dumps(["Farmer Mobile Number", "Village Address", "Aadhaar Card"]),
                "application_process": "Request mobile clinic visit via Raitha Samparka Kendra or RaitaSaathiAI app.",
                "rules": [
                    {"field": "total_land_acres", "op": ">=", "val": "0.1", "en": "Applicable for all farmers", "kn": "ಎಲ್ಲಾ ರೈತರಿಗೆ ಅನ್ವಯ", "source": "CM Krishi Vistara Guidelines"}
                ]
            }
        ]

        print(f"[SEED] Inserting/updating {len(SCHEMES_DATA)} official government schemes...")
        for s_data in SCHEMES_DATA:
            scheme = Scheme.query.filter_by(code=s_data["code"]).first()
            if not scheme:
                scheme = Scheme(
                    code=s_data["code"],
                    name_en=s_data["name_en"],
                    name_kn=s_data["name_kn"],
                    name_hi=s_data["name_hi"],
                    department_en=s_data["department_en"],
                    department_kn=s_data["department_kn"],
                    category=s_data["category"],
                    level=s_data["level"],
                    official_portal=s_data["official_portal"],
                    brief_summary_en=s_data["brief_summary_en"],
                    brief_summary_kn=s_data["brief_summary_kn"],
                    max_benefit=s_data["max_benefit"],
                    eligibility_criteria_en=s_data["eligibility_criteria_en"],
                    eligibility_criteria_kn=s_data["eligibility_criteria_kn"],
                    required_documents=s_data["required_documents"],
                    application_process=s_data["application_process"],
                    is_application_open=True,
                    is_active=True
                )
                db.session.add(scheme)
                db.session.flush()

                # Add rules
                for r_data in s_data.get("rules", []):
                    rule = EligibilityRule(
                        scheme_id=scheme.id,
                        field_name=r_data["field"],
                        operator=r_data["op"],
                        expected_value=r_data["val"],
                        rule_explanation_en=r_data["en"],
                        rule_explanation_kn=r_data["kn"],
                        source_clause=r_data["source"]
                    )
                    db.session.add(rule)
            else:
                # Update existing scheme info
                scheme.name_en = s_data["name_en"]
                scheme.name_kn = s_data["name_kn"]
                scheme.department_en = s_data["department_en"]
                scheme.department_kn = s_data["department_kn"]
                scheme.max_benefit = s_data["max_benefit"]
                scheme.official_portal = s_data["official_portal"]
                scheme.required_documents = s_data["required_documents"]

        db.session.commit()
        print("[SUCCESS] All 20 government schemes successfully configured!")

        # =====================================================================
        # 3. SEED DEMO FARMER: Ramesh Gowda (Mandya)
        # =====================================================================
        farmer_phone = "9845012345"
        farmer_user = User.query.filter_by(phone_number=farmer_phone).first()
        if not farmer_user:
            farmer_user = User.query.filter_by(username="demo_farmer").first()

        if not farmer_user:
            print("[SEED] Creating Demo Farmer: Ramesh Gowda...")
            farmer_user = User(
                farmer_id="KM-KA-2026-0842",
                username="demo_farmer",
                password_hash=hash_password("kisan2026"),
                full_name="Ramesh Gowda (ರಮೇಶ್ ಗೌಡ)",
                phone_number=farmer_phone,
                preferred_language="kn",
                role="FARMER",
                is_demo=True
            )
            db.session.add(farmer_user)
            db.session.flush()
        else:
            farmer_user.full_name = "Ramesh Gowda (ರಮೇಶ್ ಗೌಡ)"
            farmer_user.phone_number = farmer_phone
            farmer_user.farmer_id = "KM-KA-2026-0842"
            farmer_user.preferred_language = "kn"

        # Farmer Profile
        profile = FarmerProfile.query.filter_by(user_id=farmer_user.id).first()
        if not profile:
            profile = FarmerProfile(
                user_id=farmer_user.id,
                farmer_id="KM-KA-2026-0842",
                state="Karnataka",
                district="Mandya",
                taluk="Pandavapura",
                village="Chikka Byadarahalli",
                pincode="571434",
                total_land_acres=2.5,
                farmer_category="SMALL",
                social_category="GENERAL",
                irrigation_type="BOREWELL",
                soil_type="RED_LOAM",
                farming_experience_years=14,
                annual_season="KHARIF_RABI",
                verification_status="VERIFIED",
                profile_completion_pct=90,
                has_aadhaar=True,
                has_pm_kisan=True,
                has_kisan_credit_card=False,
                bank_verified=True,
                bank_account_masked="XXXX-XXXX-4589",
                bank_name="State Bank of India (Pandavapura Branch)"
            )
            db.session.add(profile)
            db.session.flush()
        else:
            profile.farmer_id = "KM-KA-2026-0842"
            profile.district = "Mandya"
            profile.taluk = "Pandavapura"
            profile.village = "Chikka Byadarahalli"
            profile.total_land_acres = 2.5
            profile.farmer_category = "SMALL"
            profile.verification_status = "VERIFIED"
            profile.profile_completion_pct = 90

        # Land details
        land = FarmerLandDetails.query.filter_by(user_id=farmer_user.id).first()
        if not land:
            land = FarmerLandDetails(
                user_id=farmer_user.id,
                profile_id=profile.id,
                total_land_acres=2.5,
                land_ownership="OWNED",
                irrigation_availability="IRRIGATED",
                irrigation_type="BOREWELL",
                soil_type="RED_LOAM",
                farming_type="CONVENTIONAL",
                survey_number="142/2A"
            )
            db.session.add(land)

        # Crops: Paddy (1.5 ac) + Ragi (1.0 ac)
        FarmCrop.query.filter_by(profile_id=profile.id).delete()
        c1 = FarmCrop(profile_id=profile.id, crop_name_english="Paddy", crop_name_kannada="ಭತ್ತ", crop_type="MAIN", acres=1.5, season="KHARIF", growth_stage="TILLERING")
        c2 = FarmCrop(profile_id=profile.id, crop_name_english="Ragi", crop_name_kannada="ರಾಗಿ", crop_type="MAIN", acres=1.0, season="KHARIF", growth_stage="VEGETATIVE")
        db.session.add(c1)
        db.session.add(c2)

        # Identity Verification record (Strictly Masked)
        IdentityVerification.query.filter_by(user_id=farmer_user.id).delete()
        idv = IdentityVerification(
            user_id=farmer_user.id,
            verification_type="AADHAAR_OTP",
            provider_name="UIDAI Authorised e-KYC Sandbox",
            transaction_ref="KYC-KA-2026-841920",
            masked_aadhaar="XXXX-XXXX-8421",
            masked_mobile="98XXXXXX45",
            verification_status="VERIFIED",
            consent_recorded=True,
            verified_name="Ramesh Gowda",
            verified_gender="M",
            verified_dob_year="1982",
            is_simulation=True
        )
        db.session.add(idv)

        # =====================================================================
        # 4. SEED REALISTIC APPLICATIONS FOR RAMESH GOWDA
        # =====================================================================
        SchemeApplication.query.filter_by(user_id=farmer_user.id).delete()

        # Application 1: PM-KISAN (APPROVED)
        pm_kisan = Scheme.query.filter_by(code="PM_KISAN").first()
        if pm_kisan:
            app1 = SchemeApplication(
                user_id=farmer_user.id,
                scheme_id=pm_kisan.id,
                application_ref="APP-2026-KM-1001",
                applicant_name="Ramesh Gowda",
                applicant_mobile="9845012345",
                district="Mandya",
                taluk="Pandavapura",
                village="Chikka Byadarahalli",
                land_acres=2.5,
                crops_summary="Paddy, Ragi",
                benefit_amount_expected="₹6,000 / year",
                benefit_amount_disbursed="₹6,000",
                status="APPROVED",
                status_notes="Verified against Land RTC 142/2A and Aadhaar e-KYC. 17th Installment processed.",
                applied_at=datetime.utcnow() - timedelta(days=25),
                is_demo_submission=True
            )
            db.session.add(app1)
            db.session.flush()

            h1 = ApplicationStatusHistory(application_id=app1.id, previous_status=None, new_status="SUBMITTED", stage_name="Application Submitted", remarks="Online application submitted through RaitaSaathiAI portal.", updated_by="FARMER", timestamp=datetime.utcnow() - timedelta(days=25))
            h2 = ApplicationStatusHistory(application_id=app1.id, previous_status="SUBMITTED", new_status="UNDER_VERIFICATION", stage_name="Document Verification", remarks="Pahani and Aadhaar authentication matched.", updated_by="Village Accountant Patil", timestamp=datetime.utcnow() - timedelta(days=20))
            h3 = ApplicationStatusHistory(application_id=app1.id, previous_status="UNDER_VERIFICATION", new_status="APPROVED", stage_name="Application Approved", remarks="Approved for DBT benefit by Assistant Director of Agriculture, Pandavapura.", updated_by="ADA Mandya", timestamp=datetime.utcnow() - timedelta(days=5))
            db.session.add_all([h1, h2, h3])

        # Application 2: Raitha Siri (BENEFIT_DISBURSED)
        raitha_siri = Scheme.query.filter_by(code="RAITHA_SIRI").first()
        if raitha_siri:
            app2 = SchemeApplication(
                user_id=farmer_user.id,
                scheme_id=raitha_siri.id,
                application_ref="APP-2026-KM-1002",
                applicant_name="Ramesh Gowda",
                applicant_mobile="9845012345",
                district="Mandya",
                taluk="Pandavapura",
                village="Chikka Byadarahalli",
                land_acres=1.0,
                crops_summary="Ragi (Millet)",
                benefit_amount_expected="₹10,000 / ha",
                benefit_amount_disbursed="₹10,000",
                status="BENEFIT_DISBURSED",
                status_notes="Millet cultivation verified via Karnataka Crop Survey 2025-26. DBT successfully credited.",
                applied_at=datetime.utcnow() - timedelta(days=40),
                is_demo_submission=True
            )
            db.session.add(app2)
            db.session.flush()

            h1 = ApplicationStatusHistory(application_id=app2.id, previous_status=None, new_status="SUBMITTED", stage_name="Application Submitted", remarks="Submitted under Karnataka Raitha Siri initiative.", updated_by="FARMER", timestamp=datetime.utcnow() - timedelta(days=40))
            h2 = ApplicationStatusHistory(application_id=app2.id, previous_status="SUBMITTED", new_status="APPROVED", stage_name="Application Approved", remarks="Millet crop survey verified.", updated_by="Agronomist RSK", timestamp=datetime.utcnow() - timedelta(days=15))
            h3 = ApplicationStatusHistory(application_id=app2.id, previous_status="APPROVED", new_status="BENEFIT_DISBURSED", stage_name="Benefit Disbursed", remarks="₹10,000 credited to SBI A/C ending in 4589.", updated_by="Treasury DBT Engine", timestamp=datetime.utcnow() - timedelta(days=2))
            db.session.add_all([h1, h2, h3])

        # Application 3: PMFBY (UNDER_VERIFICATION)
        pmfby = Scheme.query.filter_by(code="PMFBY").first()
        if pmfby:
            app3 = SchemeApplication(
                user_id=farmer_user.id,
                scheme_id=pmfby.id,
                application_ref="APP-2026-KM-1003",
                applicant_name="Ramesh Gowda",
                applicant_mobile="9845012345",
                district="Mandya",
                taluk="Pandavapura",
                village="Chikka Byadarahalli",
                land_acres=1.5,
                crops_summary="Paddy (Kharif)",
                benefit_amount_expected="Sum Insured ₹45,000",
                benefit_amount_disbursed="₹0",
                status="UNDER_VERIFICATION",
                status_notes="Sowing certificate submitted. Awaiting Samrakshane portal underwriting approval.",
                applied_at=datetime.utcnow() - timedelta(days=8),
                is_demo_submission=True
            )
            db.session.add(app3)
            db.session.flush()

            h1 = ApplicationStatusHistory(application_id=app3.id, previous_status=None, new_status="SUBMITTED", stage_name="Application Submitted", remarks="Premium of ₹900 paid online.", updated_by="FARMER", timestamp=datetime.utcnow() - timedelta(days=8))
            h2 = ApplicationStatusHistory(application_id=app3.id, previous_status="SUBMITTED", new_status="UNDER_VERIFICATION", stage_name="Document Verification", remarks="Under verification by Agriculture Insurance Company of India.", updated_by="AIC Officer", timestamp=datetime.utcnow() - timedelta(days=3))
            db.session.add_all([h1, h2])

        # Application 4: Krishi Bhagya (PENDING)
        krishi_bhagya = Scheme.query.filter_by(code="KRISHI_BHAGYA").first()
        if krishi_bhagya:
            app4 = SchemeApplication(
                user_id=farmer_user.id,
                scheme_id=krishi_bhagya.id,
                application_ref="APP-2026-KM-1004",
                applicant_name="Ramesh Gowda",
                applicant_mobile="9845012345",
                district="Mandya",
                taluk="Pandavapura",
                village="Chikka Byadarahalli",
                land_acres=2.5,
                crops_summary="Paddy, Ragi",
                benefit_amount_expected="80% Subsidy (₹1.2 Lakhs)",
                benefit_amount_disbursed="₹0",
                status="PENDING",
                status_notes="Application for Farm Pond (Krishi Honda) under departmental spot inspection.",
                applied_at=datetime.utcnow() - timedelta(days=12),
                is_demo_submission=True
            )
            db.session.add(app4)
            db.session.flush()

            h1 = ApplicationStatusHistory(application_id=app4.id, previous_status=None, new_status="SUBMITTED", stage_name="Application Submitted", remarks="Farm pond application submitted.", updated_by="FARMER", timestamp=datetime.utcnow() - timedelta(days=12))
            h2 = ApplicationStatusHistory(application_id=app4.id, previous_status="SUBMITTED", new_status="PENDING", stage_name="Department Review", remarks="Spot inspection scheduled by Assistant Agriculture Officer.", updated_by="AAO Pandavapura", timestamp=datetime.utcnow() - timedelta(days=4))
            db.session.add_all([h1, h2])

        # =====================================================================
        # 5. SEED FARMER NOTIFICATIONS
        # =====================================================================
        FarmerNotification.query.filter_by(user_id=farmer_user.id).delete()
        n1 = FarmerNotification(
            user_id=farmer_user.id,
            title_en="Scheme Approved: PM-KISAN!",
            title_kn="ಯೋಜನೆ ಅನುಮೋದನೆ: ಪಿಎಂ-ಕಿಸಾನ್!",
            title_hi="योजना स्वीकृत: पीएम-किसान!",
            message_en="Congratulations! Your application APP-2026-KM-1001 for PM-KISAN has been APPROVED. Annual benefit: ₹6,000.",
            message_kn="ಅಭಿನಂದನೆಗಳು! ಪಿಎಂ-ಕಿಸಾನ್ ಯೋಜನೆಗೆ ನಿಮ್ಮ ಅರ್ಜಿ (APP-2026-KM-1001) ಅನುಮೋದನೆಗೊಂಡಿದೆ. ವಾರ್ಷಿಕ ₹6,000 ಜಮಾ ಆಗಲಿದೆ.",
            message_hi="बधाई हो! पीएम-किसान के लिए आपका आवेदन स्वीकृत हो गया है।",
            notification_type="APPLICATION_UPDATE",
            is_read=False
        )
        n2 = FarmerNotification(
            user_id=farmer_user.id,
            title_en="Benefit Disbursed: Raitha Siri (₹10,000)",
            title_kn="ಸೌಲಭ್ಯ ವರ್ಗಾವಣೆ: ರೈತ ಸಿರಿ (₹10,000)",
            title_hi="लाभ संवितरित: रैथा सिरी (₹10,000)",
            message_en="Incentive of ₹10,000 for your 1.0-acre Ragi cultivation credited to State Bank of India A/C ending in 4589.",
            message_kn="ನಿಮ್ಮ 1 ಎಕರೆ ರಾಗಿ ಬೆಳೆಗೆ ₹10,000 ಪ್ರೋತ್ಸಾಹಧನ ನಿಮ್ಮ ಎಸ್‌ಬಿಐ ಖಾತೆಗೆ ನೇರವಾಗಿ ಜಮಾ ಆಗಿದೆ.",
            message_hi="आपकी 1 एकड़ रागी की खेती के लिए ₹10,000 का प्रोत्साहन सीधे आपके बैंक खाते में जमा किया गया है।",
            notification_type="BENEFIT_DISBURSED",
            is_read=False
        )
        n3 = FarmerNotification(
            user_id=farmer_user.id,
            title_en="New Eligible Scheme: PMKSY Drip Irrigation",
            title_kn="ಹೊಸ ಅರ್ಹ ಯೋಜನೆ: ಪಿಎಂಕೆಎಸ್‌ವೈ ಹನಿ ನೀರಾವರಿ",
            title_hi="नई पात्र योजना: पीएमकेएसवाई ड्रिप सिंचाई",
            message_en="Based on your borewell-irrigated 2.5-acre land in Mandya, you are eligible for 90% subsidy on Drip Irrigation.",
            message_kn="ಮಂಡ್ಯದ ನಿಮ್ಮ 2.5 ಎಕರೆ ಬೋರ್‌ವೆಲ್ ಜಮೀನಿಗೆ ಶೇಕಡಾ 90 ರಷ್ಟು ಸಹಾಯಧನದಲ್ಲಿ ಹನಿ ನೀರಾವರಿ ಘಟಕ ಲಭ್ಯವಿದೆ. ಇಂದೇ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ.",
            message_hi="मंड्या में आपकी 2.5 एकड़ भूमि के लिए ड्रिप सिंचाई पर 90% सब्सिडी उपलब्ध है।",
            notification_type="SCHEME_ELIGIBLE",
            is_read=True
        )
        db.session.add_all([n1, n2, n3])

        # Commit all transactions
        db.session.commit()
        print("[SUCCESS] Complete demo seeding finished successfully!")
        print(f"  - Admin: admin_krishi / krishiadmin2026")
        print(f"  - Farmer: {farmer_user.full_name} ({farmer_user.farmer_id}) / 9845012345")
        print(f"  - Total Schemes: {Scheme.query.count()}")
        print(f"  - Total Applications: {SchemeApplication.query.count()}")

if __name__ == '__main__':
    seed_all()

# RaitaSaathiAI (ರೈತಸಾಥಿ AI) — Comprehensive System Build & Architecture Guide

> **Platform Mission:** *"Understand Every Farmer. Empower Every Field."*  
> **Primary Target:** Small, marginal, and digitally excluded farmers across Karnataka and India.  
> **Key Paradigms:** Voice-First Interface • Zero-Hallucination Tri-State Scheme Engine • Transparent 5-Stage DBT Tracking • Explainable Agronomic Intelligence • Pure Bilingual Localization.

---

## 1. Executive Summary & Project Purpose

**RaitaSaathiAI** (formerly Krishi Mitra AI) is an end-to-end, voice-first agricultural intelligence and government welfare delivery platform designed specifically for rural Indian farmers. 

In India, **86% of farmers are small or marginal landholders** (< 2 hectares). Despite dozens of high-value central and state government welfare schemes (such as *PM-KISAN*, *Raitha Siri*, *Krishi Bhagya*, *PM Fasal Bima Yojana*, and *Paramparagat Krishi Vikas Yojana*), tens of billions of rupees in subsidies go unclaimed or are captured by corrupt intermediaries. Farmers face three crippling barriers:
1. **The Literacy & Digital Divide:** Inability to read or type complex bureaucratic English or formal text on cluttered government portals.
2. **Linguistic Noise & Broken UX:** Government websites are notoriously cluttered with awkward bracketed translations (e.g., `ಮುಖಪುಟ (Dashboard)`, `Ningegowda (ನಿಂಗೇಗೌಡ)`), intimidating rural users.
3. **The AI Hallucination Threat:** Off-the-shelf generative AI chatbots often invent non-existent government criteria, hallucinate eligibility, or provide potentially lethal pesticide dosage advice without accountability.

RaitaSaathiAI was engineered from scratch to solve these exact problems. It combines **browser-native speech recognition**, **deterministic tri-state statutory rule evaluation**, **grounded agricultural packages of practice (ICAR & UAS Bengaluru)**, and **a zero-framework, lightning-fast frontend** that renders in under 50 milliseconds even on rural 2G/3G mobile networks.

---

## 2. Core Architectural Philosophy: What Was Used, How, and Why

| Architecture Layer | Technology Used | How It Was Used | Why This Choice Was Made |
| :--- | :--- | :--- | :--- |
| **Frontend Core** | **Vanilla HTML5 & ES6+ JavaScript** | Powers the Single Page Application (SPA), dynamic tab routing, modal dialogs, and real-time state management. | **Zero heavy bundle overhead.** Modern React/Angular/Next.js frameworks download megabytes of JavaScript, taking 8–15 seconds to load on rural 2G/3G cellular networks. Vanilla JS loads instantly (< 50ms) with zero compilation step. |
| **Styling & Design System** | **Pure CSS3 Custom Properties** (`style.css`) | Implements a responsive, glassmorphism design system inspired by lush Karnataka agriculture (forest green `#0f3d2e`, emerald `#059669`, gold, and slate). | Delivers a native-app feel on mobile devices with zero runtime overhead, silky smooth 60fps animations for soundwave visualizers, and strict visual hierarchy. |
| **Voice & Speech Engine** | **Web Speech API & Regional Dialect Normalizer** | Captures spoken Kannada and English, renders live soundwave feedback, parses colloquial numbers (e.g., "ಎರಡೂವರೆ" -> `2.5`), and speaks back responses via Text-to-Speech (TTS). | **Accessible & Cost-Free.** Requires zero typing for illiterate farmers, operates natively inside standard mobile browsers (Chrome/Edge/Brave), and eliminates recurring third-party cloud speech API costs. |
| **Backend Framework** | **Python 3 + Flask** (`app/`) | Modular REST API built with 13 Flask Blueprints (`app/routes/`) handling auth, profile, schemes, applications, diagnostics, and admin controls. | Python is the uncontested language of agronomic modeling, NLP, and AI. Flask provides an unopinionated, lightweight, rock-solid WSGI backend that boots in seconds and has zero hidden abstraction layers. |
| **Database & ORM** | **SQLAlchemy with SQLite / PostgreSQL** | Relational data persistence with 14 relational tables in `app/models.py`. Defaults to `raitasaathi_dev.db` locally and auto-configures PostgreSQL for production. | Enforces strict relational integrity between farmers, land parcels, crops, scheme rules, and application status history logs. SQLite enables instant zero-dependency local runs and demo sandboxes. |
| **Scheme Decision Engine** | **Deterministic Tri-State Rule Engine** (`scheme_engine.py`) | Evaluates mathematical rules (`<=`, `>=`, `==`, `IN`, `BOOLEAN`) against 20 verified central and Karnataka schemes, outputting `MATCH`, `NO_MATCH`, or `UNKNOWN`. | **Zero Hallucination Guarantee.** Generative AI models must NEVER determine statutory legal eligibility. If a farmer misses information, the engine outputs `UNKNOWN` with a clear checklist rather than arbitrarily rejecting them. |
| **Agronomic Intelligence** | **ICAR / UAS Bengaluru Grounding + Gemini Flash** (`ai_provider.py`) | Hybrid advisory system: in offline/demo mode, answers are strictly pulled from verified Karnataka Package of Practices; in live cloud mode, queries Google Gemini 1.5 Flash with strict grounding prompts. | Guarantees safe, legally sound agricultural recommendations for crops like Ragi, Paddy, and Tomato, preventing crop loss from bad AI advice. |
| **Confirmation Gate** | **Krishi Echo Gate** (`speech_provider.py` & `assistant.py`) | Interactive confirmation card that asks the farmer to confirm parsed entities (crop, acreage, action) before any irreversible action or submission is taken. | Rural accents and colloquial phrasing must not lead to accidental form submissions or misdiagnoses. The confirmation gate guarantees user intent alignment. |
| **Data Visualization** | **Chart.js** | Renders interactive financial sensitivity curves in the Farm Scenario Lab (`view-calculator`) and application status graphs in the Officer Admin Portal. | Lightweight, high-performance canvas rendering that lets farmers visualize +/- 10% market price fluctuations without page reloads. |

---

## 3. Directory & Codebase Layout

```
RaitaSaathiAI/
│
├── app/                                # Backend Application Package
│   ├── routes/                         # REST API Endpoints (Flask Blueprints)
│   │   ├── __init__.py                 # Blueprint registration hub
│   │   ├── admin.py                    # District Officer portal API & broadcast engine
│   │   ├── applications.py             # Scheme application submission & 5-stage tracking
│   │   ├── assistant.py                # Voice assistant intent router & Krishi Echo
│   │   ├── auth.py                     # Demo login & Aadhaar-linked OTP simulation
│   │   ├── calculator.py               # Farm Scenario Lab financial calculations
│   │   ├── calendar.py                 # Agronomic task scheduler & crop advisory calendar
│   │   ├── crop.py                     # Crop pest & disease diagnostic engine
│   │   ├── dashboard.py                # Unified farmer dashboard metrics & status cards
│   │   ├── identity.py                 # Aadhaar eKYC simulation & FRUITS/BHOOMI sync
│   │   ├── notifications.py            # Real-time farmer notifications & alerts
│   │   ├── profile.py                  # Digital Farmer Profile & land record management
│   │   ├── schemes.py                  # 20 Official schemes lookup & Passport evaluation
│   │   └── soil.py                     # ICAR Soil Health Card interpreter
│   │
│   ├── services/                       # Core Business & Algorithmic Engines
│   │   ├── __init__.py                 # Services package export
│   │   ├── ai_provider.py              # Gemini 1.5 Flash client + ICAR Package of Practices fallback
│   │   ├── calculator_service.py       # Deterministic Python financial arithmetic & sensitivity
│   │   ├── crop_service.py             # Symptom isolator (physical symptoms vs probabilistic AI)
│   │   ├── scheme_engine.py            # Deterministic Tri-State statutory eligibility engine
│   │   ├── soil_service.py             # ICAR soil nutrient benchmark analyzer (pH, EC, N, P, K)
│   │   └── speech_provider.py          # Web Speech parser, dialect normalizer, Krishi Echo builder
│   │
│   ├── utils/                          # Common Utilities & Helpers
│   │   ├── __init__.py
│   │   ├── errors.py                   # Standardized JSON response envelope (success, data, error)
│   │   ├── security.py                 # Password hashing (Werkzeug) & token verification
│   │   └── validators.py               # Form validation & entity sanity checks
│   │
│   ├── __init__.py                     # Flask application factory (create_app)
│   ├── extensions.py                   # SQLAlchemy, Migrate, and CORS instances
│   └── models.py                       # 14 Relational Database Models
│
├── frontend/                           # Presentation Layer (Zero-Framework Vanilla Web)
│   ├── assets/
│   │   ├── css/
│   │   │   └── style.css               # 1,300+ lines responsive design system & voice visualizers
│   │   └── js/
│   │       └── app.js                  # 2,200+ lines SPA core, pure i18n dictionaries, Chart.js logic
│   ├── admin.html                      # District Agriculture Officer Administration Portal
│   ├── app.html                        # Main Farmer Single Page Application (8 tabbed views)
│   └── index.html                      # Glassmorphism Landing Page with interactive workflow steps
│
├── scripts/                            # Operational & Hackathon Tooling
│   ├── generate_pitch_deck.py          # Generates modern 16:9 PowerPoint pitch deck (.pptx)
│   ├── seed_demo_data.py               # Pre-seeds 20 official schemes, rules, and demo farmers
│   └── update_app_js.py                # Helper script for localization synchronization
│
├── tests/                              # Automated Test Suite (Pytest)
│   ├── __init__.py
│   ├── conftest.py                     # In-memory test client & database fixtures
│   ├── test_auth.py                    # Authentication & session verification tests
│   ├── test_calculator.py              # Mathematical accuracy tests for scenario lab
│   ├── test_identity_and_applications.py # eKYC & 5-stage tracking lifecycle tests
│   ├── test_scheme_engine.py           # Tri-state boundary & eligibility logic tests
│   └── test_services.py                # Crop, soil, and voice normalization tests
│
├── .env.example                        # Template environment variables
├── .gitignore                          # Git exclusions (database, cache, virtual environment)
├── config.py                           # Development, Testing & Production configuration classes
├── README.md                           # Quickstart guide & project summary
├── requirements.txt                    # Minimal production dependencies
└── run.py                              # Server bootstrap script
```

---

## 4. Step-by-Step Build Journey: From Start to End

### Step 1: Conceptualization & Problem Formulation
- **The Challenge:** Millions of rural farmers in Karnataka miss out on government assistance because existing portals (like Seva Sindhu or departmental sites) require English literacy, technical proficiency, and complex documentation.
- **The Solution:** Build a unified web application where a farmer can simply **talk in their regional Kannada dialect** to register, automatically check their eligibility across **20 official schemes**, track their benefits through an **audited 5-stage stepper**, and run financial crop scenarios with **pure mathematical certainty**.

### Step 2: Relational Data Modeling (`app/models.py`)
To prevent fragmentation and ensure auditability, 14 clean relational models were engineered:
1. `User`: Core authentication entity (supporting both demo credentials and mobile OTP).
2. `FarmerProfile`: Rich farmer metadata (Karnataka district, taluk, village, landholding size, social category, irrigation access, Aadhaar status, bank details).
3. `FarmerLandDetails`: Exact land records, survey numbers, irrigation methods (borewell, canal, drip, rain-fed), and soil type.
4. `FarmCrop`: Current season crops (Paddy, Ragi, Tomato, Sugarcane) with acreage and growth stage.
5. `IdentityVerification`: Aadhaar eKYC simulation storing **strictly masked identifiers** (`XXXX-XXXX-1234`) and explicit farmer consent timestamps.
6. `Scheme`: Complete catalog of 20 agricultural programs (14 Central + 6 Karnataka State programs) with multilingual summaries, statutory citations, official portals, and maximum benefit caps.
7. `EligibilityRule`: Granular statutory rules linked to schemes with deterministic comparison operators (`<=`, `>=`, `==`, `IN`, `BOOLEAN`).
8. `SchemeApplication`: Complete application tracking records with unique reference IDs (`APP-2026-KM-1001`), expected subsidy amounts, and current statuses.
9. `ApplicationStatusHistory`: Immutable 5-stage audit log documenting status changes from `SUBMITTED` -> `UNDER_VERIFICATION` -> `DEPARTMENT_REVIEW` -> `APPROVED` -> `BENEFIT_DISBURSED`.
10. `FarmerNotification`: Targeted in-app alerts notifying the farmer of application progress or upcoming deadlines.
11. `AdminUser` & `AdminActivityLog`: District Agricultural Officer accounts and immutable audit trails of officer actions.
12. `Conversation` & `Message`: Full chronological chat and voice logs with metadata source tags.
13. `FarmCalculation`: Persisted two-scenario budget comparisons for farmer review.
14. `DecisionEvent`: Comprehensive decision-trail logging system recording every input, extracted entity, rule evaluated, and uncertainty statement.

### Step 3: Algorithmic Core & Domain Services (`app/services/`)
Instead of burying logic inside route handlers, specialized domain services were built:
- **`scheme_engine.py` (Tri-State Scheme Engine):**
  - Evaluates user landholding, caste category, irrigation, and crop against scheme rules.
  - Outputs `MATCH` if all conditions pass; `NO_MATCH` if any fail; and `UNKNOWN` if critical fields (e.g., land records) are missing.
  - Never disqualifies a farmer due to missing fields; instead, returns a structured missing-information checklist.
- **`speech_provider.py` (Voice Parser & Krishi Echo):**
  - Analyzes spoken Kannada phrases and maps colloquial numbers:
    - `"ಒಂದು"` -> `1.0`, `"ಎರಡು"` -> `2.0`, `"ಎರಡೂವರೆ"` -> `2.5`, `"ಮೂರು"` -> `3.0`, `"ಐದು"` -> `5.0`.
  - Normalizes colloquial crops: `"ಟೊಮೇಟೊ"` -> `"Tomato"`, `"ರಾಗಿ"` -> `"Ragi"`, `"ಭತ್ತ"` -> `"Paddy"`.
  - Generates the **Krishi Echo Confirmation Prompt**: *"I understood that you cultivate 2.5 acres of Ragi in Mandya district. Is this correct?"*
- **`calculator_service.py` (Deterministic Financial Scenario Lab):**
  - Pure Python arithmetic calculating total input costs (seeds, fertilizers, labor, machinery, irrigation), gross revenue, and net profit per acre.
  - Automatically calculates sensitivity curves at **-10%, base, and +10% price and yield shocks**, helping farmers choose the more resilient crop before planting.
- **`crop_service.py` & `soil_service.py`:**
  - Isolates visible leaf symptoms (e.g., yellow spots, leaf curl) from probabilistic hypotheses.
  - Compares soil test values (pH, Electrical Conductivity, Nitrogen, Phosphorus, Potassium) against official ICAR rating charts.

### Step 4: RESTful API Layer (`app/routes/`)
13 Flask Blueprints were created, each adhering to the unified JSON envelope defined in `app/utils/errors.py`:
```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "metadata": {
    "platform": "RaitaSaathiAI",
    "version": "1.0.0"
  }
}
```
Key endpoints:
- `POST /api/auth/phone-login`: Frictionless one-tap OTP login for rural users.
- `GET /api/schemes/passport`: Runs the real-time Tri-State Scheme Passport evaluation.
- `POST /api/applications/submit`: Instant application lodgement with auto-generated tracking timeline.
- `POST /api/assistant/interact`: Natural language query processing with Krishi Echo confirmation gating.
- `POST /api/calculator/compare`: Instant server-side financial scenario modeling.
- `POST /api/admin/applications/<id>/status`: District officer workflow to approve or disburse subsidies.

### Step 5: Frontend Single Page Application (`frontend/`)
The frontend was designed with an uncompromising focus on usability, speed, and linguistic clarity:
- **`frontend/index.html` (Landing Page):**
  - Welcomes users with an accessible hero section, Kannada voice invitation button, interactive value cards, and a 3-step workflow diagram.
- **`frontend/app.html` (Farmer Web App):**
  - Contains 8 full-featured tab views that switch instantly without network latency:
    1. **Dashboard:** Displays personalized greeting, verification badge, district indicator, quick action buttons, and active application summary.
    2. **Scheme Passport:** Displays all 20 schemes with filter chips (Financial, Subsidy, Irrigation, Insurance, Organic) and real-time eligibility tags.
    3. **Application Tracking:** Visual 5-stage interactive stepper showing real-time departmental progress.
    4. **My Profile:** Aadhaar eKYC card, landholding parameters, and registered crop list.
    5. **Voice Assistant:** Center-stage glowing microphone with animated equalizers, live transcript, and Krishi Echo confirmation cards.
    6. **Farm Scenario Lab:** Side-by-side financial scenario comparison with interactive Chart.js graphs.
    7. **Crop Health Diagnostic:** Symptom inspection guide with UAS Bengaluru agronomic recommendations.
    8. **Soil Health Card:** Soil nutrient meter comparing sample values against ICAR thresholds.
- **`frontend/admin.html` (Officer Portal):**
  - Allows District Agricultural Officers to review farmer applications, inspect Pahani/Aadhaar documents, approve subsidies, and broadcast frost/pest advisories.
- **`frontend/assets/js/app.js` (Pure Bilingual Localization Engine):**
  - Solves the "bracket noise" problem by maintaining two completely distinct, unmixed dictionaries: **100% Pure Kannada (`kn`)** and **100% Pure English (`en`)**. Switching languages takes < 50ms and instantly updates every label, dropdown, and timeline stage.

### Step 6: Automated Seeding & Hackathon Tooling (`scripts/`)
- **`seed_demo_data.py`:** Initializes the SQLite database with 20 real government schemes, 50+ eligibility rules, sample Karnataka farmers (such as Ningegowda in Mandya), pre-existing applications across all 5 timeline stages, and administrative officer credentials.
- **`generate_pitch_deck.py`:** A dedicated Python script using `python-pptx` to generate a 12-slide, 16:9 widescreen PowerPoint presentation with custom color cards, stat pills, and full speaker notes.

### Step 7: Testing & Verification (`tests/`)
A complete Pytest suite validates all critical system components:
- `test_scheme_engine.py`: Verifies boundary conditions, multi-rule conjunctions, and `UNKNOWN` missing-information states.
- `test_calculator.py`: Verifies arithmetic correctness, cost breakdowns, and sensitivity shock equations.
- `test_auth.py` & `test_identity_and_applications.py`: Tests login sessions, masked Aadhaar integrity, application creation, and timeline transitions.

---

## 5. Summary of the 20 Modeled Agricultural Schemes

RaitaSaathiAI models **14 Central Government** and **6 Karnataka State Flagship** schemes with statutory fidelity:

| # | Scheme Code | Official Scheme Name | Jurisdiction | Benefit Details |
| :---: | :--- | :--- | :---: | :--- |
| 1 | `PM_KISAN` | PM-Kisan Samman Nidhi | Central | ₹6,000 / year direct bank transfer in 3 tranches |
| 2 | `RAITHA_SIRI` | Raitha Siri Yojana | Karnataka | ₹10,000 / hectare incentive for minor millet cultivation |
| 3 | `PMFBY` | Pradhan Mantri Fasal Bima Yojana | Central | Subsidized crop insurance (1.5% - 2% farmer premium) |
| 4 | `PMKSY_PDMC` | PM Krishi Sinchayee Yojana (Per Drop More Crop) | Central | 45% - 55% subsidy on drip and micro-irrigation systems |
| 5 | `KCC` | Kisan Credit Card Scheme | Central | Concessional agricultural credit at 4% effective interest |
| 6 | `KRISHI_BHAGYA` | Krishi Bhagya Yojana | Karnataka | 80% - 90% subsidy on farm ponds (Krishi Honda) & diesel pumps |
| 7 | `SMAM` | Sub-Mission on Agricultural Mechanization | Central | 40% - 50% subsidy on tractors and farm machinery |
| 8 | `PKVY` | Paramparagat Krishi Vikas Yojana | Central | ₹50,000 / hectare assistance for certified organic farming |
| 9 | `SHC` | Soil Health Card Scheme | Central | Free periodic soil nutrient testing and customized fertilizer advisory |
| 10 | `AIF` | Agriculture Infrastructure Fund | Central | 3% interest subvention for post-harvest cold storage & warehouses |
| 11 | `PM_KMY` | PM Kisan Maandhan Yojana | Central | Assured monthly pension of ₹3,000 after age 60 |
| 12 | `MIDH` | Mission for Integrated Development of Horticulture | Central | 40% - 50% subsidy on polyhouses, shade nets, and orchards |
| 13 | `NFSM` | National Food Security Mission | Central | Subsidized high-yielding variety seeds and bio-fertilizers |
| 14 | `AGRISTACK` | AgriStack Digital Farmer ID | Central | Unified digital farmer registry with automated DBT routing |
| 15 | `CM_KRISHI_VISTARA`| CM Krishi Vistara Yojana | Karnataka | Free mobile diagnostic testing & subsidized drone spraying |
| 16 | `KVK_TRAINING` | Krishi Vigyan Kendra Hands-On Skill Program | Central | Free residential farmer training on high-value crop techniques |
| 17 | `SURYA_RAITHA` | Surya Raitha Solar Irrigation Scheme | Karnataka | 90% subsidy on solar-powered water pumpsets |
| 18 | `DAIRY_PROMO` | Karnataka Ksheera Samruddhi Dairy Program | Karnataka | ₹5 / liter milk producer subsidy credited directly to bank account |
| 19 | `SERICULTURE_SUB` | Karnataka Reshme Kirana Sericulture Scheme | Karnataka | 75% subsidy on silkworm rearing sheds and equipment |
| 20 | `ORGANIC_MISSION` | Karnataka State Organic Farming Mission | Karnataka | Free bio-input kits & state organic market certification |

---

## 6. How to Run, Test, and Verify the Project

### Prerequisites
- Python 3.10+ (or Python 3.14 via `uv` or standard virtual environment).
- Modern web browser (Chrome, Edge, Brave, or Safari with Web Speech API enabled).

### 1. Setup Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Seed Demo Database
```bash
python scripts/seed_demo_data.py
```
*Creates `raitasaathi_dev.db` with all 20 schemes, eligibility rules, demo farmer profiles, and pre-populated application timelines.*

### 4. Run Automated Tests
```bash
pytest
```

### 5. Launch Application
```bash
python run.py
```
Open **`http://127.0.0.1:5000`** in your browser.
- **Farmer App:** `http://127.0.0.1:5000/app` (Login: `demo_farmer` / `kisan2026` or use 1-click OTP login)
- **Officer Admin Portal:** `http://127.0.0.1:5000/admin` (Login: `admin_krishi` / `krishiadmin2026`)
- **Landing Page:** `http://127.0.0.1:5000/`

---

## 7. Future Horizons & Scalability Roadmap

1. **Telephony IVR & WhatsApp Integration:**
   - Extend the core Python speech parser to toll-free IVR numbers and WhatsApp voice notes, allowing farmers with basic ₹1,000 2G feature phones to access all 20 schemes.
2. **Satellite Drought & Flood Verification:**
   - Integrate Sentinel-2 / Landsat NDVI vegetation index data to automatically trigger PMFBY crop insurance claims when rainfall fails in specific taluks.
3. **State Land Records API Federation (BHOOMI & FRUITS):**
   - Connect directly to Karnataka's official **BHOOMI** (land records) and **FRUITS** (Farmer Registration & Unified Beneficiary Information System) APIs for instant real-time RTC/Pahani verification.
4. **Pan-India Expansion:**
   - Expand localization beyond Kannada and English to include Marathi, Telugu, Tamil, Malayalam, and Hindi for nationwide deployment across all 28 states.


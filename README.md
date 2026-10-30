# RAITASAATHIAI (ರೈತಸಾಥಿ AI)
> *"Understand Every Farmer. Empower Every Field."*

RaitaSaathiAI is a voice-first, multimodal, explainable AI farming companion designed primarily for farmers in Karnataka and other regions of India.

---

## 🌾 Key Features

1. **🎙️ Krishi Echo & Regional Kannada Dialect Ingestion**
   - Natural Kannada speech with dialect recovery (e.g., 'ಟೊಮೆಟೊ', 'ರಾಗಿ', 'ಕಬ್ಬು').
   - Confirmation gates to confirm understanding before taking consequential farm actions.

2. **📜 Scheme Passport (Flagship Feature)**
   - Tri-State Deterministic Rule Evaluation: `MATCH`, `NO_MATCH`, or `UNKNOWN`.
   - Never disqualifies when info is missing; provides a transparent missing-information checklist.
   - Evaluates PM-Kisan, Raitha Siri, Krishi Bhagya, and other state/central schemes with statutory citations.

3. **🔬 Crop Symptom Intelligence**
   - Strictly isolates visible observations from probabilistic AI hypotheses.
   - Grounded in UAS Bangalore & ICAR package of practices.

4. **🧪 Soil Health Card Interpreter**
   - Evaluates pH, EC, N, P, and K against official ICAR standards.

5. **⚖️ Farm Scenario Lab (Financial Calculator)**
   - Deterministic Python financial calculations for crop yield, cost per acre, and net return.
   - +/- 10% price and yield sensitivity curves with interactive Chart.js visualization.

6. **🛡️ Decision Trail**
   - Audited chronological record for every query, extraction, rule evaluation, and source citation.

---

## 🚀 Quickstart (Windows / Local Dev)

### 1. Setup Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize & Seed Demo Data
```bash
python scripts/seed_demo_data.py
```

### 4. Run Automated Tests
```bash
pytest
```

### 5. Start the Server
```bash
python run.py
```
Open **`http://127.0.0.1:5000`** in your browser.

- **Landing Page**: `http://127.0.0.1:5000/`
- **Farmer App (SPA)**: `http://127.0.0.1:5000/app`
- **Demo Credentials**:
  - Username: `demo_farmer`
  - Password: `kisan2026`


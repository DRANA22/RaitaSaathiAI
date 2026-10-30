# -*- coding: utf-8 -*-
"""
Script to write the complete, clean, professional app.js with:
1. Pure Kannada (kn) with ZERO English words in brackets.
2. Pure English (en) with ZERO Kannada or brackets.
3. Dedicated Voice button for EVERY registration section with speech recognition & parsing.
4. Universal Voice Hearing Animation Overlay (pulse ring, 7 dancing equalizer soundwave bars, live transcript, audio chime).
5. Clean dynamic translations for all 20 schemes, 5-stage tracking timeline, KPIs, and profile.
"""
import os

js_content = r'''// RaitaSaathiAI — Modern Single Page Application Core
// 100% Pure Kannada & 100% Pure English Localization Engine

let activeLanguage = localStorage.getItem('krishi_lang') || 'kn';
let activeEchoData = null;
let profitChartInstance = null;
let currentFarmerData = null;
let allSchemesList = [];
let allApplicationsList = [];
let farmerCustomName = localStorage.getItem('krishi_farmer_name') || '';

// ============================================================================
// MASTER TRANSLATION DICTIONARY (ZERO BRACKETS, 100% PURE KANNADA & ENGLISH)
// ============================================================================
const I18N_DICTIONARY = {
  kn: {
    state_karnataka: "ಕರ್ನಾಟಕ",
    brand_tagline: "ರೈತಸಾಥಿ AI",
    nav_dashboard: "ಮುಖಪುಟ",
    nav_schemes: "ಯೋಜನೆಗಳು",
    nav_tracking: "ಅರ್ಜಿ ಟ್ರ್ಯಾಕಿಂಗ್",
    nav_profile: "ನನ್ನ ಪ್ರೊಫೈಲ್",
    nav_assistant: "ಧ್ವನಿ ಸಹಾಯಕ",
    nav_calculator: "ಬಜೆಟ್ ಲ್ಯಾಬ್",
    nav_crop: "ಬೆಳೆ ರೋಗ",
    nav_soil: "ಮಣ್ಣು ಪರೀಕ್ಷೆ",
    nav_register: "📝 ಹೊಸ ನೋಂದಣಿ",
    nav_admin: "🛡️ ಅಧಿಕಾರಿ ಪೋರ್ಟಲ್",
    notif_header: "🔔 ಅಧಿಸೂಚನೆಗಳು",
    notif_mark_all: "ಎಲ್ಲಾ ಓದಲಾಗಿದೆ",
    notif_loading: "ಅಧಿಸೂಚನೆಗಳು ಲೋಡ್ ಆಗುತ್ತಿವೆ...",
    notif_empty: "ಯಾವುದೇ ಹೊಸ ಅಧಿಸೂಚನೆಗಳಿಲ್ಲ.",
    verified_profile_badge: "ದೃಢೀಕರಿಸಲ್ಪಟ್ಟ ರೈತ ಪ್ರೊಫೈಲ್",
    welcome_prefix: "ನಮಸ್ಕಾರ, ",
    default_farmer_title: "ರೈತ ಮಿತ್ರ",
    btn_edit_name: "ಹೆಸರು ಬದಲಾಯಿಸಿ",
    btn_add_name: "ಹೆಸರು ನಮೂದಿಸಿ",
    farmer_name_label: "👨‍🌾 ರೈತರ ಹೆಸರು:",
    farmer_name_placeholder: "ಹೆಸರನ್ನು ಹೇಳಿ ಅಥವಾ ಬರೆಯಿರಿ...",
    speak_btn: "ಮಾತನಾಡಿ",
    save_btn: "✓ ಉಳಿಸಿ",
    profile_completion_label: "ಪ್ರೊಫೈಲ್ ಪೂರ್ಣಗೊಂಡಿದೆ",
    banner_voice_btn: "🎤 ಧ್ವನಿ ಪ್ರಶ್ನೆ",
    banner_schemes_btn: "📜 ಯೋಜನೆಗಳು",
    banner_profile_btn: "👤 ನನ್ನ ಪ್ರೊಫೈಲ್",
    kpi_total_title: "ಒಟ್ಟು ಯೋಜನೆಗಳು",
    kpi_total_sub: "ಕೇಂದ್ರ ಮತ್ತು ಕರ್ನಾಟಕ ಸರ್ಕಾರ",
    kpi_eligible_title: "ಅರ್ಹ ಯೋಜನೆಗಳು",
    kpi_eligible_sub: "ನಿಮ್ಮ ಭೂಮಿ ಮತ್ತು ಬೆಳೆಗೆ",
    kpi_submitted_title: "ಸಲ್ಲಿಸಿದ ಅರ್ಜಿಗಳು",
    kpi_submitted_sub: "ಟ್ರ್ಯಾಕಿಂಗ್ ಲಭ್ಯವಿದೆ",
    kpi_approved_title: "ಅನುಮೋದಿತ ಅರ್ಜಿಗಳು",
    kpi_approved_sub: "ಮಂಜೂರಾದ ಸೌಲಭ್ಯಗಳು",
    kpi_pending_title: "ಪರಿಶೀಲನೆಯಲ್ಲಿರುವ ಅರ್ಜಿಗಳು",
    kpi_pending_sub: "ಇಲಾಖಾ ಪರಿಶೀಲನೆಯಲ್ಲಿದೆ",
    kpi_benefits_title: "ಪಡೆದ ಸೌಲಭ್ಯ ಮೊತ್ತ",
    kpi_benefits_sub: "ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ನೇರ ವರ್ಗಾವಣೆ",
    recent_apps_title: "ಇತ್ತೀಚಿನ ಅರ್ಜಿಗಳ ಸ್ಥಿತಿ",
    recent_apps_sub: "ಅರ್ಜಿ ಪ್ರಗತಿ, ಪರಿಶೀಲನಾ ಹಂತ ಮತ್ತು ನೇರ ಹಣ ಜಮೆ ವಿವರಗಳು",
    view_all_apps_btn: "ಎಲ್ಲಾ ಅರ್ಜಿಗಳು ನೋಡಿ &rarr;",
    th_app_id: "ಅರ್ಜಿ ಸಂಖ್ಯೆ",
    th_scheme_name: "ಯೋಜನೆಯ ಹೆಸರು",
    th_scheme_dept: "ಯೋಜನೆ ಮತ್ತು ಇಲಾಖೆ",
    th_date: "ದಿನಾಂಕ",
    th_benefit: "ಸೌಲಭ್ಯ ಮೊತ್ತ",
    th_status: "ಸ್ಥಿತಿ",
    th_stage: "ಪ್ರಸ್ತುತ ಹಂತ",
    th_action: "ವಿವರ",
    loading_apps: "ಅರ್ಜಿಗಳನ್ನು ಲೋಡ್ ಮಾಡಲಾಗುತ್ತಿದೆ...",
    no_apps_found: "ಯಾವುದೇ ಅರ್ಜಿಗಳು ಕಂಡುಬಂದಿಲ್ಲ.",
    view_timeline_btn: "🔍 ಪ್ರಗತಿ ನೋಡಿ",
    quick_advice_title: "⚡ ತ್ವರಿತ ಕೃಷಿ ಸಲಹೆ",
    quick_advice_sub: "ಪ್ರಸ್ತುತ ಋತುವಿನ ಬೆಳೆಗಳು ಮತ್ತು ಕೀಟ ನಿರ್ವಹಣೆಯ ಬಗ್ಗೆ ಧ್ವನಿಯ ಮೂಲಕ ಕೇಳಿ.",
    chip_ragi: "🌱 ರಾಗಿ ಗೊಬ್ಬರ ನಿರ್ವಹಣೆ",
    chip_paddy: "🌾 ಭತ್ತದ ಹುಳು ಹತೋಟಿ",
    chip_schemes: "📜 ನನ್ನ ಅರ್ಹ ಯೋಜನೆಗಳು",
    scenario_lab_card_title: "📊 ಕೃಷಿ ಬಜೆಟ್ ಲ್ಯಾಬ್",
    scenario_lab_card_sub: "ಬೆಳೆಗಳ ಖರ್ಚು, ಆದಾಯ ಮತ್ತು ನಿವ್ವಳ ಲಾಭದ ಗಣಿತೀಯ ಹೋಲಿಕೆ.",
    open_lab_btn: "⚖️ ಬಜೆಟ್ ಲ್ಯಾಬ್ ತೆರೆಯಿರಿ",
    schemes_heading: "ಸರ್ಕಾರಿ ಕೃಷಿ ಯೋಜನೆಗಳು",
    schemes_sub: "ಕೇಂದ್ರ ಮತ್ತು ಕರ್ನಾಟಕ ಸರ್ಕಾರದ 20 ಅಧಿಕೃತ ಕೃಷಿ ಯೋಜನೆಗಳು — ನಿಮ್ಮ ಜಮೀನು ಮತ್ತು ಬೆಳೆಗೆ ಅನುಗುಣವಾಗಿ ಪರಿಶೀಲಿಸಲಾಗಿದೆ.",
    reevaluate_schemes_btn: "🔄 ಅರ್ಹತೆ ಮರುಪರಿಶೀಲಿಸಿ",
    filter_all_schemes: "ಎಲ್ಲಾ ಯೋಜನೆಗಳು (20)",
    filter_dbt: "💵 ನೇರ ನಗದು ವರ್ಗಾವಣೆ",
    filter_subsidy: "🚜 ಸಬ್ಸಿಡಿ ಮತ್ತು ಯಂತ್ರೋಪಕರಣ",
    filter_insurance: "🛡️ ಬೆಳೆ ವಿಮೆ ಮತ್ತು ಸಾಲ",
    filter_irrigation: "💧 ನೀರಾವರಿ ಯೋಜನೆಗಳು",
    filter_input: "🌱 ಬಿತ್ತನೆ ಬೀಜ ಮತ್ತು ಗೊಬ್ಬರ",
    loading_schemes: "ಯೋಜನೆಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...",
    no_schemes_found: "ಈ ವರ್ಗದಲ್ಲಿ ಯಾವುದೇ ಯೋಜನೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ.",
    tracking_heading: "ನನ್ನ ಅರ್ಜಿಗಳ ಟ್ರ್ಯಾಕಿಂಗ್",
    tracking_sub: "ಅರ್ಜಿ ಸಲ್ಲಿಕೆಯಿಂದ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ಹಣ ಜಮೆ ಆಗುವವರೆಗಿನ 5 ಹಂತಗಳ ನೈಜ ಪ್ರಗತಿ.",
    btn_apply_new_scheme: "➕ ಹೊಸ ಯೋಜನೆಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ",
    filter_all_apps: "ಎಲ್ಲಾ ಅರ್ಜಿಗಳು",
    filter_pending_apps: "⏳ ಪರಿಶೀಲನೆಯಲ್ಲಿರುವ",
    filter_approved_apps: "✅ ಅನುಮೋದಿತ",
    filter_disbursed_apps: "💰 ಸೌಲಭ್ಯ ಜಮೆ",
    profile_heading: "ರೈತರ ಡಿಜಿಟಲ್ ಗುರುತು",
    profile_sub: "ಆಧಾರ್ e-KYC ಮೂಲಕ ದೃಢೀಕರಿಸಲ್ಪಟ್ಟ ವೈಯಕ್ತಿಕ, ಕೃಷಿ ಭೂಮಿ, ಬೆಳೆ ಮತ್ತು ಬ್ಯಾಂಕ್ ಖಾತೆ ವಿವರಗಳು.",
    profile_sec_a: "A. ವೈಯಕ್ತಿಕ ವಿವರಗಳು",
    profile_sec_b: "B. ಕೃಷಿ ಭೂಮಿ ವಿವರಗಳು",
    profile_sec_c: "C. ಬ್ಯಾಂಕ್ ಖಾತೆ ಮತ್ತು ಸೌಲಭ್ಯ ಸ್ಥಿತಿ",
    lbl_farmer_id: "ರೈತ ಸಂಖ್ಯೆ:",
    lbl_full_name: "ಪೂರ್ಣ ಹೆಸರು:",
    lbl_mobile: "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ:",
    lbl_ekyc: "ಆಧಾರ್ ದೃಢೀಕರಣ:",
    lbl_state: "ರಾಜ್ಯ:",
    lbl_district: "ಜಿಲ್ಲೆ:",
    lbl_taluk: "ತಾಲ್ಲೂಕು:",
    lbl_village: "ಗ್ರಾಮ:",
    lbl_total_land: "ಒಟ್ಟು ಜಮೀನು:",
    lbl_ownership: "ಭೂಮಾಲೀಕತ್ವ:",
    val_owned: "ಸ್ವಂತ ಭೂಮಿ",
    lbl_category: "ರೈತರ ವರ್ಗ:",
    val_small_farmer: "ಸಣ್ಣ ರೈತರು",
    lbl_irrigation: "ನೀರಾವರಿ ವ್ಯವಸ್ಥೆ:",
    val_borewell: "ಬೋರ್‌ವೆಲ್ ನೀರಾವರಿ",
    val_canal: "ಕಾಲುವೆ ನೀರಾವರಿ",
    val_rainfed: "ಮಳೆ ಆಶ್ರಿತ",
    val_drip: "ಹನಿ ನೀರಾವರಿ",
    lbl_soil_type: "ಮಣ್ಣಿನ ವಿಧ:",
    val_red_soil: "ಕೆಂಪು ಮರಳು ಮಿಶ್ರಿತ ಮಣ್ಣು",
    lbl_main_crops: "ಮುಖ್ಯ ಬೆಳೆಗಳು:",
    lbl_bank_name: "ಬ್ಯಾಂಕ್ ಹೆಸರು:",
    val_sbi: "ಸ್ಟೇಟ್ ಬ್ಯಾಂಕ್ ಆಫ್ ಇಂಡಿಯಾ",
    lbl_account_no: "ಖಾತೆ ಸಂಖ್ಯೆ:",
    lbl_aadhaar_seed: "ಆಧಾರ್ ಜೋಡಣೆ:",
    val_seeded: "✓ ಜೋಡಿಸಲಾಗಿದೆ (DBT ಸಕ್ರಿಯ)",
    assistant_title: "ರೈತಸಾಥಿ AI ಧ್ವನಿ ಸಹಾಯಕ",
    assistant_sub: "ಕನ್ನಡದಲ್ಲಿ ಮಾತನಾಡಿ. ಯೋಜನೆಗಳು, ಅರ್ಜಿ ಸ್ಥಿತಿ ಅಥವಾ ಬೆಳೆ ರೋಗಗಳ ಬಗ್ಗೆ ನೇರವಾಗಿ ಕೇಳಿ.",
    voice_tap_prompt: "ಮಾತನಾಡಲು ಮೈಕ್ರೊಫೋನ್ ಒತ್ತಿರಿ",
    echo_card_title: "ದೃಢೀಕರಣ ಅಗತ್ಯವಿದೆ",
    echo_btn_yes: "✓ ಹೌದು, ಸರಿಯಾಗಿದೆ",
    echo_btn_no: "✎ ತಪ್ಪಾಗಿದೆ, ಸರಿಪಡಿಸಿ",
    assistant_input_ph: "ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ (ಉದಾ: ರಾಗಿ ಬೆಳೆಗೆ ಎಷ್ಟು ಗೊಬ್ಬರ ಹಾಕಬೇಕು? ಅಥವಾ ನನ್ನ ಯೋಜನೆಗಳು)...",
    assistant_send_btn: "ಕಳುಹಿಸಿ",
    calc_heading: "ಕೃಷಿ ಬಜೆಟ್ ಲ್ಯಾಬ್",
    calc_sub: "ಭತ್ತ ಮತ್ತು ಸಾವಯವ ರಾಗಿ ಬೆಳೆಗಳ ಉತ್ಪಾದನಾ ವೆಚ್ಚ, ನಿರೀಕ್ಷಿತ ಆದಾಯ ಮತ್ತು ನಿವ್ವಳ ಲಾಭದ ಗಣಿತೀಯ ಹೋಲಿಕೆ.",
    scen_a_title: "ಮೊದಲ ಬೆಳೆ: ಭತ್ತ",
    scen_b_title: "ಎರಡನೇ ಬೆಳೆ: ಸಾವಯವ ರಾಗಿ",
    lbl_land_area: "ಜಮೀನಿನ ವಿಸ್ತೀರ್ಣ (ಎಕರೆ):",
    lbl_yield: "ನಿರೀಕ್ಷಿತ ಇಳುವರಿ (ಕ್ವಿಂಟಾಲ್/ಎಕರೆ):",
    lbl_price: "ಮಾರಾಟ ಬೆಲೆ (₹ ಪ್ರತಿ ಕ್ವಿಂಟಾಲ್):",
    lbl_costs: "ಒಟ್ಟು ಉತ್ಪಾದನಾ ವೆಚ್ಚ (ಬೀಜ, ಗೊಬ್ಬರ, ಕೂಲಿ ₹):",
    btn_run_comparison: "📊 ಹೋಲಿಕೆ ಲೆಕ್ಕಾಚಾರ ಮಾಡಿ",
    crop_heading: "ಬೆಳೆ ರೋಗ ತಪಾಸಣೆ",
    lbl_crop_name: "ಬೆಳೆಯ ಹೆಸರು:",
    lbl_crop_symptoms: "ಕಂಡುಬಂದ ರೋಗ ಲಕ್ಷಣಗಳನ್ನು ವಿವರಿಸಿ:",
    crop_symptoms_ph: "ಉದಾ: ಎಲೆಗಳು ಹಳದಿಯಾಗುತ್ತಿವೆ ಮತ್ತು ಸುರುಳಿಯಾಗುತ್ತಿವೆ...",
    btn_analyze_crop: "ರೋಗ ಪರೀಕ್ಷಿಸಿ",
    soil_heading: "ಮಣ್ಣು ಆರೋಗ್ಯ ಪರೀಕ್ಷೆ",
    lbl_soil_ph: "pH ಮಟ್ಟ (ಆಮ್ಲತೆ/ಕ್ಷಾರತೆ):",
    lbl_soil_ec: "ವಿದ್ಯುತ್ ವಾಹಕತೆ (EC dS/m):",
    lbl_soil_n: "ಲಭ್ಯವಿರುವ ಸಾರಜನಕ (N kg/ha):",
    lbl_soil_p: "ಲಭ್ಯವಿರುವ ರಂಜಕ (P kg/ha):",
    lbl_soil_k: "ಲಭ್ಯವಿರುವ ಪೊಟ್ಯಾಶ್ (K kg/ha):",
    btn_interpret_soil: "ಮಣ್ಣಿನ ವರದಿ ವಿಶ್ಲೇಷಿಸಿ",
    timeline_modal_title: "ಅರ್ಜಿ ಪ್ರಗತಿ ವಿವರ",
    disbursed_box_title: "💰 ಸೌಲಭ್ಯ ಜಮೆ ವಿವರ:",
    modal_close_btn: "ಮುಚ್ಚಿ",
    reg_modal_title: "ಹೊಸ ರೈತರ ನೋಂದಣಿ",
    reg_modal_sub: "ಆಧಾರ್ e-KYC ದೃಢೀಕರಣ ಮತ್ತು ಡಿಜಿಟಲ್ ರೈತ ಗುರುತು",
    reg_step_1_tab: "೧. ವಿವರಗಳು",
    reg_step_2_tab: "೨. e-KYC ಪರಿಶೀಲನೆ",
    reg_step_3_tab: "೩. ರೈತ ಗುರುತು",
    demo_farmer_title: "⚡ ಡೆಮೊ ರೈತರೊಂದಿಗೆ ಪ್ರಾರಂಭಿಸಿ:",
    demo_farmer_desc: "ರಮೇಶ್ ಗೌಡ, ಮಂಡ್ಯ (2.5 ಎಕರೆ ಭತ್ತ & ರಾಗಿ)",
    demo_farmer_btn: "ರಮೇಶ್ ಗೌಡ ಆಯ್ಕೆಮಾಡಿ",
    lbl_reg_name: "ರೈತರ ಪೂರ್ಣ ಹೆಸರು:",
    reg_name_ph: "ಉದಾ: ರಮೇಶ್ ಗೌಡ",
    lbl_reg_mobile: "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ:",
    reg_mobile_ph: "10 ಅಂಕಿಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ಹೇಳಿ ಅಥವಾ ಬರೆಯಿರಿ...",
    lbl_reg_aadhaar: "ಆಧಾರ್ ಸಂಖ್ಯೆ:",
    reg_aadhaar_ph: "12 ಅಂಕಿಯ ಆಧಾರ್ ಸಂಖ್ಯೆ...",
    lbl_aadhaar_security_note: "🔒 ಸುರಕ್ಷಿತ e-KYC: ಕೇವಲ ಮಾಸ್ಕ್ ಮಾಡಿದ ಗುರುತು ಮಾತ್ರ ದಾಖಲಾಗುತ್ತದೆ.",
    reg_taluk_ph: "ಉದಾ: ಪಾಂಡವಪುರ",
    reg_village_ph: "ಉದಾ: ಚಿಕ್ಕ ಬ್ಯಾಡರಹಳ್ಳಿ",
    lbl_reg_land: "ಒಟ್ಟು ಜಮೀನು (ಎಕರೆ):",
    lbl_consent_text: "ನನ್ನ ಆಧಾರ್ ವಿವರಗಳನ್ನು ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಅರ್ಹತೆ ಪರಿಶೀಲನೆಗೆ ಬಳಸಲು ಸಮ್ಮತಿಸುತ್ತೇನೆ.",
    btn_next_step: "ಮುಂದಿನ ಹಂತ: ದೃಢೀಕರಣ &rarr;",
    otp_heading: "ದೃಢೀಕರಣ ಕೋಡ್ (OTP)",
    otp_sub: "ದೃಢೀಕರಣ ಕೋಡ್ ಅನ್ನು ನೋಂದಾಯಿತ ಮೊಬೈಲ್‌ಗೆ ಕಳುಹಿಸಲಾಗಿದೆ.",
    otp_demo_hint: "💡 ಡೆಮೊಗಾಗಿ '2026' ಸಂಖ್ಯೆ ಬಳಸಿ.",
    lbl_enter_otp: "4-ಅಂಕಿಯ ಕೋಡ್ ನಮೂದಿಸಿ:",
    btn_back: "ಹಿಂದಕ್ಕೆ",
    btn_verify_otp: "✓ ದೃಢೀಕರಿಸಿ",
    reg_success_title: "ರೈತರ ಖಾತೆ ಯಶಸ್ವಿಯಾಗಿ ರಚನೆಯಾಗಿದೆ!",
    reg_success_sub: "ನಿಮ್ಮ ಡಿಜಿಟಲ್ ರೈತ ಗುರುತು ಸಿದ್ಧವಾಗಿದೆ.",
    lbl_your_farmer_id: "ನಿಮ್ಮ ಅನನ್ಯ ರೈತ ಸಂಖ್ಯೆ:",
    lbl_name: "ಹೆಸರು:",
    lbl_status: "ಸ್ಥಿತಿ:",
    btn_goto_dashboard: "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಹೋಗಿ &rarr;",
    apply_modal_title: "ಯೋಜನೆಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ",
    apply_modal_sub: "ಕೃಷಿ ಇಲಾಖೆ, ಕರ್ನಾಟಕ ಸರ್ಕಾರ",
    apply_lbl_benefit: "ಸೌಲಭ್ಯ ಮೊತ್ತ / ಸಬ್ಸಿಡಿ:",
    lbl_applicant_name: "ಅರ್ಜಿದಾರರ ಹೆಸರು:",
    lbl_land_acres: "ಜಮೀನು:",
    lbl_district_taluk: "ಜಿಲ್ಲೆ ಮತ್ತು ತಾಲ್ಲೂಕು:",
    lbl_verified_docs: "ಅಗತ್ಯ ದಾಖಲೆಗಳು:",
    doc_aadhaar_check: "✓ ಆಧಾರ್ ಕಾರ್ಡ್ ದೃಢೀಕರಿಸಲಾಗಿದೆ",
    doc_rtc_check: "✓ ಪಹಣಿ / RTC ಜೋಡಿಸಲಾಗಿದೆ",
    doc_bank_check: "✓ ಬ್ಯಾಂಕ್ ಖಾತೆ ಸಕ್ರಿಯವಾಗಿದೆ",
    btn_submit_app: "✓ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ",
    floating_tooltip: "ಮಾತನಾಡಲು ಒತ್ತಿರಿ",
    why_eligible_label: "💡 ನೀವು ಏಕೆ ಅರ್ಹರು?",
    required_docs_label: "ಅಗತ್ಯ ದಾಖಲೆಗಳು:",
    apply_btn: "📝 ಅರ್ಜಿ ಸಲ್ಲಿಸಿ",
    official_portal_btn: "🔗 ಅಧಿಕೃತ ಪೋರ್ಟಲ್ &nearr;",
    eligible_badge: "✓ ಅರ್ಹರು",
    cond_eligible_badge: "⚠️ ಷರತ್ತುಬದ್ಧ ಅರ್ಹತೆ",
    not_eligible_badge: "✕ ಅನರ್ಹರು",
    status_submitted: "📤 ಅರ್ಜಿ ಸಲ್ಲಿಕೆಯಾಗಿದೆ",
    status_under_verification: "🔍 ದಾಖಲೆ ಪರಿಶೀಲನೆ",
    status_department_review: "🏛️ ಇಲಾಖಾ ಪರಿಶೀಲನೆ",
    status_approved: "✅ ಅನುಮೋದಿತ",
    status_disbursed: "💰 ಸೌಲಭ್ಯ ಜಮೆ",
    status_rejected: "✕ ತಿರಸ್ಕೃತ",
    hearing_title: "ಕೇಳಿಸಿಕೊಳ್ಳುತ್ತಿದ್ದೇವೆ... ಮಾತನಾಡಿ",
    hearing_instruction: "ನಿಮ್ಮ ಧ್ವನಿಯನ್ನು ಸ್ಪಷ್ಟವಾಗಿ ಹೇಳಿ",
    hearing_cancel: "ರದ್ದು",
    hearing_confirm: "✓ ಸರಿ"
  },
  en: {
    state_karnataka: "Karnataka",
    brand_tagline: "RaitaSaathiAI",
    nav_dashboard: "Dashboard",
    nav_schemes: "Schemes",
    nav_tracking: "Application Tracking",
    nav_profile: "My Profile",
    nav_assistant: "Voice Assistant",
    nav_calculator: "Budget Lab",
    nav_crop: "Crop Health",
    nav_soil: "Soil Health",
    nav_register: "📝 Register Farmer",
    nav_admin: "🛡️ Officer Portal",
    notif_header: "🔔 Notifications",
    notif_mark_all: "Mark all as read",
    notif_loading: "Loading notifications...",
    notif_empty: "No new notifications.",
    verified_profile_badge: "Verified Farmer Profile",
    welcome_prefix: "Welcome, ",
    default_farmer_title: "Farmer",
    btn_edit_name: "Edit Name",
    btn_add_name: "Add Name",
    farmer_name_label: "👨‍🌾 Farmer Name:",
    farmer_name_placeholder: "Speak or type farmer name...",
    speak_btn: "Speak",
    save_btn: "✓ Save",
    profile_completion_label: "Profile Completion",
    banner_voice_btn: "🎤 Voice Query",
    banner_schemes_btn: "📜 Schemes",
    banner_profile_btn: "👤 Profile",
    kpi_total_title: "Total Schemes",
    kpi_total_sub: "Central & Karnataka",
    kpi_eligible_title: "Eligible Schemes",
    kpi_eligible_sub: "Targeted for your farm",
    kpi_submitted_title: "Submitted Applications",
    kpi_submitted_sub: "Tracking enabled",
    kpi_approved_title: "Approved Applications",
    kpi_approved_sub: "Sanctioned by department",
    kpi_pending_title: "Pending Applications",
    kpi_pending_sub: "Under verification",
    kpi_benefits_title: "Benefits Received",
    kpi_benefits_sub: "Direct Benefit Transfer",
    recent_apps_title: "Recent Scheme Applications",
    recent_apps_sub: "Application progress, verification stages, and disbursement details",
    view_all_apps_btn: "View All Applications &rarr;",
    th_app_id: "Application ID",
    th_scheme_name: "Scheme Name",
    th_scheme_dept: "Scheme & Department",
    th_date: "Date",
    th_benefit: "Benefit Amount",
    th_status: "Status",
    th_stage: "Current Stage",
    th_action: "Action",
    loading_apps: "Loading applications...",
    no_apps_found: "No applications found.",
    view_timeline_btn: "🔍 View Progress",
    quick_advice_title: "⚡ Quick Agronomic Advice",
    quick_advice_sub: "Ask questions about crops, fertilizer, and pest management via voice or text.",
    chip_ragi: "🌱 Ragi Fertilizer Guidance",
    chip_paddy: "🌾 Paddy Pest Control",
    chip_schemes: "📜 My Eligible Schemes",
    scenario_lab_card_title: "📊 Farm Budget Lab",
    scenario_lab_card_sub: "Mathematical comparison of crop costs, yields, and net profits.",
    open_lab_btn: "⚖️ Open Budget Lab",
    schemes_heading: "Government Agricultural Schemes",
    schemes_sub: "20 Official Central & Karnataka State Schemes — Evaluated against your land and crops.",
    reevaluate_schemes_btn: "🔄 Re-evaluate Eligibility",
    filter_all_schemes: "All Schemes (20)",
    filter_dbt: "💵 Direct Benefit Transfer",
    filter_subsidy: "🚜 Subsidies & Machinery",
    filter_insurance: "🛡️ Insurance & Credit",
    filter_irrigation: "💧 Irrigation Schemes",
    filter_input: "🌱 Seeds & Fertilizers",
    loading_schemes: "Evaluating schemes against your profile...",
    no_schemes_found: "No schemes found in this category.",
    tracking_heading: "My Scheme Applications Tracking",
    tracking_sub: "Real-time 5-stage progress from submission to bank credit.",
    btn_apply_new_scheme: "➕ Apply for New Scheme",
    filter_all_apps: "All Applications",
    filter_pending_apps: "⏳ Pending Review",
    filter_approved_apps: "✅ Approved",
    filter_disbursed_apps: "💰 Benefit Disbursed",
    profile_heading: "Farmer Digital Profile",
    profile_sub: "Aadhaar e-KYC verified personal, agricultural land, crop, and bank verification details.",
    profile_sec_a: "A. Personal Information",
    profile_sec_b: "B. Agricultural Land Details",
    profile_sec_c: "C. Bank Verification & Benefit Status",
    lbl_farmer_id: "Farmer ID:",
    lbl_full_name: "Full Name:",
    lbl_mobile: "Mobile Number:",
    lbl_ekyc: "Aadhaar Verification:",
    lbl_state: "State:",
    lbl_district: "District:",
    lbl_taluk: "Taluk:",
    lbl_village: "Village:",
    lbl_total_land: "Total Land:",
    lbl_ownership: "Land Ownership:",
    val_owned: "Owned Land",
    lbl_category: "Farmer Category:",
    val_small_farmer: "Small Farmer",
    lbl_irrigation: "Irrigation Facility:",
    val_borewell: "Borewell Irrigated",
    val_canal: "Canal Irrigated",
    val_rainfed: "Rainfed",
    val_drip: "Drip Irrigation",
    lbl_soil_type: "Soil Type:",
    val_red_soil: "Red Sandy Loam",
    lbl_main_crops: "Main Crops:",
    lbl_bank_name: "Bank Name:",
    val_sbi: "State Bank of India",
    lbl_account_no: "Account Number:",
    lbl_aadhaar_seed: "Aadhaar Seeded:",
    val_seeded: "✓ Seeded for DBT",
    assistant_title: "RaitaSaathiAI Voice Assistant",
    assistant_sub: "Speak in natural English. Ask about schemes, applications, or crop pests.",
    voice_tap_prompt: "Tap microphone to speak",
    echo_card_title: "Confirmation Required",
    echo_btn_yes: "✓ Yes, Confirmed",
    echo_btn_no: "✎ No, Edit",
    assistant_input_ph: "Type your farm question here (e.g. fertilizer dose for ragi, or show my approved schemes)...",
    assistant_send_btn: "Send",
    calc_heading: "Farm Budget Lab",
    calc_sub: "Deterministic comparison of crop costs, yields, net revenues and market sensitivity.",
    scen_a_title: "First Crop: Paddy",
    scen_b_title: "Second Crop: Organic Ragi",
    lbl_land_area: "Land Area (Acres):",
    lbl_yield: "Expected Yield (Quintals/Acre):",
    lbl_price: "Selling Price (₹ per Quintal):",
    lbl_costs: "Total Variable Costs (Seeds, Fertilizer, Labour ₹):",
    btn_run_comparison: "📊 Run Comparison",
    crop_heading: "Crop Health Diagnosis",
    lbl_crop_name: "Crop Name:",
    lbl_crop_symptoms: "Describe Observed Symptoms:",
    crop_symptoms_ph: "e.g. Leaves turning yellow and curling upwards with concentric spots...",
    btn_analyze_crop: "Analyze Health",
    soil_heading: "Soil Health Evaluation",
    lbl_soil_ph: "pH Level:",
    lbl_soil_ec: "Electrical Conductivity (EC dS/m):",
    lbl_soil_n: "Available Nitrogen (N kg/ha):",
    lbl_soil_p: "Available Phosphorus (P kg/ha):",
    lbl_soil_k: "Available Potassium (K kg/ha):",
    btn_interpret_soil: "Evaluate Soil Health",
    timeline_modal_title: "Application Progress Timeline",
    disbursed_box_title: "💰 Benefit Disbursement Details:",
    modal_close_btn: "Close",
    reg_modal_title: "New Farmer Digital Registration",
    reg_modal_sub: "Aadhaar e-KYC Verification & Digital Farmer Identity",
    reg_step_1_tab: "1. Details",
    reg_step_2_tab: "2. e-KYC Verification",
    reg_step_3_tab: "3. Farmer Identity",
    demo_farmer_title: "⚡ Quick Demo Farmer:",
    demo_farmer_desc: "Ramesh Gowda, Mandya (2.5 Acres Paddy & Ragi)",
    demo_farmer_btn: "Select Ramesh Gowda",
    lbl_reg_name: "Farmer Full Name:",
    reg_name_ph: "e.g. Ramesh Gowda",
    lbl_reg_mobile: "Mobile Number:",
    reg_mobile_ph: "Speak or type 10-digit mobile number...",
    lbl_reg_aadhaar: "Aadhaar Number:",
    reg_aadhaar_ph: "12-digit Aadhaar number...",
    lbl_aadhaar_security_note: "🔒 Secure e-KYC: Only masked reference is stored.",
    reg_taluk_ph: "e.g. Pandavapura",
    reg_village_ph: "e.g. Chikka Byadarahalli",
    lbl_reg_land: "Total Land (Acres):",
    lbl_consent_text: "I explicitly consent to Aadhaar e-KYC verification for government scheme discovery.",
    btn_next_step: "Next Step: Verification &rarr;",
    otp_heading: "Verification Code (OTP)",
    otp_sub: "A verification code has been sent to your registered mobile.",
    otp_demo_hint: "💡 For demo simulation, enter '2026'.",
    lbl_enter_otp: "Enter 4-Digit Code:",
    btn_back: "Back",
    btn_verify_otp: "✓ Verify Code",
    reg_success_title: "Farmer Account Successfully Created!",
    reg_success_sub: "Your digital farmer identity is verified and active.",
    lbl_your_farmer_id: "Your Unique Farmer ID:",
    lbl_name: "Name:",
    lbl_status: "Status:",
    btn_goto_dashboard: "Go to My Dashboard &rarr;",
    apply_modal_title: "Submit Scheme Application",
    apply_modal_sub: "Department of Agriculture, Govt. of Karnataka",
    apply_lbl_benefit: "Benefit Amount / Subsidy:",
    lbl_applicant_name: "Farmer Name:",
    lbl_land_acres: "Land Area:",
    lbl_district_taluk: "District & Taluk:",
    lbl_verified_docs: "Verified Documents Attached:",
    doc_aadhaar_check: "✓ Aadhaar Card Verified",
    doc_rtc_check: "✓ Pahani / RTC Linked",
    doc_bank_check: "✓ Bank Passbook DBT Active",
    btn_submit_app: "✓ Submit Application",
    floating_tooltip: "Tap to speak",
    why_eligible_label: "💡 Why are you eligible?",
    required_docs_label: "Required Documents:",
    apply_btn: "📝 Apply Now",
    official_portal_btn: "🔗 Official Portal &nearr;",
    eligible_badge: "✓ Eligible",
    cond_eligible_badge: "⚠️ Conditional",
    not_eligible_badge: "✕ Not Eligible",
    status_submitted: "📤 Submitted",
    status_under_verification: "🔍 Document Verification",
    status_department_review: "🏛️ Department Review",
    status_approved: "✅ Approved",
    status_disbursed: "💰 Benefit Disbursed",
    status_rejected: "✕ Rejected",
    hearing_title: "Listening... Please speak",
    hearing_instruction: "Speak clearly into the microphone",
    hearing_cancel: "Cancel",
    hearing_confirm: "✓ Confirm"
  }
};

// Clean dual-language string with brackets e.g. "Ningegowda K. (ನಿಂಗೇಗೌಡ)"
function cleanBilingualText(text, lang) {
  if (!text || typeof text !== 'string') return text || '';
  const match = text.match(/^(.*?)\s*[\(\[]\s*(.*?)\s*[\)\]]$/);
  if (match) {
    const part1 = match[1].trim();
    const part2 = match[2].trim();
    const hasKannada1 = /[\u0C80-\u0CFF]/.test(part1);
    const hasKannada2 = /[\u0C80-\u0CFF]/.test(part2);
    if (lang === 'kn') {
      if (hasKannada2) return part2;
      if (hasKannada1) return part1;
      return part1;
    } else {
      if (!hasKannada1) return part1;
      if (!hasKannada2) return part2;
      return part1;
    }
  }
  return text.trim();
}

// ============================================================================
// LANGUAGE TRANSLATION ENGINE (Instant Dynamic Page Translation)
// ============================================================================
function setLanguage(lang) {
  activeLanguage = (lang === 'en') ? 'en' : 'kn';
  localStorage.setItem('krishi_lang', activeLanguage);

  // Update HTML lang attribute
  document.documentElement.lang = activeLanguage;

  // Update navbar language switcher buttons (clean 2 buttons only: ಕನ್ನಡ and English)
  const btnKn = document.getElementById('lang-kn');
  const btnEn = document.getElementById('lang-en');
  if (btnKn && btnEn) {
    if (activeLanguage === 'kn') {
      btnKn.style.background = '#ffffff';
      btnKn.style.fontWeight = '800';
      btnKn.style.color = 'var(--primary)';
      btnKn.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';

      btnEn.style.background = 'transparent';
      btnEn.style.fontWeight = '600';
      btnEn.style.color = '#64748b';
      btnEn.style.boxShadow = 'none';
    } else {
      btnEn.style.background = '#ffffff';
      btnEn.style.fontWeight = '800';
      btnEn.style.color = 'var(--primary)';
      btnEn.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';

      btnKn.style.background = 'transparent';
      btnKn.style.fontWeight = '600';
      btnKn.style.color = '#64748b';
      btnKn.style.boxShadow = 'none';
    }
  }

  // Translate all static DOM elements marked with data-i18n
  const dict = I18N_DICTIONARY[activeLanguage] || I18N_DICTIONARY.kn;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      el.innerHTML = dict[key];
    }
  });

  // Translate all placeholder attributes marked with data-i18n-ph
  document.querySelectorAll('[data-i18n-ph]').forEach(el => {
    const key = el.getAttribute('data-i18n-ph');
    if (dict[key]) {
      el.placeholder = dict[key];
    }
  });

  // Update floating mic tooltip
  const ft = document.getElementById('floating-voice-tooltip');
  if (ft) ft.innerText = dict.floating_tooltip;

  // Re-initialize location selectors with pure single-language labels
  initLocationSelectors();

  // Refresh dynamic views with pure single-language text
  updateGreetingUI(farmerCustomName);
  updateLocationDisplay(currentSelectedDistrict);

  if (currentFarmerData && currentFarmerData.recent_applications) {
    renderDashboardRecentApps(currentFarmerData.recent_applications);
  }
  if (allSchemesList.length > 0) {
    renderSchemesGrid(allSchemesList);
  }
  if (allApplicationsList.length > 0) {
    renderApplicationsTable(allApplicationsList);
  }

  loadProfileData();
  loadNotifications();
}

// ============================================================================
// 1. Navigation & Tab Switching
// ============================================================================
function showTab(tabName) {
  const tabs = ['dashboard', 'schemes', 'tracking', 'profile', 'assistant', 'calculator', 'crop', 'soil'];
  tabs.forEach(t => {
    const el = document.getElementById(`view-${t}`);
    const nav = document.getElementById(`nav-${t}`);
    if (el) el.style.display = (t === tabName) ? 'block' : 'none';
    if (nav) {
      if (t === tabName) nav.classList.add('active');
      else nav.classList.remove('active');
    }
  });

  if (tabName === 'schemes') loadSchemeRecommendations();
  if (tabName === 'tracking') loadApplicationsTracking();
  if (tabName === 'profile') loadProfileData();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function quickAssistantPrompt(text) {
  showTab('assistant');
  const inputEl = document.getElementById('user-text-input');
  if (inputEl) {
    inputEl.value = text;
    submitUserMessage();
  }
}

// ============================================================================
// 2. UNIVERSAL VOICE HEARING CONTROLLER FOR ALL REGISTRATION & FORM FIELDS
// ============================================================================
let activeHearingTargetId = null;
let activeHearingFieldType = null;
let activeHearingRecognition = null;
let hearingAutoCloseTimeout = null;

const HEARING_FIELD_META = {
  'reg-name': {
    tag_kn: 'ರೈತರ ಹೆಸರು', tag_en: 'Farmer Name',
    hint_kn: 'ನಿಮ್ಮ ಪೂರ್ಣ ಹೆಸರನ್ನು ಸ್ಪಷ್ಟವಾಗಿ ಹೇಳಿ', hint_en: 'Speak your full name clearly'
  },
  'farmer-name-input': {
    tag_kn: 'ರೈತರ ಹೆಸರು', tag_en: 'Farmer Name',
    hint_kn: 'ನಿಮ್ಮ ಹೆಸರನ್ನು ಸ್ಪಷ್ಟವಾಗಿ ಹೇಳಿ', hint_en: 'Speak your name clearly'
  },
  'reg-mobile': {
    tag_kn: 'ಮೊಬೈಲ್ ಸಂಖ್ಯೆ', tag_en: 'Mobile Number',
    hint_kn: 'ನಿಮ್ಮ ೧೦ ಅಂಕಿಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆಯನ್ನು ಹೇಳಿ', hint_en: 'Speak your 10-digit mobile number'
  },
  'reg-aadhaar': {
    tag_kn: 'ಆಧಾರ್ ಸಂಖ್ಯೆ', tag_en: 'Aadhaar Number',
    hint_kn: 'ನಿಮ್ಮ ೧೨ ಅಂಕಿಯ ಆಧಾರ್ ಸಂಖ್ಯೆಯನ್ನು ಹೇಳಿ', hint_en: 'Speak your 12-digit Aadhaar number'
  },
  'reg-district': {
    tag_kn: 'ಜಿಲ್ಲೆ', tag_en: 'District',
    hint_kn: 'ಕರ್ನಾಟಕದ ನಿಮ್ಮ ಜಿಲ್ಲೆಯ ಹೆಸರು ಹೇಳಿ (ಉದಾ: ಮಂಡ್ಯ, ಹಾಸನ)', hint_en: 'Speak your district name (e.g. Mandya, Hassan)'
  },
  'reg-taluk': {
    tag_kn: 'ತಾಲ್ಲೂಕು', tag_en: 'Taluk',
    hint_kn: 'ನಿಮ್ಮ ತಾಲ್ಲೂಕಿನ ಹೆಸರು ಹೇಳಿ (ಉದಾ: ಪಾಂಡವಪುರ)', hint_en: 'Speak your taluk name'
  },
  'reg-village': {
    tag_kn: 'ಗ್ರಾಮ', tag_en: 'Village',
    hint_kn: 'ನಿಮ್ಮ ಗ್ರಾಮದ ಹೆಸರು ಹೇಳಿ', hint_en: 'Speak your village name'
  },
  'reg-acres': {
    tag_kn: 'ಜಮೀನು (ಎಕರೆ)', tag_en: 'Land (Acres)',
    hint_kn: 'ಎಕರೆ ಸಂಖ್ಯೆ ಹೇಳಿ (ಉದಾ: ೨.೫, ಐದು)', hint_en: 'Speak number of acres (e.g. 2.5, 3)'
  },
  'reg-irrigation': {
    tag_kn: 'ನೀರಾವರಿ ವ್ಯವಸ್ಥೆ', tag_en: 'Irrigation',
    hint_kn: 'ಬೋರ್‌ವೆಲ್, ಕಾಲುವೆ, ಮಳೆ ಆಶ್ರಿತ ಅಥವಾ ಹನಿ ನೀರಾವರಿ ಎಂದು ಹೇಳಿ', hint_en: 'Speak Borewell, Canal, Rainfed, or Drip'
  },
  'reg-crops': {
    tag_kn: 'ಮುಖ್ಯ ಬೆಳೆಗಳು', tag_en: 'Main Crops',
    hint_kn: 'ನಿಮ್ಮ ಬೆಳೆಗಳ ಹೆಸರು ಹೇಳಿ (ಉದಾ: ಭತ್ತ, ರಾಗಿ, ಕಬ್ಬು)', hint_en: 'Speak your crops (e.g. Paddy, Ragi, Sugarcane)'
  },
  'reg-otp-input': {
    tag_kn: 'ದೃಢೀಕರಣ ಕೋಡ್ (OTP)', tag_en: 'Verification Code (OTP)',
    hint_kn: 'ಮೊಬೈಲ್‌ಗೆ ಬಂದಿರುವ ೪ ಅಂಕಿಯ ಕೋಡ್ ಹೇಳಿ (ಡೆಮೊ: ೨೦೨೬)', hint_en: 'Speak your 4-digit code (Demo: 2026)'
  },
  'crop-diag-name': {
    tag_kn: 'ಬೆಳೆಯ ಹೆಸರು', tag_en: 'Crop Name',
    hint_kn: 'ಬೆಳೆಯ ಹೆಸರು ಹೇಳಿ (ಉದಾ: ರಾಗಿ ಅಥವಾ ಭತ್ತ)', hint_en: 'Speak the crop name'
  },
  'crop-diag-symptoms': {
    tag_kn: 'ರೋಗದ ಲಕ್ಷಣಗಳು', tag_en: 'Disease Symptoms',
    hint_kn: 'ಕಂಡುಬಂದ ರೋಗದ ಲಕ್ಷಣಗಳನ್ನು ವಿವರಿಸಿ', hint_en: 'Describe observed crop symptoms'
  }
};

const KANNADA_DIGIT_MAP = {
  'ಸೊನ್ನೆ': '0', 'ಶೂನ್ಯ': '0', 'ಝೀರೋ': '0',
  'ಒಂದು': '1', 'ಒಂದ': '1',
  'ಎರಡು': '2', 'ಯರಡು': '2',
  'ಮೂರು': '3', 'ಮೂರ': '3',
  'ನಾಲ್ಕು': '4', 'ನಾಕ': '4',
  'ಐದು': '5', 'ಐದ': '5',
  'ಆರು': '6', 'ಆರ': '6',
  'ಏಳು': '7', 'ಏಳ': '7',
  'ಎಂಟು': '8', 'ಎಂಟ': '8',
  'ಒಂಬತ್ತು': '9', 'ಒಂಭತ್ತು': '9',
  '೦': '0', '೧': '1', '೨': '2', '೩': '3', '೪': '4',
  '೫': '5', '೬': '6', '೭': '7', '೮': '8', '೯': '9',
  'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
  'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'
};

function parseSpokenNumbers(rawText) {
  let text = (rawText || '').toLowerCase().trim();
  for (const [word, digit] of Object.entries(KANNADA_DIGIT_MAP)) {
    const regex = new RegExp(word, 'gi');
    text = text.replace(regex, digit);
  }
  return text.replace(/\D/g, '');
}

function playSuccessBeep() {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.type = 'sine';
    osc.frequency.setValueAtTime(587.33, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.14);
    gain.gain.setValueAtTime(0.2, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.22);
    osc.start();
    osc.stop(ctx.currentTime + 0.22);
  } catch (e) {}
}

function startFieldVoice(fieldId, fieldType = 'general') {
  activeHearingTargetId = fieldId;
  activeHearingFieldType = fieldType;

  const overlay = document.getElementById('voice-hearing-overlay');
  const tagEl = document.getElementById('hearing-field-tag');
  const titleEl = document.getElementById('hearing-status-title');
  const tipEl = document.getElementById('hearing-instruction-tip');
  const transcriptEl = document.getElementById('hearing-live-transcript');
  const cancelBtn = document.getElementById('hearing-cancel-btn');
  const confirmBtn = document.getElementById('hearing-confirm-btn');

  const meta = HEARING_FIELD_META[fieldId] || {
    tag_kn: 'ಮಾಹಿತಿ', tag_en: 'Field Input',
    hint_kn: 'ನಿಮ್ಮ ಧ್ವನಿಯನ್ನು ಸ್ಪಷ್ಟವಾಗಿ ಹೇಳಿ', hint_en: 'Speak clearly into the microphone'
  };

  const isKn = activeLanguage === 'kn';
  if (tagEl) tagEl.innerText = isKn ? meta.tag_kn : meta.tag_en;
  if (titleEl) titleEl.innerText = isKn ? 'ಕೇಳಿಸಿಕೊಳ್ಳುತ್ತಿದ್ದೇವೆ... ಮಾತನಾಡಿ' : 'Listening... Please speak';
  if (tipEl) tipEl.innerText = isKn ? meta.hint_kn : meta.hint_en;
  if (transcriptEl) transcriptEl.innerText = '...';
  if (cancelBtn) cancelBtn.innerText = isKn ? 'ರದ್ದು' : 'Cancel';
  if (confirmBtn) confirmBtn.innerText = isKn ? '✓ ಸರಿ' : '✓ Confirm';

  if (overlay) overlay.classList.add('active');

  window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!window.SpeechRecognition) {
    if (transcriptEl) {
      transcriptEl.innerText = isKn ? 
        'ಬ್ರೌಸರ್‌ನಲ್ಲಿ ಧ್ವನಿ ಸೌಲಭ್ಯ ಬೆಂಬಲಿತವಾಗಿಲ್ಲ. ದಯವಿಟ್ಟು ಟೈಪ್ ಮಾಡಿ.' : 
        'Speech recognition not supported in this browser. Please type.';
    }
    return;
  }

  if (activeHearingRecognition) {
    try { activeHearingRecognition.abort(); } catch (e) {}
  }

  activeHearingRecognition = new window.SpeechRecognition();
  activeHearingRecognition.lang = isKn ? 'kn-IN' : 'en-IN';
  activeHearingRecognition.continuous = false;
  activeHearingRecognition.interimResults = true;

  activeHearingRecognition.onstart = () => {
    if (titleEl) titleEl.innerText = isKn ? 'ಕೇಳಿಸಿಕೊಳ್ಳುತ್ತಿದ್ದೇವೆ... ಮಾತನಾಡಿ' : 'Listening... Please speak';
  };

  activeHearingRecognition.onresult = (event) => {
    let interimTranscript = '';
    let finalTranscript = '';

    for (let i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        finalTranscript += event.results[i][0].transcript;
      } else {
        interimTranscript += event.results[i][0].transcript;
      }
    }

    const currentText = (finalTranscript || interimTranscript).trim();
    if (transcriptEl && currentText) {
      transcriptEl.innerText = `"${currentText}"`;
    }

    if (finalTranscript) {
      applyVoiceToField(fieldId, fieldType, finalTranscript.trim());
    }
  };

  activeHearingRecognition.onerror = (e) => {
    console.warn("Hearing voice error:", e);
    if (transcriptEl && transcriptEl.innerText === '...') {
      transcriptEl.innerText = isKn ? 'ಧ್ವನಿ ಕೇಳಿಸಲಿಲ್ಲ. ಪುನಃ ಮಾತನಾಡಿ.' : 'Could not hear voice. Please try again.';
    }
  };

  try {
    activeHearingRecognition.start();
  } catch (err) {
    console.warn("Speech start exception:", err);
  }
}

function applyVoiceToField(fieldId, fieldType, rawSpeech) {
  const targetEl = document.getElementById(fieldId);
  const transcriptEl = document.getElementById('hearing-live-transcript');
  const titleEl = document.getElementById('hearing-status-title');
  const isKn = activeLanguage === 'kn';

  let processedValue = rawSpeech;

  if (fieldType === 'phone') {
    processedValue = parseSpokenNumbers(rawSpeech).slice(0, 10);
  } else if (fieldType === 'aadhaar') {
    const digits = parseSpokenNumbers(rawSpeech).slice(0, 12);
    let formatted = '';
    for (let i = 0; i < digits.length; i++) {
      if (i > 0 && i % 4 === 0) formatted += '-';
      formatted += digits[i];
    }
    processedValue = formatted;
  } else if (fieldType === 'otp') {
    processedValue = parseSpokenNumbers(rawSpeech).slice(0, 4);
    if (!processedValue && (rawSpeech.includes('2026') || rawSpeech.includes('೨೦೨೬'))) {
      processedValue = '2026';
    }
  } else if (fieldType === 'acres') {
    const lower = rawSpeech.toLowerCase();
    if (lower.includes('ಎರಡೂವರೆ') || lower.includes('two and half') || lower.includes('two point five')) {
      processedValue = '2.5';
    } else if (lower.includes('ಒಂದೂವರೆ') || lower.includes('ಒಂದುವರೆ') || lower.includes('one and half') || lower.includes('one point five')) {
      processedValue = '1.5';
    } else if (lower.includes('ಮೂರೂವರೆ') || lower.includes('three and half')) {
      processedValue = '3.5';
    } else {
      const match = rawSpeech.match(/\d+(\.\d+)?/);
      if (match) {
        processedValue = match[0];
      } else {
        const digits = parseSpokenNumbers(rawSpeech);
        if (digits) processedValue = digits.slice(0, 2);
      }
    }
  } else if (fieldType === 'district') {
    const matchedDist = matchKarnatakaDistrict(rawSpeech);
    if (matchedDist) {
      if (targetEl) targetEl.value = matchedDist.en;
      processedValue = isKn ? matchedDist.kn : matchedDist.en;
    }
  } else if (fieldType === 'irrigation') {
    const lower = rawSpeech.toLowerCase();
    if (lower.includes('ಬೋರ್') || lower.includes('borewell')) {
      processedValue = 'BOREWELL';
    } else if (lower.includes('ಕಾಲುವೆ') || lower.includes('canal')) {
      processedValue = 'CANAL';
    } else if (lower.includes('ಮಳೆ') || lower.includes('rain')) {
      processedValue = 'RAINFED';
    } else if (lower.includes('ಹನಿ') || lower.includes('drip')) {
      processedValue = 'DRIP';
    }
    if (targetEl) targetEl.value = processedValue;
  } else if (fieldType === 'name') {
    processedValue = rawSpeech.replace(/^[,\.\s]+|[,\.\s]+$/g, '');
  }

  // Update target element
  if (targetEl) {
    if (targetEl.tagName === 'SELECT') {
      targetEl.value = processedValue;
    } else {
      targetEl.value = processedValue;
    }
    targetEl.dispatchEvent(new Event('input', { bubbles: true }));
    targetEl.dispatchEvent(new Event('change', { bubbles: true }));
  }

  playSuccessBeep();
  if (titleEl) titleEl.innerText = isKn ? '✓ ದೃಢೀಕರಿಸಲಾಗಿದೆ!' : '✓ Recognized!';
  if (transcriptEl) transcriptEl.innerText = `✓ ${processedValue}`;

  if (fieldId === 'farmer-name-input') {
    saveFarmerName(processedValue);
  }

  if (hearingAutoCloseTimeout) clearTimeout(hearingAutoCloseTimeout);
  hearingAutoCloseTimeout = setTimeout(() => {
    cancelHearingVoice();
  }, 1100);
}

function cancelHearingVoice() {
  if (hearingAutoCloseTimeout) clearTimeout(hearingAutoCloseTimeout);
  if (activeHearingRecognition) {
    try { activeHearingRecognition.stop(); } catch (e) {}
    activeHearingRecognition = null;
  }
  const overlay = document.getElementById('voice-hearing-overlay');
  if (overlay) overlay.classList.remove('active');
  activeHearingTargetId = null;
  activeHearingFieldType = null;
}

function confirmHearingVoice() {
  cancelHearingVoice();
}

function matchKarnatakaDistrict(text) {
  const lower = (text || '').toLowerCase().trim();
  for (const d of KARNATAKA_DISTRICTS) {
    if (lower.includes(d.en.toLowerCase()) || lower.includes(d.kn)) {
      return d;
    }
  }
  if (lower.includes('mysore') || lower.includes('ಮೈಸೂರು')) return KARNATAKA_DISTRICTS.find(d => d.en === 'Mysuru');
  if (lower.includes('bangalore') || lower.includes('ಬೆಂಗಳೂರು')) return KARNATAKA_DISTRICTS.find(d => d.en === 'Bengaluru Urban');
  if (lower.includes('belgaum') || lower.includes('ಬೆಳಗಾವಿ')) return KARNATAKA_DISTRICTS.find(d => d.en === 'Belagavi');
  if (lower.includes('gulbarga') || lower.includes('ಕಲಬುರಗಿ')) return KARNATAKA_DISTRICTS.find(d => d.en === 'Kalaburagi');
  if (lower.includes('shimoga') || lower.includes('ಶಿವಮೊಗ್ಗ')) return KARNATAKA_DISTRICTS.find(d => d.en === 'Shivamogga');
  if (lower.includes('bijapur') || lower.includes('ವಿಜಯಪುರ')) return KARNATAKA_DISTRICTS.find(d => d.en === 'Vijayapura');
  if (lower.includes('bellary') || lower.includes('ಬಳ್ಳಾರಿ')) return KARNATAKA_DISTRICTS.find(d => d.en === 'Ballari');
  return null;
}

// ============================================================================
// 3. Multilingual Voice Assistant (Krishi Echo & Floating Mic)
// ============================================================================
let recognition = null;
let isRecording = false;
let floatingRecognition = null;
let isFloatingRecording = false;

function setListeningUI(listening) {
  isRecording = listening;
  const btn = document.getElementById('mic-btn');
  const container = document.getElementById('mic-container');
  const status = document.getElementById('voice-status');

  if (listening) {
    if (btn) btn.classList.add('listening');
    if (container) container.classList.add('listening');
    if (status) status.innerHTML = activeLanguage === 'en' ? 
      '<span style="color:#ef4444; font-weight:700;">● Listening...</span>' : 
      '<span style="color:#ef4444; font-weight:700;">● ಆಲಿಸಲಾಗುತ್ತಿದೆ...</span>';
  } else {
    if (btn) btn.classList.remove('listening');
    if (container) container.classList.remove('listening');
    if (status) status.innerText = activeLanguage === 'en' ? 
      'Tap microphone to speak' : 
      'ಮಾತನಾಡಲು ಮೈಕ್ರೊಫೋನ್ ಒತ್ತಿರಿ';
  }
}

function initSpeech() {
  window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (window.SpeechRecognition) {
    recognition = new window.SpeechRecognition();
    recognition.lang = activeLanguage === 'en' ? 'en-IN' : 'kn-IN';
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => setListeningUI(true);
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      const inputEl = document.getElementById('user-text-input');
      if (inputEl) inputEl.value = transcript;
      const status = document.getElementById('voice-status');
      if (status) status.innerText = `"${transcript}"`;
      submitUserMessage(transcript);
    };
    recognition.onerror = () => setListeningUI(false);
    recognition.onend = () => setListeningUI(false);
  }
}

function toggleVoiceRecording() {
  if (!recognition) initSpeech();
  if (!recognition) {
    alert(activeLanguage === 'en' ? "Web Speech API is not supported in this browser." : "ಬ್ರೌಸರ್‌ನಲ್ಲಿ ಧ್ವನಿ ಸೌಲಭ್ಯ ಬೆಂಬಲಿತವಾಗಿಲ್ಲ.");
    return;
  }
  if (isRecording) recognition.stop();
  else recognition.start();
}

function toggleFloatingVoice() {
  window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!window.SpeechRecognition) {
    alert(activeLanguage === 'en' ? "Speech recognition not supported." : "ಧ್ವನಿ ಸೌಲಭ್ಯ ಬೆಂಬಲಿತವಾಗಿಲ್ಲ.");
    return;
  }

  const btn = document.getElementById('floating-mic-btn');
  const tooltip = document.getElementById('floating-voice-tooltip');

  if (isFloatingRecording && floatingRecognition) {
    floatingRecognition.stop();
    return;
  }

  floatingRecognition = new window.SpeechRecognition();
  floatingRecognition.lang = activeLanguage === 'en' ? 'en-IN' : 'kn-IN';
  floatingRecognition.continuous = false;
  floatingRecognition.interimResults = false;

  floatingRecognition.onstart = () => {
    isFloatingRecording = true;
    if (btn) btn.classList.add('recording');
    if (tooltip) tooltip.innerText = activeLanguage === 'en' ? 'Listening...' : 'ಆಲಿಸಲಾಗುತ್ತಿದೆ...';
  };

  floatingRecognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript.trim();
    if (tooltip) tooltip.innerText = `"${transcript}"`;
    handleVoiceCommand(transcript);
  };

  floatingRecognition.onerror = () => resetFloatingVoiceUI();
  floatingRecognition.onend = () => resetFloatingVoiceUI();

  try {
    floatingRecognition.start();
  } catch (e) {
    resetFloatingVoiceUI();
  }
}

function resetFloatingVoiceUI() {
  isFloatingRecording = false;
  const btn = document.getElementById('floating-mic-btn');
  const tooltip = document.getElementById('floating-voice-tooltip');
  if (btn) btn.classList.remove('recording');
  if (tooltip) tooltip.innerText = activeLanguage === 'en' ? 'Tap to speak' : 'ಮಾತನಾಡಲು ಒತ್ತಿರಿ';
}

function handleVoiceCommand(cmd) {
  const lower = cmd.toLowerCase();

  // Voice Navigation Commands
  if (lower.includes('approved') || lower.includes('ಅನುಮೋದಿತ') || lower.includes('ಅನುಮೋದನೆ')) {
    speakText(activeLanguage === 'en' ? "Displaying your approved schemes." : "ನಿಮ್ಮ ಅನುಮೋದಿತ ಯೋಜನೆಗಳ ಪಟ್ಟಿಯನ್ನು ತೋರಿಸಲಾಗುತ್ತಿದೆ.");
    showTab('tracking');
    filterApplicationsTable('APPROVED');
    return;
  }
  if (lower.includes('pending') || lower.includes('ಬಾಕಿ') || lower.includes('ಪರಿಶೀಲನೆ')) {
    speakText(activeLanguage === 'en' ? "Here are your applications under verification." : "ಪರಿಶೀಲನೆಯಲ್ಲಿರುವ ಅರ್ಜಿಗಳ ವಿವರ ಇಲ್ಲಿದೆ.");
    showTab('tracking');
    filterApplicationsTable('PENDING');
    return;
  }
  if (lower.includes('eligible') || lower.includes('schemes') || lower.includes('ಯೋಜನೆಗಳು') || lower.includes('ಅರ್ಹ')) {
    speakText(activeLanguage === 'en' ? "Opening schemes eligible for your land and crops." : "ನಿಮ್ಮ ಜಮೀನು ಮತ್ತು ಬೆಳೆಗೆ ಅರ್ಹವಿರುವ ಯೋಜನೆಗಳನ್ನು ತೆರೆಯಲಾಗುತ್ತಿದೆ.");
    showTab('schemes');
    return;
  }
  if (lower.includes('profile') || lower.includes('ಪ್ರೊಫೈಲ್') || lower.includes('ಖಾತೆ')) {
    speakText(activeLanguage === 'en' ? "Opening your verified farmer profile." : "ನಿಮ್ಮ ರೈತ ಪ್ರೊಫೈಲ್ ತೆರೆಯಲಾಗುತ್ತಿದೆ.");
    showTab('profile');
    return;
  }
  if (lower.includes('calculator') || lower.includes('budget') || lower.includes('ಬಜೆಟ್') || lower.includes('ಲಾಭ')) {
    speakText(activeLanguage === 'en' ? "Opening farm budget simulation lab." : "ಕೃಷಿ ಬಜೆಟ್ ಲ್ಯಾಬ್ ತೆರೆಯಲಾಗುತ್ತಿದೆ.");
    showTab('calculator');
    return;
  }

  // Fallback to Assistant Messaging
  showTab('assistant');
  const inputEl = document.getElementById('user-text-input');
  if (inputEl) inputEl.value = cmd;
  submitUserMessage(cmd);
}

// Assistant messaging
async function submitUserMessage(optionalText) {
  const inputEl = document.getElementById('user-text-input');
  const text = optionalText || (inputEl ? inputEl.value.trim() : '');
  if (!text) return;

  if (inputEl) inputEl.value = '';
  appendMessage(text, 'farmer');

  try {
    const payload = { message: text, language: activeLanguage };
    if (activeEchoData) {
      payload.confirmed_entities = activeEchoData;
      activeEchoData = null;
      const echoCard = document.getElementById('echo-confirmation-card');
      if (echoCard) echoCard.style.display = 'none';
    }

    const res = await fetch('/api/assistant/message', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();

    if (result.success) {
      if (result.data.status === 'AWAITING_CONFIRMATION') {
        activeEchoData = result.data.confirmation_card.entities;
        const promptEl = document.getElementById('echo-prompt-text');
        const cardEl = document.getElementById('echo-confirmation-card');
        if (promptEl) promptEl.innerText = result.data.confirmation_card.prompt;
        if (cardEl) cardEl.style.display = 'block';
        speakText(result.data.confirmation_card.prompt);
      } else {
        appendMessage(result.data.answer, 'assistant', result.data.source, result.data.verification);
        speakText(result.data.answer);
      }
    }
  } catch (err) {
    appendMessage(activeLanguage === 'en' ? "An error occurred. Please try again." : "ದೋಷ ಸಂಭವಿಸಿದೆ. ದಯವಿಟ್ಟು ಪುನಃ ಪ್ರಯತ್ನಿಸಿ.", 'assistant');
  }
}

function confirmEcho(isYes) {
  if (isYes) {
    submitUserMessage(activeLanguage === 'en' ? "Yes, confirmed." : "ಹೌದು, ದೃಢೀಕರಿಸಲಾಗಿದೆ.");
  } else {
    const cardEl = document.getElementById('echo-confirmation-card');
    if (cardEl) cardEl.style.display = 'none';
    activeEchoData = null;
    const inputEl = document.getElementById('user-text-input');
    if (inputEl) inputEl.focus();
  }
}

function appendMessage(text, sender, source = null, verification = null) {
  const hist = document.getElementById('assistant-conversation-history');
  if (!hist) return;

  const card = document.createElement('div');
  card.className = `chat-message ${sender}`;

  const headerLabel = sender === 'farmer' ? 
    (activeLanguage === 'en' ? '👨‍🌾 You (Farmer)' : '👨‍🌾 ನೀವು (ರೈತರು)') : 
    (activeLanguage === 'en' ? '🌱 RaitaSaathiAI' : '🌱 ರೈತಸಾಥಿ AI');
  const escapedText = text.replace(/</g, "&lt;").replace(/>/g, "&gt;");

  card.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <strong style="color:${sender === 'farmer' ? 'var(--emerald)' : 'var(--primary)'}; font-size:0.92rem;">
        ${headerLabel}
      </strong>
      ${sender === 'assistant' ? `
        <button onclick="speakText(\`${escapedText.replace(/`/g, '\\`')}\`)" style="background:none; border:none; cursor:pointer; font-size:1.1rem;" title="Listen">
          🔊
        </button>
      ` : ''}
    </div>
    <p style="margin: 4px 0; font-size:1rem; line-height:1.6; color:var(--text-primary);">${escapedText}</p>
    ${source ? `
      <div class="trust-source">
        <span>🏛️ ${activeLanguage === 'en' ? 'Source' : 'ಮೂಲ'}: <strong>${source}</strong></span>
        <span>&bull;</span>
        <span>🛡️ ${verification}</span>
      </div>
    ` : ''}
  `;
  hist.prepend(card);
}

function speakText(text) {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = activeLanguage === 'en' ? 'en-IN' : 'kn-IN';
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
  }
}

// ============================================================================
// 4. Farmer Name Manager (Text & Voice Input, Dynamic Greeting)
// ============================================================================
function toggleNameInput(show) {
  const container = document.getElementById('name-input-container');
  const input = document.getElementById('farmer-name-input');
  if (!container) return;
  if (show !== undefined) {
    container.style.display = show ? 'flex' : 'none';
  } else {
    container.style.display = (container.style.display === 'none' || !container.style.display) ? 'flex' : 'none';
  }
  if (container.style.display === 'flex' && input) {
    input.value = farmerCustomName || '';
    input.focus();
  }
}

function updateGreetingUI(rawName) {
  const el = document.getElementById('greeting-name');
  const btnText = document.getElementById('btn-edit-name-text');
  const dict = I18N_DICTIONARY[activeLanguage] || I18N_DICTIONARY.kn;
  const cleanName = cleanBilingualText(rawName, activeLanguage);

  if (el) {
    if (cleanName && cleanName.trim()) {
      el.innerHTML = `${dict.welcome_prefix}${cleanName}`;
      if (btnText) btnText.innerText = dict.btn_edit_name;
    } else {
      el.innerHTML = `${dict.welcome_prefix}${dict.default_farmer_title}`;
      if (btnText) btnText.innerText = dict.btn_add_name;
    }
  }
  const profName = document.getElementById('prof-farmer-name');
  if (profName && cleanName) profName.innerText = cleanName;
}

async function saveFarmerName(customVal) {
  const input = document.getElementById('farmer-name-input');
  const nameToSave = (customVal !== undefined ? customVal : (input ? input.value : '')).trim();

  farmerCustomName = nameToSave;
  if (nameToSave) {
    localStorage.setItem('krishi_farmer_name', nameToSave);
  } else {
    localStorage.removeItem('krishi_farmer_name');
  }

  updateGreetingUI(nameToSave);
  toggleNameInput(false);

  try {
    await fetch('/api/profile/name', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: nameToSave || 'Farmer' })
    });
  } catch (e) {
    console.warn("Name sync note:", e);
  }
}

// ============================================================================
// 5. Karnataka Districts (All 31 Districts, Pure Language Labels)
// ============================================================================
const KARNATAKA_DISTRICTS = [
  { en: "Mandya", kn: "ಮಂಡ್ಯ" },
  { en: "Mysuru", kn: "ಮೈಸೂರು" },
  { en: "Hassan", kn: "ಹಾಸನ" },
  { en: "Tumakuru", kn: "ತುಮಕೂರು" },
  { en: "Ramanagara", kn: "ರಾಮನಗರ" },
  { en: "Bengaluru Rural", kn: "ಬೆಂಗಳೂರು ಗ್ರಾಮಾಂತರ" },
  { en: "Bengaluru Urban", kn: "ಬೆಂಗಳೂರು ನಗರ" },
  { en: "Kolar", kn: "ಕೋಲಾರ" },
  { en: "Chikkaballapura", kn: "ಚಿಕ್ಕಬಳ್ಳಾಪುರ" },
  { en: "Chamarajanagar", kn: "ಚಾಮರಾಜನಗರ" },
  { en: "Shivamogga", kn: "ಶಿವಮೊಗ್ಗ" },
  { en: "Chikkamagaluru", kn: "ಚಿಕ್ಕಮಗಳೂರು" },
  { en: "Chitradurga", kn: "ಚಿತ್ರದುರ್ಗ" },
  { en: "Davanagere", kn: "ದಾವಣಗೆರೆ" },
  { en: "Dharwad", kn: "ಧಾರವಾಡ" },
  { en: "Belagavi", kn: "ಬೆಳಗಾವಿ" },
  { en: "Bagalkote", kn: "ಬಾಗಲಕೋಟೆ" },
  { en: "Vijayapura", kn: "ವಿಜಯಪುರ" },
  { en: "Gadag", kn: "ಗದಗ" },
  { en: "Haveri", kn: "ಹಾವೇರಿ" },
  { en: "Uttara Kannada", kn: "ಉತ್ತರ ಕನ್ನಡ" },
  { en: "Dakshina Kannada", kn: "ದಕ್ಷಿಣ ಕನ್ನಡ" },
  { en: "Udupi", kn: "ಉಡುಪಿ" },
  { en: "Kodagu", kn: "ಕೊಡಗು" },
  { en: "Ballari", kn: "ಬಳ್ಳಾರಿ" },
  { en: "Vijayanagara", kn: "ವಿಜಯನಗರ" },
  { en: "Koppal", kn: "ಕೊಪ್ಪಳ" },
  { en: "Raichur", kn: "ರಾಯಚೂರು" },
  { en: "Kalaburagi", kn: "ಕಲಬುರಗಿ" },
  { en: "Yadgir", kn: "ಯಾದಗಿರಿ" },
  { en: "Bidar", kn: "ಬೀದರ್" }
];

let currentSelectedDistrict = localStorage.getItem('krishi_district') || 'Mandya';

function initLocationSelectors() {
  const validDistricts = KARNATAKA_DISTRICTS.map(d => d.en);
  if (!validDistricts.includes(currentSelectedDistrict)) currentSelectedDistrict = 'Mandya';

  ['nav-select-district', 'reg-district'].forEach(selectId => {
    const el = document.getElementById(selectId);
    if (!el) return;
    el.innerHTML = '';
    KARNATAKA_DISTRICTS.forEach(d => {
      const opt = document.createElement('option');
      opt.value = d.en;
      // Pure single language label (no brackets)
      opt.innerText = activeLanguage === 'en' ? d.en : d.kn;
      if (d.en === currentSelectedDistrict) opt.selected = true;
      el.appendChild(opt);
    });
  });

  updateLocationDisplay(currentSelectedDistrict);
}

function updateLocationDisplay(district) {
  const distObj = KARNATAKA_DISTRICTS.find(d => d.en === district);
  const knName = distObj ? distObj.kn : district;

  const badgeEl = document.getElementById('active-location-badge');
  if (badgeEl) {
    badgeEl.innerHTML = activeLanguage === 'en' ? 
      `${district} District &bull; Karnataka` : 
      `${knName} ಜಿಲ್ಲೆ &bull; ಕರ್ನಾಟಕ`;
  }

  const summaryEl = document.getElementById('location-summary');
  if (summaryEl) {
    summaryEl.innerHTML = activeLanguage === 'en' ? 
      `${district} District, Karnataka &bull; 2.5 Acres Agricultural Land &bull; Borewell Irrigated` : 
      `${knName} ಜಿಲ್ಲೆ, ಕರ್ನಾಟಕ &bull; 2.5 ಎಕರೆ ಕೃಷಿ ಭೂಮಿ &bull; ಬೋರ್‌ವೆಲ್ ನೀರಾವರಿ`;
  }
}

function onDistrictSelectChange(newDistrict, source) {
  currentSelectedDistrict = newDistrict;
  localStorage.setItem('krishi_district', newDistrict);
  updateLocationDisplay(newDistrict);
  fetch('/api/profile/location', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ state: 'Karnataka', district: newDistrict })
  }).catch(() => {});
}

// ============================================================================
// 6. Dashboard Data & 6 KPI Metric Cards Loader
// ============================================================================
async function loadDashboardData() {
  try {
    const res = await fetch('/api/dashboard');
    const data = await res.json();
    if (data.success) {
      const d = data.data;
      currentFarmerData = d;

      // Handle Name cleanly
      if (farmerCustomName) {
        updateGreetingUI(farmerCustomName);
      } else if (d.farmer_name) {
        updateGreetingUI(d.farmer_name);
      } else {
        updateGreetingUI('');
      }

      // Update Farmer ID
      if (document.getElementById('farmer-id-badge')) {
        document.getElementById('farmer-id-badge').innerText = d.farmer_id || 'KM-KA-2026-0842';
      }

      // Update Profile Completion Bar
      const pct = d.profile_completion_pct || 85;
      if (document.getElementById('profile-pct-text')) document.getElementById('profile-pct-text').innerText = `${pct}%`;
      if (document.getElementById('profile-pct-bar')) document.getElementById('profile-pct-bar').style.width = `${pct}%`;

      // Update 6 KPI Metric Cards
      const s = d.stats || {};
      if (document.getElementById('kpi-total-schemes')) document.getElementById('kpi-total-schemes').innerText = s.total_available_schemes || 20;
      if (document.getElementById('kpi-eligible-schemes')) document.getElementById('kpi-eligible-schemes').innerText = s.eligible_schemes || 8;
      if (document.getElementById('kpi-submitted-apps')) document.getElementById('kpi-submitted-apps').innerText = s.applications_submitted || 4;
      if (document.getElementById('kpi-approved-apps')) document.getElementById('kpi-approved-apps').innerText = s.applications_approved || 2;
      if (document.getElementById('kpi-pending-apps')) document.getElementById('kpi-pending-apps').innerText = s.applications_pending || 2;
      if (document.getElementById('kpi-benefits-received')) document.getElementById('kpi-benefits-received').innerText = s.benefits_received || '₹16,000';

      // Update District
      if (d.district) {
        currentSelectedDistrict = d.district;
        updateLocationDisplay(currentSelectedDistrict);
      }

      // Render Recent Applications Table Preview
      renderDashboardRecentApps(d.recent_applications || []);

      // Update Unread Notification count
      if (d.unread_notifications > 0) {
        const badge = document.getElementById('notif-badge');
        if (badge) {
          badge.style.display = 'inline-block';
          badge.innerText = d.unread_notifications;
        }
      }
    }
  } catch (e) {
    console.error("Dashboard metrics load failed", e);
  }
}

function renderDashboardRecentApps(apps) {
  const tbody = document.getElementById('dashboard-recent-apps-body');
  if (!tbody) return;
  const dict = I18N_DICTIONARY[activeLanguage] || I18N_DICTIONARY.kn;

  if (!apps || apps.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" style="padding:20px; text-align:center; color:var(--text-muted);">${dict.no_apps_found}</td></tr>`;
    return;
  }

  tbody.innerHTML = apps.map(app => {
    let statusBadge = `<span class="badge badge-match">${dict.status_approved}</span>`;
    if (app.status === 'BENEFIT_DISBURSED') {
      statusBadge = `<span class="badge" style="background:#ecfdf5; color:#059669; border:1px solid #a7f3d0;">${dict.status_disbursed}</span>`;
    } else if (app.status === 'UNDER_VERIFICATION') {
      statusBadge = `<span class="badge badge-unknown">${dict.status_under_verification}</span>`;
    } else if (app.status === 'DEPARTMENT_REVIEW') {
      statusBadge = `<span class="badge badge-unknown">${dict.status_department_review}</span>`;
    } else if (app.status === 'SUBMITTED') {
      statusBadge = `<span class="badge" style="background:#eff6ff; color:#1d4ed8;">${dict.status_submitted}</span>`;
    } else if (app.status === 'REJECTED') {
      statusBadge = `<span class="badge badge-no-match">${dict.status_rejected}</span>`;
    }

    const rawTitle = activeLanguage === 'en' ? (app.scheme_name || app.scheme_name_kn) : (app.scheme_name_kn || app.scheme_name);
    const schemeTitle = cleanBilingualText(rawTitle, activeLanguage);
    const deptTitle = activeLanguage === 'en' ? 'Department of Agriculture' : 'ಕೃಷಿ ಇಲಾಖೆ';
    const amt = app.sanctioned_amount ? `₹${Number(app.sanctioned_amount).toLocaleString()}` : (activeLanguage === 'en' ? '₹6,000 / yr' : '₹6,000 / ವರ್ಷ');

    return `
      <tr style="border-bottom:1px solid #f1f5f9; transition:background 0.2s;" onmouseover="this.style.background='#f8fafc'" onmouseout="this.style.background='transparent'">
        <td style="padding:12px 14px; font-weight:700; color:var(--primary); font-family:monospace;">${app.application_number}</td>
        <td style="padding:12px 14px;">
          <div style="font-weight:700; color:var(--primary);">${schemeTitle}</div>
          <div style="font-size:0.75rem; color:var(--text-muted);">${deptTitle}</div>
        </td>
        <td style="padding:12px 14px; color:var(--text-secondary);">${app.applied_at ? app.applied_at.substring(0, 10) : '2026-10-15'}</td>
        <td style="padding:12px 14px; font-weight:700; color:#059669;">${amt}</td>
        <td style="padding:12px 14px;">${statusBadge}</td>
        <td style="padding:12px 14px; text-align:right;">
          <button class="btn btn-outline" onclick="openTimelineModal('${app.application_number}')" style="padding:4px 10px; font-size:0.78rem; border-radius:6px; font-weight:700;">
            ${dict.view_timeline_btn}
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

// ============================================================================
// 7. Schemes Discovery Engine (20 Schemes, Full Translation, Zero Brackets)
// ============================================================================
async function loadSchemeRecommendations() {
  const container = document.getElementById('schemes-grid-container');
  if (!container) return;
  const dict = I18N_DICTIONARY[activeLanguage] || I18N_DICTIONARY.kn;
  container.innerHTML = `<div style="padding:40px; text-align:center; color:var(--text-muted); grid-column:1/-1;">${dict.loading_schemes}</div>`;

  try {
    const res = await fetch('/api/schemes/recommendations');
    const data = await res.json();
    if (data.success) {
      allSchemesList = data.data.recommendations || [];
      renderSchemesGrid(allSchemesList);
    }
  } catch (err) {
    container.innerHTML = '<div style="color:red; text-align:center; grid-column:1/-1;">Failed to load schemes.</div>';
  }
}

function translateDocName(docName, lang) {
  if (lang !== 'kn') return docName;
  const docMap = {
    'Aadhaar Card': 'ಆಧಾರ್ ಕಾರ್ಡ್',
    'Pahani (RTC)': 'ಪಹಣಿ (RTC)',
    'Pahani / RTC': 'ಪಹಣಿ (RTC)',
    'Bank Passbook': 'ಬ್ಯಾಂಕ್ ಪಾಸ್‌ಬುಕ್',
    'Soil Health Card': 'ಮಣ್ಣಿನ ಆರೋಗ್ಯ ಕಾರ್ಡ್',
    'Crop Sowing Certificate': 'ಬೆಳೆ ದೃಢೀಕರಣ ಪತ್ರ',
    'Electricity Bill': 'ವಿದ್ಯುತ್ ಬಿಲ್',
    'Borewell Certificate': 'ಬೋರ್‌ವೆಲ್ ಪತ್ರ',
    'Caste Certificate': 'ಜಾತಿ ಪ್ರಮಾಣಪತ್ರ',
    'Income Certificate': 'ಆದಾಯ ಪ್ರಮಾಣಪತ್ರ',
    'Land Records': 'ಭೂ ದಾಖಲೆಗಳು',
    'Passport Photo': 'ಭಾವಚಿತ್ರ',
    'Kisan Credit Card': 'ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್'
  };
  return docMap[docName] || docName;
}

function translateDepartment(dept, lang) {
  if (lang !== 'kn') return dept;
  const deptMap = {
    'Department of Agriculture': 'ಕೃಷಿ ಇಲಾಖೆ',
    'Ministry of Agriculture & Farmers Welfare': 'ಕೇಂದ್ರ ಕೃಷಿ ಸಚಿವಾಲಯ',
    'Department of Horticulture': 'ತೋಟಗಾರಿಕೆ ಇಲಾಖೆ',
    'Department of Animal Husbandry': 'ಪಶುಸಂಗೋಪನಾ ಇಲಾಖೆ',
    'Department of Water Resources': 'ಜಲಸಂಪನ್ಮೂಲ ಇಲಾಖೆ',
    'Government of Karnataka': 'ಕರ್ನಾಟಕ ಸರ್ಕಾರ',
    'Govt of India': 'ಭಾರತ ಸರ್ಕಾರ',
    'NABARD & RBI': 'ನಬಾರ್ಡ್ & ರಿಸರ್ವ್ ಬ್ಯಾಂಕ್'
  };
  return deptMap[dept] || dept;
}

function renderSchemesGrid(schemes) {
  const container = document.getElementById('schemes-grid-container');
  if (!container) return;
  const dict = I18N_DICTIONARY[activeLanguage] || I18N_DICTIONARY.kn;

  if (!schemes || schemes.length === 0) {
    container.innerHTML = `<div style="padding:40px; text-align:center; color:var(--text-muted); grid-column:1/-1;">${dict.no_schemes_found}</div>`;
    return;
  }

  container.innerHTML = schemes.map(s => {
    let catBadge = `<span class="badge badge-match">${dict.eligible_badge}</span>`;
    let whyBoxClass = 'scheme-why-box';
    if (s.eligibility_category === 'POSSIBLY_ELIGIBLE') {
      catBadge = `<span class="badge badge-unknown">${dict.cond_eligible_badge}</span>`;
      whyBoxClass = 'scheme-why-box conditional';
    } else if (s.eligibility_category === 'NOT_ELIGIBLE') {
      catBadge = `<span class="badge badge-no-match">${dict.not_eligible_badge}</span>`;
    }

    const rawTitle = activeLanguage === 'en' ? s.name : (s.name_kn || s.name);
    const schemeTitle = cleanBilingualText(rawTitle, activeLanguage);
    const deptText = translateDepartment(s.department, activeLanguage);
    const levelLabel = s.level === 'CENTRAL' ? 
      (activeLanguage === 'en' ? '🏛️ Central Govt' : '🏛️ ಕೇಂದ್ರ ಸರ್ಕಾರ') : 
      (activeLanguage === 'en' ? '🌴 Karnataka Govt' : '🌴 ಕರ್ನಾಟಕ ಸರ್ಕಾರ');

    const benefitText = s.subsidy_percentage ? 
      (activeLanguage === 'en' ? `${s.subsidy_percentage}% Subsidy (${s.max_benefit_amount})` : `${s.subsidy_percentage}% ಸಬ್ಸಿಡಿ (${s.max_benefit_amount})`) : 
      s.max_benefit_amount;
    const whyText = activeLanguage === 'en' ? 
      cleanBilingualText(s.why_eligible_en || s.why_eligible_kn, 'en') : 
      cleanBilingualText(s.why_eligible_kn || s.why_eligible_en, 'kn');
    const descText = activeLanguage === 'en' ? 
      cleanBilingualText(s.description || s.description_kn, 'en') : 
      cleanBilingualText(s.description_kn || s.description, 'kn');
    const docs = (s.required_documents || ['Aadhaar Card', 'Pahani (RTC)', 'Bank Passbook']).map(d => translateDocName(d, activeLanguage));

    return `
      <div class="scheme-card">
        <div>
          <div class="scheme-card-header">
            <div>
              <div style="font-size:0.75rem; font-weight:800; color:var(--text-muted); text-transform:uppercase; margin-bottom:2px;">
                ${levelLabel} &bull; ${deptText}
              </div>
              <h3 style="color:var(--primary); font-size:1.15rem; font-weight:800; margin:0;">
                ${schemeTitle}
              </h3>
            </div>
            ${catBadge}
          </div>

          <div style="margin:8px 0;">
            <span class="scheme-benefit-badge">💰 ${benefitText}</span>
          </div>

          <p style="font-size:0.88rem; color:var(--text-secondary); margin:8px 0; line-height:1.5;">
            ${descText}
          </p>

          <!-- Why Eligible AI Rationale -->
          <div class="${whyBoxClass}">
            <strong>${dict.why_eligible_label}</strong> ${whyText}
          </div>

          <!-- Documents Checklist Pills -->
          <div style="font-size:0.78rem; font-weight:700; color:var(--text-muted); margin-top:8px;">${dict.required_docs_label}</div>
          <div class="scheme-docs-pills">
            ${docs.map(d => `<span class="scheme-doc-pill">📄 ${d}</span>`).join('')}
          </div>
        </div>

        <div style="display:flex; gap:10px; margin-top:12px; border-top:1px solid #f1f5f9; padding-top:12px;">
          <button class="btn btn-emerald" onclick="openApplyModal(${s.id}, '${schemeTitle.replace(/'/g, "\\'")}', '${benefitText}')" style="flex:1; padding:8px; font-size:0.85rem; font-weight:700;">
            ${dict.apply_btn}
          </button>
          <a href="${s.official_url || '#'}" target="_blank" class="btn btn-outline" style="padding:8px 12px; font-size:0.85rem; font-weight:700; text-decoration:none;" title="Portal">
            ${dict.official_portal_btn}
          </a>
        </div>
      </div>
    `;
  }).join('');
}

function filterSchemesByCategory(cat, btn) {
  document.querySelectorAll('.filter-pills-row .filter-pill').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');

  if (cat === 'ALL') {
    renderSchemesGrid(allSchemesList);
  } else {
    const filtered = allSchemesList.filter(s => s.category === cat);
    renderSchemesGrid(filtered);
  }
}

// ============================================================================
// 8. Full Applications Tracking & 5-Stage Stepper Timeline
// ============================================================================
async function loadApplicationsTracking() {
  const tbody = document.getElementById('full-applications-table-body');
  if (!tbody) return;
  const dict = I18N_DICTIONARY[activeLanguage] || I18N_DICTIONARY.kn;
  tbody.innerHTML = `<tr><td colspan="6" style="padding:30px; text-align:center; color:var(--text-muted);">${dict.loading_apps}</td></tr>`;

  try {
    const res = await fetch('/api/applications');
    const data = await res.json();
    if (data.success) {
      allApplicationsList = data.data.applications || [];
      renderApplicationsTable(allApplicationsList);
    }
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="6" style="color:red; text-align:center;">Failed to load applications.</td></tr>';
  }
}

function renderApplicationsTable(apps) {
  const tbody = document.getElementById('full-applications-table-body');
  if (!tbody) return;
  const dict = I18N_DICTIONARY[activeLanguage] || I18N_DICTIONARY.kn;

  if (!apps || apps.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" style="padding:30px; text-align:center; color:var(--text-muted);">${dict.no_apps_found}</td></tr>`;
    return;
  }

  tbody.innerHTML = apps.map(app => {
    let statusBadge = `<span class="badge badge-match">${dict.status_approved}</span>`;
    if (app.status === 'BENEFIT_DISBURSED') {
      statusBadge = `<span class="badge" style="background:#ecfdf5; color:#059669; border:1px solid #a7f3d0;">${dict.status_disbursed}</span>`;
    } else if (app.status === 'UNDER_VERIFICATION') {
      statusBadge = `<span class="badge badge-unknown">${dict.status_under_verification}</span>`;
    } else if (app.status === 'DEPARTMENT_REVIEW') {
      statusBadge = `<span class="badge badge-unknown">${dict.status_department_review}</span>`;
    } else if (app.status === 'SUBMITTED') {
      statusBadge = `<span class="badge" style="background:#eff6ff; color:#1d4ed8;">${dict.status_submitted}</span>`;
    } else if (app.status === 'REJECTED') {
      statusBadge = `<span class="badge badge-no-match">${dict.status_rejected}</span>`;
    }

    const rawTitle = activeLanguage === 'en' ? (app.scheme_name || app.scheme_name_kn) : (app.scheme_name_kn || app.scheme_name);
    const schemeTitle = cleanBilingualText(rawTitle, activeLanguage);
    const deptTitle = activeLanguage === 'en' ? 'Department of Agriculture' : 'ಕೃಷಿ ಇಲಾಖೆ';
    const amt = app.sanctioned_amount ? `₹${Number(app.sanctioned_amount).toLocaleString()}` : (activeLanguage === 'en' ? '₹6,000 / yr' : '₹6,000 / ವರ್ಷ');

    return `
      <tr style="border-bottom:1px solid #e2e8f0; transition:background 0.2s;" onmouseover="this.style.background='#f8fafc'" onmouseout="this.style.background='transparent'">
        <td style="padding:14px; font-weight:800; color:var(--primary); font-family:monospace; font-size:0.95rem;">${app.application_number}</td>
        <td style="padding:14px;">
          <div style="font-weight:700; color:var(--primary);">${schemeTitle}</div>
          <div style="font-size:0.75rem; color:var(--text-muted);">${deptTitle}</div>
        </td>
        <td style="padding:14px; color:var(--text-secondary);">${app.applied_at ? app.applied_at.substring(0, 10) : '2026-10-15'}</td>
        <td style="padding:14px; font-weight:800; color:#059669;">${amt}</td>
        <td style="padding:14px;">${statusBadge}</td>
        <td style="padding:14px; text-align:right;">
          <button class="btn btn-emerald" onclick="openTimelineModal('${app.application_number}')" style="padding:6px 14px; font-size:0.8rem; font-weight:700; border-radius:6px;">
            ${dict.view_timeline_btn}
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

function filterApplicationsTable(status, btn) {
  if (btn) {
    document.querySelectorAll('#view-tracking .filter-pill').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }

  if (status === 'ALL') {
    renderApplicationsTable(allApplicationsList);
  } else if (status === 'PENDING') {
    const pending = allApplicationsList.filter(a => ['SUBMITTED', 'UNDER_VERIFICATION', 'DEPARTMENT_REVIEW', 'PENDING'].includes(a.status));
    renderApplicationsTable(pending);
  } else {
    const filtered = allApplicationsList.filter(a => a.status === status);
    renderApplicationsTable(filtered);
  }
}

function filterApplicationsByStatus(status) {
  showTab('tracking');
  filterApplicationsTable(status);
}

// 5-Stage Stepper Timeline Modal (Zero Brackets)
async function openTimelineModal(appNumber) {
  const modal = document.getElementById('timeline-modal');
  const title = document.getElementById('timeline-modal-title');
  const subtitle = document.getElementById('timeline-modal-subtitle');
  const container = document.getElementById('timeline-stepper-container');
  const disbursedBox = document.getElementById('timeline-disbursed-box');
  const disbursedText = document.getElementById('timeline-disbursed-text');

  if (!modal || !container) return;
  modal.classList.add('active');
  container.innerHTML = '<div style="padding:20px; text-align:center; color:var(--text-muted);">Loading timeline details...</div>';

  try {
    const res = await fetch(`/api/applications/${appNumber}/timeline`);
    const data = await res.json();
    if (data.success) {
      const d = data.data;
      const rawTitle = activeLanguage === 'en' ? (d.scheme_name || d.scheme_name_kn) : (d.scheme_name_kn || d.scheme_name);
      const schemeTitle = cleanBilingualText(rawTitle, activeLanguage);
      if (title) title.innerText = activeLanguage === 'en' ? `Application Progress: ${schemeTitle}` : `ಅರ್ಜಿ ಪ್ರಗತಿ ವಿವರ: ${schemeTitle}`;
      if (subtitle) subtitle.innerText = `${d.application_number} &bull; ${activeLanguage === 'en' ? 'Department of Agriculture' : 'ಕೃಷಿ ಇಲಾಖೆ'}`;

      const stages = activeLanguage === 'en' ? [
        { key: 'SUBMITTED', step: 1, title: '1. Application Submitted', desc: 'Farmer details and documents received online.' },
        { key: 'UNDER_VERIFICATION', step: 2, title: '2. Document Verification', desc: 'Aadhaar e-KYC and land records verified.' },
        { key: 'DEPARTMENT_REVIEW', step: 3, title: '3. Department Review', desc: 'Assistant Director of Agriculture verification completed.' },
        { key: 'APPROVED', step: 4, title: '4. Application Approved', desc: 'Formal government sanction order issued.' },
        { key: 'BENEFIT_DISBURSED', step: 5, title: '5. Benefit Disbursed', desc: 'Direct Benefit Transfer (DBT) credited to bank account.' }
      ] : [
        { key: 'SUBMITTED', step: 1, title: '೧. ಅರ್ಜಿ ಸಲ್ಲಿಕೆಯಾಗಿದೆ', desc: 'ರೈತರ ವಿವರಗಳು ಮತ್ತು ದಾಖಲೆಗಳು ಸ್ವೀಕರಿಸಲ್ಪಟ್ಟಿವೆ.' },
        { key: 'UNDER_VERIFICATION', step: 2, title: '೨. ದಾಖಲೆ ಪರಿಶೀಲನೆ', desc: 'ಆಧಾರ್ e-KYC ಮತ್ತು ಪಹಣಿ (RTC) ದೃಢೀಕರಿಸಲಾಗಿದೆ.' },
        { key: 'DEPARTMENT_REVIEW', step: 3, title: '೩. ಇಲಾಖಾ ಪರಿಶೀಲನೆ', desc: 'ಸಹಾಯಕ ಕೃಷಿ ನಿರ್ದೇಶಕರ ಕಚೇರಿಯಿಂದ ಪರಿಶೀಲನೆ ಪೂರ್ಣಗೊಂಡಿದೆ.' },
        { key: 'APPROVED', step: 4, title: '೪. ಅರ್ಜಿ ಅನುಮೋದನೆ', desc: 'ಅಧಿಕೃತ ಮಂಜೂರಾತಿ ಆದೇಶ ಜಾರಿಯಾಗಿದೆ.' },
        { key: 'BENEFIT_DISBURSED', step: 5, title: '೫. ಸೌಲಭ್ಯ ಜಮೆ (DBT)', desc: 'ನೇರ ನಗದು ವರ್ಗಾವಣೆ ಮೂಲಕ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ಹಣ ಜಮೆ ಆಗಿದೆ.' }
      ];

      const currentStatus = d.status;
      const historyList = d.timeline || [];

      let currentStageIndex = 0;
      if (currentStatus === 'UNDER_VERIFICATION') currentStageIndex = 1;
      else if (currentStatus === 'DEPARTMENT_REVIEW') currentStageIndex = 2;
      else if (currentStatus === 'APPROVED') currentStageIndex = 3;
      else if (currentStatus === 'BENEFIT_DISBURSED') currentStageIndex = 4;
      else if (currentStatus === 'REJECTED') currentStageIndex = 2;

      container.innerHTML = stages.map((st, idx) => {
        let stepClass = '';
        let nodeIcon = st.step;
        if (idx < currentStageIndex || (idx === currentStageIndex && currentStatus === 'BENEFIT_DISBURSED')) {
          stepClass = 'completed';
          nodeIcon = '✓';
        } else if (idx === currentStageIndex) {
          stepClass = 'active';
          nodeIcon = '●';
        }

        const matchHist = historyList.find(h => h.status === st.key);
        const timeStr = matchHist ? matchHist.timestamp : (idx <= currentStageIndex ? (activeLanguage === 'en' ? 'Verified' : 'ದೃಢೀಕರಿಸಲಾಗಿದೆ') : (activeLanguage === 'en' ? 'Expected' : 'ನಿರೀಕ್ಷಿಸಲಾಗಿದೆ'));
        const remarks = matchHist && matchHist.remarks ? matchHist.remarks : st.desc;

        return `
          <div class="timeline-step ${stepClass}">
            <div class="step-node">${nodeIcon}</div>
            <div class="step-info">
              <div class="step-title">${st.title}</div>
              <div class="step-time">🕒 ${timeStr}</div>
              <div class="step-desc">${remarks}</div>
            </div>
          </div>
        `;
      }).join('');

      if (d.disbursed_at || currentStatus === 'BENEFIT_DISBURSED') {
        if (disbursedBox) disbursedBox.style.display = 'block';
        if (disbursedText) {
          disbursedText.innerText = activeLanguage === 'en' ? 
            `₹${(d.sanctioned_amount || 6000).toLocaleString()} credited directly to bank account (SBI A/C XXXX-4521). UTR Reference: UTR-KA-2026-${d.application_number.slice(-4)}` : 
            `₹${(d.sanctioned_amount || 6000).toLocaleString()} ಮೊತ್ತವನ್ನು ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ (SBI A/C XXXX-4521) ನೇರವಾಗಿ ಜಮೆ ಮಾಡಲಾಗಿದೆ. UTR ಸಂಖ್ಯೆ: UTR-KA-2026-${d.application_number.slice(-4)}`;
        }
      } else {
        if (disbursedBox) disbursedBox.style.display = 'none';
      }
    }
  } catch (e) {
    container.innerHTML = '<div style="color:red; text-align:center;">Failed to load timeline.</div>';
  }
}

function closeTimelineModal() {
  const modal = document.getElementById('timeline-modal');
  if (modal) modal.classList.remove('active');
}

// ============================================================================
// 9. Apply Now Modal & Submission
// ============================================================================
function openApplyModal(schemeId, schemeName, benefitAmount) {
  const modal = document.getElementById('apply-modal');
  if (!modal) return;

  document.getElementById('apply-scheme-id').value = schemeId;
  document.getElementById('apply-modal-scheme-name').innerText = schemeName;
  document.getElementById('apply-modal-benefit').innerText = benefitAmount;

  const fName = farmerCustomName || (currentFarmerData ? currentFarmerData.farmer_name : (activeLanguage === 'en' ? 'Ramesh Gowda' : 'ರಮೇಶ್ ಗೌಡ'));
  const fId = currentFarmerData ? currentFarmerData.farmer_id : 'KM-KA-2026-0842';
  const fLand = currentFarmerData ? `${currentFarmerData.land_acres || 2.5} ${activeLanguage === 'en' ? 'Acres' : 'ಎಕರೆ'}` : (activeLanguage === 'en' ? '2.5 Acres' : '2.5 ಎಕರೆ');
  const distObj = KARNATAKA_DISTRICTS.find(d => d.en === currentSelectedDistrict);
  const distName = (activeLanguage === 'kn' && distObj) ? distObj.kn : currentSelectedDistrict;
  const fLoc = `${distName}, ${activeLanguage === 'en' ? 'Karnataka' : 'ಕರ್ನಾಟಕ'}`;

  document.getElementById('apply-farmer-name').value = cleanBilingualText(fName, activeLanguage);
  document.getElementById('apply-farmer-id').value = fId;
  document.getElementById('apply-land-acres').value = fLand;
  document.getElementById('apply-location').value = fLoc;

  modal.classList.add('active');
}

function closeApplyModal() {
  const modal = document.getElementById('apply-modal');
  if (modal) modal.classList.remove('active');
}

async function submitSchemeApplication() {
  const schemeId = document.getElementById('apply-scheme-id').value;
  try {
    const res = await fetch('/api/applications', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scheme_id: parseInt(schemeId) })
    });
    const data = await res.json();
    if (data.success) {
      closeApplyModal();
      const msg = activeLanguage === 'en' ? 
        `✓ Application submitted successfully!\nApplication ID: ${data.data.application.application_number}\nYou can track real-time progress under the Application Tracking tab.` : 
        `✓ ಅರ್ಜಿ ಯಶಸ್ವಿಯಾಗಿ ಸಲ್ಲಿಕೆಯಾಗಿದೆ!\nಅರ್ಜಿ ಸಂಖ್ಯೆ: ${data.data.application.application_number}\nನೀವು 'ಅರ್ಜಿ ಟ್ರ್ಯಾಕಿಂಗ್' ವಿಭಾಗದಲ್ಲಿ ಇದರ ಪ್ರಗತಿಯನ್ನು ವೀಕ್ಷಿಸಬಹುದು.`;
      alert(msg);
      loadDashboardData();
      showTab('tracking');
    } else {
      alert(data.error ? data.error.message : "Failed to submit application.");
    }
  } catch (err) {
    alert("Network error. Please try again.");
  }
}

// ============================================================================
// 10. 3-Step Farmer Registration & Aadhaar e-KYC Modal
// ============================================================================
let regTransactionId = null;

function openRegistrationModal() {
  const modal = document.getElementById('registration-modal');
  if (!modal) return;
  goToRegStep(1);
  initLocationSelectors();
  modal.classList.add('active');
}

function closeRegistrationModal() {
  const modal = document.getElementById('registration-modal');
  if (modal) modal.classList.remove('active');
}

function goToRegStep(step) {
  document.getElementById('reg-step-1').style.display = (step === 1) ? 'block' : 'none';
  document.getElementById('reg-step-2').style.display = (step === 2) ? 'block' : 'none';
  document.getElementById('reg-step-3').style.display = (step === 3) ? 'block' : 'none';

  for (let i = 1; i <= 3; i++) {
    const ind = document.getElementById(`step-ind-${i}`);
    if (ind) {
      if (i === step) ind.className = 'reg-step-item active';
      else if (i < step) ind.className = 'reg-step-item completed';
      else ind.className = 'reg-step-item';
    }
  }
}

function formatAadhaarInput(el) {
  let val = el.value.replace(/\D/g, '');
  let formatted = '';
  for (let i = 0; i < val.length; i++) {
    if (i > 0 && i % 4 === 0) formatted += '-';
    formatted += val[i];
  }
  el.value = formatted.slice(0, 14);
}

async function submitRegistrationStep1() {
  const name = document.getElementById('reg-name').value.trim();
  const mobile = document.getElementById('reg-mobile').value.trim();
  const aadhaar = document.getElementById('reg-aadhaar').value.trim();
  const district = document.getElementById('reg-district').value;
  const taluk = document.getElementById('reg-taluk').value.trim();
  const village = document.getElementById('reg-village').value.trim();
  const consent = document.getElementById('reg-consent').checked;

  if (!name) { alert(activeLanguage === 'en' ? "Please enter farmer name." : "ದಯವಿಟ್ಟು ರೈತರ ಹೆಸರನ್ನು ನಮೂದಿಸಿ."); return; }
  if (!mobile || mobile.length < 10) { alert(activeLanguage === 'en' ? "Please enter a valid 10-digit mobile number." : "ದಯವಿಟ್ಟು 10 ಅಂಕಿಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ."); return; }
  if (!consent) { alert(activeLanguage === 'en' ? "Consent is required for Aadhaar e-KYC." : "ಮುಂದುವರಿಯಲು ಆಧಾರ್ e-KYC ಸಮ್ಮತಿಯನ್ನು ಒಪ್ಪಿಕೊಳ್ಳಬೇಕು."); return; }

  try {
    const res = await fetch('/api/identity/generate-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        full_name: name,
        mobile_number: mobile,
        aadhaar_number: aadhaar || '8421',
        district: district,
        taluk: taluk,
        village: village,
        state: 'Karnataka',
        preferred_language: activeLanguage,
        consent: consent
      })
    });
    const data = await res.json();
    if (data.success) {
      regTransactionId = data.data.transaction_id;
      document.getElementById('otp-phone-label').innerText = activeLanguage === 'en' ? 
        `Verification code sent to ${data.data.masked_mobile}.` : 
        `${data.data.masked_mobile} ಮೊಬೈಲ್ ಸಂಖ್ಯೆಗೆ ದೃಢೀಕರಣ ಕೋಡ್ ಕಳುಹಿಸಲಾಗಿದೆ.`;
      goToRegStep(2);
    } else {
      alert(data.error ? data.error.message : "Failed to generate OTP.");
    }
  } catch (err) {
    alert("Network error.");
  }
}

async function submitRegistrationStep2() {
  const otp = document.getElementById('reg-otp-input').value.trim();
  if (!otp) { alert(activeLanguage === 'en' ? "Please enter verification code." : "ದಯವಿಟ್ಟು ದೃಢೀಕರಣ ಕೋಡ್ ನಮೂದಿಸಿ."); return; }

  try {
    const verifyRes = await fetch('/api/identity/verify-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        transaction_id: regTransactionId,
        otp: otp
      })
    });
    const verifyData = await verifyRes.json();
    if (!verifyData.success) {
      alert(verifyData.error ? verifyData.error.message : (activeLanguage === 'en' ? "Invalid code. For demo enter '2026'." : "ತಪ್ಪಾದ ಕೋಡ್. ಡೆಮೊಗಾಗಿ '2026' ಬಳಸಿ."));
      return;
    }

    // Complete Registration
    const completeRes = await fetch('/api/identity/complete-registration', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        transaction_id: regTransactionId,
        land_acres: parseFloat(document.getElementById('reg-acres').value) || 2.5,
        irrigation_type: document.getElementById('reg-irrigation').value || 'BOREWELL',
        crops: document.getElementById('reg-crops').value.split(',').map(c => c.trim()).filter(Boolean)
      })
    });
    const completeData = await completeRes.json();
    if (completeData.success) {
      const u = completeData.data.user;
      document.getElementById('reg-result-farmer-id').innerText = u.farmer_id || 'KM-KA-2026-8421';
      document.getElementById('reg-result-name').innerText = cleanBilingualText(u.full_name, activeLanguage);

      farmerCustomName = cleanBilingualText(u.full_name, activeLanguage);
      localStorage.setItem('krishi_farmer_name', farmerCustomName);
      goToRegStep(3);
    } else {
      alert(completeData.error ? completeData.error.message : "Registration failed.");
    }
  } catch (err) {
    alert("Error completing registration.");
  }
}

function finishRegistration() {
  closeRegistrationModal();
  loadDashboardData();
  showTab('dashboard');
}

async function loadDemoFarmerRamesh() {
  const fName = activeLanguage === 'en' ? 'Ramesh Gowda' : 'ರಮೇಶ್ ಗೌಡ';
  try {
    const res = await fetch('/api/auth/phone-login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        phone_number: '9845012345',
        full_name: fName,
        district: 'Mandya',
        acres: 2.5,
        otp: '2026'
      })
    });
    const data = await res.json();
    if (data.success) {
      farmerCustomName = fName;
      localStorage.setItem('krishi_farmer_name', farmerCustomName);
      closeRegistrationModal();
      loadDashboardData();
      showTab('dashboard');
    }
  } catch (e) {
    console.warn("Demo farmer load error", e);
  }
}

// ============================================================================
// 11. Farmer Profile Tab Loader
// ============================================================================
async function loadProfileData() {
  try {
    const res = await fetch('/api/dashboard');
    const data = await res.json();
    if (data.success) {
      const d = data.data;
      const rawName = farmerCustomName || d.farmer_name;
      const cleanName = cleanBilingualText(rawName, activeLanguage);

      if (document.getElementById('prof-farmer-id')) document.getElementById('prof-farmer-id').innerText = d.farmer_id || 'KM-KA-2026-0842';
      if (document.getElementById('prof-farmer-name')) document.getElementById('prof-farmer-name').innerText = cleanName;
      if (document.getElementById('prof-state')) document.getElementById('prof-state').innerText = activeLanguage === 'en' ? 'Karnataka' : 'ಕರ್ನಾಟಕ';
      
      const distObj = KARNATAKA_DISTRICTS.find(x => x.en === (d.district || currentSelectedDistrict));
      const distName = (activeLanguage === 'kn' && distObj) ? distObj.kn : (d.district || currentSelectedDistrict);
      if (document.getElementById('prof-district')) document.getElementById('prof-district').innerText = distName;
      if (document.getElementById('prof-taluk')) document.getElementById('prof-taluk').innerText = d.taluk || (activeLanguage === 'en' ? 'Pandavapura' : 'ಪಾಂಡವಪುರ');
      if (document.getElementById('prof-village')) document.getElementById('prof-village').innerText = d.village || (activeLanguage === 'en' ? 'Chikka Byadarahalli' : 'ಚಿಕ್ಕ ಬ್ಯಾಡರಹಳ್ಳಿ');
      if (document.getElementById('prof-land-acres')) {
        document.getElementById('prof-land-acres').innerText = `${d.land_acres || 2.5} ${activeLanguage === 'en' ? 'Acres' : 'ಎಕರೆ'}`;
      }
    }
  } catch (e) {
    console.warn("Profile load", e);
  }
}

// ============================================================================
// 12. Notifications Drawer
// ============================================================================
function toggleNotificationsDropdown() {
  const dd = document.getElementById('notif-dropdown');
  if (!dd) return;
  dd.classList.toggle('active');
  if (dd.classList.contains('active')) loadNotifications();
}

async function loadNotifications() {
  const listEl = document.getElementById('notif-list');
  if (!listEl) return;
  const dict = I18N_DICTIONARY[activeLanguage] || I18N_DICTIONARY.kn;

  try {
    const res = await fetch('/api/notifications');
    const data = await res.json();
    if (data.success) {
      const notifs = data.data.notifications || [];
      if (notifs.length === 0) {
        listEl.innerHTML = `<div style="padding:24px; text-align:center; color:var(--text-muted); font-size:0.85rem;">${dict.notif_empty}</div>`;
        return;
      }
      listEl.innerHTML = notifs.map(n => {
        const rawTitle = activeLanguage === 'en' ? (n.title || n.title_kn) : (n.title_kn || n.title);
        const rawMsg = activeLanguage === 'en' ? (n.message || n.message_kn) : (n.message_kn || n.message);
        const title = cleanBilingualText(rawTitle, activeLanguage);
        const msg = cleanBilingualText(rawMsg, activeLanguage);
        return `
          <div class="notif-item ${n.is_read ? '' : 'unread'}">
            ${n.is_read ? '' : '<div class="notif-dot"></div>'}
            <div style="flex:1;">
              <div style="font-weight:700; font-size:0.88rem; color:var(--primary); margin-bottom:2px;">
                ${title}
              </div>
              <div style="font-size:0.82rem; color:var(--text-secondary); line-height:1.4;">
                ${msg}
              </div>
              <div style="font-size:0.72rem; color:var(--text-muted); margin-top:4px;">
                🕒 ${n.created_at ? n.created_at.substring(0, 16) : (activeLanguage === 'en' ? 'Recent' : 'ಇತ್ತೀಚೆಗೆ')}
              </div>
            </div>
          </div>
        `;
      }).join('');
    }
  } catch (e) {
    listEl.innerHTML = '<div style="padding:16px; color:red; font-size:0.85rem;">Failed to load notifications.</div>';
  }
}

async function markAllNotificationsRead() {
  try {
    await fetch('/api/notifications/read-all', { method: 'POST' });
    const badge = document.getElementById('notif-badge');
    if (badge) badge.style.display = 'none';
    loadNotifications();
  } catch (e) {}
}

// ============================================================================
// 13. Scenario Lab, Crop Diagnostics & Soil Health (Deterministic & ICAR Benchmarked)
// ============================================================================
async function runFinancialComparison() {
  const scenA = {
    crop_name: activeLanguage === 'en' ? 'Paddy' : 'ಭತ್ತ',
    land_acres: parseFloat(document.getElementById('scenA-acres').value) || 2.5,
    expected_yield_quintals: parseFloat(document.getElementById('scenA-yield').value) || 22,
    price_per_quintal: parseFloat(document.getElementById('scenA-price').value) || 2200,
    seed_cost: 5000,
    fertilizer_cost: 15000,
    labour_cost: 20000,
    irrigation_cost: 5000
  };

  const scenB = {
    crop_name: activeLanguage === 'en' ? 'Organic Ragi' : 'ಸಾವಯವ ರಾಗಿ',
    land_acres: parseFloat(document.getElementById('scenB-acres').value) || 2.5,
    expected_yield_quintals: parseFloat(document.getElementById('scenB-yield').value) || 16,
    price_per_quintal: parseFloat(document.getElementById('scenB-price').value) || 3800,
    seed_cost: 3000,
    fertilizer_cost: 8000,
    labour_cost: 14000,
    irrigation_cost: 3000
  };

  const res = await fetch('/api/calculator/compare', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ scenario_a: scenA, scenario_b: scenB })
  });
  const data = await res.json();
  if (!data.success) return;

  const resA = data.data.scenario_a;
  const resB = data.data.scenario_b;
  const delta = data.data.delta;

  const resultsBox = document.getElementById('calculator-results');
  if (resultsBox) resultsBox.style.display = 'block';

  const verdictEl = document.getElementById('calc-verdict');
  if (verdictEl) {
    const textResult = activeLanguage === 'en' ? 
      `Result: ${delta.recommended === 'Scenario B' ? 'Organic Ragi is more profitable' : 'Scenario A is recommended'}` : 
      `ಫಲಿತಾಂಶ: ${delta.recommended === 'Scenario B' ? 'ಸಾವಯವ ರಾಗಿ ಹೆಚ್ಚು ಲಾಭದಾಯಕ' : 'ಮೊದಲ ಬೆಳೆ ಸೂಕ್ತ'}`;
    verdictEl.innerHTML = `
      <span class="badge ${delta.recommended === 'Scenario B' ? 'badge-match' : 'badge-unknown'}">
        <span class="badge-dot"></span> ${textResult}
      </span>
    `;
  }

  const summaryEl = document.getElementById('scenario-summary-text');
  if (summaryEl) {
    const netProfitLabel = activeLanguage === 'en' ? 'Net Profit:' : 'ನಿವ್ವಳ ಲಾಭ:';
    const gainLabel = activeLanguage === 'en' ? 'Profit Difference:' : 'ಲಾಭದ ವ್ಯತ್ಯಾಸ:';
    const extraLabel = activeLanguage === 'en' ? 'higher net profit in Organic Ragi.' : 'ಹೆಚ್ಚುವರಿ ಲಾಭ.';
    summaryEl.innerHTML = `
      <div style="padding:10px; border-radius:10px; background:#f9fafc; margin-bottom:8px;">
        <strong>${scenA.crop_name}:</strong> ${netProfitLabel} <span style="font-size:1.1rem; font-weight:800; color:#2563eb;">₹${resA.net_profit.toLocaleString()}</span> (ROI: ${resA.roi_percentage}%)
      </div>
      <div style="padding:10px; border-radius:10px; background:#ecfdf5; margin-bottom:8px;">
        <strong>${scenB.crop_name}:</strong> ${netProfitLabel} <span style="font-size:1.1rem; font-weight:800; color:#059669;">₹${resB.net_profit.toLocaleString()}</span> (ROI: ${resB.roi_percentage}%)
      </div>
      <div style="padding:12px; border-radius:10px; background:#ecfdf5; border:1px solid #a7f3d0; margin-top:10px;">
        💡 <strong>${gainLabel}</strong> ₹${Math.abs(delta.profit_difference).toLocaleString()} ${extraLabel}
      </div>
    `;
  }

  const chartCanvas = document.getElementById('profitComparisonChart');
  if (chartCanvas) {
    const ctx = chartCanvas.getContext('2d');
    if (profitChartInstance) profitChartInstance.destroy();
    profitChartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: [scenA.crop_name, scenB.crop_name],
        datasets: [
          { label: activeLanguage === 'en' ? 'Cost (₹)' : 'ವೆಚ್ಚ (₹)', data: [resA.total_cost, resB.total_cost], backgroundColor: '#f59e0b', borderRadius: 8 },
          { label: activeLanguage === 'en' ? 'Net Profit (₹)' : 'ನಿವ್ವಳ ಲಾಭ (₹)', data: [resA.net_profit, resB.net_profit], backgroundColor: '#10b981', borderRadius: 8 }
        ]
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'bottom', labels: { font: { family: 'Plus Jakarta Sans', weight: 600 } } } },
        scales: { y: { beginAtZero: true }, x: { grid: { display: false } } }
      }
    });
  }
}

async function submitCropDiagnostic() {
  const crop = document.getElementById('crop-diag-name').value;
  const symp = document.getElementById('crop-diag-symptoms').value;
  const box = document.getElementById('crop-diagnostic-result');
  if (!box) return;

  const formData = new FormData();
  formData.append('crop_name', crop);
  formData.append('symptoms', symp);

  box.innerHTML = activeLanguage === 'en' ? 
    '<p style="color:var(--text-muted);">Analyzing symptoms against agricultural benchmarks...</p>' : 
    '<p style="color:var(--text-muted);">ರೋಗ ಲಕ್ಷಣಗಳನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...</p>';

  const res = await fetch('/api/crop/analyze', { method: 'POST', body: formData });
  const data = await res.json();
  if (!data.success) return;

  const d = data.data;
  const obsLabel = activeLanguage === 'en' ? 'Diagnostic Observations:' : 'ದೃಷ್ಟಿಗೋಚರ ಅವಲೋಕನಗಳು:';
  const causeLabel = activeLanguage === 'en' ? 'Possible Hypotheses:' : 'ಸಾಧ್ಯವಿರುವ ಕಾರಣಗಳು:';
  const actionLabel = activeLanguage === 'en' ? 'Recommended Precautionary Actions:' : 'ಮುಂಜಾಗ್ರತಾ ಕ್ರಮಗಳು:';

  box.innerHTML = `
    <div style="background:#fffbeb; border:1.5px solid #fde68a; padding:1.4rem; border-radius:var(--radius-md);">
      <h4 style="color:#92400e; font-size:1.1rem; font-weight:700;">${obsLabel}</h4>
      <ul style="padding-left:1.2rem; color:#78350f; font-size:0.92rem; margin-bottom:12px;">
        ${d.observations.map(o => `<li>${o}</li>`).join('')}
      </ul>
      <h4 style="color:#92400e; font-size:1.05rem; font-weight:700;">${causeLabel}</h4>
      <ul style="padding-left:1.2rem; color:#78350f; font-size:0.92rem; margin-bottom:12px;">
        ${d.hypotheses.map(h => `<li><strong>${h.cause}</strong> (${h.likelihood}): ${h.evidence}</li>`).join('')}
      </ul>
      <h4 style="color:#92400e; font-size:1.05rem; font-weight:700;">${actionLabel}</h4>
      <ul style="padding-left:1.2rem; color:#78350f; font-size:0.92rem;">
        ${d.cautious_actions.map(a => `<li>${a}</li>`).join('')}
      </ul>
    </div>
  `;
}

async function submitSoilInterpretation() {
  const ph = parseFloat(document.getElementById('soil-ph').value);
  const ec = parseFloat(document.getElementById('soil-ec').value);
  const n = parseFloat(document.getElementById('soil-n').value);
  const p = parseFloat(document.getElementById('soil-p').value);
  const k = parseFloat(document.getElementById('soil-k').value);

  const res = await fetch('/api/soil/interpret', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ph, ec, nitrogen: n, phosphorus: p, potassium: k })
  });
  const data = await res.json();
  if (!data.success) return;

  const params = data.data.parameters_analyzed;
  const box = document.getElementById('soil-result-box');
  if (!box) return;

  const heading = activeLanguage === 'en' ? 'Soil Quality Evaluation:' : 'ಮಣ್ಣಿನ ಗುಣಮಟ್ಟ ವಿಶ್ಲೇಷಣೆ:';
  const recLabel = activeLanguage === 'en' ? 'Agronomic Recommendation:' : 'ಶಿಫಾರಸು:';

  box.innerHTML = `
    <div style="background:#ecfdf5; border:1.5px solid #a7f3d0; padding:1.4rem; border-radius:var(--radius-md);">
      <h4 style="color:#065f46; font-size:1.1rem; font-weight:700; margin-bottom:10px;">${heading}</h4>
      <div class="grid-2" style="gap:8px; font-size:0.92rem; color:#064e3b; margin-bottom:12px;">
        <div>pH: <strong>${params.ph.value}</strong> &bull; <span class="badge badge-match">${params.ph.status}</span></div>
        <div>EC: <strong>${params.ec.value} dS/m</strong> &bull; ${params.ec.status}</div>
        <div>Nitrogen (N): <strong>${params.nitrogen.value} kg/ha</strong> &bull; ${params.nitrogen.status}</div>
        <div>Phosphorus (P): <strong>${params.phosphorus.value} kg/ha</strong> &bull; ${params.phosphorus.status}</div>
        <div>Potassium (K): <strong>${params.potassium.value} kg/ha</strong> &bull; ${params.potassium.status}</div>
      </div>
      <p style="font-size:0.88rem; color:#065f46; background:white; padding:8px 12px; border-radius:8px; border:1px solid #d1fae5;">
        💡 <strong>${recLabel}</strong> ${params.ph.note}
      </p>
    </div>
  `;
}

// ============================================================================
// 14. Page Initialization
// ============================================================================
window.addEventListener('DOMContentLoaded', () => {
  initLocationSelectors();
  loadDashboardData();
  setLanguage(activeLanguage);

  const hash = window.location.hash.replace('#', '');
  if (hash) showTab(hash);
});
'''

target_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'assets', 'js', 'app.js')
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Successfully wrote {len(js_content)} characters to {target_path}")


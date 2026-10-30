/**
 * Next-Generation AI SaaS Glassmorphism Micro-Interactions
 * Spotlight Cursor Tracking, Interactive AI Dashboard Preview, Pricing Switcher, Contact Toast
 */

document.addEventListener('DOMContentLoaded', () => {
  initSpotlightEffect();
  initDashboardTabs();
  initPricingToggle();
  initContactForm();
});

// 1. Interactive Spotlight Effect (Light Reflection Tracking)
function initSpotlightEffect() {
  const cards = document.querySelectorAll('.glass-card-interactive, .stat-glass-card, .pricing-card');
  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);
    });
  });
}

// 2. Interactive AI Dashboard Preview Tab Switcher
const DASHBOARD_TABS_DATA = {
  vision: {
    badge: "PyTorch 4-Block CNN • 25 Classes • 99.5% Acc",
    leftTitle: "Live Neural Camera Leaf Scan",
    leftContent: `
      <div style="background:#090d16; border-radius:12px; padding:16px; border:1px solid rgba(0, 240, 255, 0.25); position:relative; overflow:hidden;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <span style="font-size:0.75rem; background:rgba(0,240,255,0.15); color:#00F0FF; padding:3px 10px; border-radius:999px; font-weight:800;">🟢 REAL-TIME SCANNER</span>
          <span style="font-size:0.72rem; color:#94a3b8; font-family:var(--font-mono);">1280x720 @ 60fps</span>
        </div>
        <div style="position:relative; height:180px; border-radius:8px; background:radial-gradient(circle at 50% 50%, #1e293b 0%, #0f172a 100%); display:flex; align-items:center; justify-content:center; overflow:hidden;">
          <div style="position:absolute; inset:14px; border:2px dashed rgba(56,189,248,0.5); border-radius:8px;"></div>
          <div style="position:absolute; width:100%; height:2px; background:linear-gradient(90deg, transparent, #00F0FF, #A855F7, transparent); box-shadow:0 0 12px #00F0FF; animation:laserSweep 2s infinite ease-in-out;"></div>
          <div style="text-align:center;">
            <span style="font-size:2.4rem;">🍅</span>
            <span style="display:block; font-size:0.78rem; font-weight:700; color:#38bdf8; margin-top:4px;">Solanum lycopersicum (Tomato Foliage)</span>
          </div>
        </div>
        <div style="margin-top:12px; display:flex; flex-direction:column; gap:6px;">
          <div style="display:flex; justify-content:space-between; font-size:0.78rem;">
            <span style="color:#e2e8f0; font-weight:700;">Alternaria solani (Early Blight)</span>
            <strong style="color:#00F0FF;">98.4% Match</strong>
          </div>
          <div style="height:6px; background:rgba(255,255,255,0.1); border-radius:3px; overflow:hidden;">
            <div style="width:98.4%; height:100%; background:linear-gradient(90deg, #00F0FF, #8B5CF6);"></div>
          </div>
        </div>
      </div>
    `,
    rightTitle: "Autonomous Agronomic Prescription",
    rightContent: `
      <div style="display:flex; flex-direction:column; gap:12px;">
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:14px;">
          <span style="font-size:0.72rem; color:#A855F7; font-weight:800; text-transform:uppercase;">UAS Bengaluru Recommendation</span>
          <h4 style="font-size:0.95rem; margin:4px 0 6px; color:#fff;">Mancozeb 75 WP Protocol</h4>
          <p style="font-size:0.82rem; color:#94a3b8; margin:0;">Apply foliar spray at 2.0g per litre of water. Repeat in 8-10 days.</p>
        </div>
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:14px;">
          <span style="font-size:0.72rem; color:#10B981; font-weight:800; text-transform:uppercase;">Bio-Organic Control</span>
          <h4 style="font-size:0.95rem; margin:4px 0 6px; color:#fff;">Cold-Pressed Neem Oil (1500 PPM)</h4>
          <p style="font-size:0.82rem; color:#94a3b8; margin:0;">Spray at 3-5ml/L with bio-spreader to eradicate fungal spores.</p>
        </div>
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:14px;">
          <span style="font-size:0.72rem; color:#38BDF8; font-weight:800; text-transform:uppercase;">Audio Synthesis</span>
          <div style="display:flex; align-items:center; gap:8px; margin-top:4px;">
            <button onclick="simulateAudioPlay()" style="background:rgba(56,189,248,0.2); border:1px solid #38bdf8; color:#fff; border-radius:999px; padding:4px 12px; font-size:0.78rem; font-weight:700; cursor:pointer;">🔊 Play Kannada Advisory</button>
            <span style="font-size:0.75rem; color:#64748b;">kn-IN 0.95x rate</span>
          </div>
        </div>
      </div>
    `
  },
  voice: {
    badge: "Vernacular Dialect Normalizer • Krishi Echo AI",
    leftTitle: "Multi-Dialect Audio Stream",
    leftContent: `
      <div style="background:#090d16; border-radius:12px; padding:16px; border:1px solid rgba(168,85,247,0.3);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <span style="font-size:0.75rem; background:rgba(168,85,247,0.2); color:#A855F7; padding:3px 10px; border-radius:999px; font-weight:800;">🎙️ LIVE WEBSOCKET AUDIO</span>
          <span style="font-size:0.72rem; color:#94a3b8; font-family:var(--font-mono);">16kHz PCM</span>
        </div>
        <div style="height:120px; display:flex; align-items:center; justify-content:center; gap:4px; padding:0 20px; background:rgba(255,255,255,0.02); border-radius:8px;">
          <div style="width:4px; height:30px; background:#A855F7; border-radius:2px; animation:soundWave 1.2s infinite ease-in-out;"></div>
          <div style="width:4px; height:65px; background:#00F0FF; border-radius:2px; animation:soundWave 0.8s infinite ease-in-out 0.1s;"></div>
          <div style="width:4px; height:85px; background:#38BDF8; border-radius:2px; animation:soundWave 1.4s infinite ease-in-out 0.2s;"></div>
          <div style="width:4px; height:45px; background:#8B5CF6; border-radius:2px; animation:soundWave 0.9s infinite ease-in-out 0.3s;"></div>
          <div style="width:4px; height:95px; background:#00F0FF; border-radius:2px; animation:soundWave 1.1s infinite ease-in-out 0.4s;"></div>
          <div style="width:4px; height:40px; background:#A855F7; border-radius:2px; animation:soundWave 1.3s infinite ease-in-out 0.5s;"></div>
          <div style="width:4px; height:70px; background:#10B981; border-radius:2px; animation:soundWave 0.7s infinite ease-in-out 0.6s;"></div>
        </div>
        <div style="margin-top:14px; font-size:0.85rem; color:#E2E8F0; background:rgba(0,0,0,0.3); padding:10px 14px; border-radius:8px; border-left:3px solid #00F0FF;">
          <em>"ನನ್ನ ಎರಡು ಎಕರೆ ಜಮೀನಿಗೆ ಪಿಎಂ ಕಿಸಾನ್ ಹಣ ಯಾವಾಗ ಬರುತ್ತೆ?"</em>
        </div>
      </div>
    `,
    rightTitle: "Normalized Entity Extraction",
    rightContent: `
      <div style="display:flex; flex-direction:column; gap:10px; font-size:0.85rem;">
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:12px;">
          <span style="color:#64748b; font-size:0.75rem;">Parsed Intent:</span>
          <strong style="display:block; color:#00F0FF;">APPLICATION_STATUS (PM-KISAN)</strong>
        </div>
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:12px;">
          <span style="color:#64748b; font-size:0.75rem;">Acreage Extracted:</span>
          <strong style="display:block; color:#fff;">2.0 Acres (ಎರಡು ಎಕರೆ)</strong>
        </div>
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:12px;">
          <span style="color:#64748b; font-size:0.75rem;">Verification State:</span>
          <strong style="display:block; color:#10B981;">Aadhaar & Pahani Matched (100%)</strong>
        </div>
      </div>
    `
  },
  yield: {
    badge: "Multivariate Optimization Engine",
    leftTitle: "Crop Economics & Profit Margin",
    leftContent: `
      <div style="background:#090d16; border-radius:12px; padding:16px; border:1px solid rgba(16,185,129,0.3);">
        <h5 style="color:#fff; font-size:0.9rem; margin-bottom:12px;">Comparative Yield Simulation</h5>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:14px;">
          <div style="background:rgba(255,255,255,0.04); padding:10px; border-radius:8px;">
            <span style="font-size:0.75rem; color:#94a3b8;">Scenario A: Paddy</span>
            <strong style="display:block; font-size:1.15rem; color:#38bdf8;">₹38,400 Net</strong>
            <span style="font-size:0.7rem; color:#64748b;">Water: 1200mm</span>
          </div>
          <div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); padding:10px; border-radius:8px;">
            <span style="font-size:0.75rem; color:#10B981;">Scenario B: Ragi</span>
            <strong style="display:block; font-size:1.15rem; color:#34D399;">₹52,800 Net (+37%)</strong>
            <span style="font-size:0.7rem; color:#64748b;">Water: 450mm</span>
          </div>
        </div>
        <div style="height:70px; display:flex; align-items:flex-end; gap:8px;">
          <div style="flex:1; height:45%; background:#38bdf8; border-radius:4px 4px 0 0;"></div>
          <div style="flex:1; height:85%; background:#10b981; border-radius:4px 4px 0 0;"></div>
          <div style="flex:1; height:60%; background:#818cf8; border-radius:4px 4px 0 0;"></div>
          <div style="flex:1; height:95%; background:#a855f7; border-radius:4px 4px 0 0;"></div>
        </div>
      </div>
    `,
    rightTitle: "Soil Chemistry Balancing",
    rightContent: `
      <div style="display:flex; flex-direction:column; gap:10px; font-size:0.85rem;">
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:12px;">
          <span style="color:#64748b; font-size:0.75rem;">Soil pH Index:</span>
          <strong style="color:#fff;">6.5 (Neutral / Optimal)</strong>
        </div>
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:12px;">
          <span style="color:#64748b; font-size:0.75rem;">Electrical Conductivity:</span>
          <strong style="color:#10B981;">0.8 dS/m (Safe Salinity)</strong>
        </div>
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:12px;">
          <span style="color:#64748b; font-size:0.75rem;">Nutrient Recommendation:</span>
          <span style="color:#38bdf8; font-size:0.8rem; display:block;">Reduce Urea by 15%, add 20kg Zinc Sulphate per acre.</span>
        </div>
      </div>
    `
  },
  schemes: {
    badge: "Autonomous Seva Sindhu & Central Integration",
    leftTitle: "Zero-Click Entitlement Match",
    leftContent: `
      <div style="display:flex; flex-direction:column; gap:10px;">
        <div style="background:#090d16; border:1px solid rgba(56,189,248,0.25); border-radius:12px; padding:14px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="color:#fff; font-size:0.92rem;">PM-KISAN Samman Nidhi</strong>
            <span style="background:#ecfdf5; color:#065f46; font-size:0.75rem; padding:2px 8px; border-radius:999px; font-weight:800;">₹6,000 / yr</span>
          </div>
          <span style="font-size:0.78rem; color:#10B981; display:block; margin-top:4px;">✓ Land Holding Matched & KYC Completed</span>
        </div>
        <div style="background:#090d16; border:1px solid rgba(168,85,247,0.25); border-radius:12px; padding:14px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="color:#fff; font-size:0.92rem;">KUSUM Solar Pump 7.5 HP</strong>
            <span style="background:#f3e8ff; color:#6b21a8; font-size:0.75rem; padding:2px 8px; border-radius:999px; font-weight:800;">80% Subsidy</span>
          </div>
          <span style="font-size:0.78rem; color:#A855F7; display:block; margin-top:4px;">✓ Borewell Depth & Water Table Validated</span>
        </div>
      </div>
    `,
    rightTitle: "5-Stage Application Tracker",
    rightContent: `
      <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:14px;">
        <span style="font-size:0.75rem; color:#64748b; font-family:var(--font-mono);">APP-2026-KM-8421</span>
        <h5 style="color:#fff; font-size:0.95rem; margin:4px 0 12px;">Stage 4: Taluk ADA Verification</h5>
        <div style="display:flex; gap:6px; margin-bottom:10px;">
          <div style="flex:1; height:6px; background:#10B981; border-radius:3px;"></div>
          <div style="flex:1; height:6px; background:#10B981; border-radius:3px;"></div>
          <div style="flex:1; height:6px; background:#10B981; border-radius:3px;"></div>
          <div style="flex:1; height:6px; background:#38BDF8; border-radius:3px;"></div>
          <div style="flex:1; height:6px; background:rgba(255,255,255,0.15); border-radius:3px;"></div>
        </div>
        <span style="font-size:0.78rem; color:#94a3b8;">Est. Direct Benefit Transfer in 48 hours.</span>
      </div>
    `
  }
};

function initDashboardTabs() {
  const tabBtns = document.querySelectorAll('.window-tab-btn');
  const badgeEl = document.getElementById('dash-badge');
  const leftTitleEl = document.getElementById('dash-left-title');
  const leftContentEl = document.getElementById('dash-left-content');
  const rightTitleEl = document.getElementById('dash-right-title');
  const rightContentEl = document.getElementById('dash-right-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const tabKey = btn.getAttribute('data-tab');
      const data = DASHBOARD_TABS_DATA[tabKey];
      if (data) {
        if (badgeEl) badgeEl.textContent = data.badge;
        if (leftTitleEl) leftTitleEl.textContent = data.leftTitle;
        if (leftContentEl) leftContentEl.innerHTML = data.leftContent;
        if (rightTitleEl) rightTitleEl.textContent = data.rightTitle;
        if (rightContentEl) rightContentEl.innerHTML = data.rightContent;
      }
    });
  });
}

// 3. Interactive Pricing Switcher
function initPricingToggle() {
  const optMonthly = document.getElementById('opt-monthly');
  const optAnnual = document.getElementById('opt-annual');
  const priceStarter = document.getElementById('price-starter');
  const pricePro = document.getElementById('price-pro');
  const periodEls = document.querySelectorAll('.price-period');

  if (!optMonthly || !optAnnual) return;

  optMonthly.addEventListener('click', () => {
    optMonthly.classList.add('active');
    optAnnual.classList.remove('active');
    if (priceStarter) priceStarter.textContent = '₹0';
    if (pricePro) pricePro.textContent = '₹3,999';
    periodEls.forEach(el => el.textContent = '/ month');
  });

  optAnnual.addEventListener('click', () => {
    optAnnual.classList.add('active');
    optMonthly.classList.remove('active');
    if (priceStarter) priceStarter.textContent = '₹0';
    if (pricePro) pricePro.textContent = '₹2,999';
    periodEls.forEach(el => el.textContent = '/ month, billed annually');
  });
}

// 4. Contact Form Simulation
function initContactForm() {
  const form = document.getElementById('saas-contact-form');
  const toast = document.getElementById('glass-toast');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<span>⚡ Transmitting Request...</span>';
    }

    setTimeout(() => {
      form.reset();
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = '<span>🚀 Send Enterprise Inquiry</span>';
      }
      if (toast) {
        toast.style.display = 'flex';
        toast.style.animation = 'fadeInUp 0.3s ease forwards';
        setTimeout(() => {
          toast.style.display = 'none';
        }, 5000);
      }
    }, 900);
  });
}

function simulateAudioPlay() {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const msg = new SpeechSynthesisUtterance("ಟೊಮೆಟೊ ಬೆಳೆಯಲ್ಲಿ ಅಂಗಮಾರಿ ರೋಗ ಪತ್ತೆಯಾಗಿದೆ. ಮ್ಯಾಂಕೋಜೆಬ್ ಎರಡು ಗ್ರಾಂ ಪ್ರತಿ ಲೀಟರ್ ನೀರಿಗೆ ಸಿಂಪಡಿಸಿ.");
    msg.lang = 'kn-IN';
    msg.rate = 0.95;
    window.speechSynthesis.speak(msg);
  }
}

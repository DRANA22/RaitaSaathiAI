print("Updating application symbol across HTML and CSS...")

# 1. Update frontend/assets/css/style.css
with open("frontend/assets/css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

old_brand_icon = """.brand-icon {
  width: 36px;
  height: 36px;
  background: var(--emerald-gradient);
  color: white;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  box-shadow: 0 2px 6px rgba(16, 185, 129, 0.25);
  flex-shrink: 0;
}"""

new_brand_icon = """.brand-icon {
  width: 38px;
  height: 38px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  overflow: hidden;
}

.brand-icon img, .brand-icon svg {
  width: 100%;
  height: 100%;
  display: block;
}

.brand:hover .brand-icon {
  transform: scale(1.08) rotate(3deg);
}"""

if old_brand_icon in css:
    css = css.replace(old_brand_icon, new_brand_icon)
    print("Replaced .brand-icon CSS successfully")
else:
    print("Warning: old_brand_icon not found in style.css")

with open("frontend/assets/css/style.css", "w", encoding="utf-8") as f:
    f.write(css)

# 2. Update frontend/app.html
with open("frontend/app.html", "r", encoding="utf-8") as f:
    app_html = f.read()

if '<link rel="icon" type="image/svg+xml"' not in app_html:
    app_html = app_html.replace(
        '<title>RaitaSaathiAI — Farmer Digital Identity & Government Benefit Hub</title>',
        '<title>RaitaSaathiAI — Farmer Digital Identity & Government Benefit Hub</title>\n  <link rel="icon" type="image/svg+xml" href="/assets/images/brand-logo.svg">'
    )
app_html = app_html.replace(
    '<div class="brand-icon">🌱</div>',
    '<div class="brand-icon"><img src="/assets/images/brand-logo.svg" alt="RaitaSaathiAI" width="38" height="38"></div>'
)

with open("frontend/app.html", "w", encoding="utf-8") as f:
    f.write(app_html)
print("Updated frontend/app.html symbol and favicon")

# 3. Update frontend/login.html
with open("frontend/login.html", "r", encoding="utf-8") as f:
    login_html = f.read()

if '<link rel="icon" type="image/svg+xml"' not in login_html:
    login_html = login_html.replace(
        '<title>RaitaSaathiAI — Secure Farmer Login & Government Portal</title>',
        '<title>RaitaSaathiAI — Secure Farmer Login & Government Portal</title>\n  <link rel="icon" type="image/svg+xml" href="/assets/images/brand-logo.svg">'
    )
login_html = login_html.replace(
    '<div class="brand-icon" style="font-size:1.6rem;">🌱</div>',
    '<div class="brand-icon" style="width:40px; height:40px;"><img src="/assets/images/brand-logo.svg" alt="RaitaSaathiAI" width="40" height="40"></div>'
)
login_html = login_html.replace(
    '<a href="/" class="brand"',
    '<a href="/app" class="brand"'
)

with open("frontend/login.html", "w", encoding="utf-8") as f:
    f.write(login_html)
print("Updated frontend/login.html symbol and favicon")

# 4. Update frontend/admin.html
with open("frontend/admin.html", "r", encoding="utf-8") as f:
    admin_html = f.read()

if '<link rel="icon" type="image/svg+xml"' not in admin_html:
    admin_html = admin_html.replace(
        '<title>RaitaSaathiAI — Karnataka Agri Officer Admin Portal</title>',
        '<title>RaitaSaathiAI — Karnataka Agri Officer Admin Portal</title>\n  <link rel="icon" type="image/svg+xml" href="/assets/images/brand-logo.svg">'
    )

with open("frontend/admin.html", "w", encoding="utf-8") as f:
    f.write(admin_html)
print("Updated frontend/admin.html favicon")

print("All symbol updates completed successfully!")

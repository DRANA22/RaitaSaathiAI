import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

app = create_app()
client = app.test_client()

print("Testing route resolution & branding assets...")

# 1. Test root route '/'
res_root = client.get('/')
assert res_root.status_code == 200, f"Expected 200 for '/', got {res_root.status_code}"
assert b'RaitaSaathiAI' in res_root.data, "Expected 'RaitaSaathiAI' in root response"
assert b'brand-logo.svg' in res_root.data, "Expected 'brand-logo.svg' in root response"
assert b'The Autonomous Intelligence Platform' not in res_root.data, "Landing page content must NOT be in root response"
print("[OK] Root '/' successfully serves app.html with new brand logo")

# 2. Test '/app'
res_app = client.get('/app')
assert res_app.status_code == 200, f"Expected 200 for '/app', got {res_app.status_code}"
assert b'brand-logo.svg' in res_app.data, "Expected 'brand-logo.svg' in /app response"
print("[OK] '/app' successfully serves app.html")

# 3. Test '/saas' redirect
res_saas = client.get('/saas')
assert res_saas.status_code == 301, f"Expected 301 redirect for '/saas', got {res_saas.status_code}"
assert '/app' in res_saas.headers.get('Location', ''), f"Expected redirect to /app, got {res_saas.headers.get('Location')}"
print("[OK] '/saas' successfully permanently redirects (301) to '/app'")

# 4. Test '/login'
res_login = client.get('/login')
assert res_login.status_code == 200, f"Expected 200 for '/login', got {res_login.status_code}"
assert b'brand-logo.svg' in res_login.data, "Expected 'brand-logo.svg' in /login response"
print("[OK] '/login' successfully serves login.html with new brand logo")

# 5. Test '/admin'
res_admin = client.get('/admin')
assert res_admin.status_code == 200, f"Expected 200 for '/admin', got {res_admin.status_code}"
assert b'brand-logo.svg' in res_admin.data, "Expected 'brand-logo.svg' in /admin response"
print("[OK] '/admin' successfully serves admin.html with favicon")

# 6. Test '/assets/images/brand-logo.svg'
res_logo = client.get('/assets/images/brand-logo.svg')
assert res_logo.status_code == 200, f"Expected 200 for logo asset, got {res_logo.status_code}"
assert b'<svg' in res_logo.data, "Expected SVG markup in brand-logo.svg"
print("[OK] '/assets/images/brand-logo.svg' serves high-res SVG asset")

print("\nAll routing and branding verifications passed 100%!")

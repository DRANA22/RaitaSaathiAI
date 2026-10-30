with open("frontend/assets/css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

# 1. Revert body to clean off-white theme
old_body = """body {
  background-color: var(--bg-page);
  background-image: 
    linear-gradient(180deg, rgba(248, 250, 249, 0.92) 0%, rgba(248, 250, 249, 0.96) 35%, rgba(248, 250, 249, 0.93) 100%),
    url('/assets/images/indian-crops-bg.jpg');
  background-size: cover;
  background-position: center top;
  background-attachment: fixed;
  color: var(--text-primary);
  font-family: var(--font-sans);
  font-size: 1rem;
  line-height: 1.6;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
  width: 100%;
  overflow-x: hidden;
}"""

new_body = """body {
  background-color: var(--bg-page);
  background-image: 
    radial-gradient(at 0% 0%, rgba(16, 185, 129, 0.04) 0px, transparent 50%),
    radial-gradient(at 100% 100%, rgba(20, 184, 166, 0.03) 0px, transparent 50%);
  color: var(--text-primary);
  font-family: var(--font-sans);
  font-size: 1rem;
  line-height: 1.6;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
  width: 100%;
  overflow-x: hidden;
}"""

if old_body in css:
    css = css.replace(old_body, new_body)
    print("Replaced body background with clean off-white theme")
else:
    print("Warning: old_body not found")

# 2. Revert .farmer-greeting-card background image
old_greeting = """/* 4K Indian Farmer & Lush Crop Greeting Hero Card */
.farmer-greeting-card {
  margin-bottom: 1.8rem;
  background: 
    linear-gradient(90deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 255, 255, 0.94) 50%, rgba(255, 255, 255, 0.72) 75%, rgba(255, 255, 255, 0.45) 100%),
    url('/assets/images/indian-farmer-hero.jpg') right center / cover no-repeat !important;
  border-left: 6px solid var(--emerald) !important;
  box-shadow: 0 12px 36px -4px rgba(15, 61, 46, 0.1), 0 2px 6px rgba(0, 0, 0, 0.03) !important;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  position: relative;
  overflow: hidden;
}"""

new_greeting = """/* Clean Off-White Greeting Hero Card */
.farmer-greeting-card {
  margin-bottom: 1.8rem;
  background: #ffffff !important;
  border-left: 6px solid var(--emerald) !important;
  box-shadow: 0 4px 20px -2px rgba(15, 61, 46, 0.06), 0 2px 6px -1px rgba(0, 0, 0, 0.02) !important;
  border: 1px solid rgba(15, 61, 46, 0.08);
  position: relative;
  overflow: hidden;
}"""

if old_greeting in css:
    css = css.replace(old_greeting, new_greeting)
    print("Replaced .farmer-greeting-card background with clean off-white theme")
else:
    print("Warning: old_greeting not found")

# 3. Revert .crop-scanner-container background image
old_scanner = """.crop-scanner-container {
  max-width: 100%;
  width: 100%;
  margin: 0 auto;
  background: 
    linear-gradient(135deg, rgba(255, 255, 255, 0.96) 0%, rgba(240, 253, 244, 0.92) 65%, rgba(255, 255, 255, 0.82) 100%),
    url('/assets/images/lush-paddy-crops.jpg') right bottom / 420px auto no-repeat !important;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
}"""

new_scanner = """.crop-scanner-container {
  max-width: 100%;
  width: 100%;
  margin: 0 auto;
  background: #ffffff !important;
  border: 1px solid rgba(15, 61, 46, 0.08);
  box-shadow: 0 4px 20px -2px rgba(15, 61, 46, 0.06);
}"""

if old_scanner in css:
    css = css.replace(old_scanner, new_scanner)
    print("Replaced .crop-scanner-container background with clean off-white theme")
else:
    print("Warning: old_scanner not found")

with open("frontend/assets/css/style.css", "w", encoding="utf-8") as f:
    f.write(css)

print("Finished applying off-white dashboard theme updates!")

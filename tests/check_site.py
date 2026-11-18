"""Static privacy and security checks for the Ready-Set Solutions site.

Run from the repository root:  python tests/check_site.py
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://readyset.charleysllc.com/"
PAGES = sorted(list(ROOT.glob("*.html")) + list(ROOT.glob("services/*.html")))
failures = []


def check(condition, message):
    if not condition:
        failures.append(message)


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def csp(html):
    m = re.search(r'<meta http-equiv="Content-Security-Policy" content="([^"]+)"', html)
    return m.group(1) if m else ""


# --- Every page -------------------------------------------------------------
for page in PAGES:
    name = str(page.relative_to(ROOT))
    html = page.read_text(encoding="utf-8")
    policy = csp(html)
    check(policy, f"{name}: missing Content-Security-Policy")
    check("default-src 'self'" in policy, f"{name}: CSP lacks default-src 'self'")
    check("object-src 'none'" in policy, f"{name}: CSP lacks object-src 'none'")
    check("base-uri 'self'" in policy, f"{name}: CSP lacks base-uri 'self'")
    check("script-src 'self'" in policy and "script-src 'self' 'unsafe" not in policy,
          f"{name}: CSP must restrict scripts to 'self' with no unsafe-* sources")
    # No inline executable scripts (JSON-LD data blocks are allowed).
    for attrs in re.findall(r"<script\b([^>]*)>", html):
        check("src=" in attrs or "application/ld+json" in attrs, f"{name}: inline script found")
    check(not re.search(r'\son[a-z]+\s*=\s*"', html), f"{name}: inline event handler found")
    check("innerHTML" not in html, f"{name}: innerHTML used")
    # No phone number until a business-controlled line exists.
    check("tel:" not in html, f"{name}: tel: link published")
    check(not re.search(r"\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b", html), f"{name}: phone-like number published")
    # No unverified social proof.
    check(not re.search(r"aggregateRating|\"review\"|testimonial|5[- ]star|★", html, re.I),
          f"{name}: review/testimonial/rating content found")
    # No third-party scripts, trackers or mixed content.
    for src in re.findall(r'<(?:script|img|link|iframe)\b[^>]*?(?:src|href)="([^"]+)"', html):
        check(not src.startswith("http://"), f"{name}: insecure resource {src}")
        check(not src.startswith(("https://", "//")) or src.startswith(SITE),
              f"{name}: third-party resource {src}")
    # Only the contact page may submit a form.
    if page.name != "contact.html":
        check("<form" not in html, f"{name}: unexpected form")
        check("form-action 'none'" in policy, f"{name}: CSP should set form-action 'none'")
    # Internal links resolve to real files.
    for href in re.findall(r'href="([^"#?]+)', html):
        if href.startswith(("http", "mailto:")) or href in ("./", "../"):
            continue
        check((page.parent / href).exists(), f"{name}: broken link {href}")

# --- Contact form -----------------------------------------------------------
contact = read("contact.html")
forms = re.findall(r"<form\b([^>]*)>", contact)
check(len(forms) == 1, "contact.html: expected exactly one form")
check('action="https://formsubmit.co/support@charleysllc.com"' in contact, "contact.html: form action changed")
check('method="POST"' in contact, "contact.html: form must POST")
check("form-action https://formsubmit.co" in csp(contact), "contact.html: CSP form-action must be FormSubmit only")
check('name="_honey"' in contact, "contact.html: honeypot field missing")
check('type="file"' not in contact and "multipart/form-data" not in contact, "contact.html: file uploads not allowed")
check('name="_next" value="https://readyset.charleysllc.com/thank-you.html"' in contact, "contact.html: _next redirect changed")
check('name="_cc"' not in contact and 'name="_autoresponse"' not in contact, "contact.html: unexpected FormSubmit forwarding field")
check(re.search(r'name="Permission to contact"[^>]*required', contact), "contact.html: consent checkbox must be required")
check(" checked" not in contact, "contact.html: no pre-checked boxes")
check("Do not send sensitive information" in contact, "contact.html: sensitive-information warning missing")
check('href="privacy.html"' in contact, "contact.html: privacy notice link missing")
for field in re.findall(r"<(?:input|textarea)\b[^>]*>", contact):
    if 'type="hidden"' in field or 'type="checkbox"' in field or "_honey" in field:
        continue
    check("maxlength=" in field, f"contact.html: field without maxlength: {field[:60]}")
for field in re.findall(r'name="([^"]+)"', contact):
    check(not re.search(r"card|ssn|password|gate|access.?code", field, re.I), f"contact.html: sensitive field {field}")

js_path = ROOT / "assets" / "contact.js"
check(js_path.exists(), "assets/contact.js: missing")
js = js_path.read_text(encoding="utf-8") if js_path.exists() else ""
check("innerHTML" not in js and "eval(" not in js and "document.write" not in js, "assets/contact.js: unsafe DOM use")

# --- Privacy notice, disclosures -------------------------------------------
privacy = read("privacy.html")
check("FormSubmit" in privacy, "privacy.html: must name the form provider")
check("support@charleysllc.com" in privacy, "privacy.html: contact email missing")
index = read("index.html")
check(re.search(r"not a licensed contractor", index, re.I), "index.html: license disclosure missing")

# --- Structured data --------------------------------------------------------
blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', index, re.S)
check(len(blocks) == 1, "index.html: expected one JSON-LD block")
for raw in blocks + [read("structured-data.json")]:
    try:
        data = json.loads(raw)
    except ValueError as exc:
        check(False, f"structured data is not valid JSON: {exc}")
        continue
    check("telephone" not in data, "structured data: telephone published")
    check("aggregateRating" not in data and "review" not in data, "structured data: rating/review present")
    check(data.get("url") == SITE, "structured data: wrong url")

# --- Sitemap, robots, domain ------------------------------------------------
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = {n.text for n in ET.fromstring(read("sitemap.xml")).findall("sm:url/sm:loc", ns)}
for required in ("", "contact.html", "privacy.html"):
    check(SITE + required in urls, f"sitemap.xml: missing {SITE + required}")
for url in urls:
    check(url.startswith(SITE), f"sitemap.xml: off-site url {url}")
    rel = url[len(SITE):] or "index.html"
    check((ROOT / rel).exists(), f"sitemap.xml: {url} has no file")
    if (ROOT / rel).exists():
        check("noindex" not in read(rel), f"sitemap.xml: {url} is marked noindex")
check(read("CNAME").strip() == "readyset.charleysllc.com", "CNAME changed")

# --- Nothing private in the public repo -------------------------------------
SECRET = re.compile(r"sk_(live|test)_[0-9A-Za-z]{10,}|rk_live_[0-9A-Za-z]{10,}|whsec_[0-9A-Za-z]{10,}|"
                    r"gh[pousr]_[0-9A-Za-z]{30,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----")
for path in ROOT.rglob("*"):
    if ".git" in path.parts or not path.is_file():
        continue
    check(path.suffix.lower() not in (".env", ".pem", ".key", ".csv", ".xlsx", ".sqlite", ".db"),
          f"{path.relative_to(ROOT)}: file type not allowed in the public repo")
    check(path.name != ".env", ".env file committed")
    if path.suffix.lower() in (".html", ".js", ".json", ".md", ".yml", ".txt", ".xml", ".css", ".py"):
        check(not SECRET.search(path.read_text(encoding="utf-8", errors="ignore")),
              f"{path.relative_to(ROOT)}: possible credential")

if failures:
    print(f"{len(failures)} check(s) failed:")
    for f in failures:
        print(" -", f)
    sys.exit(1)
print(f"Static privacy/security checks passed ({len(PAGES)} pages).")

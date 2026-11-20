#!/usr/bin/env python3
"""Read-only BB369TECH static website release gates. Python standard library only."""
from pathlib import Path
from html.parser import HTMLParser
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
errors = []
checks = 0

def check(ok, message):
    global checks
    checks += 1
    print(("PASS" if ok else "FAIL") + " " + message)
    if not ok:
        errors.append(message)

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = []
        self.lang = None
        self.description = []
        self.links = []
        self.title = False
        self.has_title = False
        self.redirect = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "meta" and a.get("http-equiv", "").lower() == "refresh":
            self.redirect = a.get("content")
        if tag == "title":
            self.has_title = True
        if tag == "link":
            if a.get("rel") == "canonical":
                self.canonical.append(a.get("href"))
            if a.get("href"):
                self.links.append(a["href"])
        if tag == "meta" and a.get("name") == "description":
            self.description.append(a.get("content"))

check((ROOT / "index.html").exists(), "root homepage exists")
check((ROOT / "public/index.html").exists(), "Cloudflare homepage exists")
if (ROOT / "index.html").exists() and (ROOT / "public/index.html").exists():
    check((ROOT / "index.html").read_bytes() == (ROOT / "public/index.html").read_bytes(),
          "homepage mirrors match exactly")

for path in sorted(ROOT.glob("*.html")):
    page = Page()
    try:
        page.feed(path.read_text(encoding="utf-8"))
        if page.redirect:
            check("url=/" in page.redirect.lower(), f"{path.name}: internal legacy redirect")
            check(len(page.canonical) == 1, f"{path.name}: redirect canonical declared")
        else:
            check(bool(page.lang), f"{path.name}: language declared")
        check(page.has_title, f"{path.name}: title exists")
        check(len(page.canonical) == 1 and page.canonical[0].startswith("https://bb369tech.com/"),
              f"{path.name}: one first-party canonical")
        if not page.redirect:
            check(bool(page.description and page.description[0]), f"{path.name}: meta description")
        mirror = ROOT / "public" / path.name
        check(mirror.exists() and mirror.read_bytes() == path.read_bytes(),
              f"{path.name}: deployment mirror matches")
    except (OSError, UnicodeError, ValueError) as exc:
        check(False, f"{path.name}: parse/read error {exc}")

robots = ROOT / "robots.txt"
check(robots.exists() and "Sitemap: https://bb369tech.com/sitemap.xml" in robots.read_text(),
      "robots sitemap declaration")
sitemap = ROOT / "sitemap.xml"
try:
    tree = ET.parse(sitemap)
    locs = [n.text for n in tree.iter() if n.tag.endswith("}loc")]
    check(bool(locs), "sitemap contains URLs")
    check(len(locs) == len(set(locs)), "sitemap has no duplicate URLs")
    check(all((u or "").startswith("https://bb369tech.com/") for u in locs),
          "sitemap uses first-party HTTPS URLs")
except (OSError, ET.ParseError) as exc:
    check(False, f"sitemap XML valid: {exc}")

# Non-invasive conversion and multilingual release checks.
for path in ("contact.html", "zh/contact.html"):
    file = ROOT / path
    check(file.exists(), f"{path}: contact page exists")
    if file.exists():
        html = file.read_text(encoding="utf-8")
        check('data-corporate-contact' in html, f"{path}: contact form marker")
        check('https://bb369-sendgrid-api.onrender.com/api/corporate-inquiry' in html,
              f"{path}: expected inquiry endpoint preserved")
        check('corporate-contact.js' in html, f"{path}: form handler included")
        mirror = ROOT / "public" / path
        check(mirror.exists() and mirror.read_bytes() == file.read_bytes(),
              f"{path}: deployed copy identical")

handler = ROOT / "assets/corporate-contact.js"
check(handler.exists(), "contact handler exists")
if handler.exists():
    js = handler.read_text(encoding="utf-8")
    check("response.ok" in js and "data.success !== true" in js,
          "contact handler rejects failed responses")
    check("sending = true" in js and "sending = false" in js,
          "contact handler protects against duplicate submissions")
    mirror = ROOT / "public/assets/corporate-contact.js"
    check(mirror.exists() and mirror.read_bytes() == handler.read_bytes(),
          "contact handler mirrored to Cloudflare")

for lang, path in (("en", "index.html"), ("zh-Hans", "zh/index.html")):
    file = ROOT / path
    check(file.exists(), f"{lang}: homepage exists")
    if file.exists():
        p = Page()
        p.feed(file.read_text(encoding="utf-8"))
        check(p.lang == lang, f"{lang}: homepage language correct")
        mirror = ROOT / "public" / path
        check(mirror.exists() and mirror.read_bytes() == file.read_bytes(),
              f"{lang}: homepage mirror matches")

# Validate the static site itself without making network requests.
from urllib.parse import urlsplit, unquote

for file in sorted(ROOT.rglob("*.html")):
    if "public" in file.relative_to(ROOT).parts:
        continue
    p = Page()
    p.feed(file.read_text(encoding="utf-8"))
    for href in p.links:
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
            continue
        parsed = urlsplit(href)
        if parsed.scheme and parsed.scheme not in ("http", "https"):
            continue
        if parsed.netloc and parsed.netloc not in ("bb369tech.com", "www.bb369tech.com"):
            continue
        if parsed.netloc or href.startswith("/"):
            target = ROOT / unquote(parsed.path).lstrip("/")
        else:
            target = file.parent / unquote(parsed.path)
        if not parsed.path or parsed.path == "/":
            target = ROOT / "index.html"
        elif target.is_dir():
            target = target / "index.html"
        check(target.is_file(), f"{file.relative_to(ROOT)}: local link {href}")

# Batch 1: responsive navigation, structured metadata and contact entry gates.
import json
import re

for path in ("index.html", "contact.html", "zh/index.html", "zh/contact.html"):
    file = ROOT / path
    if not file.exists():
        continue
    html = file.read_text(encoding="utf-8")
    check(bool(re.search(r'<meta\\s+name="viewport"\\s+content="width=device-width,initial-scale=1"', html)),
          f"{path}: mobile viewport")
    check('href="/assets/site.css"' in html and 'href="/assets/premium-polish.css"' in html,
          f"{path}: approved responsive stylesheets")
    check('data-menu' in html, f"{path}: mobile navigation control")
    check('href="/contact.html"' in html or 'href="/zh/contact.html"' in html or path.endswith("contact.html"),
          f"{path}: contact navigation")
    for block in re.findall(r'<script\\s+type="application/ld\\+json"[^>]*>(.*?)</script>', html, re.S):
        try:
            payload = json.loads(block)
            check(isinstance(payload, (dict, list)), f"{path}: valid JSON-LD")
        except json.JSONDecodeError:
            check(False, f"{path}: valid JSON-LD")

navigation = ROOT / "assets/site.js"
check(navigation.exists(), "shared navigation script exists")
if navigation.exists():
    js = navigation.read_text(encoding="utf-8")
    check('aria-expanded' in js and 'aria-controls' in js,
          "mobile navigation exposes expanded state and controlled region")
    check('Escape' in js, "mobile navigation supports Escape")
    mirror = ROOT / "public/assets/site.js"
    check(mirror.exists() and mirror.read_bytes() == navigation.read_bytes(),
          "mobile navigation script mirrored for Cloudflare")

for path in ("assets/site.css", "assets/premium-polish.css"):
    file = ROOT / path
    check(file.exists(), f"{path}: approved stylesheet exists")
    if file.exists():
        mirror = ROOT / "public" / path
        check(mirror.exists() and mirror.read_bytes() == file.read_bytes(),
              f"{path}: stylesheet deployment mirror matches")

print(f"RESULT: {checks - len(errors)}/{checks} checks passed")
sys.exit(1 if errors else 0)

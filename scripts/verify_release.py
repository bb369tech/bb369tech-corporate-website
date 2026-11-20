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

print(f"RESULT: {checks - len(errors)}/{checks} checks passed")
sys.exit(1 if errors else 0)

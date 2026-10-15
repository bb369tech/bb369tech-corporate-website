"""Read-only checks for additive changes against the verified production commit."""
import collections
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import unittest
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
BASE='7f3ee14594726fa7d7ca2794efeddaeb7e24e857'
PAGES=['index.html','company.html','services.html','products.html','projects.html','industries.html','faq.html','contact.html','resources.html']
ZH=['index.html','services.html','industries.html','faq.html','contact.html']
def original(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=ROOT).decode()
class Doc(HTMLParser):
    def __init__(self,s):
        super().__init__();self.tags=[];self.words=[];self.skip=0;self.feed(s)
    def handle_starttag(self,t,a):
        self.tags.append((t,dict(a)))
        if t in ['script','style']:self.skip+=1
    def handle_endtag(self,t):
        if t in ['script','style']:self.skip-=1
    def handle_data(self,d):
        if not self.skip:self.words.extend(d.split())
    def attrs(self,t):return [a for tag,a in self.tags if tag==t]
def maintext(s):return Doc(re.search(r'<main>(.*?)</main>',s,re.S)[1]).words
def links(s):return [x['href'] for x in Doc(s).attrs('a') if 'href' in x]
def fields(s):
    d=Doc(re.search(r'<form.*?</form>',s,re.S)[0]);return [(t,a) for t,a in d.tags if t in ['form','input','textarea','select']]

class PublicSiteRegression(unittest.TestCase):
    def test_all_baseline_files_retained(self):
        paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=ROOT).decode().splitlines()
        for p in paths:
            with self.subTest(path=p):self.assertTrue((ROOT/p).is_file())
    def test_original_english_body_words_and_links_retained(self):
        for p in PAGES:
            with self.subTest(page=p):
                old=original(p);new=(ROOT/p).read_text()
                self.assertFalse(collections.Counter(maintext(old))-collections.Counter(maintext(new)))
                self.assertFalse(set(links(old))-set(links(new)))
    def test_protected_files_unchanged(self):
        for p in ['assets/site.js','robots.txt','privacy.html','terms.html','security.html','CNAME','VERSION.md','data/organization.json','public/assets/site.js','public/robots.txt','public/privacy.html','public/terms.html','public/security.html','public/CNAME','public/data/organization.json']:
            with self.subTest(path=p):self.assertEqual(original(p),(ROOT/p).read_text())
    def test_contact_contract_unchanged(self):
        original_fields=fields(original('contact.html'))
        for p in ['contact.html','zh/contact.html']:
            current_fields=fields((ROOT/p).read_text())
            self.assertEqual(original_fields[0][0],current_fields[0][0])
            for key,value in original_fields[0][1].items():self.assertEqual(value,current_fields[0][1][key])
            for t,a in original_fields[1:]:
                if a.get('name')=='topic':continue
                self.assertIn((t,a),current_fields)
            self.assertIn(('select',{'name':'inquiryType','required':None}),current_fields)
            self.assertIn(('input',{'type':'checkbox','name':'privacyConsent','value':'accepted','required':None}),current_fields)
        oldoptions=re.findall(r'<option>(.*?)</option>',original('contact.html'))
        self.assertEqual(oldoptions,re.findall(r'<option value="(.*?)">',(ROOT/'zh/contact.html').read_text()))
    def test_jsonld_and_logo_asset(self):
        for p in PAGES+['zh/'+p for p in ZH]:
            with self.subTest(page=p):
                s=(ROOT/p).read_text();g=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)[1])
                self.assertIn('WebPage',[n['@type'] for n in g['@graph']])
                self.assertIn('Organization',[n['@type'] for n in g['@graph']])
                for n in g['@graph']:
                    if n.get('logo'):self.assertTrue((ROOT/urlsplit(n['logo']).path.lstrip('/')).is_file())
        self.assertTrue((ROOT/'assets/logo-512.png').read_bytes().startswith(b'\x89PNG'))
    def test_internal_links_and_fragments_resolve(self):
        for f in list(ROOT.glob('*.html'))+list((ROOT/'zh').glob('*.html')):
            for u in links(f.read_text()):
                parsed=urlsplit(u)
                if parsed.scheme or parsed.netloc:continue
                target=(ROOT/parsed.path.lstrip('/')) if parsed.path.startswith('/') else f.parent/parsed.path
                if not parsed.path:target=f
                if target.is_dir():target=target/'index.html'
                with self.subTest(page=str(f.relative_to(ROOT)),url=u):
                    self.assertTrue(target.is_file())
                    if parsed.fragment:self.assertRegex(target.read_text(),r'id=[\"\']'+re.escape(parsed.fragment)+r'[\"\']')
    def test_new_service_schema_matches_visible_choices(self):
        s=(ROOT/'services.html').read_text();g=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s)[1]);names={n['name'] for n in g['@graph'] if n['@type']=='Service'}
        self.assertTrue({'Business Website Design','Get More Customers','Custom Business Solutions'}<=names)
        self.assertIn('https://tools.bb369tech.com',links((ROOT/'index.html').read_text()))
    def test_reciprocal_languages_and_one_h1(self):
        for p in ZH:
            en='https://bb369tech.com/'+('' if p=='index.html' else p)
            zh='https://bb369tech.com/zh/'+p
            for path,canonical in [(p,en),('zh/'+p,zh)]:
                s=(ROOT/path).read_text();d=Doc(s)
                self.assertEqual(1,len(d.attrs('h1')))
                self.assertIn({'rel':'canonical','href':canonical},d.attrs('link'))
                self.assertIn({'rel':'alternate','hreflang':'en','href':en},d.attrs('link'))
                self.assertIn({'rel':'alternate','hreflang':'zh-Hans','href':zh},d.attrs('link'))
    def test_changed_website_mirrors_match(self):
        for p in PAGES+['assets/site.css','assets/logo-512.png','assets/corporate-contact.js','assets/corporate-contact.css','sitemap.xml','llms.txt']+['zh/'+p for p in ZH]:
            with self.subTest(path=p):self.assertEqual((ROOT/p).read_bytes(),(ROOT/'public'/p).read_bytes())
    def test_sitemap_preserves_old_and_adds_chinese(self):
        def urls(s):return {e.text for e in ET.fromstring(s).iter() if e.tag.endswith('loc')}
        current=urls((ROOT/'sitemap.xml').read_text())
        self.assertTrue(urls(original('sitemap.xml'))<=current)
        self.assertTrue({'https://bb369tech.com/zh/'+p for p in ZH}<=current)

if __name__=='__main__':unittest.main(verbosity=2)

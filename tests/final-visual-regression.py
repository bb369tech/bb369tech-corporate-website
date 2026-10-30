"""Final visual candidate integrity checks. No network calls or customer submissions."""
from pathlib import Path
from lxml import html
from urllib.parse import urlsplit,unquote
import json,subprocess,unittest,runpy,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];P=R/'public';BASE='49c4bf9ce734b44694d1f33fcf85973cbe8b60d8'
def old(rel):return subprocess.check_output(['git','show',BASE+':public/'+rel],cwd=R,text=True)
def d(s):return html.document_fromstring(s)
def norm(s):return ' '.join(s.split())
def maintext(doc):return norm(doc.xpath('string(//main)'))
pages={str(p.relative_to(P)):d(p.read_text()) for p in P.rglob('*.html') if '__qa' not in p.parts}
class FinalVisual(unittest.TestCase):
 def test_all_original_public_paths_retained(self):
  for path in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'public'],cwd=R,text=True).splitlines():self.assertTrue((R/path).exists(),path)
 def test_search_identity_unchanged(self):
  for rel,doc in pages.items():
   prev=d(old(rel))
   for xp in ['//title/text()','//meta[@name="description"]/@content','//link[@rel="canonical"]/@href','//meta[@name="robots"]/@content','//script[@type="application/ld+json"]/text()','//link[@hreflang]/@href']:
    self.assertEqual(prev.xpath(xp),doc.xpath(xp),(rel,xp))
   for raw in doc.xpath('//script[@type="application/ld+json"]/text()'):json.loads(raw)
 def test_content_is_retained_or_explicitly_migrated(self):
  combined=' '.join(maintext(x) for x in pages.values())
  for rel,doc in pages.items():
   prev=d(old(rel));target=combined if rel in ['index.html','zh/index.html','projects.html','zh/projects.html'] else maintext(doc)
   for el in prev.xpath('//main//p|//main//li|//main//summary'):
    t=norm(''.join(el.itertext()))
    if t:self.assertIn(t,target,(rel,t))
 def test_five_homepage_regions(self):
  for rel in ['index.html','zh/index.html']:
   self.assertEqual(pages[rel].xpath('//main/section/@data-section'),['hero','services','solutions','projects','contact'])
   self.assertEqual(len(pages[rel].xpath('//article[@data-project-category]')),3)
 def test_case_publication_gate(self):
  records=json.loads((P/'projects.json').read_text())['projects'];self.assertEqual(len({x['id'] for x in records}),len(records))
  for x in records:
   self.assertEqual(x['state'],'published');self.assertTrue(x['public_display_approved']);self.assertTrue((P/x['image'].lstrip('/')).is_file())
   self.assertNotRegex(x['name'].lower(),r'demo|supermarket|antique')
  for rel in ['projects.html','zh/projects.html']:
   self.assertEqual(len(pages[rel].xpath('//button[@data-project-filter]')),3)
 def test_existing_forms_and_business_scripts_unchanged(self):
  for rel in ['contact.html','zh/contact.html']:
   prev=d(old(rel));doc=pages[rel]
   self.assertEqual([html.tostring(x) for x in prev.xpath('//form')],[html.tostring(x) for x in doc.xpath('//form')])
  for rel in ['assets/site.js','assets/corporate-contact.js','assets/corporate-contact.css','robots.txt','data/organization.json','products.json']:
   current=(P/rel).read_text()
   if rel=='assets/corporate-contact.js':current=runpy.run_path(str(R/'scripts/contact-status-preservation.py'))['original_contact_status'](current)
   self.assertEqual(current,old(rel),rel)
  wrangler=subprocess.check_output(['git','show',BASE+':wrangler.jsonc'],cwd=R,text=True)
  before=json.loads(wrangler); after=json.loads((R/'wrangler.jsonc').read_text())
  self.assertEqual(after['assets'].pop('html_handling'),'none')
  self.assertEqual(after['assets'].pop('not_found_handling'),'404-page')
  self.assertEqual(after,before)
  rules=(P/'_redirects').read_text()
  self.assertIn('/ /index.html 200',rules)
  self.assertIn('/zh/ /zh/index.html 200',rules)
 def test_original_collapsed_text_and_links_visible(self):
  subprocess.run(['python',str(R/'scripts/final-details-audit.py')],cwd=R,check=True,capture_output=True)
 def test_legal_bodies_unchanged(self):
  for rel in ['privacy.html','terms.html','security.html']:self.assertEqual(maintext(pages[rel]),maintext(d(old(rel))))
 def test_internal_links_and_language_targets(self):
  for rel,doc in pages.items():
   if doc.xpath('//main'):self.assertEqual(len(doc.xpath('//h1')),1,rel)
   for node in doc.xpath('//*[@href or @src]'):
    u=node.get('href') or node.get('src');s=urlsplit(u)
    if s.scheme or s.netloc:continue
    path=(P/s.path.lstrip('/')) if s.path.startswith('/') else P/Path(rel).parent/s.path
    if not s.path:path=P/rel
    if path.is_dir():path=path/'index.html'
    self.assertTrue(path.is_file(),(rel,u))
    if s.fragment and path.suffix=='.html':self.assertIn(unquote(s.fragment),d(path.read_text()).xpath('//*[@id]/@id'),(rel,u))
   for u in doc.xpath('//link[@hreflang]/@href'):
    path=P/urlsplit(u).path.lstrip('/');path=path/'index.html' if path.is_dir() else path
    self.assertTrue(path.is_file(),(rel,u))
    self.assertIn(doc.xpath('//link[@rel="canonical"]/@href')[0],d(path.read_text()).xpath('//link[@hreflang]/@href'),rel)
 def test_sitemap_unchanged(self):self.assertEqual((P/'sitemap.xml').read_text(),old('sitemap.xml'));ET.fromstring((P/'sitemap.xml').read_text())
 def test_static_case_generation_and_root_mirrors(self):
  subprocess.run(['python',str(R/'scripts/render-projects.py'),'--check'],cwd=R,check=True,capture_output=True)
  subprocess.run(['python',str(R/'scripts/sync-public-mirror.py'),'--check'],cwd=R,check=True,capture_output=True)
 def test_formal_main_and_production_semantic_preservation(self):
  subprocess.run(['python',str(R/'scripts/audit-semantic-preservation.py')],cwd=R,check=True,capture_output=True)
 def test_small_self_contained_frontend(self):
  self.assertLess((P/'assets/site.css').stat().st_size,35000)
  for rel in ['index.html','zh/index.html']:self.assertLess((P/rel).stat().st_size,30000)
  self.assertNotIn('@import',(P/'assets/site.css').read_text())
if __name__=='__main__':unittest.main(verbosity=2)

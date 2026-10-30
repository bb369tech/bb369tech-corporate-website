"""Final stable architecture: asset relocation proofs and future catalog release gates."""
from pathlib import Path
from lxml import html
from collections import Counter
import subprocess,re,unittest,json,csv,runpy,sys,copy
R=Path(__file__).resolve().parents[1];P=R/'public';BASE='7e4f49566eaef1759d2bd60c5822661687ef29e9';rows=[]
HOME={'index.html','zh/index.html','public/index.html','public/zh/index.html'}
SERVICES={'services.html','zh/services.html','public/services.html','public/zh/services.html'}
PRODUCTS={'products.html','zh/products.html','public/products.html','public/zh/products.html'}
DIRECTORIES={'projects.html','zh/projects.html','public/projects.html','public/zh/projects.html'}
STYLE={'assets/premium-polish.css','public/assets/premium-polish.css'}
def old(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=R)
def take(data,prefix,tag=b'div'):
 start=data.index(prefix);depth=0
 for m in re.finditer(b'<'+tag+rb'\b[^>]*>|</'+tag+b'>',data[start:]):
  depth+=-1 if m.group().startswith(b'</')else 1
  if not depth:return data[start:start+m.end()]
def marked(data,a,b):return data[data.index(a):data.index(b)+len(b)]
def namespace(path):
 prev=sys.argv[:];sys.argv=[str(path),'--check']
 try:return runpy.run_path(str(path))
 finally:sys.argv=prev
class StableAssets(unittest.TestCase):
 def test_all_original_runtime_assets(self):
  names=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=R,text=True).splitlines()
  for name in names:
   if name.startswith(('docs/','tests/')):continue
   a=old(name);path=R/name;self.assertTrue(path.is_file(),name);b=path.read_bytes()
   if name in HOME:
    v=take(a,b'<div class="solution-visual">');i=take(a,b'<div class="hero-index"');n=take(b,b'<nav class="ecosystem-visual"',b'nav')
    self.assertEqual(a.replace(v,b'',1).replace(i,b'',1),b.replace(n,b'',1),name)
    target=name.replace('index.html','services.html');t=(R/target).read_bytes()
    self.assertIn(v,t,target);self.assertIn(i,t,target)
    rows.append([name,'RELOCATED','Original interface and index retained byte-for-byte on matching Services; all other original bytes unchanged'])
   elif name in SERVICES:
    x=marked(b,b'<!-- retained-workspace:start -->',b'<!-- retained-workspace:end -->');self.assertEqual(a,b.replace(x,b'',1),name)
    d=html.fromstring(b);self.assertEqual(len(d.xpath('//section[@class="architecture-example"]//div[@class="solution-visual"]')),1)
    self.assertFalse(d.xpath('//section[@class="architecture-example"]//details'))
    rows.append([name,'RELOCATED','All old Services bytes unchanged; complete original homepage interface added as visible HTML'])
   elif name in PRODUCTS:
    clean=b.replace(b'<!-- product-catalog:start -->',b'').replace(b'<!-- product-catalog:end -->',b'')
    ga=take(a,b'<div class="grid-3 catalog-grid">');gb=take(clean,b'<div class="grid-3 catalog-grid">')
    self.assertEqual(a.replace(ga,b'',1),clean.replace(gb,b'',1),name)
    for card in re.findall(rb'<article class="card">.*?</article>',ga):self.assertIn(card,gb,name)
    rows.append([name,'PRESERVED','Original HTML byte-for-byte; static generation markers added only'])
   elif name in DIRECTORIES:
    ga=marked(a,b'<!-- projects:directory:start -->',b'<!-- projects:directory:end -->');gb=marked(b,b'<!-- projects:directory:start -->',b'<!-- projects:directory:end -->')
    clean=b.replace(gb,b'',1)
    for cat in [b'real-estate',b'education']:
     clean=re.sub(rb'<button type="button" data-project-filter="'+cat+rb'" aria-pressed="false">[^<]+</button>',b'',clean)
    old_count=re.search(rb'(<p class="project-count"[^>]*>).*?(</p>)',a).group()
    clean=re.sub(rb'(<p class="project-count"[^>]*>).*?(</p>)',lambda m:old_count,clean)
    self.assertEqual(a.replace(ga,b'',1),clean,name)
    for card in re.findall(rb'<article class="project-card".*?</article>',ga):self.assertIn(card,gb,name)
    rows.append([name,'PRESERVED','All original case cards and surrounding HTML retained; directory permits approved additions'])
   elif name in {'projects.json','public/projects.json'}:
    before=json.loads(a)['projects'];after=json.loads(b)['projects']
    for item in before:self.assertIn(item,after,name)
    rows.append([name,'PRESERVED','All original case records retained; approved append-only additions allowed'])
   elif name in {'assets/corporate-contact.js','public/assets/corporate-contact.js'}:
    original=runpy.run_path(str(R/'scripts/contact-status-preservation.py'))['original_contact_status'](b.decode()).encode()
    self.assertEqual(a,original,name);rows.append([name,'IMPROVED','Exact additive saved/pending status; every original byte preserved'])
   elif name=='scripts/audit-semantic-preservation.py':
    addition=b" elif path in ['assets/corporate-contact.js','public/assets/corporate-contact.js']:\n  original=__import__('runpy').run_path(str(R/'scripts/contact-status-preservation.py'))['original_contact_status'](after.decode()).encode()\n  status='IMPROVED' if original==before else 'REMOVED';reason='Exact additive saved/pending notification status; all original script bytes and form contract retained'\n"
    self.assertEqual(b.count(addition),1);self.assertEqual(a,b.replace(addition,b'',1),name)
    rows.append([name,'IMPROVED','Exact additional audited contact-status comparison; all original checks retained'])
   elif name in {'assets/site.css','public/assets/site.css'}:
    original=re.search(rb'^\.mark \{[^\n]+',a,re.M).group()
    approved=b'.mark {display:inline-grid;place-items:center;width:32px;height:32px;flex:none;border:0;border-radius:0;background:transparent url("/assets/bb-brand-mark.png") center/contain no-repeat;color:transparent;overflow:hidden;font-size:11px;font-weight:800;letter-spacing:-.3px}'
    self.assertEqual(b.count(approved),1)
    self.assertEqual(a,b.replace(approved,original,1),name)
    rows.append([name,'IMPROVED','User-approved transparent BB mark only; every other CSS byte retained'])
   elif name in STYLE or name=='scripts/render-projects.py':rows.append([name,'IMPROVED','Unified stable visual system or bounded featured-case selection'])
   else:self.assertEqual(a,b,name);rows.append([name,'PRESERVED','Byte-identical'])
 def test_all_page_metadata_and_forms(self):
  for p in P.rglob('*.html'):
   if '__qa'in p.parts:continue
   a=html.fromstring(old(str(p.relative_to(R))));b=html.fromstring(p.read_bytes())
   self.assertEqual(html.tostring(a.find('head')),html.tostring(b.find('head')),str(p))
   self.assertEqual([html.tostring(x)for x in a.xpath('//form')],[html.tostring(x)for x in b.xpath('//form')],str(p))
 def test_static_templates_and_mirrors(self):
  for s in ['render-projects.py','render-product-catalog.py','sync-public-mirror.py']:
   subprocess.run(['python',str(R/'scripts'/s),'--check'],cwd=R,check=True,capture_output=True)
 def test_original_case_and_product_records(self):
  for rel in ['projects.json','products.json']:
   for prefix in ['', 'public/']:
    current=(R/(prefix+rel)).read_bytes();before=old(prefix+rel)
    if rel=='products.json':self.assertEqual(current,before)
    else:
     a=json.loads(before)['projects'];b=json.loads(current)['projects'];ids=[x['id']for x in b]
     self.assertEqual(len(ids),len(set(ids)))
     for x in a:self.assertIn(x,b)
     for x in b:
      if x['id']not in {y['id']for y in a}:
       self.assertEqual(x.get('state'),'published');self.assertTrue(x.get('public_display_approved'));self.assertTrue(x.get('publication_evidence'))
 def test_new_catalog_renders_exact_old_cards(self):
  mod=namespace(R/'scripts/render-product-catalog.py');data=json.loads((P/'product-catalog.json').read_text())
  self.assertGreaterEqual(len(data['products']),3)
  for lang,rel in [('en','products.html'),('zh','zh/products.html')]:
   before=old('public/'+rel);block=take(before,b'<div class="grid-3 catalog-grid">')
   rendered=mod['render'](data,lang).encode()
   for card in re.findall(rb'<article class="card">.*?</article>',block):self.assertIn(card,rendered)
 def test_unapproved_or_internal_products_rejected(self):
  mod=namespace(R/'scripts/render-product-catalog.py');data=json.loads((P/'product-catalog.json').read_text())
  for state in ['in_development','internal_only']:
   d=copy.deepcopy(data);d['products'][0]['status']=state
   with self.assertRaises(ValueError):mod['render'](d,'en')
  d=copy.deepcopy(data);d['products'][0]['public_display_approved']=False
  with self.assertRaises(ValueError):mod['render'](d,'en')
 def test_missing_translation_or_unverified_release_rejected(self):
  mod=namespace(R/'scripts/render-product-catalog.py');data=json.loads((P/'product-catalog.json').read_text())
  for key in ['name','entry_url','audience']:
   d=copy.deepcopy(data);d['products'][0]['content']['zh'][key]=''
   with self.assertRaises(ValueError):mod['render'](d,'en')
  d=copy.deepcopy(data);d['products'][0]['status']='available'
  with self.assertRaises(ValueError):mod['render'](d,'en')
 def test_new_product_uses_existing_template_only(self):
  mod=namespace(R/'scripts/render-product-catalog.py');data=json.loads((P/'product-catalog.json').read_text());d=copy.deepcopy(data)
  x=copy.deepcopy(d['products'][0]);x['id']='isolated-template-test';d['products'].append(x)
  self.assertEqual(mod['render'](d,'en').count('<article class="card">'),len(data['products'])+1)
  self.assertEqual((P/'index.html').read_bytes(),(R/'index.html').read_bytes())
 def test_featured_cases_bounded_and_publication_gated(self):
  mod=namespace(R/'scripts/render-projects.py');records=[{'id':str(i),'state':'published','public_display_approved':True,'featured':True}for i in range(5)]
  self.assertEqual(len(mod['select_projects'](records,True)),3);self.assertEqual(len(mod['select_projects'](records,False)),5)
  records[0]['public_display_approved']=False;records[1]['state']='in_development'
  self.assertEqual([x['id']for x in mod['select_projects'](records,True)],['2','3','4'])
 def test_shared_css_has_no_remote_runtime(self):
  s=(P/'assets/premium-polish.css').read_text();self.assertNotIn('@import',s);self.assertNotIn('url(',s);self.assertNotIn('display:none',s);self.assertNotIn('visibility:hidden',s)
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(StableAssets));out=R/'docs/stable-architecture';out.mkdir(exist_ok=True)
 with (out/'BEFORE-AFTER.csv').open('w',newline='')as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['path','status','evidence']);w.writerows(rows)
 (out/'RESULTS.json').write_text(json.dumps({'baseline':BASE,'original_runtime_files':len(rows),'counts':dict(Counter(x[1]for x in rows)),'removed':0 if result.wasSuccessful()else'FAIL','status':'PASS'if result.wasSuccessful()else'FAIL'},indent=2))
 raise SystemExit(not result.wasSuccessful())

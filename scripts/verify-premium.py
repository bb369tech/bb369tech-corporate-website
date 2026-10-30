from pathlib import Path
from lxml import html
import json,subprocess,re,hashlib,csv,io
from urllib.parse import urlsplit,unquote
from collections import Counter
from xml.etree import ElementTree as ET
P=Path('public');D=Path('docs/premium-v3');BASE='86fa3c68c65c0fc722b1a176c9f64e094e04d782';fail=[];rows=[]
def old(p):return subprocess.check_output(['git','show',BASE+':'+str(p)],text=True)
def doc(t):return html.document_fromstring(t)
def require(ok,msg):
 if not ok:fail.append(msg)
def signature(d):
 return [{'action':f.get('action'),'method':f.get('method'),'controls':[{k:e.get(k) for k in ['name','type','value','required','pattern','minlength','maxlength']} for e in f.xpath('.//input|.//select|.//textarea')],'options':f.xpath('.//option/@value')} for f in d.xpath('//form')]
def canon(d):return d.xpath('//link[@rel="canonical"]/@href')
for p in sorted(P.rglob('*.html')):
 if '__qa' in p.parts:continue
 d=doc(p.read_text());rel=str(p.relative_to(P));b=None
 try:b=doc(old(p))
 except subprocess.CalledProcessError:pass
 if not d.xpath('//main'):continue
 require(len(d.xpath('//h1'))==1,rel+': H1')
 if b is not None:
  for xp in ['//title/text()','//meta[@name="description"]/@content','//meta[@name="robots"]/@content','//link[@rel="canonical"]/@href','//script[@type="application/ld+json"]/text()']:
   require(d.xpath(xp)==b.xpath(xp) or (rel=='404.html' and xp=='//meta[@name="robots"]/@content' and d.xpath(xp)==['noindex,follow']),rel+': protected metadata '+xp)
  require(signature(d)==signature(b),rel+': form contract')
  if p.name in ['privacy.html','terms.html','security.html']:
   require(d.xpath('string(//main)')==b.xpath('string(//main)'),rel+': legal body')
  if p.name not in ['index.html']:
   # preserve every existing prose/FAQ/service paragraph, not only total word count
   for e in b.xpath('//main//p|//main//li|//main//summary'):
    t=' '.join(''.join(e.itertext()).split())
    require(t in ' '.join(d.xpath('string(//main)').split()),rel+': missing body text '+t[:50])
 for text in d.xpath('//script[@type="application/ld+json"]/text()'):
  try:json.loads(text)
  except Exception:fail.append(rel+': invalid JSON-LD')
 for e in d.xpath('//*[@href or @src]'):
  u=e.get('href') or e.get('src');parts=urlsplit(u)
  if parts.scheme or parts.netloc:continue
  target=(P/parts.path.lstrip('/')) if parts.path.startswith('/') else p.parent/parts.path
  if not parts.path:target=p
  if target.is_dir():target=target/'index.html'
  require(target.exists(),rel+': broken asset/link '+u)
  if parts.fragment and target.suffix=='.html' and target.exists():
   ids=doc(target.read_text()).xpath('//*[@id]/@id');require(unquote(parts.fragment) in ids,rel+': missing fragment '+u)
 for alt in d.xpath('//link[@hreflang]'):
  ap=urlsplit(alt.get('href')).path;target=P/ap.lstrip('/');target=target/'index.html' if target.is_dir() else target
  require(target.is_file(),rel+': missing hreflang target')
  if target.is_file():require(canon(d)[0] in doc(target.read_text()).xpath('//link[@hreflang]/@href'),rel+': nonreciprocal language')
 rows.append({'path':'/'+rel,'canonical':';'.join(canon(d)),'robots':';'.join(d.xpath('//meta[@name="robots"]/@content')),'local_file':'PASS','production_http':'NOT VERIFIED','preview_http':'NOT VERIFIED','metadata':'PASS' if not any(x.startswith(rel+': protected') for x in fail) else 'FAIL'})
for path in ['assets/corporate-contact.js','assets/corporate-contact.css','assets/site.js','robots.txt','products.json','data/organization.json']:
 require((P/path).read_text()==old(P/path),path+': protected functional asset')
urls=lambda s:{e.text for e in ET.fromstring(s).iter() if e.tag.endswith('loc')}
require(urls(old(P/'sitemap.xml'))<=urls((P/'sitemap.xml').read_text()),'sitemap removed URLs')
for u in urls((P/'sitemap.xml').read_text()):
 q=P/urlsplit(u).path.lstrip('/');q=q/'index.html' if q.is_dir() else q;require(q.is_file(),'sitemap broken '+u)
with (D/'URL-SEO-MAP.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys(),lineterminator='\n');w.writeheader();w.writerows(rows)
result={'status':'FAIL' if fail else 'PASS','html_pages':len(rows),'failures':fail,'form_posts':0,'production_http':'NOT VERIFIED','cloudflare_preview':'NOT VERIFIED'}
(D/'static-results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False));print(json.dumps(result,indent=2,ensure_ascii=False));raise SystemExit(bool(fail))

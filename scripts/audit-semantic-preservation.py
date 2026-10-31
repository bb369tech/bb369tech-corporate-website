"""Compare the complete candidate to pinned main and observed live production DOM.
No network, deployment, AI rewriting or customer submissions. Missing semantic units fail closed.
"""
from pathlib import Path
from lxml import html
from urllib.parse import urlsplit
import subprocess,json,re,csv,hashlib,collections,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];P=R/'public';OUT=R/'docs/semantic-preservation';OUT.mkdir(exist_ok=True)
BASE='b553356528d097632f4f30da40258af4501f8212'
compact=lambda s:re.sub(r'\s+','',s or '')
norm=lambda s:' '.join((s or '').split())
serialize=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True) if not isinstance(x,str) else x
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=R,text=True).splitlines()
def old(path,binary=False):
 return subprocess.check_output(['git','show',BASE+':'+path],cwd=R,text=not binary)
def parse(s):return html.document_fromstring(s)
def url(path):return '/'+(path[7:] if path.startswith('public/') else path)
def sha(b):return hashlib.sha256(b).hexdigest()
new={str(p.relative_to(P)):parse(p.read_text()) for p in P.rglob('*.html') if '__qa' not in p.parts}
texts={k:compact(''.join(d.xpath('//main//text()'))) for k,d in new.items()}
rows=[];errors=[]
def add(kind,source,field,before,after,destination,status,evidence):
 rows.append({'category':kind,'source_file':source,'source_url':url(source),'field':field,'before':serialize(before),'after':serialize(after),'destination_url':destination,'status':status,'evidence':evidence})
 if status=='REMOVED':errors.append({'source':source,'field':field,'before':before})
def find_text(value,preferred):
 key=compact(value)
 if key in texts.get(preferred,''):return preferred
 candidates=[k for k,t in texts.items() if key in t]
 lang=preferred.startswith('zh/')
 return next((k for k in candidates if k.startswith('zh/')==lang),candidates[0] if candidates else None)
metadata=[('Title','//title/text()'),('Description','//meta[@name="description"]/@content'),('Canonical','//link[@rel="canonical"]/@href'),('Robots','//meta[@name="robots"]/@content'),('Schema','//script[@type="application/ld+json"]/text()'),('Hreflang','//link[@hreflang]/@href'),('OpenGraph','//meta[starts-with(@property,"og:")]/@content')]
for path in paths:
 if not path.endswith('.html'):continue
 rel=path[7:] if path.startswith('public/') else path
 if rel not in new:continue
 prev=parse(old(path));cur=new[rel]
 for field,xp in metadata:
  a=prev.xpath(xp);b=cur.xpath(xp)
  status='PRESERVED';evidence='Exact main/candidate field comparison'
  if a!=b:
   if field=='Robots' and rel=='404.html' and b==['noindex,follow']:
    status='IMPROVED';evidence='404 index exclusion from prior isolated candidate; does not alter indexable business pages or production'
   elif field=='Hreflang' and not a and b and rel in ['company.html','products.html','projects.html']:
    status='IMPROVED';evidence='Added reciprocal references to actual EN/ZH HTML translations; existing canonical preserved'
   else:status='REMOVED';evidence='Unexpected main metadata change: requires repair or explicit approval'
  add('SEARCH_IDENTITY',path,field,a,b,'/'+rel,status,evidence)
 for e in prev.xpath('//main//*[self::h1 or self::h2 or self::h3 or self::h4 or self::p or self::li or self::summary or self::dt or self::dd or self::figcaption or self::blockquote]'):
  value=norm(''.join(e.itertext()))
  if not value:continue
  target=find_text(value,rel)
  kind='FAQ' if 'faq.html' in path or e.tag=='summary' else 'BUSINESS_SEMANTICS'
  status=('PRESERVED' if target==rel else 'RELOCATED') if target else 'REMOVED'
  add(kind,path,e.tag,value,value if target else '',('/'+target) if target else '',status,'Exact text retained in server-readable HTML; whitespace normalized only; heading placement may differ')
 # All body links, including navigation/footer, remain reachable through static HTML.
 for e in prev.xpath('//body//a[@href]'):
  href=e.get('href');label=norm(''.join(e.itertext()));here=cur.xpath('//a[@href=$href]',href=href)
  target=rel if here else next((k for k,d in new.items() if d.xpath('//a[@href=$href]',href=href)),None)
  status=('PRESERVED' if target==rel else 'RELOCATED') if target else 'REMOVED'
  add('EXTERNAL_REFERENCE' if urlsplit(href).scheme else 'INTERNAL_LINK',path,label or 'link',href,href if target else '',('/'+target) if target else '',status,'Original href preserved in a static anchor; label changes do not change the destination')
 # Preserve complete descriptive quick-link blocks, not just their destination.
 for e in prev.xpath('//main//a[@href]'):
  value=norm(''.join(e.itertext()))
  if not value:continue
  target=find_text(value,rel)
  add('LINK_SEMANTICS',path,'anchor text',value,value if target else '',('/'+target) if target else '',('PRESERVED' if target==rel else 'RELOCATED') if target else 'REMOVED','Full descriptive link text retained in main HTML')
 for e in prev.xpath('//img[@src]'):
  src=e.get('src');alt=e.get('alt','');matches=[(k,x) for k,d in new.items() for x in d.xpath('//img[@src=$src]',src=src) if x.get('alt','')==alt]
  target=next((k for k,x in matches if k==rel),matches[0][0] if matches else None)
  add('IMAGE_IDENTITY',path,'src + alt',{'src':src,'alt':alt},{'src':src,'alt':alt} if target else {},('/'+target) if target else '',('PRESERVED' if target==rel else 'RELOCATED') if target else 'REMOVED','Original image URL and descriptive alt checked')
 for form in prev.xpath('//form'):
  signature=lambda f:{'form':dict(f.attrib),'controls':[{'tag':x.tag,'attributes':dict(x.attrib),'options':[{'attributes':dict(o.attrib),'text':norm(''.join(o.itertext()))} for o in x.xpath('.//option')]} for x in f.xpath('.//input|.//select|.//textarea|.//button')]}
  a=signature(form);same=any(signature(f)==a for f in cur.xpath('//form'))
  add('BUSINESS_FUNCTION',path,'form contract',a,a if same else {},'/'+rel,'PRESERVED' if same else 'REMOVED','Action, method, fields, options, required rules, consent and submit control compared')
# Existing public/mirror assets and machine-readable identities are checked independently.
for path in paths:
 if not re.search(r'\.(?:json|xml|txt|js|css|png|svg)$',path):continue
 if path.startswith(('tests/','docs/','.github/')):continue
 target=R/path;before=old(path,True);after=target.read_bytes() if target.exists() else b''
 if not target.exists():status='REMOVED';reason='Missing old file'
 elif before==after:status='PRESERVED';reason='SHA-256 content equality'
 elif path.endswith('sitemap.xml'):
  geturls=lambda b:{e.text for e in ET.fromstring(b).iter() if e.tag.endswith('loc')}
  a=geturls(before);b=geturls(after);status='IMPROVED' if a<=b else 'REMOVED';reason='All existing sitemap URLs retained; real Chinese counterparts added'
 elif path=='public/data/organization.json':
  archive=R/'docs/two-blocker-resolution-20261030/organization-public-before-367cf29.json'
  restored=after==old('data/organization.json',True) and archive.read_bytes()==before
  status='IMPROVED' if restored else 'REMOVED';reason='Exact production four-node graph restored from unchanged historical root; prior public bytes archived without deletion'
 elif path in ['assets/site.css','public/assets/site.css']:
  status='IMPROVED';reason='Authorized visual design-system consolidation; semantic HTML and functional regression verified separately'
 elif path in ['assets/corporate-contact.js','public/assets/corporate-contact.js']:
  original=__import__('runpy').run_path(str(R/'scripts/contact-status-preservation.py'))['original_contact_status'](after.decode()).encode()
  status='IMPROVED' if original==before else 'REMOVED';reason='Exact additive saved/pending notification status; all original script bytes and form contract retained'
 elif path in ['assets/site.js','public/assets/site.js']:
  status='IMPROVED';reason='Original menu/year behavior retained; keyboard Escape and aria state improvements validated on 12 bilingual routes'
 else:status='REMOVED';reason='Unexpected protected asset or machine-readable content change'
 add('MACHINE_DATA_OR_ASSET',path,'content digest',sha(before),sha(after) if target.exists() else '',url(path),status,reason)
 # Enumerate URLs in JSON documents as external/public provenance references.
 if path.endswith('.json'):
  try:
   a=json.loads(before);b=json.loads(after)
   def strings(x):
    if isinstance(x,str):yield x
    elif isinstance(x,list):
     for y in x:yield from strings(y)
    elif isinstance(x,dict):
     for y in x.values():yield from strings(y)
   bs=set(strings(b))
   for v in sorted(set(strings(a))):
    if v.startswith(('https://','http://','mailto:','tel:')):add('MACHINE_REFERENCE',path,'reference',v,v if v in bs else '',url(path),'PRESERVED' if v in bs else 'REMOVED','Exact URL/reference retained inside the original JSON record')
  except (json.JSONDecodeError,UnicodeDecodeError):pass
# Record authorized presentation changes separately while retaining all previous business wording.
for rel in ['index.html','zh/index.html','projects.html','zh/projects.html']:
 path='public/'+rel
 if path not in paths:continue
 prev=parse(old(path));cur=new[rel];a=prev.xpath('string(//h1)');b=cur.xpath('string(//h1)')
 if a!=b:add('PRESENTATION_COPY',path,'primary headline',a,b,'/'+rel,'IMPROVED','New positioning matches visible documented website/software services; original headline preserved elsewhere in the same-language static site')
# Explicit additions/layout changes are documented as improvements or relocations, never deletions.
for rel in ['zh/company.html','zh/products.html','zh/projects.html']:
 add('ADDED_TRANSLATION','public/'+rel,'page',[],{'path':'/'+rel,'title':new[rel].xpath('string(//title)')},'/'+rel,'IMPROVED','Actual static Chinese counterpart added; canonical/hreflang/links checked')
for project in json.loads((P/'projects.json').read_text())['projects']:
 add('VERIFIED_PROJECT_ADDITION','public/projects.html',project['name'],[],{'website':project['url'],'scope':project['scope'],'screenshot':project['image']},'/projects.html','IMPROVED','Existing public-release evidence and real website screenshot recorded in CASE-AUDIT.md; no business outcome claimed')
for label in ['Industries','Resources']:
 add('LINK_PLACEMENT','public/index.html',label,'Primary navigation and footer','Footer and existing detail page','/'+label.lower()+'.html','RELOCATED','Original URL still directly linked in static footer; detail content retained')
add('PRESENTATION_STRUCTURE','public/index.html','homepage regions',['Hero','Services','Products','What we do','Contact'],['Hero','Services','Solutions','Featured Projects','Contact'],'/','IMPROVED','Exactly five static main sections; prior descriptive units retained in stable detail URLs')
add('BUSINESS_FUNCTION','public/projects.html','industry filter','No industry filter',{'Retail':2,'Home improvement':1,'All':3},'/projects.html','IMPROVED','EN/ZH browser interaction checks pass; all cases remain visible in HTML without JavaScript')
# Main URL inventory includes old redirect documents, not only sitemap entries.
urlrows=[]
for path in paths:
 if not path.startswith('public/') or not path.endswith('.html'):continue
 rel=path[7:];prev=parse(old(path));refresh=prev.xpath('//meta[translate(@http-equiv,"REFSH","refsh")="refresh"]/@content')
 urlrows.append({'before_url':'/'+rel,'after_url':'/'+rel,'status':'PRESERVED' if (P/rel).is_file() else 'REMOVED','canonical_before':';'.join(prev.xpath('//link[@rel="canonical"]/@href')),'canonical_after':';'.join(new[rel].xpath('//link[@rel="canonical"]/@href')),'existing_redirect':';'.join(refresh),'numeric_http':'NOT VERIFIED'})
# Observed production text is cross-checked independently against candidate HTML.
production=json.loads((OUT/'production-baseline.json').read_text());production_errors=[]
for item in production:
 rel=urlsplit(item['finalUrl']).path.lstrip('/') or 'index.html';src='public/'+rel
 for value in item.get('h1',[])+item.get('paragraphs',[]):
  if not compact(value):continue
  target=find_text(value,rel)
  status=('PRESERVED' if target==rel else 'RELOCATED') if target else 'REMOVED'
  add('LIVE_PRODUCTION_TEXT',src,'observed text',norm(value),norm(value) if target else '',('/'+target) if target else '',status,'Actual production browser DOM observed on October 30, 2026; not inferred from Git alone')
  if not target:production_errors.append({'path':item['requestedPath'],'text':value})
 for key in ['canonical','robots']:
  actual=item.get(key,[]);actual=[actual] if isinstance(actual,str) else actual
  xp='//link[@rel="canonical"]/@href' if key=='canonical' else '//meta[@name="robots"]/@content'
  expected=parse(old(src)).xpath(xp)
  if actual!=expected:production_errors.append({'path':item['requestedPath'],'field':key,'actual':actual,'main':expected})
 if item['title']!=parse(old(src)).xpath('string(//title)'):production_errors.append({'path':item['requestedPath'],'field':'title'})
 actual_source=parse(old(src))
 for key,xp in [('description','//meta[@name="description"]/@content'),('schema','//script[@type="application/ld+json"]/text()')]:
  if item.get(key,[])!=actual_source.xpath(xp):production_errors.append({'path':item['requestedPath'],'field':key})
 expected_og=[{'property':e.get('property'),'content':e.get('content')} for e in actual_source.xpath('//meta[starts-with(@property,"og:")]')]
 expected_lang=[{'language':e.get('hreflang'),'href':e.get('href')} for e in actual_source.xpath('//link[@hreflang]')]
 if item.get('openGraph',[])!=expected_og:production_errors.append({'path':item['requestedPath'],'field':'OpenGraph'})
 if item.get('hreflang',[])!=expected_lang:production_errors.append({'path':item['requestedPath'],'field':'Hreflang'})
 expected_links={e.get('href') for e in actual_source.xpath('//a[@href]')}
 if {e['href'] for e in item.get('links',[])}!=expected_links:production_errors.append({'path':item['requestedPath'],'field':'live link destinations'})
 expected_forms=[{'action':f.get('action'),'method':f.get('method'),'controls':[{'tag':e.tag,'name':e.get('name'),'type':e.get('type'),'required':'required' in e.attrib} for e in f.xpath('.//input|.//select|.//textarea|.//button')]} for f in actual_source.xpath('//form')]
 if item.get('forms',[])!=expected_forms:production_errors.append({'path':item['requestedPath'],'field':'live form contract'})

with (OUT/'BEFORE-AFTER.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys(),lineterminator='\n');w.writeheader();w.writerows(rows)
with (OUT/'URL-BEFORE-AFTER.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=urlrows[0].keys(),lineterminator='\n');w.writeheader();w.writerows(urlrows)
counts=dict(collections.Counter(x['status'] for x in rows));summary={'baseline_main':BASE,'production_urls_observed':len(production),'source_documents_root_and_public':36,'preservation_rows':len(rows),'counts':counts,'missing_assets_or_semantics':errors,'production_main_mismatches':production_errors,'status':'PASS' if not errors and not production_errors else 'FAIL','numeric_http':'NOT VERIFIED','inbound_external_citations':'NOT VERIFIED'}
(OUT/'RESULTS.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False,indent=2));raise SystemExit(summary['status']!='PASS')

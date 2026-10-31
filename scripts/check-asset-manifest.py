"""Fail-closed additive asset contract. No writes, submissions, credentials or deployments."""
from pathlib import Path
import argparse,hashlib,json,re,sys,mimetypes
from urllib.parse import urlsplit,unquote
from xml.etree import ElementTree as ET
from lxml import html
N=lambda s:re.sub(r'\s+','',s or '')
H=lambda b:hashlib.sha256(b).hexdigest()

def contains(before,after):
 if isinstance(before,dict):return isinstance(after,dict) and all(k in after and contains(v,after[k]) for k,v in before.items())
 if isinstance(before,list):return isinstance(after,list) and all(any(contains(x,y) for y in after) for x in before)
 return type(before)==type(after) and before==after

def verify(root,manifest,allow_new_assets=False):
 root=Path(root);P=root/'public';errors=[];pages={};direct={};alltext={}
 def fail(kind,path,detail):errors.append({'kind':kind,'path':path,'detail':detail})
 for row in manifest['files']:
  if not (root/row['path']).is_file():fail('removed-file',row['path'],'Frozen historical path missing')
  elif row['path'].startswith('docs/') and H((root/row['path']).read_bytes())!=row['sha256']:fail('historical-overwrite',row['path'],'Frozen history must not be silently regenerated or replaced')
 for p in sorted(P.rglob('*.html')):
  rel=p.relative_to(P).as_posix()
  try:
   d=html.fromstring(p.read_bytes());pages[rel]=d
   direct[rel]=N(''.join(d.xpath('//main//text()[not(ancestor::details or ancestor::script or ancestor::style)]')))
   alltext[rel]=N(''.join(d.xpath('//main//text()[not(ancestor::script or ancestor::style)]')))
  except Exception as e:fail('html-parse',rel,str(e))
 for rel,old in manifest['pages'].items():
  d=pages.get(rel)
  if d is None:fail('removed-page',rel,'Missing parseable HTML');continue
  for key,xp in {'title':'//title/text()','description':'//meta[@name="description"]/@content','canonical':'//link[@rel="canonical"]/@href','robots':'//meta[@name="robots"]/@content','meta_refresh':'//meta[translate(@http-equiv,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz")="refresh"]/@content'}.items():
   if d.xpath(xp)!=old[key]:fail('seo-or-redirect',rel,key)
  if d.get('lang')!=old['language']:fail('language',rel,'HTML language changed')
  if not contains(old['hreflang'],[dict(x.attrib) for x in d.xpath('//link[@hreflang]')]):fail('hreflang',rel,'Original language relationship lost')
  try:
   if not contains(old['schema'],[json.loads(s) for s in d.xpath('//script[@type="application/ld+json"]/text()')]):fail('html-schema',rel,'Original node/field/relation changed')
  except ValueError:fail('html-schema',rel,'Invalid JSON-LD')
  if not set(old['links'])<=set(d.xpath('//a/@href')):fail('lost-link',rel,sorted(set(old['links'])-set(d.xpath('//a/@href'))))
  if not contains(old['images'],[dict(x.attrib) for x in d.xpath('//img')]):fail('lost-image',rel,'Original src/alt/dimensions changed')
  if old['forms']!=[html.tostring(f,with_tail=False).decode() for f in d.xpath('//form')]:fail('form-contract',rel,'Fields, action, method, consent or original form content changed')
  language=rel.startswith('zh/');scope={k:v for k,v in alltext.items() if k.startswith('zh/')==language};visible={k:v for k,v in direct.items() if k.startswith('zh/')==language}
  for unit in old['semantics']:
   corpus=visible if unit['direct'] else scope
   if not any(N(unit['text']) in text for text in corpus.values()):fail('lost-semantics',rel,unit['text'][:160])
 for unit in manifest['legacy_semantics']:
  language=unit['page'].startswith('zh/')
  if not any(N(unit['text']) in text for key,text in alltext.items() if key.startswith('zh/')==language):fail('lost-legacy-semantics',unit['page'],unit['text'][:160])
 for rel,old in manifest['json'].items():
  try:
   current=json.loads((P/rel).read_text())
   if not contains(old,current):fail('machine-contract',rel,'Original node ID, relationship, field or catalog record changed/reduced')
   graph=current.get('@graph',[]) if isinstance(current,dict) else []
   ids=[x['@id'] for x in graph if isinstance(x,dict) and '@id' in x]
   if len(ids)!=len(set(ids)):fail('machine-contract',rel,'Conflicting duplicate graph node IDs')
  except Exception as e:fail('machine-contract',rel,str(e))
 for rel,sha in manifest['immutable_public'].items():
  p=P/rel
  if not p.is_file() or H(p.read_bytes())!=sha:fail('immutable-runtime',rel,'Unapproved script/style/image/robots/redirect/sitemap change')
 # All current source links resolve before anything reaches a deployment.
 for rel,d in pages.items():
  for raw in d.xpath('//*[@href]/@href|//*[@src]/@src'):
   u=urlsplit(raw)
   if u.scheme or u.netloc:continue
   target=P/u.path.lstrip('/') if u.path.startswith('/') else P/Path(rel).parent/u.path
   if not u.path:target=P/rel
   if target.is_dir():target=target/'index.html'
   if not target.is_file():fail('broken-internal-link',rel,raw);continue
   if u.fragment and target.suffix=='.html':
    try:
     if unquote(u.fragment) not in html.fromstring(target.read_bytes()).xpath('//*[@id]/@id'):fail('broken-fragment',rel,raw)
    except Exception:fail('broken-fragment',rel,raw)
  for raw in d.xpath('//link[@hreflang]/@href'):
   u=urlsplit(raw)
   if u.hostname!='bb369tech.com':continue
   target=P/u.path.lstrip('/');target=target/'index.html' if target.is_dir() else target
   if not target.is_file():fail('hreflang-target',rel,raw)
 for p in P.rglob('*'):
  if not p.is_file():continue
  rel=p.relative_to(P).as_posix();mirror=root/rel
  if not mirror.is_file() or mirror.read_bytes()!=p.read_bytes():fail('mirror-drift',rel,'public and root differ')
 covered=set(manifest['pages'])|set(manifest['json'])|set(manifest['immutable_public'])
 if not allow_new_assets:
  for p in P.rglob('*'):
   if p.is_file() and p.relative_to(P).as_posix() not in covered:fail('unenrolled-asset',str(p.relative_to(P)),'Add an append-only manifest record for the new asset')
 try:
  locations={x.text for x in ET.parse(P/'sitemap.xml').iter() if x.tag.endswith('loc')}
  if not set(manifest['sitemap'])<=locations:fail('sitemap','sitemap.xml','Original URLs removed')
 except Exception as e:fail('sitemap','sitemap.xml',str(e))
 return {'status':'FAIL' if errors else 'PASS','baseline':manifest['frozen_candidate'],'frozen_paths':len(manifest['files']),'html_pages':len(pages),'errors':errors,'live_http':'NOT RUN; offline gate never submits data'}


def verify_http(root,manifest,base):
 from urllib.request import Request,urlopen
 from urllib.error import HTTPError
 from concurrent.futures import ThreadPoolExecutor
 allowed={'https://bb369tech.com','https://design-premium-visual-baseline-2026-bb369tech-corporate-website.bb369-ai.workers.dev'}
 if base not in allowed:raise ValueError('Only explicitly approved public origins are permitted')
 root=Path(root);urls=[(base+'/'+p,None) for p in sorted(set(manifest['pages'])|set(manifest['json'])|set(manifest['immutable_public'])) if p not in {'CNAME','_redirects'}]
 urls += [(base+'/',None),(base+'/zh/',None),(base+'/nonexistent-asset-gate-20261030',404)]
 urls += [(x['url'],None) for x in manifest['external_entries']]
 def get(task):
  url,expected=task
  try:
   try:r=urlopen(Request(url,headers={'User-Agent':'BB369TECH-Asset-ReadOnly-Check/1.0','Accept-Encoding':'identity'}),timeout=25)
   except HTTPError as e:r=e
   with r:b=r.read();status=r.code;final=r.url;ct=r.headers.get_content_type()
   issues=[]
   if status!=(expected or 200):issues.append('HTTP status')
   if url.startswith(base+'/') and status==200:
    rel=url[len(base)+1:];rel='index.html' if rel=='' else 'zh/index.html' if rel=='zh/' else rel
    if final!=url:issues.append('Unexpected HTTP redirect')
    if rel in manifest['pages']:
     if ct!='text/html':issues.append('Content-Type')
     d=html.fromstring(b);old=manifest['pages'][rel]
     for key,xp in {'title':'//title/text()','description':'//meta[@name="description"]/@content','canonical':'//link[@rel="canonical"]/@href','robots':'//meta[@name="robots"]/@content'}.items():
      if d.xpath(xp)!=old[key]:issues.append(key)
     try:
      if not contains(old['schema'],[json.loads(s) for s in d.xpath('//script[@type="application/ld+json"]/text()')]):issues.append('Schema')
     except ValueError:issues.append('Invalid Schema')
    elif rel in manifest['json']:
     if ct!='application/json':issues.append('Content-Type')
     if not contains(manifest['json'][rel],json.loads(b)):issues.append('Machine graph or catalog contract')
    elif rel=='robots.txt':
     if not (root/'public/robots.txt').read_bytes() in b:issues.append('Original robots rules missing')
     if base=='https://bb369tech.com' and manifest['production_robots_response'] not in b.decode():issues.append('Production managed robots rules changed')
    elif rel in manifest['immutable_public']:
     if H(b)!=H((root/'public'/rel).read_bytes()):issues.append('Source/deployed asset mismatch')
   return {'url':url,'status':status,'final_url':final,'content_type':ct,'errors':issues}
  except Exception as e:return {'url':url,'errors':[str(e)]}
 with ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(get,urls))
 return {'status':'FAIL' if any(x['errors'] for x in rows) else 'PASS','method':'GET only; no submissions or credentials','observations':rows}

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--root',default=str(Path(__file__).resolve().parents[1]));a.add_argument('--manifest');a.add_argument('--allow-new-assets',action='store_true');a.add_argument('--output');a.add_argument('--http-base');v=a.parse_args()
 try:
  m=json.loads(Path(v.manifest or Path(v.root)/'docs/asset-protection/manifest.json').read_text());r=verify(v.root,m,v.allow_new_assets)
  if v.http_base:
   r['live_http']=verify_http(v.root,m,v.http_base)
   if r['live_http']['status']!='PASS':r['status']='FAIL'
 except Exception as e:r={'status':'FAIL','errors':[{'kind':'gate-error','detail':str(e)}]}
 out=json.dumps(r,ensure_ascii=False,indent=2);print(out)
 if v.output:Path(v.output).write_text(out+'\n')
 sys.exit(0 if r['status']=='PASS' else 1)

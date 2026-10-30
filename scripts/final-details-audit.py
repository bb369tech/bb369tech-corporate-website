"""Verify every original collapsed text node and link remains in visible static HTML."""
from pathlib import Path
from lxml import html
import subprocess,re,json
root=Path(__file__).resolve().parents[1]
baseline='49c4bf9ce734b44694d1f33fcf85973cbe8b60d8'
def norm(s):return re.sub(r'\s+','',s).lower()
pages=[]
for f in (root/'public').rglob('*.html'):
 if '__qa' in f.parts:continue
 d=html.fromstring(f.read_text())
 pages.append(('/'+str(f.relative_to(root/'public')),norm(' '.join(d.xpath('//main//text()[not(ancestor::details)]'))),set(d.xpath('//main//a[not(ancestor::details)]/@href'))))
rows=[]
for rel in ['public/index.html','public/zh/index.html']:
 d=html.fromstring(subprocess.check_output(['git','show',baseline+':'+rel],cwd=root))
 for x in d.xpath('//details//text()'):
  text=' '.join(x.split())
  if not text:continue
  found=[p for p,t,links in pages if norm(text) in t]
  rows.append({'before_page':rel,'kind':'visible_text','before':text,'after_pages':found,'status':'RELOCATED' if found else 'REMOVED'})
 for x in d.xpath('//details//a[@href]'):
  href=x.get('href');found=[p for p,t,links in pages if href in links]
  rows.append({'before_page':rel,'kind':'link','before':href,'text':x.text_content(),'after_pages':found,'status':'PRESERVED' if found else 'REMOVED'})
out=root/'docs/final-release-review/DETAILS-ALL-TEXT-AND-LINKS.json'
out.write_text(json.dumps({'baseline':baseline,'rows':rows,'missing':[x for x in rows if x['status']=='REMOVED']},ensure_ascii=False,indent=2))
print(f'{len(rows)} collapsed text/link records checked; {sum(x["status"]=="REMOVED" for x in rows)} missing')
raise SystemExit(any(x['status']=='REMOVED' for x in rows))

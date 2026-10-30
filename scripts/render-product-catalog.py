"""Static bilingual product directory. No browser JavaScript or backend required."""
from pathlib import Path
from html import escape
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
def render(data,lang):
 products=data['products'];ids=set();cards=[]
 for x in products:
  if x['id']in ids:raise ValueError('Duplicate product ID')
  ids.add(x['id'])
  if x.get('public_display_approved')is not True or not x.get('publication_evidence'):raise ValueError('Public catalog requires explicit approval and evidence')
  if x.get('status')not in {'available','service','public_unconfirmed','pilot'}:raise ValueError('Internal or unfinished products must not be stored in public catalog')
  if x['status']=='available' and x.get('release_verified')is not True:raise ValueError('Available software requires verified release')
  for l in ['en','zh']:
   c=x['content'][l]
   for k in ['status_label','name','description','entry_label','entry_url','audience_label','audience']:
    if not c.get(k):raise ValueError('Both languages require complete content')
   if not(c['entry_url'].startswith('/')or c['entry_url'].startswith('https://')):raise ValueError('Invalid entry URL')
  c=x['content'][lang];E=lambda v:escape(str(v),quote=True)
  extra=' lang="'+E(c['entry_lang'])+'"' if c.get('entry_lang')else''
  cards.append('<article class="card"><span class="pill">'+E(c['status_label'])+'</span><h3>'+E(c['name'])+'</h3><p>'+E(c['description'])+'</p><a class="card-link" href="'+E(c['entry_url'])+'"'+extra+'>'+E(c['entry_label'])+'</a><p class="product-audience"><strong>'+E(c['audience_label'])+'</strong> '+E(c['audience'])+'</p></article>')
 return '<div class="grid-3 catalog-grid">'+''.join(cards)+'</div>'
def main():
 data=json.loads((ROOT/'public/product-catalog.json').read_text());drift=[]
 for lang,rel in [('en','products.html'),('zh','zh/products.html')]:
  p=ROOT/'public'/rel;s=p.read_text();body=render(data,lang);a='<!-- product-catalog:start -->';b='<!-- product-catalog:end -->';new=re.sub(re.escape(a)+'.*?'+re.escape(b),lambda m:a+body+b,s,flags=re.S)
  if new!=s:
   drift.append(rel)
   if '--check'not in sys.argv:p.write_text(new)
 if '--check'in sys.argv and drift:raise SystemExit('Product catalog drift: '+str(drift))
 print('Product catalog PASS')
if __name__=='__main__':main()

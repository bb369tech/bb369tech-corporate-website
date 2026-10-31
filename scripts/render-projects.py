"""Build static project cards from projects.json. Add approved facts + screenshot, then run.
--check verifies shipping HTML without writing it. No runtime request is required.
"""
from pathlib import Path
from html import escape as esc
import json,re,sys
root=Path(__file__).resolve().parents[1];public=root/'public'
projects=json.loads((public/'projects.json').read_text())['projects'];drift=[]
def select_projects(records,featured):
 eligible=[x for x in records if x.get('state')=='published' and x.get('public_display_approved') and (not featured or x.get('featured'))]
 return eligible[:3] if featured else eligible
for rel,featured in [('index.html',True),('zh/index.html',True),('projects.html',False),('zh/projects.html',False)]:
 lang='zh' if rel.startswith('zh/') else 'en';zh=lang=='zh';p=public/rel
 cards=[]
 for x in select_projects(projects,featured):
  E=lambda v:esc(str(v),quote=True)
  loading='lazy' if featured else 'eager'
  cards.append(f'<article class="project-card" data-project-category="{E(x["category"])}"><a class="project-image" href="{E(x["url"])}" aria-label="{E(x["name"])}"><img src="{E(x["image"])}" width="1348" height="926" loading="{loading}" decoding="async" alt="{E(x["name"])} '+('网站实际截图' if zh else 'actual website screenshot')+'"></a><div class="project-info"><div class="project-meta"><span>'+E(x['industry'][lang])+'</span><span>'+E(x['languages'][lang])+'</span></div><h3>'+E(x['name'])+'</h3><p>'+E(x['scope'][lang])+'</p><ul class="project-features">'+''.join('<li>'+E(v)+'</li>' for v in x['features'][lang])+f'</ul><a class="card-link" href="{E(x["url"])}">'+('查看已发布网站' if zh else 'View published website')+' <span aria-hidden="true">↗</span></a></div></article>')
 kind='featured' if featured else 'directory';body='<div class="projects-grid"'+(' data-project-grid' if not featured else '')+'>'+''.join(cards)+'</div>'
 begin=f'<!-- projects:{kind}:start -->';end=f'<!-- projects:{kind}:end -->';old=p.read_text();new=re.sub(re.escape(begin)+'.*?'+re.escape(end),lambda m:begin+body+end,old,flags=re.S)
 if not featured:
  total=len(select_projects(projects,False))
  new=re.sub(r'(<p class="project-count"[^>]*>).*?(</p>)',lambda m:m[1]+(str(total)+' 个已公开项目' if zh else str(total)+' published projects')+m[2],new)
  labels={'real-estate':('Real estate','房地产'),'education':('Education inquiry pages','教育咨询页面')}
  for category,label in labels.items():
   if any(x['category']==category for x in select_projects(projects,False)) and 'data-project-filter="'+category+'"' not in new:
    new=new.replace('</button></div><p class="project-count"','</button><button type="button" data-project-filter="'+category+'" aria-pressed="false">'+label[1 if zh else 0]+'</button></div><p class="project-count"',1)
 if old!=new:
  drift.append(rel)
  if '--check' not in sys.argv:p.write_text(new)
if '--check' in sys.argv and drift:raise SystemExit('Project HTML drift: '+str(drift))
print('Project templates PASS' if '--check' in sys.argv else 'Project cards rendered')

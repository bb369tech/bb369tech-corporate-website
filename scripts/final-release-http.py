from pathlib import Path
import json,concurrent.futures,hashlib,subprocess
from types import SimpleNamespace
class requests:
 @staticmethod
 def get(url,timeout):
  p=subprocess.run(["curl","-sS","-L","--max-time",str(timeout),"-D","-","-w","\n%{http_code}\n%{url_effective}\n%{content_type}",url],capture_output=True)
  if p.returncode:raise RuntimeError(p.stderr.decode())
  body,status,final,ct=p.stdout.rsplit(b"\n",3)
  blocks=body.split(b"\r\n\r\n"); headers=[]
  while blocks and blocks[0].startswith(b"HTTP/"):headers.append(blocks.pop(0).decode(errors="replace"))
  body=b"\r\n\r\n".join(blocks)
  return SimpleNamespace(content=body,status_code=int(status),url=final.decode(),headers={"content-type":ct.decode(),"x-robots-tag":next((v.split(":",1)[1].strip() for h in headers for v in h.splitlines() if v.lower().startswith("x-robots-tag:")),"")},history=[SimpleNamespace(status_code=int(h.splitlines()[0].split()[1]),headers={"Location":next((v.split(":",1)[1].strip() for v in h.splitlines() if v.lower().startswith("location:")),"")}) for h in headers if next((v for v in h.splitlines() if v.lower().startswith("location:")),None)])
from lxml import html
root=Path(__file__).resolve().parents[1]
bases=['https://bb369tech.com','https://design-premium-visual-baseline-2026-bb369tech-corporate-website.bb369-ai.workers.dev']
paths=['/','/index.html','/services.html','/products.html','/projects.html','/company.html','/industries.html','/resources.html','/faq.html','/contact.html','/privacy.html','/terms.html','/security.html','/zh/index.html','/zh/services.html','/zh/products.html','/zh/projects.html','/zh/company.html','/zh/industries.html','/zh/faq.html','/zh/contact.html','/404.html','/zh/','/credentials.html','/media.html','/news.html','/partners.html','/platforms.html','/why-us.html','/nonexistent-final-review-20261030','/robots.txt','/sitemap.xml']
urls=[b+p for b in bases for p in paths]+['https://platform.bb369tech.com/clients/'+x+'/' for x in ['sj-blinds-closets-windows','botanica-de-la-luz','productos-la-rosa']]+['https://platform.bb369tech.com/merchant/','https://platform.bb369tech.com/business-website/','https://platform.bb369tech.com/business-website/#monthly-support','https://tools.bb369tech.com/']
def run(url):
 try:
  r=requests.get(url,timeout=25);d={'url':url,'status':r.status_code,'final_url':r.url,'redirects':[{'status':x.status_code,'location':x.headers.get('Location')} for x in r.history],'x_robots_tag':r.headers.get('x-robots-tag')}
  if 'html' in r.headers.get('content-type',''):
   t=html.fromstring(r.content);d.update(title=t.xpath('//title/text()'),robots=t.xpath('//meta[@name="robots"]/@content'),canonical=t.xpath('//link[@rel="canonical"]/@href'),h1=t.xpath('//h1//text()'),meta_refresh=t.xpath('//meta[translate(@http-equiv,"REFSH","refsh")="refresh"]/@content'))
   if url==bases[1]+'/':d['latest_candidate']=b'Websites and software.' in r.content;d['sha256']=hashlib.sha256(r.content).hexdigest()
  return d
 except Exception as e:return {'url':url,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:rows=list(pool.map(run,urls))
(root/'docs/final-release-review/HTTP-RESULTS.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print(json.dumps({'requests':len(rows),'errors':[x for x in rows if 'error' in x]},ensure_ascii=False))

"""Allow only the approved intact interface relocation and visual stylesheet change."""
from pathlib import Path
import subprocess,re,unittest,csv,json
from lxml import html
from collections import Counter
R=Path(__file__).resolve().parents[1];BASE='ec90d20cbf3cd7f6e69fe3969fd33e4f0012cd45';rows=[]
HOME={'index.html','zh/index.html','public/index.html','public/zh/index.html'}
CSS={'assets/premium-polish.css','public/assets/premium-polish.css'}
def block(data):
 start=data.index(b'<div class="solution-visual">');depth=0
 for m in re.finditer(rb'<div\b[^>]*>|</div>',data[start:]):
  depth+=-1 if m.group().startswith(b'</')else 1
  if not depth:return data[start:start+m.end()]
class Composition(unittest.TestCase):
 def test_all_runtime_files_and_original_html(self):
  names=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=R,text=True).splitlines()
  for name in names:
   if name.startswith(('docs/','tests/')):continue
   a=subprocess.check_output(['git','show',BASE+':'+name],cwd=R);p=R/name;self.assertTrue(p.is_file(),name);b=p.read_bytes()
   if name in HOME:
    x=block(a);self.assertEqual(block(b),x,name)
    self.assertEqual(a.replace(x,b'',1),b.replace(x,b'',1),name)
    da=html.fromstring(a);db=html.fromstring(b)
    self.assertEqual(html.tostring(da.find('head')),html.tostring(db.find('head')),name)
    self.assertEqual(Counter(da.xpath('//a/@href')),Counter(db.xpath('//a/@href')),name)
    self.assertEqual(Counter(t.strip() for t in da.xpath('//body//text()') if t.strip()),Counter(t.strip() for t in db.xpath('//body//text()') if t.strip()),name)
    self.assertEqual(len(db.xpath('//section[@data-section="hero"]//div[@class="solution-visual"]')),1)
    rows.append([name,'RELOCATED','Exact existing interface block moved to hero; every other original byte, text, link and head preserved'])
   elif name in CSS:rows.append([name,'IMPROVED','Unified composition and responsive refinements in existing stylesheet'])
   else:self.assertEqual(a,b,name);rows.append([name,'PRESERVED','Byte-identical'])
 def test_mirror_and_static_templates(self):
  for script in ['sync-public-mirror.py','render-projects.py']:
   subprocess.run(['python',str(R/'scripts'/script),'--check'],cwd=R,check=True,capture_output=True)
 def test_no_new_runtime_or_external_asset(self):
  s=(R/'public/assets/premium-polish.css').read_text()
  self.assertNotIn('@import',s);self.assertNotIn('url(',s)
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Composition));out=R/'docs/composition-upgrade';out.mkdir(exist_ok=True)
 with (out/'BEFORE-AFTER.csv').open('w',newline='')as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['path','status','evidence']);w.writerows(rows)
 (out/'RESULTS.json').write_text(json.dumps({'baseline':BASE,'runtime_files_checked':len(rows),'counts':dict(Counter(r[1]for r in rows)),'removed':0 if result.wasSuccessful()else'FAIL','status':'PASS'if result.wasSuccessful()else'FAIL'},indent=2))
 raise SystemExit(not result.wasSuccessful())

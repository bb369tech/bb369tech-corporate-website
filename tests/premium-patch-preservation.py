"""Strict additive-only audit against the last reviewed design branch."""
from pathlib import Path
import subprocess,json,csv,io,unittest
R=Path(__file__).resolve().parents[1];BASE='6437dc713a8736ae937d96da8a0852cf8be29091'
LINK='<link rel="stylesheet" href="/assets/premium-polish.css">'
files=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=R,text=True).splitlines()
rows=[]
class PatchPreservation(unittest.TestCase):
 def test_all_original_files_preserved(self):
  for name in files:
   before=subprocess.check_output(['git','show',BASE+':'+name],cwd=R);p=R/name
   self.assertTrue(p.is_file(),name)
   after=p.read_bytes()
   if name.endswith('.html') and LINK.encode() in after:
    self.assertEqual(after.count(LINK.encode()),1,name)
    self.assertEqual(after.replace(LINK.encode(),b''),before,name)
    self.assertIn(b'/assets/site.css">'+LINK.encode(),after,name)
    rows.append([name,'PRESERVED','All original HTML bytes; one additional stylesheet link only'])
   else:
    self.assertEqual(after,before,name);rows.append([name,'PRESERVED','Byte-identical'])
 def test_root_mirror(self):
  subprocess.run(['python','scripts/sync-public-mirror.py','--check'],cwd=R,check=True,capture_output=True)
 def test_new_stylesheet_is_local_and_non_destructive(self):
  s=(R/'public/assets/premium-polish.css').read_text()
  self.assertNotIn('@import',s);self.assertNotIn('url(',s)
  self.assertNotIn('display:none',s);self.assertNotIn('visibility:hidden',s)
  self.assertIn('.card:not(form):hover',s)
  self.assertEqual((R/'assets/premium-polish.css').read_text(),s)
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PatchPreservation))
 out=R/'docs/premium-patch';out.mkdir(exist_ok=True)
 with (out/'BEFORE-AFTER.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['path','status','evidence']);w.writerows(rows)
 (out/'PRESERVATION-RESULTS.json').write_text(json.dumps({'baseline':BASE,'original_files_checked':len(rows),'html_link_only':sum('HTML' in x[2]for x in rows),'removed':0 if result.wasSuccessful()else'CHECK FAILURE','status':'PASS'if result.wasSuccessful()else'FAIL'},indent=2))
 raise SystemExit(not result.wasSuccessful())

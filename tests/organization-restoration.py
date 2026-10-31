"""Exact approved restoration only; no changes to HTML, runtime, URLs or other assets."""
from pathlib import Path
import unittest,subprocess,json,hashlib
R=Path(__file__).resolve().parents[1];BASE='367cf29f74425d0badee55bf58319510bed0bb0b';D=R/'docs/two-blocker-resolution-20261030'
def old(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R)
class OrganizationRestoration(unittest.TestCase):
 def test_exact_live_root_public_graph(self):
  a=(D/'production-organization.json').read_bytes();b=(R/'public/data/organization.json').read_bytes()
  self.assertEqual(a,b);self.assertEqual(b,(R/'data/organization.json').read_bytes());self.assertEqual(b,old('data/organization.json'))
  self.assertEqual(hashlib.sha256(a).hexdigest(),'391f76ae12888a73465ec31d7dd55bc67e7a8aa64dd044a8c4d195001e29c40a')
  graph=json.loads(b)['@graph'];self.assertEqual([x['@id'] for x in graph],['https://bb369tech.com/#organization','https://bb369tech.com/#machine-profile','https://bb369tech.com/#machine-capabilities','https://bb369tech.com/#agent-context'])
 def test_original_public_variant_archived_without_rewrite(self):
  a=(D/'organization-public-before-367cf29.json').read_bytes();self.assertEqual(a,old('public/data/organization.json'))
  self.assertEqual(hashlib.sha256(a).hexdigest(),'aae45df3a28b7d31aac7c5cc4472edf9939d4cbf475045fcf36d9d113f9285be')
 def test_all_other_public_and_root_runtime_bytes_unchanged(self):
  for p in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=R,text=True).splitlines():
   self.assertTrue((R/p).is_file(),p)
   if p.startswith(('docs/','tests/')) or p in ['scripts/audit-semantic-preservation.py','public/data/organization.json']:continue
   self.assertEqual((R/p).read_bytes(),old(p),p)
 def test_all_prior_machine_references_remain(self):
  def strings(x):
   if isinstance(x,str):yield x
   elif isinstance(x,list):
    for y in x:yield from strings(y)
   elif isinstance(x,dict):
    for y in x.values():yield from strings(y)
  before={x for x in strings(json.loads(old('public/data/organization.json'))) if x.startswith(('https://','http://','mailto:','tel:'))}
  self.assertTrue(before<=set(strings(json.loads((R/'public/data/organization.json').read_text()))))
if __name__=='__main__':unittest.main(verbosity=2)

"""Adversarial checks: an asset gate must reject the failures it claims to stop."""
from pathlib import Path
import copy,importlib.util,json,shutil,tempfile,unittest
R=Path(__file__).resolve().parents[1];M=json.loads((R/'docs/asset-protection/manifest.json').read_text());s=importlib.util.spec_from_file_location('gate',R/'scripts/check-asset-manifest.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
class AssetGate(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
  for x in M['files']:
   p=self.root/x['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/x['path'],p)
 def tearDown(self):self.temp.cleanup()
 def check(self,kind):self.assertIn(kind,{x['kind'] for x in g.verify(self.root,M)['errors']})
 def test_baseline(self):self.assertEqual(g.verify(self.root,M)['status'],'PASS')
 def test_historical_overwrite(self):
  rel=next(x['path'] for x in M['files'] if x['path'].startswith('docs/'));p=self.root/rel;p.write_text('unauthorized overwrite');self.check('historical-overwrite')
 def test_removed_history(self): (self.root/'resources.html').unlink();self.check('removed-file')
 def test_graph_node_reduction(self):
  p=self.root/'public/data/organization.json';d=json.loads(p.read_text());d['@graph'].pop();p.write_text(json.dumps(d));self.check('machine-contract')
 def test_graph_field_change(self):
  p=self.root/'public/data/organization.json';d=json.loads(p.read_text());d['@graph'][0]['@id']='https://example.invalid/wrong';p.write_text(json.dumps(d));self.check('machine-contract')
 def test_link_loss(self):
  p=self.root/'public/index.html';p.write_text(p.read_text().replace('href="/services.html"','href="/missing-service.html"'));self.check('lost-link');self.check('broken-internal-link')
 def test_form_consent(self):
  p=self.root/'public/contact.html';p.write_text(p.read_text().replace('name="privacyConsent"','name="removedConsent"'));self.check('form-contract')
 def test_meta_change(self):
  p=self.root/'public/faq.html';p.write_text(p.read_text().replace('<title>','<title>Wrong '));self.check('seo-or-redirect')
 def test_redirect_change(self):
  p=self.root/'public/credentials.html';p.write_text(p.read_text().replace('/company.html','/products.html'));self.check('seo-or-redirect')
 def test_mirror_drift(self):
  p=self.root/'assets/site.css';p.write_text(p.read_text()+'\n/* drift */');self.check('mirror-drift')
 def test_duplicate_graph_id(self):
  p=self.root/'public/data/organization.json';d=json.loads(p.read_text());d['@graph'].append(dict(d['@graph'][0],name='Conflicting identity'));p.write_text(json.dumps(d));self.check('machine-contract')
 def test_unenrolled_public_asset(self):
  (self.root/'public/unreviewed.html').write_text('<html><h1>Unenrolled</h1></html>');self.check('unenrolled-asset')
 def test_business_semantic_loss(self):
  from lxml import html
  p=self.root/'public/faq.html';d=html.fromstring(p.read_bytes());node=d.xpath('//main//p')[-1];node.getparent().remove(node);p.write_bytes(html.tostring(d));self.check('lost-semantics')
 def test_additive_json(self):
  for prefix in ['', 'public/']:
   p=self.root/(prefix+'data/organization.json');d=json.loads(p.read_text());d['@graph'][0]['additionalPropertyForTest']='synthetic additive';p.write_text(json.dumps(d))
  self.assertEqual(g.verify(self.root,M)['status'],'PASS')
if __name__=='__main__':unittest.main(verbosity=2)

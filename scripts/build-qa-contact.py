"""Prepare isolated browser fixtures. Never published or sent to a real inquiry endpoint."""
from pathlib import Path
from lxml import html
root=Path(__file__).resolve().parents[1];qa=root/'public/__qa';qa.mkdir(exist_ok=True)
for lang,rel in [('en','contact.html'),('zh','zh/contact.html')]:
 d=html.document_fromstring((root/'public'/rel).read_text());form=d.xpath('//form')[0];form.set('action','/__qa/non-delivery-trap')
 body=d.xpath('//body')[0];panel=html.fragment_fromstring('<aside style="padding:15px;background:#fff2bd"><strong>LOCAL QA · NO NETWORK OR MAIL</strong><select data-qa-mode><option value="success">success</option><option value="server-error">server-error</option><option value="false-success">false-success</option><option value="network-error">network-error</option></select><pre data-qa-capture></pre></aside>');body.insert(0,panel)
 s=html.fragment_fromstring('<script></script>');s.text=(root/'tests/fixtures/contact-browser-mock.js').read_text();d.xpath('//head')[0].append(s)
 (qa/f'contact-{lang}-mock.html').write_text('<!doctype html>\n'+html.tostring(d,encoding='unicode'))

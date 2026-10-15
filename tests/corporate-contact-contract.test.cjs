// Runs the pinned backend handler and browser UI with mail delivery intercepted.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),http=require('node:http');
const root=path.resolve(__dirname,'..');
const fixture=fs.readFileSync(path.join(__dirname,'fixtures/corporate-inquiry-handler.js'),'utf8');
function backend(){
  const messages=[];let handler;let fail=false;
  vm.runInNewContext(fixture,{app:{post:(route,fn)=>{assert.equal(route,'/api/corporate-inquiry');handler=fn;}},sgMail:{send:async m=>{if(fail)throw new Error('Synthetic mail-provider rejection');messages.push(m);}},FROM_EMAIL:'sender@example.invalid',CORPORATE_TO_EMAIL:'owner@example.invalid',escapeHtml:v=>String(v).replace(/[&<>"']/g,'_'),console:{error:()=>{}}});
  return {messages,setFail:v=>{fail=v;},call:async body=>{let result;const res={status(n){this.code=n;return this},json(data){result={status:this.code,data};return this}};await handler({body},res);return result;}};
}
test('original topic-only form is rejected before email; corrected fields are accepted',async()=>{
  const api=backend();const base={name:'Synthetic',company:'Test',email:'client@example.invalid',topic:'Business website',message:'Synthetic contract check'};
  assert.equal((await api.call(base)).status,400);assert.equal(api.messages.length,0);
  assert.equal((await api.call({...base,inquiryType:base.topic})).status,400);assert.equal(api.messages.length,0);
  assert.equal((await api.call({...base,inquiryType:base.topic,privacyConsent:'accepted'})).status,200);
  assert.equal(api.messages.length,2);assert.equal(api.messages[0].to,'owner@example.invalid');assert.equal(api.messages[1].to,'client@example.invalid');
});
test('English and Chinese forms meet the backend contract and handle failure honestly',{timeout:60000},async()=>{
  const {chromium}=require('playwright');
  const server=http.createServer((req,res)=>{try{let p=path.join(root,req.url.split('?')[0]);const data=fs.readFileSync(p);res.setHeader('Content-Type',p.endsWith('.js')?'text/javascript':p.endsWith('.css')?'text/css':'text/html; charset=utf-8');res.end(data)}catch{res.statusCode=404;res.end('Not found')}});
  await new Promise(r=>server.listen(0,'127.0.0.1',r));
  const origin='http://127.0.0.1:'+server.address().port;
  const b=await chromium.launch({executablePath:process.env.BB369_CHROMIUM_EXECUTABLE||undefined,args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'],headless:true});
  try{
    for(const rel of ['contact.html','zh/contact.html'].filter(p=>fs.existsSync(path.join(root,p)))){
      const api=backend();const p=await b.newPage({viewport:{width:390,height:844}});let requests=0;let posted;let mode='normal';
      await p.route('https://bb369-sendgrid-api.onrender.com/api/corporate-inquiry',async route=>{
        requests++;assert.equal(route.request().method(),'POST');posted=Object.fromEntries(new URLSearchParams(route.request().postData()));
        assert.equal(posted.inquiryType,'Business website');assert.equal(posted.topic,'Business website');assert.equal(posted.privacyConsent,'accepted');
        const result=await api.call(posted);
        await route.fulfill({status:mode==='false-success'?200:result.status,contentType:'application/json',body:JSON.stringify(mode==='false-success'?{success:false}:result.data)});
      });
      await p.goto(origin+'/'+rel);
      await p.locator('[name=name]').fill('Synthetic contract check');await p.locator('[name=company]').fill('Synthetic only');await p.locator('[name=email]').fill('client@example.invalid');await p.locator('[name=message]').fill('Contract check. Not a real customer inquiry.');
      await p.locator('button[type=submit]').click();assert.equal(requests,0);assert.equal(api.messages.length,0);
      await p.locator('[name=privacyConsent]').check();await p.locator('button[type=submit]').click();
      await p.waitForFunction(()=>document.querySelector('[data-contact-status]').textContent.includes('submitted')||document.querySelector('[data-contact-status]').textContent.includes('已提交'));
      assert.equal(requests,1);assert.equal(api.messages.length,2);assert.equal(await p.locator('[name=name]').inputValue(),'');
      for(const failure of ['provider','false-success']){
        api.setFail(failure==='provider');mode=failure;
        await p.locator('[name=name]').fill('Retain on failure');await p.locator('[name=email]').fill('client@example.invalid');await p.locator('[name=message]').fill('Synthetic failure check');await p.locator('[name=privacyConsent]').check();await p.locator('button[type=submit]').click();await p.locator('[data-contact-status][role=alert]').waitFor();
        assert.equal(await p.locator('[name=name]').inputValue(),'Retain on failure');assert(await p.locator('button[type=submit]').isEnabled());
      }
      const dimensions=await p.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));assert(dimensions.scroll<=dimensions.width+1);await p.close();
    }
  }finally{await b.close();await new Promise(r=>server.close(r));}
});

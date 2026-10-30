'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs'),path=require('node:path');
async function submit({zh=false,response={success:true},http=200,fail=false}={}){
 let handler,reset=0,calls=0;const status={textContent:'',setAttribute(){}},button={disabled:false};
 const form={action:'https://example.invalid/synthetic-only',querySelector:s=>s==='button[type="submit"]'?button:status,addEventListener:(name,fn)=>handler=fn,reportValidity:()=>true,setAttribute(){},removeAttribute(){},reset(){reset++;}};
 const FormDataMock=function(){return [['name','Synthetic'],['email','owner@example.invalid'],['inquiryType','Website'],['privacyConsent','accepted'],['message','Synthetic only']];};
 vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../public/assets/corporate-contact.js'),'utf8'),{document:{documentElement:{lang:zh?'zh-Hans':'en'},querySelectorAll:()=>[form]},FormData:FormDataMock,URLSearchParams,fetch:async()=>{calls++;if(fail)throw Error('synthetic network failure');return{ok:http>=200&&http<300,status:http,json:async()=>response};}});
 await handler({preventDefault(){}});return{message:status.textContent,reset,calls,disabled:button.disabled};
}
for(const zh of [false,true]){
 test('saved/pending gives truthful manual-follow-up status '+zh,async()=>{const r=await submit({zh,http:202,response:{success:true,dataSaved:true,notificationStatus:'pending'}});assert.match(r.message,zh?/咨询已保存，邮件通知暂未发出/:/saved.*pending/);assert.equal(r.reset,1);assert.equal(r.calls,1);assert.equal(r.disabled,false);});
 test('original accepted-mail status is retained '+zh,async()=>{const r=await submit({zh,response:{success:true,dataSaved:true,notificationStatus:'accepted'}});assert.match(r.message,zh?/确认邮件/:/confirmation/);assert.equal(r.reset,1);});
 test('unknown network outcome retains input and never automatically resends '+zh,async()=>{const r=await submit({zh,fail:true});assert.equal(r.reset,0);assert.equal(r.calls,1);assert.equal(r.disabled,false);});
 test('rejected submission never claims CRM saved '+zh,async()=>{const r=await submit({zh,http:503,response:{success:false}});assert.equal(r.reset,0);assert.doesNotMatch(r.message,zh?/咨询已保存/:/has been saved/);});
}

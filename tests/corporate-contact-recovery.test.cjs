const test=require('node:test'),assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
const source=fs.readFileSync(require.resolve('../assets/corporate-contact.js'),'utf8');
async function run(code,zh=false,network=false){
 let listener,reset=false;const button={disabled:false},status={setAttribute(){}};
 const form={querySelector:s=>s==='button[type="submit"]'?button:status,addEventListener:(_,fn)=>listener=fn,reportValidity:()=>true,setAttribute(){},removeAttribute(){},reset(){reset=true}};
 vm.runInNewContext(source,{document:{documentElement:{lang:zh?'zh-Hans':'en'},querySelectorAll:()=>[form]},URLSearchParams,FormData:class{*[Symbol.iterator](){yield ['inquiryType','Other']}},fetch:async()=>{if(network)throw Error('network');return {ok:code===200,status:code,json:async()=>({success:code===200})}}});
 await listener({preventDefault(){}});return {button,status,reset};
}
test('English and Chinese status recovery never resets failed input',async()=>{for(const zh of [false,true])for(const code of [200,400,409,429,500,503]){const r=await run(code,zh);assert.equal(r.reset,code===200);assert.equal(r.button.disabled,false);assert.ok(r.status.textContent.length>0);if(code>=500)assert.match(r.status.textContent,/avoid a duplicate|避免重复/);}});
test('network ambiguity uses contact fallback instead of encouraging retry',async()=>{assert.match((await run(0,false,true)).status.textContent,/avoid a duplicate/)});
test('published script mirror matches source',()=>assert.equal(source,fs.readFileSync(require.resolve('../public/assets/corporate-contact.js'),'utf8')));

/* LOCAL QA ONLY. Used on a copy whose form action points to a local non-delivery trap. */
(function () {
  var calls = 0;
  window.fetch = async function (url, options) {
    if (!String(url).endsWith('/__qa/non-delivery-trap')) throw Error('QA refuses an external destination');
    var output = document.querySelector('[data-qa-capture]');
    calls += 1;
    var fields = Object.fromEntries(new URLSearchParams(options.body));
    output.textContent = JSON.stringify({calls:calls,method:options.method,fields:fields,networkRequests:0});
    var mode = document.querySelector('[data-qa-mode]').value;
    if (mode === 'network-error') throw Error('Synthetic network failure');
    return {ok:mode!=='server-error',status:mode==='server-error'?503:200,json:async function(){return {success:mode==='success'}}};
  };
}());

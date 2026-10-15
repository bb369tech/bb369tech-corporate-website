/* Corporate contact only: the existing endpoint and customer paths are unchanged. */
(function () {
  'use strict';
  document.querySelectorAll('form[data-corporate-contact]').forEach(function (form) {
    var button = form.querySelector('button[type="submit"]');
    var status = form.querySelector('[data-contact-status]');
    var zh = document.documentElement.lang === 'zh-Hans';
    var sending = false;
    form.addEventListener('submit', async function (event) {
      event.preventDefault();
      if (sending || !form.reportValidity()) return;
      var body = new URLSearchParams(new FormData(form));
      // Retain the former topic alias while supplying the backend's required field.
      body.set('topic', body.get('inquiryType') || '');
      sending = true;
      button.disabled = true;
      form.setAttribute('aria-busy', 'true');
      status.setAttribute('role', 'status');
      status.textContent = zh ? '正在提交，请稍候…' : 'Submitting your inquiry…';
      try {
        var response = await fetch(form.action, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' },
          body: body.toString(),
          credentials: 'omit'
        });
        var data = await response.json();
        if (!response.ok || data.success !== true) throw new Error('Submission rejected');
        status.textContent = zh
          ? '咨询已提交。请留意确认邮件及垃圾邮件文件夹。'
          : 'Your inquiry was submitted. Please check your inbox and spam folder for a confirmation.';
        form.reset();
      } catch (_) {
        status.setAttribute('role', 'alert');
        status.textContent = zh
          ? '未能确认提交成功。请稍后重试，或发送邮件至 business@bb369tech.com。'
          : 'We could not confirm submission. Please try again later or email business@bb369tech.com.';
      } finally {
        sending = false;
        button.disabled = false;
        form.removeAttribute('aria-busy');
      }
    });
  });
})();

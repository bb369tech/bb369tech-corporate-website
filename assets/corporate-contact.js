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
        if (!response.ok || data.success !== true) {
          var error = new Error('Submission rejected');
          error.status = response.status;
          throw error;
        }
        if (data.dataSaved === true && data.notificationStatus === 'pending') {
          status.textContent = zh
            ? '咨询已保存，邮件通知暂未发出。团队将人工跟进，请勿重复提交。'
            : 'Your inquiry has been saved. Email notifications are pending. Our team will follow up; please do not resubmit.';
        } else {
        status.textContent = zh
          ? '咨询已提交。请留意确认邮件及垃圾邮件文件夹。'
          : 'Your inquiry was submitted. Please check your inbox and spam folder for a confirmation.';
        }
        form.reset();
      } catch (error) {
        status.setAttribute('role', 'alert');
        status.textContent = error.status === 429
          ? (zh ? '提交过于频繁，请稍后再试，或发送邮件至 business@bb369tech.com。' : 'Too many inquiries. Please wait before trying again, or email business@bb369tech.com.')
          : error.status === 409
          ? (zh ? '这条咨询仍在处理中，请稍候，不要重复提交。' : 'This inquiry is still processing. Please wait without resubmitting.')
          : error.status === 400
          ? (zh ? '请检查必填内容、邮箱与隐私同意后再提交。' : 'Please check the required fields, email and privacy consent before submitting.')
          : (zh ? '未能确认提交结果。请发送邮件至 business@bb369tech.com，避免重复提交。' : 'We could not confirm the result. Please email business@bb369tech.com to avoid a duplicate submission.');
      } finally {
        sending = false;
        button.disabled = false;
        form.removeAttribute('aria-busy');
      }
    });
  });
})();

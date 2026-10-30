"""Verify the single authorized additive saved-but-not-notified status branch."""
OLD = """        status.textContent = zh
          ? '咨询已提交。请留意确认邮件及垃圾邮件文件夹。'
          : 'Your inquiry was submitted. Please check your inbox and spam folder for a confirmation.';"""
PREFIX = """        if (data.dataSaved === true && data.notificationStatus === 'pending') {
          status.textContent = zh
            ? '咨询已保存，邮件通知暂未发出。团队将人工跟进，请勿重复提交。'
            : 'Your inquiry has been saved. Email notifications are pending. Our team will follow up; please do not resubmit.';
        } else {
"""
SUFFIX = "\n        }"
def original_contact_status(source):
    block = PREFIX + OLD + SUFFIX
    assert source.count(block) == 1, 'Expected exact reviewed status addition, no broader exception'
    return source.replace(block, OLD, 1)

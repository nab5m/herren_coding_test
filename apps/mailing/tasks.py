from smtplib import SMTPException

from django.core.mail import send_mail

from apps.mailing.models import MailHistory
from project.settings.celery import app


@app.task
def send_mails(mail_history_ids):
    print(mail_history_ids)
    mail_histories = MailHistory.objects.filter(id__in=mail_history_ids)
    print(mail_histories)
    # celery 까지는 APITestCase 로는 확인 어려움

    for mail_history in mail_histories:
        try:
            print(mail_history.id)
            sent_count = send_mail(
                mail_history.subject,
                mail_history.content,
                None,
                (mail_history.receiver.email,),
                fail_silently=False,
            )
            if sent_count:
                mail_history.success = True
                mail_history.save()

        except SMTPException as e:
            print(e)

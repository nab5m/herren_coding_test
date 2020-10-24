from django.db import models
from django.utils.translation import ugettext as _

from project.models import (
    TimeStampedModel,
    SoftDeletionModel,
    SoftDeletionManager,
    SoftDeletionQuerySet,
)


class Subscriber(TimeStampedModel, SoftDeletionModel):
    name = models.CharField(_("이름"), max_length=100)
    email = models.EmailField(_("이메일"), max_length=320, unique=True)
    # 검색해보니 이메일 최대 길이는 320으로 나왔습니다

    class Meta:
        verbose_name = _("구독자")
        verbose_name_plural = _("구독자")

    def __str__(self):
        return f"({self.id}) {self.name}: {self.email}"


class MailHistoryQuerySet(SoftDeletionQuerySet):
    pass


class MailHistoryManager(SoftDeletionManager):
    def get_queryset(self):
        # 구독자가 None이거나 deletedAt이 있는 애들은 넘겨주면 안돼!
        if self.alive_only:
            return (
                MailHistoryQuerySet(self.model)
                .select_related("receiver")
                .filter(deleted_at=None, receiver__deleted_at=None)
                .exclude(receiver=None)
            )
        return MailHistoryQuerySet(self.model).select_related("receiver")


class MailHistory(TimeStampedModel, SoftDeletionModel):
    sender = models.EmailField(_("보낸 이"), max_length=320)
    receiver = models.ForeignKey(
        to="mailing.Subscriber",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="구독자",
    )

    subject = models.CharField(_("제목"), max_length=255)
    content = models.TextField(_("내용"))

    success = models.BooleanField(_("전송 성공 여부"), default=False)

    objects = MailHistoryManager()

    class Meta:
        verbose_name = _("보낸 메일 내역")
        verbose_name_plural = _("보낸 메일 내역")

    def __str__(self):
        if self.receiver:
            return f"({self.id}) 제목: {self.subject}, 받는사람: {str(self.receiver)}"
        else:
            return f"({self.id}) 제목: {self.subject}, 받는사람: 구독 취소자"

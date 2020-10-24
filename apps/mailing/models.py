from django.db import models
from django.utils.translation import ugettext as _

from project.models import TimeStampedModel, SoftDeletionModel


class Subscriber(TimeStampedModel, SoftDeletionModel):
    name = models.CharField(_("이름"), max_length=100)
    email = models.EmailField(_("이메일"), max_length=320, unique=True)
    # 검색해보니 이메일 최대 길이는 320으로 나왔습니다

    class Meta:
        verbose_name = _("구독자")
        verbose_name_plural = _("구독자")

    def __str__(self):
        return f"({self.id}) {self.name}: {self.email}"

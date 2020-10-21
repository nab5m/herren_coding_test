from django.db import models
from django.utils.translation import ugettext as _


class Subscriber(models.Model):
    name = models.CharField(_('이름'), max_length=100)
    email = models.EmailField(_('이메일'), max_length=320)
    # 검색해보니 이메일 최대 길이는 320으로 나왔습니다

    created_at = models.DateTimeField(verbose_name='생성 날짜', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정 날짜', auto_now=True)

    class Meta:
        verbose_name = _('구독자')

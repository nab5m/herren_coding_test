from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import viewsets, mixins, status, pagination
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.mailing.serializers import SubscriberSerializer, MailHistorySerializer
from api.v1.mailing.viewsets import MailHistoryPagination
from api.v1.permissions import IsSafeRequest
from apps.mailing.models import Subscriber, MailHistory
from apps.mailing.tasks import send_mails


class MailHistoryViewSetV2(viewsets.GenericViewSet):
    """
    수신인이 gmail과 naver일 때 이용하는 API입니다.
    기존의 v1 API로 gmail과 naver에 보내는 경우 v2로 redirect(301) 됩니다.
    """

    queryset = MailHistory.objects.success()
    serializer_class = MailHistorySerializer
    pagination_class = MailHistoryPagination
    permission_classes = (IsSafeRequest,)

    @swagger_auto_schema(
        responses={
            201: "메일 전송 성공",
            301: "v1을 이용해주세요",
            400: "일치하는 구독자가 없습니다",
            500: "메일 전송에 실패했습니다",
        }
    )
    def mail_one(self, request, *args, **kwargs):
        mailto = request.data.get("mailto")
        subject = request.data.get("subject")
        content = request.data.get("content")

        if mailto and subject and content:
            if not (mailto.endswith("@gmail.com") or mailto.endswith("@naver.com")):
                return redirect(
                    reverse("mail"),
                    permanent=True,
                    data="gmail과 naver를 제외하 /api/v1/mail을 이용해주세요",
                )

            try:
                subscriber = Subscriber.objects.get(email=mailto)
                mail_history = MailHistory.objects.create(
                    sender=settings.DEFAULT_FROM_EMAIL,
                    receiver=subscriber,
                    subject=subject,
                    content=content,
                )

                send_mails.delay((mail_history.id,))

                return Response(
                    data=MailHistorySerializer(instance=mail_history).data,
                    status=status.HTTP_201_CREATED,
                )
            except Subscriber.DoesNotExist:
                return Response(
                    data="일치하는 구독자가 없습니다", status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            data="mailto, subject, content는 필수 값입니다", status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, name="mail_all")
    @swagger_auto_schema(
        responses={201: "메일 전송 성공", 400: "일치하는 구독자가 없습니다", 500: "메일 전송에 실패했습니다"}
    )
    def mail_all(self, request, *args, **kwargs):
        subject = request.data.get("subject")
        content = request.data.get("content")

        if subject and content:
            subscriber_ids = Subscriber.objects.gmail_or_naver().values_list(
                "id", flat=True
            )
            mail_histories = MailHistory.objects.bulk_create(
                [
                    MailHistory(
                        sender=settings.DEFAULT_FROM_EMAIL,
                        receiver_id=receiver_id,
                        subject=subject,
                        content=content,
                    )
                    for receiver_id in subscriber_ids
                ]
            )

            send_mails.delay([item.id for item in mail_histories])

            response = self.get_paginated_response(
                MailHistorySerializer(
                    instance=self.paginate_queryset(mail_histories), many=True
                ).data
            )
            response.status_code = status.HTTP_201_CREATED
            return response

        return Response(
            data="subject, content는 필수 값입니다", status=status.HTTP_400_BAD_REQUEST
        )

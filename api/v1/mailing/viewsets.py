from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import viewsets, mixins, status, pagination
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.mailing.serializers import SubscriberSerializer, MailHistorySerializer
from api.v1.permissions import IsSafeRequest
from apps.mailing.models import Subscriber, MailHistory


class SubscriberViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    메일링 리스트 구독과 구독 취소 API
    """

    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

    @action(detail=False, name="unsubscribe")
    @swagger_auto_schema(responses={204: "구독 취소 성공", 400: "일치하는 구독자가 없습니다"})
    def unsubscribe(self, request, *args, **kwargs):
        name = request.data.get("name", "")
        email = request.data.get("email", "")

        try:
            # email이 unique라서 한 개 이하임
            subscriber = Subscriber.objects.filter(name=name, email=email).get()
            data = SubscriberSerializer(instance=subscriber).data
            subscriber.hard_delete()
            return Response(status=status.HTTP_204_NO_CONTENT, data=data)
        except Subscriber.DoesNotExist as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="일치하는 구독자가 없습니다",)


class MailHistoryPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    # max_page_size = 10000


class MailHistoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    메일 전송 및 보낸메일 내역 확인 API
    """

    queryset = MailHistory.objects.success()
    serializer_class = MailHistorySerializer
    pagination_class = MailHistoryPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("receiver__email",)
    permission_classes = (IsSafeRequest,)

    @action(detail=False, name="mail_one")
    @swagger_auto_schema(
        responses={201: "메일 전송 성공", 400: "일치하는 구독자가 없습니다", 500: "메일 전송에 실패했습니다"}
    )
    def mail_one(self, request, *args, **kwargs):
        mailto = request.data.get("mailto")
        subject = request.data.get("subject")
        content = request.data.get("content")

        if mailto and subject and content:
            try:
                subscriber = Subscriber.objects.get(email=mailto)
                mail_history = MailHistory.objects.create(
                    sender=settings.DEFAULT_FROM_EMAIL,
                    receiver=subscriber,
                    subject=subject,
                    content=content,
                )

                sent_count = send_mail(
                    subject, content, None, (subscriber.email,), fail_silently=False
                )
                if sent_count:
                    mail_history.success = True
                    mail_history.save()

                return Response(
                    data=MailHistorySerializer(instance=mail_history).data,
                    status=status.HTTP_201_CREATED,
                )
            except Subscriber.DoesNotExist:
                return Response(
                    data="일치하는 구독자가 없습니다", status=status.HTTP_400_BAD_REQUEST
                )
            except SMTPException as e:
                print(e)
                return Response(
                    data="메일 전송에 실패했습니다", status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
            try:
                subscriber_ids = Subscriber.objects.values_list("id", flat=True)
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

                for mail_history in mail_histories:
                    sent_count = send_mail(
                        subject,
                        content,
                        None,
                        (mail_history.receiver.email,),
                        fail_silently=False,
                    )
                    if sent_count:
                        mail_history.success = True
                        mail_history.save()

                response = self.get_paginated_response(
                    MailHistorySerializer(
                        instance=self.paginate_queryset(mail_histories), many=True
                    ).data
                )
                response.status_code = status.HTTP_201_CREATED
                return response
            except SMTPException as e:
                print(e)
                return Response(
                    data="메일 전송에 실패했습니다", status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(
            data="subject, content는 필수 값입니다", status=status.HTTP_400_BAD_REQUEST
        )

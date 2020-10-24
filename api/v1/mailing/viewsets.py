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
    보낸메일 내역 확인 API
    """

    queryset = MailHistory.objects.success()
    serializer_class = MailHistorySerializer
    pagination_class = MailHistoryPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("receiver__email",)
    permission_classes = (IsSafeRequest,)

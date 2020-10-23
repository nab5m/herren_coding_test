from drf_yasg2.utils import swagger_auto_schema
from rest_framework import viewsets, mixins, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.mailing.serializers import SubscriberSerializer
from apps.mailing.models import Subscriber


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
            subscriber = Subscriber.objects.filter(name=name, email=email)
            subscriber.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )
        except Subscriber.DoesNotExist as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data="일치하는 구독자가 없습니다",
            )

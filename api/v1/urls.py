from django.urls import path

from api.v1.mailing.viewsets import SubscriberViewSet


urlpatterns = [
    path('/subscribe', SubscriberViewSet.as_view({'post': 'create'}), name='subscribe'),
    path('/unsubscribe', SubscriberViewSet.as_view({'post': 'unsubscribe'}), name='unsubscribe'),
]

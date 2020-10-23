from django.test.client import urlencode

from rest_framework import status
from rest_framework.test import APITestCase

from apps.mailing.models import Subscriber


class SubscriberTests(APITestCase):
    def setUp(self):
        Subscriber.objects.create(name="테스터", email="tester1@naver.com")

    def test_subscribe_post(self):
        response = self.client.post(
            "/api/v1/subscribe",
            urlencode({"name": "김준영", "email": "kimjun136@naver.com",}),
            content_type="application/x-www-form-urlencoded",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "김준영")
        self.assertEqual(response.data["email"], "kimjun136@naver.com")

    def test_unsubscribe_post(self):
        response = self.client.post(
            "/api/v1/unsubscribe",
            urlencode({"name": "테스터", "email": "tester1@naver.com",}),
            content_type="application/x-www-form-urlencoded",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

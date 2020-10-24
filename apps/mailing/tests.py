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


class SendMailTests(APITestCase):
    def setUp(self):
        self.authorization = "herren-recruit-python"
        self.email = "tester1@naver.com"

        Subscriber.objects.bulk_create(
            [
                Subscriber(name="테스터1", email="disnwkdl420@gmail.com"),
                Subscriber(name="테스터2", email="kimjun136@naver.com"),
                Subscriber(name="테스터3", email="sk990240@naver.com"),
            ]
        )

        print(f"구독자 수: {Subscriber.objects.count()}")
        print("test 실행 마다 setUp 하는 것 확인")

    def test_inbox_get(self):
        headers = {"HTTP_AUTHORIZATION": self.authorization}
        response = self.client.get(f"/api/v1/inbox/{self.email}", **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mail_post_to_subscriber(self):
        headers = {"HTTP_AUTHORIZATION": self.authorization}
        response = self.client.post(
            "/api/v1/mail",
            urlencode(
                {
                    "mailto": "disnwkdl420@gmail.com",
                    "subject": "메일 하나 보내기 테스트",
                    "content": "내용입니다",
                }
            ),
            content_type="application/x-www-form-urlencoded",
            **headers,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_mail_post_to_not_subscriber(self):
        headers = {"HTTP_AUTHORIZATION": self.authorization}
        response = self.client.post(
            "/api/v1/mail",
            urlencode(
                {
                    "mailto": "tester@gmail.com",
                    "subject": "메일 하나 보내기 테스트",
                    "content": "내용입니다",
                }
            ),
            content_type="application/x-www-form-urlencoded",
            **headers,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_mail_all_post(self):
        headers = {"HTTP_AUTHORIZATION": self.authorization}
        response = self.client.post(
            "/api/v1/mail-all",
            urlencode({"subject": "메일 전체에게 보내기 테스트", "content": "내용2다",}),
            content_type="application/x-www-form-urlencoded",
            **headers,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

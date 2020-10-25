from django.conf import settings
from django.test.client import urlencode

from rest_framework import status
from rest_framework.test import APITestCase

from apps.mailing.models import Subscriber, MailHistory


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

        subscribers = Subscriber.objects.bulk_create(
            [
                Subscriber(name="테스터0", email=self.email),
                Subscriber(name="테스터1", email="kimjun136@konkuk.ac.kr"),
                Subscriber(name="테스터2", email="kimjun136@naver.com"),
                Subscriber(name="테스터3", email="sk990240@naver.com"),
            ]
        )
        subscriber1 = subscribers[0]
        subscriber2 = subscribers[1]
        MailHistory.objects.bulk_create(
            [
                MailHistory(
                    sender=settings.DEFAULT_FROM_EMAIL,
                    receiver=subscriber1,
                    subject="안녕1",
                    content="안녕1",
                ),
                MailHistory(
                    sender=settings.DEFAULT_FROM_EMAIL,
                    receiver=subscriber1,
                    subject="안녕2",
                    content="안녕2",
                    success=True,
                ),
                MailHistory(
                    sender=settings.DEFAULT_FROM_EMAIL,
                    receiver=subscriber2,
                    subject="안녕3",
                    content="안녕3",
                ),
            ]
        )

    def test_inbox_get(self):
        headers = {"HTTP_AUTHORIZATION": self.authorization}
        response = self.client.get(
            f"/api/v1/inbox?receiver__email={self.email}", **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mail_post_to_subscriber(self):
        headers = {"HTTP_AUTHORIZATION": self.authorization}
        response = self.client.post(
            "/api/v1/mail",
            urlencode(
                {
                    "mailto": "kimjun136@konkuk.ac.kr",
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
                    "mailto": "hello@duam.net",
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


class SendMailV2Tests(APITestCase):
    def setUp(self):
        self.authorization = "herren-recruit-python"

        Subscriber.objects.bulk_create(
            [
                Subscriber(name="테스터1", email="disnwkdl420@gmail.com"),
                Subscriber(name="테스터2", email="kimjun136@naver.com"),
                Subscriber(name="테스터3", email="sk990240@naver.com"),
                Subscriber(name="테스터4", email="kimjun136@konkuk.ac.kr"),
            ]
        )

    def test_mail_v1_post_redirection(self):
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
        print(response.__dict__)

        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

    def test_mail_v2_post_(self):
        headers = {"HTTP_AUTHORIZATION": self.authorization}
        response = self.client.post(
            "/api/v2/mail",
            urlencode(
                {
                    "mailto": "disnwkdl420@gmail.com",
                    "subject": "메일 하나 보내기 v2 테스트",
                    "content": "내용입니다",
                }
            ),
            content_type="application/x-www-form-urlencoded",
            **headers,
        )
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_mail_all_v2_post_(self):
        headers = {"HTTP_AUTHORIZATION": self.authorization}
        response = self.client.post(
            "/api/v2/mail-all",
            urlencode({"subject": "메일 전체 보내기 v2 테스트", "content": "내용입니다",}),
            content_type="application/x-www-form-urlencoded",
            **headers,
        )
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_mail_v2_post_redirection(self):
        headers = {"HTTP_AUTHORIZATION": self.authorization}
        response = self.client.post(
            "/api/v2/mail",
            urlencode(
                {
                    "mailto": "kimjun136@konkuk.ac.kr",
                    "subject": "메일 하나 보내기 v2 테스트",
                    "content": "내용입니다",
                }
            ),
            content_type="application/x-www-form-urlencoded",
            **headers,
        )
        print(response.__dict__)

        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

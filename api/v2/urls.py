from django.urls import path, re_path

from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi
from rest_framework import permissions

from api.v2.mailing.viewsets import MailHistoryViewSetV2

schema_view = get_schema_view(
    openapi.Info(
        title="헤렌 코딩 테스트",
        default_version="v2",
        description="헤렌 코딩 테스트 API 문서입니다 ㅎ-ㅎ",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kimjun136@naver.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)

urlpatterns = [
    path("/mail", MailHistoryViewSetV2.as_view({"post": "mail_one"}), name="mail_v2"),
    path(
        "/mail-all",
        MailHistoryViewSetV2.as_view({"post": "mail_all"}),
        name="mail_all_v2",
    ),
    re_path(
        r"^/swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^/swagger$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^/redoc$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

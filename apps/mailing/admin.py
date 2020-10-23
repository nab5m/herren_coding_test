from django.contrib import admin

from apps.mailing.models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "name",
        "email",
    )

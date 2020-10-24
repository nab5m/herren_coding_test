from django.contrib import admin
from django.utils.html import format_html

from apps.mailing.models import Subscriber, MailHistory


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    search_fields = (
        "name",
        "email",
    )


@admin.register(MailHistory)
class MailHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sender",
        "view_receiver",
        "subject",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    search_fields = ("receiver__name", "subject", "content")

    def view_receiver(self, obj):
        if not obj.receiver:
            return None

        return format_html(
            f"<a href='/mailing/subscriber/?id={obj.receiver.id}'>"
            f"  {str(obj.receiver)}"
            f"</a>"
        )

    view_receiver.short_description = "구독자"

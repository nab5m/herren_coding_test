from rest_framework import serializers

from apps.mailing.models import Subscriber, MailHistory


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = (
            "id",
            "name",
            "email",
            "created_at",
            "updated_at",
            "deleted_at",
        )


class MailHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MailHistory
        fields = (
            "id",
            "sender",
            "receiver",
            "subject",
            "content",
            "success",
            "created_at",
            "updated_at",
            "deleted_at",
        )

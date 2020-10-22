from rest_framework import serializers

from apps.mailing.models import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ('id', 'name', 'email', 'created_at', 'updated_at',)

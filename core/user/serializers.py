from rest_framework import serializers 
from core.user.models import User 
from core.abstract.serializers import AbstractSerializer
from django.conf import settings
from urllib.parse import urlparse


class UserSerializer(AbstractSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        avatar = representation.get("avatar")

        # Case 1: Avatar is empty or missing
        if not avatar:
            representation["avatar"] = settings.DEFAULT_AVATAR_URL
            return representation

        # Case 2: Add full URL only if it's a relative path and request is available
        request = self.context.get("request")
        if settings.DEBUG and request:
            parsed = urlparse(avatar)
            if not parsed.netloc:  # If not a full URL
                representation["avatar"] = request.build_absolute_uri(avatar)

        return representation

    class Meta:
        model = User
        fields = [
            "id", "username", "first_name", "last_name", "bio",
            "avatar", "email", "is_active", "created", "updated"
        ]
        read_only_fields = ["is_active"]

from urllib.parse import urlparse

from rest_framework import serializers


def validate_youtube_url(value):
    hostname = urlparse(value).hostname

    if hostname and "youtube.com" not in value:
        raise serializers.ValidationError("Разрешены только ссылки на youtube.com.")

    return value

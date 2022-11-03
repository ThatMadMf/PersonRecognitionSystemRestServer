from django.contrib.auth.models import User
from rest_framework import serializers

from server.models import CaptureSession


class UserSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name')

    class Meta:
        model = User
        fields = [
            'id',
            'firstName',
        ]


class CreateCaptureSessionSerializer(serializers.ModelSerializer):
    sessionType = serializers.CharField(source='session_type')

    class Meta:
        model = CaptureSession
        fields = [
            'id',
            'sessionType',

        ]

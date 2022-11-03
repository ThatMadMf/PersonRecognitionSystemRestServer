import face_recognition
from rest_framework import serializers

from server.models import *


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    firstName = serializers.CharField(source='first_name')

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'firstName',
        ]


class UserFaceEncodingSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects.all())
    image = serializers.ImageField(write_only=True)

    class Meta:
        model = UserFaceEncoding
        fields = [
            'id',
            'userId',
            'image'
        ]

    def create(self, validated_data):
        image = validated_data.pop('image')
        image_rgb = face_recognition.load_image_file(image)
        image_encoding = face_recognition.face_encodings(image_rgb)[0]
        # image_encoding_bytes = pickle.dumps(image_encoding)

        validated_data['encoding'] = image_encoding

        return super(UserFaceEncodingSerializer, self).create(validated_data)


class CreateCaptureSessionSerializer(serializers.ModelSerializer):
    sessionType = serializers.CharField(source='session_type')

    class Meta:
        model = CaptureSession
        fields = [
            'id',
            'sessionType',

        ]

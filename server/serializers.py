import face_recognition
from rest_framework import serializers

from server.models import *


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    lastLogin = serializers.DateTimeField(source='last_login', read_only=True)
    dateJoined = serializers.DateTimeField(source='date_joined', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'firstName',
            'lastName',
            'lastLogin',
            'dateJoined',
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
    attachedDeviceToken = serializers.SlugRelatedField(
        source='attached_device',
        write_only=True,
        slug_field='auth_token',
        queryset=AttachedInputDevice.objects.all(),
    )
    deviceName = serializers.CharField(source='device_name', read_only=True)
    startTime = serializers.DateTimeField(source='start_time', read_only=True)
    endTime = serializers.DateTimeField(source='end_time', read_only=True)
    resultType = serializers.CharField(source='result_type', read_only=True)
    resultDetails = serializers.CharField(source='result_details', read_only=True)

    class Meta:
        model = CaptureSession
        fields = [
            'id',
            'attachedDeviceToken',
            'deviceName',
            'startTime',
            'endTime',
            'resultType',
            'resultDetails',
        ]

    def create(self, validated_data):
        validated_data['session_type'] = validated_data['attached_device'].reservation.input_type

        return super(CreateCaptureSessionSerializer, self).create(validated_data)


class FaceRecognitionSerializer(serializers.Serializer):  # noqa
    image = serializers.ImageField(required=True, allow_empty_file=False)

    class Meta:
        fields = ['image']


class SessionFrameSerializer(serializers.ModelSerializer):
    frameDetails = serializers.CharField(source='frame_details', read_only=True)
    captureSessionId = serializers.IntegerField(source='capture_session_id', read_only=True)

    class Meta:
        model = SessionFrame
        fields = [
            'id',
            'frameDetails',
            'timestamp',
            'captureSessionId',
        ]


class AttachedInputDeviceSerializer(serializers.ModelSerializer):
    deviceName = serializers.CharField(source='device_name', read_only=True)
    attachedAt = serializers.DateTimeField(source='attached_at', read_only=True)
    validUntil = serializers.DateTimeField(source='valid_until', read_only=True)
    inputType = serializers.CharField(source='input_type', read_only=True)
    authorizationType = serializers.CharField(source='authorization_type', read_only=True)

    class Meta:
        model = AttachedInputDevice
        fields = [
            'id',
            'deviceName',
            'attachedAt',
            'validUntil',
            'inputType',
            'authorizationType',
        ]

import uuid

import numpy as np
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, User
from django.db import models
from django.utils import timezone
from ndarraydjango.fields import NDArrayField


class UserFaceEncoding(models.Model):
    user = models.ForeignKey(User, models.CASCADE, 'face_encodings')
    encoding = NDArrayField(dtype=np.float64)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'user_face_encodings'


class InputDeviceReservation(models.Model):
    input_type = models.TextField()
    authorization_type = models.TextField()

    max_device_count = models.IntegerField(default=1)

    created_at = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'input_device_reservations'


class AttachedInputDevice(models.Model):
    reservation = models.ForeignKey(InputDeviceReservation, on_delete=models.CASCADE)

    device_name = models.TextField()
    device_code = models.TextField()

    auth_token = models.UUIDField(default=uuid.uuid4)

    attached_at = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'attached_input_devices'


class CaptureSession(models.Model):
    session_type = models.TextField()

    attached_device = models.ForeignKey(AttachedInputDevice, on_delete=models.CASCADE)

    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'capture_sessions'


class SessionFrame(models.Model):
    capture_session = models.ForeignKey(CaptureSession, on_delete=models.CASCADE)

    input_frame = models.BinaryField(null=True)
    output_frame = models.BinaryField(null=True)

    frame_details = models.TextField()

    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'session_frames'


class SessionFrameUsers(models.Model):
    session_frame = models.ForeignKey(SessionFrame, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    value = models.FloatField(default=0)

    class Meta:
        db_table = 'session_frame_users'


class CaptureSessionResult(models.Model):
    capture_session = models.OneToOneField(CaptureSession, on_delete=models.CASCADE)

    result_type = models.TextField()
    result_details = models.TextField()

    class Meta:
        db_table = 'capture_session_results'

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, User
from django.db import models
from django.utils import timezone


class CustomUser(User):
    class Meta:
        db_table = 'users'


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

    attached_at = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'attached_input_devices'


class CaptureSession(models.Model):
    session_type = models.TextField()

    attached_device = models.ForeignKey(AttachedInputDevice, on_delete=models.CASCADE)

    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()

    class Meta:
        db_table = 'capture_sessions'


class SessionFrame(models.Model):
    capture_session = models.ForeignKey(CaptureSession, on_delete=models.CASCADE)

    input_frame = models.BinaryField()
    output_frame = models.BinaryField()

    frame_details = models.TextField()

    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'session_frames'


class CaptureSessionResult(models.Model):
    capture_session = models.OneToOneField(CaptureSession, on_delete=models.CASCADE)

    result_type = models.TextField()
    result_details = models.TextField()

    class Meta:
        db_table = 'capture_session_results'

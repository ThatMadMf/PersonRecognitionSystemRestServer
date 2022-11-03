# Generated by Django 3.0.7 on 2022-11-03 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('server', '0002_sessionframe_capture_session'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFaceEncoding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encoding', models.BinaryField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='face_encodings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_face_encodings',
            },
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
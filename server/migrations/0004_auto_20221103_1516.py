# Generated by Django 3.0.7 on 2022-11-03 15:16

from django.db import migrations
import ndarraydjango.fields
import numpy


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_auto_20221103_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfaceencoding',
            name='encoding',
            field=ndarraydjango.fields.NDArrayField(dtype=numpy.float64, editable=True),
        ),
    ]

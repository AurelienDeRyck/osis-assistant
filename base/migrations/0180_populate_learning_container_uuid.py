# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-27 14:47
from __future__ import unicode_literals
from base.migrations.utils import utils
import uuid

from django.db import migrations


def set_uuid_field(apps, schema_editor):
    utils.set_uuids_model(apps, "learningcontainer")


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0179_learningcontainer_uuid'),
    ]

    operations = [
        migrations.RunPython(set_uuid_field),
    ]
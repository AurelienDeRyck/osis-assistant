# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-18 15:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0261_offerenrollment_education_group_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='educationgroupyear',
            name='credits',
        ),
    ]
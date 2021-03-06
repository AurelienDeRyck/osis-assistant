# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-20 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0022_auto_20170413_0330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assistantmandate',
            name='appeal',
            field=models.CharField(choices=[('NONE', 'NONE'), ('POSITIVE_APPEAL', 'POSITIVE_APPEAL'), ('NEGATIVE_APPEAL', 'NEGATIVE_APPEAL'), ('APPEAL_IN_PROGRESS', 'APPEAL_IN_PROGRESS'), ('NO_APPEAL', 'NO_APPEAL')], default='NONE', max_length=20),
        ),
        migrations.AlterField(
            model_name='assistantmandate',
            name='assistant_type',
            field=models.CharField(choices=[('ASSISTANT', 'ASSISTANT'), ('TEACHING_ASSISTANT', 'TEACHING_ASSISTANT')], default='ASSISTANT', max_length=20),
        ),
        migrations.AlterField(
            model_name='assistantmandate',
            name='renewal_type',
            field=models.CharField(choices=[('NORMAL', 'NORMAL'), ('SPECIAL', 'SPECIAL'), ('EXCEPTIONAL', 'EXCEPTIONAL')], default='NORMAL', max_length=12),
        ),
        migrations.AlterField(
            model_name='assistantmandate',
            name='state',
            field=models.CharField(choices=[('DECLINED', 'DECLINED'), ('TO_DO', 'TO_DO'), ('TRTS', 'TRTS'), ('PHD_SUPERVISOR', 'PHD_SUPERVISOR'), ('RESEARCH', 'RESEARCH'), ('SUPERVISION', 'SUPERVISION'), ('VICE_RECTOR', 'VICE_RECTOR'), ('DONE', 'DONE')], default='TO_DO', max_length=20),
        ),
    ]

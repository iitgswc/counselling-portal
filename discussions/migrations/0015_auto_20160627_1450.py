# -*- coding: utf-8 -*-
# Generated by Django 1.10a1 on 2016-06-27 09:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discussions', '0014_auto_20160623_1648'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='author',
            new_name='writer',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-17 16:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alpha', '0004_archchat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requests',
            name='requests',
        ),
    ]

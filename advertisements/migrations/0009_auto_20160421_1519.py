# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 22:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0008_auto_20160421_1513'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('title', 'state')]),
        ),
    ]

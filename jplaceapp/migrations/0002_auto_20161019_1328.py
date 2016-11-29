# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jplaceapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Testimony',
            new_name='Testimonies',
        ),
        migrations.RenameField(
            model_name='my_testimony',
            old_name='testimonys',
            new_name='testimony',
        ),
    ]

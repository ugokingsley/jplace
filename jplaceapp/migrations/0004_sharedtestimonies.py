# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jplaceapp', '0003_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedTestimonies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('votes', models.IntegerField(default=1)),
                ('testimony', models.ForeignKey(to='jplaceapp.Testimonies', unique=True)),
                ('users_voted', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

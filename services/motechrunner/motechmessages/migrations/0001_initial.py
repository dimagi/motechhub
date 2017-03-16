# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-16 19:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('streams', '0002_auto_20170310_2225'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', jsonfield.fields.JSONField(default=dict)),
                ('stream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streams.Stream')),
            ],
        ),
        migrations.CreateModel(
            name='MessageRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField()),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motechmessages.Message')),
            ],
        ),
        migrations.CreateModel(
            name='MessageRunArtifact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now=True)),
                ('level', models.CharField(choices=[('DEBUG', 'Debug'), ('INFO', 'Info'), ('WARN', 'Warn'), ('ERROR', 'Error')], max_length=5)),
                ('body', jsonfield.fields.JSONField(default=dict)),
                ('message_run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motechmessages.MessageRun')),
            ],
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-05-17 16:05


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brambling', '0058_auto_20190114_0455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='stripe_access_token',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='stripe_publishable_key',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='stripe_refresh_token',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='stripe_test_access_token',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='stripe_test_publishable_key',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='stripe_test_refresh_token',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='stripe_test_user_id',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='stripe_user_id',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]

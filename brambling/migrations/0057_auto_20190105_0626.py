# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-01-05 06:26


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brambling', '0056_auto_20170606_1844'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='orderdiscount',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='orderdiscount',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='orderdiscount',
            name='order',
        ),
        migrations.DeleteModel(
            name='OrderDiscount',
        ),
    ]

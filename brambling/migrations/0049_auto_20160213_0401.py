# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brambling', '0048_auto_20160204_0314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='additional_editors',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='editors',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='owner',
        ),
    ]

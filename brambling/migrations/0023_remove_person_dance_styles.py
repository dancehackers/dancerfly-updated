# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brambling', '0022_auto_20150908_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='dance_styles',
        ),
    ]

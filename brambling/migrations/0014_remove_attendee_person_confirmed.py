# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brambling', '0013_auto_20150605_1920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendee',
            name='person_confirmed',
        ),
    ]

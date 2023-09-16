# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brambling', '0033_attendee_notes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='default_event_city',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='default_event_country',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='default_event_currency',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='default_event_dance_styles',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='default_event_state_or_province',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='default_event_timezone',
        ),
    ]

# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brambling', '0031_auto_20151010_0621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='dietary_restrictions',
        ),
        migrations.DeleteModel(
            name='DietaryRestriction',
        ),
    ]

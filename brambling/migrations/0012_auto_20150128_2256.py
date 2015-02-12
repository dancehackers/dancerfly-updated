# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def copy_purchaser(apps, schema_editor):
    Transaction = apps.get_model("brambling", "Transaction")
    for transaction in Transaction.objects.filter(created_by__isnull=True).select_related('order'):
        transaction.created_by_id = transaction.order.person_id
        transaction.save()


class Migration(migrations.Migration):

    dependencies = [
        ('brambling', '0011_auto_20150128_2256'),
    ]

    operations = [
        migrations.RunPython(copy_purchaser, lambda *a, **k: None)
    ]
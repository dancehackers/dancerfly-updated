# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brambling', '0039_auto_20151222_2146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='dwolla_access_token',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dwolla_access_token_expires',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dwolla_refresh_token',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dwolla_refresh_token_expires',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dwolla_test_access_token',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dwolla_test_access_token_expires',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dwolla_test_refresh_token',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dwolla_test_refresh_token_expires',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dwolla_test_user_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dwolla_user_id',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='dwolla_access_token',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='dwolla_access_token_expires',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='dwolla_refresh_token',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='dwolla_refresh_token_expires',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='dwolla_test_access_token',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='dwolla_test_access_token_expires',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='dwolla_test_refresh_token',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='dwolla_test_refresh_token_expires',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='dwolla_test_user_id',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='dwolla_user_id',
        ),
        migrations.RemoveField(
            model_name='person',
            name='dwolla_access_token',
        ),
        migrations.RemoveField(
            model_name='person',
            name='dwolla_access_token_expires',
        ),
        migrations.RemoveField(
            model_name='person',
            name='dwolla_refresh_token',
        ),
        migrations.RemoveField(
            model_name='person',
            name='dwolla_refresh_token_expires',
        ),
        migrations.RemoveField(
            model_name='person',
            name='dwolla_test_access_token',
        ),
        migrations.RemoveField(
            model_name='person',
            name='dwolla_test_access_token_expires',
        ),
        migrations.RemoveField(
            model_name='person',
            name='dwolla_test_refresh_token',
        ),
        migrations.RemoveField(
            model_name='person',
            name='dwolla_test_refresh_token_expires',
        ),
        migrations.RemoveField(
            model_name='person',
            name='dwolla_test_user_id',
        ),
        migrations.RemoveField(
            model_name='person',
            name='dwolla_user_id',
        ),
    ]

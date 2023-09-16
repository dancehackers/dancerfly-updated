# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brambling', '0006_remove_organization_check_postmark_cutoff'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('report_type', models.CharField(max_length=8, choices=[('attendee', 'Attendee'), ('order', 'Order')])),
                ('name', models.CharField(max_length=40)),
                ('querystring', models.TextField()),
                ('event', models.ForeignKey(to='brambling.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

# Generated by Django 5.2.1 on 2025-06-30 08:03

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0007_auto_20250601_0953'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='subgroup',
            new_name='subgroup_language',
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='level',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, size=None),
        ),
    ]

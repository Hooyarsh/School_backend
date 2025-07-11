# Generated by Django 5.2.1 on 2025-05-28 05:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=20)),
                ('invoice_date', models.DateField()),
                ('total_amount', models.BigIntegerField()),
                ('supplier_details', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('submit_timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('level', models.CharField(max_length=20)),
                ('invoice_type', models.CharField(max_length=50)),
                ('subgroup_language', models.CharField(blank=True, max_length=10, null=True)),
                ('student_national_id', models.CharField(blank=True, max_length=10, null=True)),
                ('category', models.CharField(max_length=100)),
                ('sub_code', models.CharField(max_length=100)),
                ('detail_code', models.CharField(max_length=100)),
                ('other_detail_code', models.CharField(blank=True, max_length=255, null=True)),
                ('unit_price', models.BigIntegerField()),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='invoices.invoice')),
            ],
        ),
    ]

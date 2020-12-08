# Generated by Django 3.1.4 on 2020-12-06 19:50

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculator',
            name='matrix_a',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), size=0), blank=True, size=0),
        ),
        migrations.AlterField(
            model_name='calculator',
            name='result',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), blank=True, size=0),
        ),
        migrations.AlterField(
            model_name='calculator',
            name='vector_b',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), blank=True, size=0),
        ),
    ]

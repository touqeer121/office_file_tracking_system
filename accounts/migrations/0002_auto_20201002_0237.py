# Generated by Django 3.1.2 on 2020-10-01 21:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='registration_number',
            field=models.CharField(blank=True, max_length=7, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Invalid Registration Number', regex='[a-zA-Z]{2}[0-9]{5}')], verbose_name='Registration number'),
        ),
    ]
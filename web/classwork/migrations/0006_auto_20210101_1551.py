# Generated by Django 3.1.4 on 2021-01-01 23:51

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('classwork', '0005_auto_20200827_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='billing_country_code',
            field=django_countries.fields.CountryField(blank=True, default='US', max_length=2, verbose_name='country'),
        ),
    ]

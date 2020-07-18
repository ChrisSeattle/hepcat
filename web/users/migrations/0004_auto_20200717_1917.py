# Generated by Django 3.0.8 on 2020-07-18 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200711_0539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userhc',
            name='billing_address_1',
            field=models.CharField(blank=True, max_length=191, verbose_name='street address (line 1)'),
        ),
        migrations.AlterField(
            model_name='userhc',
            name='billing_address_2',
            field=models.CharField(blank=True, max_length=191, verbose_name='street address (continued)'),
        ),
        migrations.AlterField(
            model_name='userhc',
            name='billing_city',
            field=models.CharField(blank=True, default='Seattle', max_length=191, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='userhc',
            name='billing_country_area',
            field=models.CharField(blank=True, default='WA', help_text='State, Territory, or Province', max_length=2, verbose_name='state'),
        ),
        migrations.AlterField(
            model_name='userhc',
            name='billing_country_code',
            field=models.CharField(blank=True, default='USA', max_length=191, verbose_name='country'),
        ),
        migrations.AlterField(
            model_name='userhc',
            name='billing_postcode',
            field=models.CharField(blank=True, help_text='Zip or Postal Code', max_length=191, verbose_name='zipcode'),
        ),
        migrations.AlterField(
            model_name='userhc',
            name='uses_email_username',
            field=models.BooleanField(default=True, verbose_name='using email as username'),
        ),
    ]

# Generated by Django 3.0.8 on 2020-07-25 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classwork', '0009_auto_20200724_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='listing',
            field=models.SmallIntegerField(blank=True, default=0, help_text='listing order'),
        ),
    ]

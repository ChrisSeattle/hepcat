# Generated by Django 2.1.3 on 2019-01-15 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20190106_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='level',
            field=models.IntegerField(default=0, verbose_name='skill level'),
        ),
    ]

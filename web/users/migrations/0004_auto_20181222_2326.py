# Generated by Django 2.1.3 on 2018-12-23 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20181219_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userhc',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='admin'),
        ),
        migrations.AlterField(
            model_name='userhc',
            name='is_student',
            field=models.BooleanField(default=True, verbose_name='student'),
        ),
        migrations.AlterField(
            model_name='userhc',
            name='is_teacher',
            field=models.BooleanField(default=False, verbose_name='teacher'),
        ),
        migrations.AlterField(
            model_name='userhc',
            name='uses_email_username',
            field=models.BooleanField(default=True, verbose_name='Using Email'),
        ),
    ]
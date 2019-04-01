# Generated by Django 2.1.7 on 2019-03-19 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classwork', '0015_auto_20190318_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='link',
            field=models.CharField(blank=True, help_text='External or Internal links go here', max_length=255),
        ),
        migrations.AlterField(
            model_name='resource',
            name='text',
            field=models.TextField(blank=True, help_text='Text chunk used in page or email publication'),
        ),
    ]
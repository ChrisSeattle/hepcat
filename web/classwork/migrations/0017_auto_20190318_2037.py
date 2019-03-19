# Generated by Django 2.1.7 on 2019-03-19 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classwork', '0016_auto_20190318_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='classoffer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='classwork.ClassOffer'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='filepath',
            field=models.FileField(blank=True, help_text='If a file, upload here', upload_to='resource/'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='imagepath',
            field=models.ImageField(blank=True, help_text='If an image, upload here', upload_to='resource/'),
        ),
    ]

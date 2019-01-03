# Generated by Django 2.1.3 on 2019-01-03 04:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classwork', '0001_initial'),
        ('users', '0004_auto_20181222_2326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('level', models.IntegerField(default=0, verbose_name='Student Skill Level Number')),
                ('credit', models.FloatField(default=0, verbose_name='Class Payment Credit')),
                ('taken', models.ManyToManyField(to='classwork.Subject')),
            ],
        ),
    ]
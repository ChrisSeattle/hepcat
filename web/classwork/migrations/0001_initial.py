# Generated by Django 2.1.3 on 2018-12-07 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teachers', models.CharField(default='Chris Chapman', max_length=125)),
                ('class_day', models.SmallIntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], default=3)),
                ('start_time', models.TimeField()),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('code', models.CharField(max_length=120)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(default='Seattle', max_length=120)),
                ('state', models.CharField(default='WA', max_length=63)),
                ('zipcode', models.CharField(max_length=15)),
                ('map_google', models.URLField(verbose_name='Google Maps Link')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('key_day_date', models.DateField(verbose_name='Main Class Start Date')),
                ('max_day_shift', models.SmallIntegerField(verbose_name='Number of days other classes are away from Main Class')),
                ('num_weeks', models.PositiveSmallIntegerField(default=5)),
                ('publish_date', models.DateField(blank=True)),
                ('expire_date', models.DateField(blank=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('Beg', 'Beginning'), ('L2', 'Lindy 2'), ('L3', 'Lindy 3'), ('Spec', 'Special Focus'), ('WS', 'Workshop'), ('Priv', 'Private Lesson'), ('PrivSet', 'Private - Multiple Lessons'), ('Other', 'Other')], default='Spec', max_length=8)),
                ('version', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('N', 'NA')], max_length=1)),
                ('title', models.CharField(default='Untitled', max_length=125)),
                ('short_desc', models.CharField(max_length=100)),
                ('num_weeks', models.PositiveSmallIntegerField(default=5)),
                ('num_minutes', models.PositiveSmallIntegerField(default=60)),
                ('description', models.TextField()),
                ('syllabus', models.TextField(blank=True)),
                ('teacher_plan', models.TextField(blank=True)),
                ('video_wk1', models.URLField(blank=True)),
                ('video_wk2', models.URLField(blank=True)),
                ('video_wk3', models.URLField(blank=True)),
                ('video_wk4', models.URLField(blank=True)),
                ('video_wk5', models.URLField(blank=True)),
                ('email_wk1', models.TextField(blank=True)),
                ('email_wk2', models.TextField(blank=True)),
                ('email_wk3', models.TextField(blank=True)),
                ('email_wk4', models.TextField(blank=True)),
                ('email_wk5', models.TextField(blank=True)),
                ('image', models.URLField(blank=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='classoffer',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classwork.Session'),
        ),
        migrations.AddField(
            model_name='classoffer',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classwork.Subject'),
        ),
    ]

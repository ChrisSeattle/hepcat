# Generated by Django 3.0.8 on 2020-07-25 06:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('classwork', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('Beg', 'Beginning'), ('L2', 'Lindy 2'), ('L3', 'Lindy 3'), ('Spec', 'Special Focus'), ('WS', 'Workshop'), ('Priv', 'Private Lesson'), ('PrivSet', 'Private - Multiple Lessons'), ('Other', 'Other')], default='Spec', max_length=8)),
                ('level_num', models.DecimalField(blank=True, decimal_places=1, default=0, help_text='Will be computed if left blank. ', max_digits=3)),
                ('version', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('N', 'NA')], max_length=1)),
                ('title', models.CharField(default='Untitled', max_length=125)),
                ('tagline_1', models.CharField(blank=True, max_length=23)),
                ('tagline_2', models.CharField(blank=True, max_length=23)),
                ('tagline_3', models.CharField(blank=True, max_length=23)),
                ('num_weeks', models.PositiveSmallIntegerField(default=5)),
                ('num_minutes', models.PositiveSmallIntegerField(default=60)),
                ('description', models.TextField()),
                ('image', models.URLField(blank=True, max_length=191)),
                ('full_price', models.DecimalField(decimal_places=2, default=70.0, max_digits=6)),
                ('pre_pay_discount', models.DecimalField(decimal_places=2, default=5.0, max_digits=6)),
                ('multiple_purchase_discount', models.DecimalField(decimal_places=2, default=10.0, max_digits=6)),
                ('qualifies_as_multi_class_discount', models.BooleanField(default=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bio', models.TextField(blank=True, max_length=760)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('level', models.IntegerField(blank=True, default=0, verbose_name='skill level')),
                ('credit', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('taken', models.ManyToManyField(related_name='students', through='classwork.Registration', to='classwork.ClassOffer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bio', models.TextField(blank=True, max_length=760)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('listing', models.SmallIntegerField(blank=True, default=0, help_text='listing order')),
                ('tax_doc', models.CharField(blank=True, max_length=9)),
                ('taught', models.ManyToManyField(related_name='teachers', to='classwork.ClassOffer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='resource',
            name='classoffer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='classwork.ClassOffer'),
        ),
        migrations.AddField(
            model_name='resource',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='classwork.Subject'),
        ),
        migrations.AddField(
            model_name='registration',
            name='classoffer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classwork.ClassOffer'),
        ),
        migrations.AddField(
            model_name='registration',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='classwork.Payment'),
        ),
        migrations.AddField(
            model_name='registration',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classwork.Student'),
        ),
        migrations.AddField(
            model_name='payment',
            name='paid_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='paid_for', to='classwork.Student'),
        ),
        migrations.AddField(
            model_name='payment',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment', to='classwork.Student'),
        ),
        migrations.AddField(
            model_name='classoffer',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classwork.Location'),
        ),
        migrations.AddField(
            model_name='classoffer',
            name='session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classwork.Session'),
        ),
        migrations.AddField(
            model_name='classoffer',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classwork.Subject'),
        ),
    ]

# Generated by Django 2.1.7 on 2019-03-06 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classwork', '0007_auto_20190303_2254'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('related_type', models.CharField(choices=[('Subject', 'Subject'), ('ClassOffer', 'ClassOffer'), ('Other', 'Other')], default='Subject', max_length=15)),
                ('content_type', models.CharField(choices=[('url', 'External Link'), ('file', 'Formatted Text File'), ('text', 'Plain Text'), ('video', 'Video file on our site'), ('image', 'Image file on our site'), ('link', 'Webpage on our site'), ('email', 'Email file')], max_length=15)),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'Student'), (2, 'Teacher'), (4, 'Admin'), (8, 'Public')], help_text='Who is this for?')),
                ('avail', models.PositiveSmallIntegerField(choices=[(0, 'On Sign-up, before week 1'), (1, 'After week 1'), (2, 'After week 2'), (3, 'After week 3'), (4, 'After week 4'), (5, 'After week 5'), (200, 'After completion')], help_text='When is this resource available?')),
                ('filepath', models.FileField(help_text='If a file, upload here', upload_to='resource/')),
                ('description', models.TextField(blank=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('classoffer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classwork.ClassOffer')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classwork.Subject')),
            ],
        ),
    ]
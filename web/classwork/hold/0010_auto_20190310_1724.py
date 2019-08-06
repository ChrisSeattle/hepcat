# Generated by Django 2.1.7 on 2019-03-11 00:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classwork', '0009_auto_20190310_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='email_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subj_email_1', to='classwork.Resource'),
        ),
        migrations.AddField(
            model_name='subject',
            name='email_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subj_email_2', to='classwork.Resource'),
        ),
        migrations.AddField(
            model_name='subject',
            name='email_3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subj_email_3', to='classwork.Resource'),
        ),
        migrations.AddField(
            model_name='subject',
            name='email_4',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subj_email_4', to='classwork.Resource'),
        ),
        migrations.AddField(
            model_name='subject',
            name='email_5',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subj_email_5', to='classwork.Resource'),
        ),
    ]
# Generated by Django 4.0.3 on 2022-05-26 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iSmartcoApp', '0016_alter_jobcard_job_card_employees'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobcard',
            name='job_card_last_pause',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='jobcard',
            name='job_card_nva_time',
            field=models.DurationField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.0.3 on 2022-04-26 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iSmartcoApp', '0002_remove_jobcard_job_card_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'sysAdmin'), (2, 'CompAdmin'), (3, 'Client'), (4, 'Employee')], default=2),
        ),
    ]

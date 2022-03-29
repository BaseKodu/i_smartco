# Generated by Django 4.0.3 on 2022-03-29 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iSmartcoApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id_num', models.CharField(max_length=13, unique=True)),
                ('employee_name', models.CharField(blank=True, max_length=50, null=True)),
                ('employee_phone', models.CharField(blank=True, max_length=10, null=True)),
                ('employee_address', models.CharField(blank=True, max_length=100, null=True)),
                ('employee_designation', models.CharField(blank=True, max_length=50, null=True)),
                ('employee_joining_date', models.DateField(blank=True, null=True)),
                ('employee_leaving_date', models.DateField(blank=True, null=True)),
                ('employee_company', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='jobcard',
            old_name='Job_card_completed_at',
            new_name='job_card_completed_at',
        ),
    ]

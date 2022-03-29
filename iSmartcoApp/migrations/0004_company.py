# Generated by Django 4.0.3 on 2022-03-29 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iSmartcoApp', '0003_alter_employee_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]
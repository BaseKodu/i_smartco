# Generated by Django 4.0.3 on 2022-03-29 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iSmartcoApp', '0002_employee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
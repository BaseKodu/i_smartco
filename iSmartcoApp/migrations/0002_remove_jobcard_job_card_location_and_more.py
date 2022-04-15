# Generated by Django 4.0.3 on 2022-04-07 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iSmartcoApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobcard',
            name='job_card_location',
        ),
        migrations.RemoveField(
            model_name='jobcard',
            name='job_card_type',
        ),
        migrations.AddField(
            model_name='employee',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='jobcard',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='jobcard',
            name='job_card_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='jobcard',
            name='job_card_priority',
            field=models.CharField(choices=[(1, 'Low'), (2, 'Normal'), (3, 'High')], default=3, max_length=100),
        ),
        migrations.CreateModel(
            name='MaterialUsed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_name', models.CharField(blank=True, max_length=100, null=True)),
                ('material_barcode', models.CharField(blank=True, max_length=100, null=True)),
                ('material_quantity', models.IntegerField(blank=True, null=True)),
                ('material_unit', models.CharField(blank=True, max_length=100, null=True)),
                ('material_price', models.IntegerField(blank=True, null=True)),
                ('material_remarks', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('material_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iSmartcoApp.jobcard')),
            ],
        ),
        migrations.CreateModel(
            name='JobCardCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('owned_by', models.ManyToManyField(blank=True, to='iSmartcoApp.company')),
            ],
        ),
        migrations.CreateModel(
            name='ClientUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='iSmartcoApp.company')),
            ],
        ),
        migrations.AddField(
            model_name='jobcard',
            name='job_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='iSmartcoApp.jobcardcategory'),
        ),
        migrations.AlterField(
            model_name='jobcard',
            name='job_card_requester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='iSmartcoApp.clientuser'),
        ),
    ]
# Generated by Django 2.2 on 2019-04-17 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_beat', '0006_periodictask_priority'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('watchman_group_id', models.TextField(null=True, unique=True)),
                ('repairshopr_id', models.TextField(null=True, unique=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='WatchmanComputer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('computer_id', models.TextField(unique=True)),
                ('date_reported', models.DateField(auto_now_add=True)),
                ('date_last_reported', models.DateField(auto_now_add=True)),
                ('name', models.TextField()),
                ('os_type', models.CharField(max_length=7)),
                ('os_version', models.TextField()),
                ('ram_gb', models.FloatField()),
                ('hdd_capacity_gb', models.FloatField()),
                ('hdd_usage_gb', models.FloatField()),
                ('watchman_group_id', models.ForeignKey(db_column='watchman_group_id', on_delete=django.db.models.deletion.CASCADE, to='reporter.Customer', to_field='watchman_group_id')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='WatchmanWarning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warning_id', models.TextField()),
                ('date_reported', models.DateField(auto_now_add=True)),
                ('date_last_checked', models.DateField(auto_now_add=True)),
                ('date_resolved', models.DateField(null=True)),
                ('name', models.TextField()),
                ('details', models.TextField()),
                ('computer_id', models.ForeignKey(db_column='computer_id', on_delete=django.db.models.deletion.CASCADE, to='reporter.WatchmanComputer', to_field='computer_id')),
                ('watchman_group_id', models.ForeignKey(db_column='watchman_group_id', on_delete=django.db.models.deletion.CASCADE, to='reporter.Customer', to_field='watchman_group_id')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.CharField(max_length=25)),
                ('customer', models.ForeignKey(db_column='customer_id', on_delete=django.db.models.deletion.CASCADE, to='reporter.Customer')),
                ('periodic_task', models.ForeignKey(db_column='periodic_task_id', on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.PeriodicTask')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('date_generated', models.DateField(auto_now_add=True)),
                ('num_current_warnings', models.IntegerField(default=0)),
                ('num_resolved_warnings', models.IntegerField(default=0)),
                ('num_mac_os', models.IntegerField(default=0)),
                ('num_windows_os', models.IntegerField(default=0)),
                ('num_linux_os', models.IntegerField(default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporter.Customer')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]

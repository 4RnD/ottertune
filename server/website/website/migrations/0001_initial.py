# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2019-10-08 21:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BackupData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw_knobs', models.TextField()),
                ('raw_initial_metrics', models.TextField()),
                ('raw_final_metrics', models.TextField()),
                ('raw_summary', models.TextField()),
                ('knob_log', models.TextField()),
                ('metric_log', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DBMSCatalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'MySQL'), (2, 'Postgres'), (3, 'Db2'), (4, 'Oracle'), (6, 'SQLite'), (7, 'HStore'), (8, 'Vector'), (5, 'SQL Server'), (9, 'MyRocks')])),
                ('version', models.CharField(max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Hardware',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu', models.IntegerField(default=4, verbose_name='Number of CPUs')),
                ('memory', models.IntegerField(default=16, verbose_name='Memory (GB)')),
                ('storage', models.IntegerField(default=32, verbose_name='Storage (GB)')),
                ('storage_type', models.IntegerField(choices=[(5, 'SSD'), (10, 'HDD')], default=5, verbose_name='Storage Type')),
                ('additional_specs', models.TextField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KnobCatalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('vartype', models.IntegerField(choices=[(1, 'STRING'), (2, 'INTEGER'), (3, 'REAL'), (4, 'BOOL'), (5, 'ENUM'), (6, 'TIMESTAMP')], verbose_name='variable type')),
                ('unit', models.IntegerField(choices=[(1, 'bytes'), (2, 'milliseconds'), (3, 'other')])),
                ('category', models.TextField(null=True)),
                ('summary', models.TextField(null=True, verbose_name='description')),
                ('description', models.TextField(null=True)),
                ('scope', models.CharField(max_length=16)),
                ('minval', models.CharField(max_length=32, null=True, verbose_name='minimum value')),
                ('maxval', models.CharField(max_length=32, null=True, verbose_name='maximum value')),
                ('default', models.TextField(verbose_name='default value')),
                ('enumvals', models.TextField(null=True, verbose_name='valid values')),
                ('context', models.CharField(max_length=32)),
                ('tunable', models.BooleanField(verbose_name='tunable')),
                ('resource', models.IntegerField(choices=[(1, 'Memory'), (2, 'CPU'), (3, 'Storage'), (4, 'Other')], default=4)),
                ('dbms', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.DBMSCatalog')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KnobData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('creation_time', models.DateTimeField()),
                ('data', models.TextField()),
                ('knobs', models.TextField()),
                ('dbms', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.DBMSCatalog')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MetricCatalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('vartype', models.IntegerField(choices=[(1, 'STRING'), (2, 'INTEGER'), (3, 'REAL'), (4, 'BOOL'), (5, 'ENUM'), (6, 'TIMESTAMP')])),
                ('default', models.CharField(max_length=32, null=True)),
                ('summary', models.TextField(null=True, verbose_name='description')),
                ('scope', models.CharField(max_length=16)),
                ('metric_type', models.IntegerField(choices=[(1, 'COUNTER'), (2, 'INFO'), (3, 'STATISTICS')])),
                ('dbms', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.DBMSCatalog')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MetricData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('creation_time', models.DateTimeField()),
                ('data', models.TextField()),
                ('metrics', models.TextField()),
                ('dbms', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.DBMSCatalog')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PipelineData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.IntegerField(choices=[(1, 'Pruned Metrics'), (2, 'Ranked Knobs'), (3, 'Knob Data'), (4, 'Metric Data')])),
                ('data', models.TextField()),
                ('creation_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='PipelineRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='project name')),
                ('description', models.TextField(blank=True, null=True)),
                ('creation_time', models.DateTimeField()),
                ('last_update', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField()),
                ('observation_start_time', models.DateTimeField()),
                ('observation_end_time', models.DateTimeField()),
                ('observation_time', models.FloatField()),
                ('task_ids', models.CharField(max_length=180, null=True)),
                ('next_configuration', models.TextField(null=True)),
                ('dbms', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.DBMSCatalog')),
                ('knob_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.KnobData')),
                ('metric_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.MetricData')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='session name')),
                ('description', models.TextField(blank=True, null=True)),
                ('algorithm', models.IntegerField(choices=[(1, 'Gaussian Process Bandits'), (2, 'Deep Deterministic Policy Gradients'), (3, 'Deep Neural Network')], default=1)),
                ('ddpg_actor_model', models.BinaryField(blank=True, null=True)),
                ('ddpg_critic_model', models.BinaryField(blank=True, null=True)),
                ('ddpg_reply_memory', models.BinaryField(blank=True, null=True)),
                ('dnn_model', models.BinaryField(blank=True, null=True)),
                ('creation_time', models.DateTimeField()),
                ('last_update', models.DateTimeField()),
                ('upload_code', models.CharField(max_length=30, unique=True)),
                ('tuning_session', models.CharField(choices=[('tuning_session', 'Tuning Session'), ('no_tuning_session', 'No Tuning'), ('randomly_generate', 'Randomly Generate')], default='tuning_session', max_length=64, verbose_name='session type')),
                ('target_objective', models.CharField(default='throughput_txn_per_sec', max_length=64)),
                ('dbms', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.DBMSCatalog')),
                ('hardware', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Hardware')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SessionKnob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minval', models.CharField(max_length=32, null=True, verbose_name='minimum value')),
                ('maxval', models.CharField(max_length=32, null=True, verbose_name='maximum value')),
                ('tunable', models.BooleanField(verbose_name='tunable')),
                ('knob', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.KnobCatalog')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Session')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Workload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='workload name')),
                ('status', models.IntegerField(choices=[(1, 'MODIFIED'), (2, 'PROCESSING'), (3, 'PROCESSED')], default=1, editable=False)),
                ('dbms', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.DBMSCatalog')),
                ('hardware', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Hardware')),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Session', verbose_name='session name'),
        ),
        migrations.AddField(
            model_name='result',
            name='workload',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Workload'),
        ),
        migrations.AddField(
            model_name='pipelinedata',
            name='pipeline_run',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.PipelineRun', verbose_name='group'),
        ),
        migrations.AddField(
            model_name='pipelinedata',
            name='workload',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Workload'),
        ),
        migrations.AddField(
            model_name='metricdata',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Session'),
        ),
        migrations.AddField(
            model_name='knobdata',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Session'),
        ),
        migrations.AlterUniqueTogether(
            name='hardware',
            unique_together=set([('cpu', 'memory', 'storage', 'storage_type')]),
        ),
        migrations.AddField(
            model_name='backupdata',
            name='result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Result'),
        ),
        migrations.AlterUniqueTogether(
            name='workload',
            unique_together=set([('dbms', 'hardware', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([('user', 'project', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('user', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='pipelinedata',
            unique_together=set([('pipeline_run', 'task_type', 'workload')]),
        ),
    ]

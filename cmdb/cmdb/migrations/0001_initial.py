# Generated by Django 2.2.6 on 2019-11-02 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.IntegerField(db_column='Id', primary_key=True, serialize=False)),
                ('nichen', models.CharField(max_length=30, unique=True)),
                ('email', models.CharField(max_length=30, unique=True)),
                ('passwd', models.CharField(max_length=50)),
                ('isready', models.IntegerField()),
            ],
            options={
                'db_table': 'people',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('cpu_jg', models.CharField(max_length=10)),
                ('czxt', models.CharField(max_length=200)),
                ('cpu_count', models.IntegerField()),
                ('cpu_type', models.CharField(max_length=100)),
                ('memory_size', models.CharField(max_length=10)),
                ('root_size', models.CharField(max_length=10)),
                ('ipv4', models.CharField(max_length=50)),
                ('mac', models.CharField(max_length=50)),
                ('hostname', models.CharField(max_length=50)),
                ('create_time', models.DateTimeField()),
                ('localtion', models.CharField(blank=True, default='机柜1', max_length=50, null=True)),
                ('use_people', models.CharField(blank=True, default='开发', max_length=20, null=True)),
                ('application', models.CharField(blank=True, default='部署pro3', max_length=30, null=True)),
            ],
            options={
                'db_table': 'server',
                'managed': False,
            },
        ),
    ]

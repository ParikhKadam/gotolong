# Generated by Django 3.1.5 on 2021-03-07 16:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('othinv', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Othinv',
            fields=[
                ('othinv_name', models.TextField(primary_key=True, serialize=False)),
                ('othinv_buy', models.FloatField(blank=True, null=True)),
                ('othinv_hold', models.FloatField(blank=True, null=True)),
                ('othinv_enabled', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'global_othinv',
            },
        ),
        migrations.DeleteModel(
            name='Weight',
        ),
    ]
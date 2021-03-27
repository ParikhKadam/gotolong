# Generated by Django 3.1.5 on 2021-03-07 16:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('fratio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fratio',
            fields=[
                ('fratio_name', models.TextField(primary_key=True, serialize=False)),
                ('fratio_buy', models.FloatField(blank=True, null=True)),
                ('fratio_hold', models.FloatField(blank=True, null=True)),
                ('fratio_enabled', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'global_fratio',
            },
        ),
        migrations.DeleteModel(
            name='Weight',
        ),
    ]
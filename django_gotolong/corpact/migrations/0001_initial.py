# Generated by Django 3.1.5 on 2021-03-07 16:32

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Corpact',
            fields=[
                ('ca_ticker', models.TextField(primary_key=True, serialize=False)),
                ('ca_total', models.IntegerField(blank=True, null=True)),
                ('ca_bonus', models.IntegerField(blank=True, null=True)),
                ('ca_buyback', models.IntegerField(blank=True, null=True)),
                ('ca_dividend', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'global_corpact',
            },
        ),
    ]
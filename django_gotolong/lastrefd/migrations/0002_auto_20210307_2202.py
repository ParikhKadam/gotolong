# Generated by Django 3.1.5 on 2021-03-07 16:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('lastrefd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lastrefd',
            fields=[
                ('lastrefd_module', models.TextField(primary_key=True, serialize=False)),
                ('lastrefd_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'both_lastrefd',
            },
        ),
        migrations.DeleteModel(
            name='Weight',
        ),
    ]
# Generated by Django 3.1.5 on 2021-03-07 16:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('indices', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='indices',
            old_name='comp_industry',
            new_name='ind_industry',
        ),
        migrations.RenameField(
            model_name='indices',
            old_name='comp_isin',
            new_name='ind_isin',
        ),
        migrations.RenameField(
            model_name='indices',
            old_name='comp_name',
            new_name='ind_name',
        ),
        migrations.RenameField(
            model_name='indices',
            old_name='comp_ticker',
            new_name='ind_series',
        ),
        migrations.RenameField(
            model_name='indices',
            old_name='series',
            new_name='ind_ticker',
        ),
        migrations.AlterModelTable(
            name='indices',
            table='global_indices',
        ),
    ]